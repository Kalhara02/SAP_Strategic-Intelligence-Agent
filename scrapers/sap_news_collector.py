import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://news.sap.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

rows = []

for tag in soup.find_all(["h2", "h3", "h4"]):

    title = tag.get_text(strip=True)

    if len(title) > 20:

        rows.append({
            "title": title,
            "content": title,
            "source": "SAP News",
            "date": "",
            "url": url,
            "category": "Company News"
        })

df = pd.DataFrame(rows)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/sap_news.csv",
    index=False
)

print("Collected:", len(df))