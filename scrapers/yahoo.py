import feedparser
import pandas as pd

feeds = [
    "https://finance.yahoo.com/rss/headline?s=SAP"
]

rows = []

for feed_url in feeds:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:

        rows.append({
            "title": entry.get("title", ""),
            "content": entry.get("summary", ""),
            "source": "Yahoo Finance",
            "date": entry.get("published", ""),
            "url": entry.get("link", ""),
            "category": "Financial News"
        })

df = pd.DataFrame(rows)

df.to_csv(
    "data/AI.csv",
    index=False
)
print("Collected:", len(df))