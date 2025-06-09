from bs4 import BeautifulSoup
import logging
from scraper import config

def parse_kuensel(html):
    articles = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for all divs containing h2-h6 tags (likely article titles)
    potential_articles = []
    for heading in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
        # Get the parent div that might contain the full article
        container = heading.find_parent('div')
        if container:
            potential_articles.append(container)
    
    logging.info(f"Found {len(potential_articles)} potential article containers")
    
    # Try to extract article information from each container
    for container in potential_articles:
        try:
            # Look for title in headings
            title_elem = container.find(['h2', 'h3', 'h4', 'h5', 'h6'])
            if not title_elem:
                continue
            title = title_elem.get_text(strip=True)
            
            # Look for link in the heading or its parent
            link_elem = title_elem.find('a') or title_elem.parent.find('a')
            if not link_elem or not link_elem.has_attr('href'):
                continue
            link = link_elem['href']
            if not link.startswith('http'):
                link = f"{config.KUENSAL_URL.rstrip('/')}/{link.lstrip('/')}"
            
            # Look for description in paragraphs
            desc_elem = container.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Look for date
            date_elem = container.find(['time', 'span'], class_=lambda x: x and ('date' in x.lower() or 'time' in x.lower()))
            date = date_elem.get_text(strip=True) if date_elem else ""
            
            # Look for image
            img_elem = container.find('img')
            image = img_elem['src'] if img_elem and img_elem.has_attr('src') else ""
            if image and not image.startswith('http'):
                image = f"{config.KUENSAL_URL.rstrip('/')}/{image.lstrip('/')}"
            
            # Log what we found
            logging.info(f"Found article: {title}")
            logging.info(f"- Link: {link}")
            logging.info(f"- Description: {description[:100]}...")
            
            # Only add article if we have at least a title and link
            if title and link:
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'date': date,
                    'image': image
                })
                
        except Exception as e:
            logging.error(f"Parsing error in Kuensel item: {e}")
            continue
            
    logging.info(f"Successfully parsed {len(articles)} articles from Kuensel")
    return articles

def parse_bbs(html):
    articles = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for articles in the main content area
    items = soup.select('article')
    logging.info(f"Found {len(items)} potential BBS articles")
    
    for item in items:
        try:
            # Look for title and link
            title_elem = item.find('h2') or item.find('h3')
            if not title_elem:
                continue
            
            link_elem = title_elem.find('a')
            if not link_elem or not link_elem.has_attr('href'):
                continue
                
            title = title_elem.get_text(strip=True)
            link = link_elem['href']
            
            # Look for description
            desc_elem = item.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Look for date
            date_elem = item.find(class_='entry-date')
            date = date_elem.get_text(strip=True) if date_elem else ""
            
            # Look for image
            img_elem = item.find('img')
            image = img_elem['src'] if img_elem and img_elem.has_attr('src') else ""
            
            # Log what we found
            logging.info(f"Found BBS article: {title}")
            logging.info(f"- Link: {link}")
            logging.info(f"- Description: {description[:100]}...")
            
            # Only add article if we have at least a title and link
            if title and link:
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'date': date,
                    'image': image
                })
                
        except Exception as e:
            logging.error(f"Parsing error in BBS item: {e}")
            continue
            
    logging.info(f"Successfully parsed {len(articles)} articles from BBS")
    return articles

def parse_bhutanese(html):
    articles = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # Log the HTML structure to understand what we're working with
    logging.info("Analyzing The Bhutanese HTML structure:")
    logging.info(f"Found tags: {', '.join(set(tag.name for tag in soup.find_all()))}")
    
    # Try different potential article containers
    containers = [
        ('.post', 'post class'),
        ('article', 'article tag'),
        ('.type-post', 'type-post class'),
        ('.entry', 'entry class'),
        ('.blog-post', 'blog-post class')
    ]
    
    for selector, desc in containers:
        items = soup.select(selector)
        if items:
            logging.info(f"Found {len(items)} items with {desc}")
            if len(items) > 0:
                logging.info(f"Sample structure for {desc}:")
                logging.info(str(items[0])[:500])
    
    # Look for articles in the main content area
    items = soup.select('.post, article, .type-post')
    logging.info(f"Found {len(items)} potential Bhutanese articles")
    
    for item in items:
        try:
            # Look for title in headings or links
            title_elem = item.find(['h1', 'h2', 'h3', 'h4']) or item.find('a', class_='entry-title')
            if not title_elem:
                continue
                
            # Get title text
            title = title_elem.get_text(strip=True)
            
            # Look for link in title or as a separate element
            link_elem = title_elem.find('a') if title_elem.name != 'a' else title_elem
            if not link_elem or not link_elem.has_attr('href'):
                continue
            link = link_elem['href']
            
            # Look for description in excerpts or paragraphs
            desc_elem = item.find(class_=['entry-content', 'entry-summary']) or item.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Look for date
            date_elem = item.find(['time', 'span'], class_=lambda x: x and ('date' in x.lower() or 'time' in x.lower()))
            date = date_elem.get_text(strip=True) if date_elem else ""
            
            # Look for image
            img_elem = item.find('img')
            image = img_elem['src'] if img_elem and img_elem.has_attr('src') else ""
            
            # Log what we found
            logging.info(f"Found Bhutanese article: {title}")
            logging.info(f"- Link: {link}")
            logging.info(f"- Description: {description[:100]}...")
            
            # Only add article if we have at least a title and link
            if title and link:
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'date': date,
                    'image': image
                })
                
        except Exception as e:
            logging.error(f"Parsing error in Bhutanese item: {e}")
            continue
            
    logging.info(f"Successfully parsed {len(articles)} articles from The Bhutanese")
    return articles
