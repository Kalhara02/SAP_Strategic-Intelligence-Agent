import feedparser
import pandas as pd

rss_feeds = [
    "https://www.reddit.com/r/SAP/.rss",
    "https://www.reddit.com/r/artificial/.rss",
    "https://www.reddit.com/r/technology/.rss"
]

rows = []

for feed_url in rss_feeds:

    print(f"Reading: {feed_url}")

    feed = feedparser.parse(feed_url)

    subreddit = feed.feed.get("title", "Reddit")

    for entry in feed.entries:

        rows.append({
            "title": entry.get("title", ""),
            "content": entry.get("summary", ""),
            "source": subreddit,
            "date": entry.get("published", ""),
            "url": entry.get("link", ""),
            "category": "Community Discussion"
        })

df = pd.DataFrame(rows)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/reddit_rss.csv",
    index=False
)

print(f"Collected {len(df)} posts")