import pandas as pd
from bs4 import BeautifulSoup
from ftfy import fix_text

# Load merged dataset
df = pd.read_csv("data/master_documents.csv")

print("================================")
print("BEFORE CLEANING")
print("================================")
print("Documents:", len(df))


def clean_text(text):

    # Handle missing values
    if pd.isna(text):
        return ""

    text = str(text)

    # Fix encoding issues
    text = fix_text(text)

    # Remove HTML tags
    text = BeautifulSoup(
        text,
        "html.parser"
    ).get_text(
        separator=" ",
        strip=True
    )

    # Remove extra spaces
    text = " ".join(text.split())

    return text


# Clean columns
df["title"] = df["title"].apply(clean_text)
df["content"] = df["content"].apply(clean_text)

# Fill remaining nulls
df.fillna("", inplace=True)

# Remove duplicate articles
df.drop_duplicates(
    subset=["title"],
    inplace=True
)

print("\n================================")
print("AFTER CLEANING")
print("================================")
print("Documents:", len(df))

# Save cleaned file
df.to_csv(
    "data/clean_documents.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print("data/clean_documents.csv")