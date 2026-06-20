import feedparser
import pandas as pd
from urllib.parse import quote

queries = [
    "SAP",
    "SAP AI",
    "SAP Cloud",
    "SAP ERP",
    "Enterprise AI"
]

rows = []

for query in queries:

    rss_url = (
        f"https://news.google.com/rss/search?q={quote(query)}"
    )

    feed = feedparser.parse(rss_url)

    for entry in feed.entries:

        rows.append({
            "title": entry.get("title", ""),
            "content": entry.get("summary", ""),
            "source": "Google News",
            "date": entry.get("published", ""),
            "url": entry.get("link", ""),
            "category": "Market News"
        })

df = pd.DataFrame(rows)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/google_news_1.csv",
    index=False
)

print("Collected:", len(df))