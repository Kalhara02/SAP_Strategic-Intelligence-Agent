from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv("data/google_news_1.csv")

def clean_html(text):

    if pd.isna(text):
        return ""

    return BeautifulSoup(
        str(text),
        "html.parser"
    ).get_text(" ", strip=True)

df["content"] = df["content"].apply(
    clean_html
)

df.to_csv(
    "data/clean_documents.csv",
    index=False
)

print("Done")