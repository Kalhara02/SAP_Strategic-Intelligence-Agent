import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://news.sap.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

rows = []

print("Loading SAP News homepage...")

response = requests.get(
    BASE_URL,
    headers=headers
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

links = []

for a in soup.find_all("a", href=True):

    href = a["href"]

    if "/20" in href:  # many SAP articles contain year paths
        full_url = urljoin(BASE_URL, href)

        if full_url not in links:
            links.append(full_url)

print(f"Found {len(links)} candidate links")

for idx, url in enumerate(links[:50]):

    print(f"[{idx+1}] {url}")

    try:

        article = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        article_soup = BeautifulSoup(
            article.text,
            "html.parser"
        )

        title = article_soup.title.get_text(strip=True)

        paragraphs = article_soup.find_all("p")

        content = " ".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        if len(content) > 200:

            rows.append({
                "title": title,
                "content": content,
                "source": "SAP News",
                "date": "",
                "url": url,
                "category": "Company News"
            })

    except Exception as e:

        print("ERROR:", e)

    time.sleep(1)

df = pd.DataFrame(rows)

df.to_csv(
    "data/sap_news_detailed.csv",
    index=False
)

print(f"\nCollected {len(df)} articles")