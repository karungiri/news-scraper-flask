import os
import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import fetcher, parser, rss_generator, config

aggregated_articles = []
rss_feed_xml = b""

def run_scraping_job():
    try:
        articles = []
        logging.info("Starting scraping job")
        
        # Fetch and parse Kuensel
        html_kuensel = fetcher.fetch_url(config.KUENSAL_URL)
        if html_kuensel:
            kuensel_articles = parser.parse_kuensel(html_kuensel)
            for article in kuensel_articles:
                article['source'] = 'Kuensel'
            articles.extend(kuensel_articles)
            logging.info(f"Kuensel: Fetched {len(kuensel_articles)} articles")
        else:
            logging.warning("Kuensel: Failed to fetch HTML")
            
        # Fetch and parse BBS
        html_bbs = fetcher.fetch_url(config.BBS_URL)
        if html_bbs:
            bbs_articles = parser.parse_bbs(html_bbs)
            for article in bbs_articles:
                article['source'] = 'BBS'
            articles.extend(bbs_articles)
            logging.info(f"BBS: Fetched {len(bbs_articles)} articles")
        else:
            logging.warning("BBS: Failed to fetch HTML")
            
        # Fetch and parse The Bhutanese
        html_bhutanese = fetcher.fetch_url(config.BHUTANESE_URL)
        if html_bhutanese:
            bhutanese_articles = parser.parse_bhutanese(html_bhutanese)
            for article in bhutanese_articles:
                article['source'] = 'The Bhutanese'
            articles.extend(bhutanese_articles)
            logging.info(f"Bhutanese: Fetched {len(bhutanese_articles)} articles")
        else:
            logging.warning("Bhutanese: Failed to fetch HTML")
        
        # Save articles to JSON file
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/articles.json', 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            logging.info(f"Saved {len(articles)} articles to JSON file")
        except Exception as e:
            logging.error(f"Error saving articles to JSON: {e}")
        
        # Generate RSS feed
        try:
            rss_feed_xml = rss_generator.generate_rss(articles)
            with open('data/rss.xml', 'wb') as f:
                f.write(rss_feed_xml)
            logging.info("Successfully generated and saved RSS feed")
        except Exception as e:
            logging.error(f"Error generating RSS feed: {e}")
            
        logging.info(f"Scraping job completed with total {len(articles)} articles")
    except Exception as e:
        logging.error(f"Error in scheduled scraping job: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scraping_job, 'interval', minutes=config.SCRAPE_INTERVAL_MINUTES)
    scheduler.start()
    # Run once immediately on start
    run_scraping_job()
