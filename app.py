import os
import json
from flask import Flask, render_template, Response
from scraper.scheduler import start_scheduler, run_scraping_job
import logging

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.INFO)

def get_cached_articles():
    try:
        if os.path.exists('data/articles.json'):
            with open('data/articles.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error reading cached articles: {e}")
    return []

def get_cached_rss():
    try:
        if os.path.exists('data/rss.xml'):
            with open('data/rss.xml', 'rb') as f:
                return f.read()
    except Exception as e:
        logging.error(f"Error reading cached RSS: {e}")
    return b""

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Start scraping scheduler
start_scheduler()

# Run initial scrape
run_scraping_job()

@app.route('/')
def index():
    articles = get_cached_articles()
    logging.info(f"Rendering homepage with {len(articles)} articles")
    return render_template('index.html', articles=articles)

@app.route('/rss')
def rss_feed():
    return Response(get_cached_rss(), mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(debug=True)
