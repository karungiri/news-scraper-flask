import requests
import logging
from scraper import config

def fetch_url(url):
    try:
        logging.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=config.HEADERS, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        logging.info(f"Successfully fetched {url} (status code: {response.status_code})")
        # Log a snippet of the response to verify content
        content_preview = response.text[:200] if response.text else "Empty response"
        logging.info(f"Content preview: {content_preview}")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error fetching {url}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching {url}: {str(e)}")
        return None
