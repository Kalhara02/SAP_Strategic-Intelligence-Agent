import feedparser
import pandas as pd
from urllib.parse import quote

queries = [
    "SAP",
    "SAP AI",
    "SAP Cloud",
    "SAP ERP",
    "SAP partnership"
]

rows = []

for query in queries:

    url = (
        f"https://news.google.com/rss/search?q={quote(query)}"
    )

    print("Searching:", query)

    feed = feedparser.parse(url)

    for entry in feed.entries:

        rows.append({
            "title": entry.title,
            "content": entry.title,
            "source": "Google News",
            "date": entry.get("published", ""),
            "url": entry.link,
            "category": "Market News"
        })

df = pd.DataFrame(rows)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/google_news.csv",
    index=False
)

print("Collected:", len(df))