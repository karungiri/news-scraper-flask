from feedgen.feed import FeedGenerator
import datetime
from datetime import timezone

def generate_rss(articles):
    fg = FeedGenerator()
    fg.title('Bhutan News Aggregator')
    fg.link(href='http://yourdomain.com/rss')
    fg.description('Aggregated Bhutan news from Kuensel Online, BBS & The Bhutanese')
    fg.language('en')
    
    for article in articles:
        fe = fg.add_entry()
        fe.title(article.get('title'))
        fe.link(href=article.get('link'))
        fe.description(article.get('description'))
        # Attempt to parse date, fallback to now with UTC timezone
        try:
            pub_date = datetime.datetime.strptime(article.get('date'), '%b %d, %Y')
            pub_date = pub_date.replace(tzinfo=timezone.utc)
            fe.pubDate(pub_date)
        except Exception:
            fe.pubDate(datetime.datetime.now(timezone.utc))
        # Add enclosure if image exists
        if article.get('image'):
            fe.enclosure(url=article.get('image'), type='image/jpeg')
    
    return fg.rss_str(pretty=True)
