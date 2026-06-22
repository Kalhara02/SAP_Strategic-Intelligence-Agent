import pandas as pd

df = pd.read_csv(
    "data/clean_documents.csv"
)

print(
    "Rows with dates:",
    df["date"].notna().sum()
)

print(
    "Total rows:",
    len(df)
)