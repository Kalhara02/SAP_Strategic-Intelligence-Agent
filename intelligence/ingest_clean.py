import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading documents...")

df = pd.read_csv(
    "data/clean_documents.csv"
)

print("Documents:", len(df))

print("Loading embedding model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Creating ChromaDB repository...")

client = chromadb.PersistentClient(
    path="chroma_db_clean"
)

collection = client.get_or_create_collection(
    name="sap_intelligence"
)

for idx, row in df.iterrows():

    title = str(row.get("title", ""))
    content = str(row.get("content", ""))

    if title == content:
        text = title
    else:
        text = f"""
Title:
{title}

Content:
{content}
"""

    embedding = model.encode(
        text
    ).tolist()

    collection.add(
        ids=[str(idx)],
        documents=[text],
        embeddings=[embedding],
        metadatas=[
            {
                "title": row.get("title", ""),
                "source": row.get("source", ""),
                "url": row.get("url", "")
            }
        ]
    )

print("Knowledge Repository Created Successfully")
print("Indexed Documents:", len(df))