import feedparser
from datetime import datetime, timezone, timedelta

def get_recent_articles(feed_url, days=2):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    # Current date and time
    now = datetime.now(timezone.utc)

    # List to store recent articles
    recent_articles = []

    for entry in feed.entries:
        if 'published_parsed' in entry:
            # Convert published date to datetime object
            published_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            # Check if the article is from the last 'days' days
            if now - published_date <= timedelta(days=days):
                recent_articles.append({
                    "title": entry.title,
                    "link": entry.link,
                })
        else:
            print(f"Article '{entry.title}' does not have a published date.")

    return recent_articles
def parse_feeds():
    # List of RSS feeds you want to parse
    rss_feeds = [
        "https://www.wired.com/feed/category/security/latest/rss",
        "https://www.bleepingcomputer.com/feed/",
        #"https://therecord.media/news/cybercrime/feed",
        # Add more RSS feed URLs here
    ]

    # Collecting articles from all feeds
    all_articles = []
    for feed_url in rss_feeds:
        print(f"Checking feed: {feed_url}")
        articles = get_recent_articles(feed_url)
        all_articles.extend(articles)

    # Print the collected articles
    if all_articles:
        return(all_articles)
    else:
        return("No recent articles found.")

