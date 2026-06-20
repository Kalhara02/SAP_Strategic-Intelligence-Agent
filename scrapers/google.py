import feedparser
import pandas as pd
import trafilatura
import requests
from urllib.parse import quote
import time

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

    print(f"\nSearching: {query}")

    feed = feedparser.parse(rss_url)

    for entry in feed.entries:

        try:

            google_url = entry.link

            # Follow Google redirect
            response = requests.get(
                google_url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=15,
                allow_redirects=True
            )

            final_url = response.url

            print("Publisher:", final_url)

            downloaded = trafilatura.fetch_url(
                final_url
            )

            article_text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False
            )

            if not article_text:
                article_text = ""

            rows.append({
                "title": entry.title,
                "content": article_text,
                "source": "Google News",
                "date": entry.get("published", ""),
                "url": final_url,
                "category": "Market News"
            })

            time.sleep(1)

        except Exception as e:

            print("ERROR:", e)

df = pd.DataFrame(rows)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/google_news_detailed.csv",
    index=False
)

print(
    f"\nCollected {len(df)} articles"
)