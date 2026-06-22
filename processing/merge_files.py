import pandas as pd

files = [
    "data/sap_news_articles.csv",
    "data/google_news_articles.csv",
    "data/reddit_articles.csv",
    "data/finance_articles.csv",
    "data/ai_articles.csv"
]

dfs = []

for file in files:

    try:
        df = pd.read_csv(file)

        print(f"Loaded {file}")
        print(f"Rows: {len(df)}")

        dfs.append(df)

    except Exception as e:

        print(f"Could not load {file}")
        print(e)

master_df = pd.concat(
    dfs,
    ignore_index=True
)

# Ensure standard columns exist
required_columns = [
    "title",
    "content",
    "source",
    "date",
    "url",
    "category"
]

for col in required_columns:

    if col not in master_df.columns:
        master_df[col] = ""

master_df = master_df[required_columns]

master_df.to_csv(
    "data/master_documents.csv",
    index=False
)

print("\n====================")
print("MERGE COMPLETE")
print("====================")
print("Total Documents:", len(master_df))
print("Saved: data/master_documents.csv")