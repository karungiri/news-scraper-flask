# scraper/config.py
KUENSAL_URL = 'https://kuenselonline.com'
BBS_URL = 'https://www.bbs.bt'
BHUTANESE_URL = 'https://thebhutanese.bt'

# CSS selectors for each news site
KUENSAL_SELECTOR = '.post, .news-item, .article, .story'  # Try multiple common article containers
BBS_SELECTOR = '.news-item, .article, .post'  # Common news article selectors
BHUTANESE_SELECTOR = '.post, article, .news-item' # Common blog/news post selectors

# Specific selectors for article components
KUENSAL_TITLE_SELECTOR = '.post-title, .entry-title, h1, h2, h3, .title'
KUENSAL_LINK_SELECTOR = 'a[href*="kuenselonline"]'  # Links containing kuenselonline
KUENSAL_DESC_SELECTOR = '.post-excerpt, .entry-content p, .excerpt, .description'
KUENSAL_DATE_SELECTOR = '.post-date, .entry-date, .date, time'
KUENSAL_IMAGE_SELECTOR = '.post-thumbnail img, .featured-image img, img'

# HTTP settings
REQUEST_TIMEOUT = 10  # seconds
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; BhutanNewsAggregator/1.0)'
}

# Scheduler settings
SCRAPE_INTERVAL_MINUTES = 60
