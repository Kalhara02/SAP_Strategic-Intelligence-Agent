import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading documents...")

df = pd.read_csv(
    "data/master_documents.csv"
)

print("Documents:", len(df))

print("Loading embedding model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Creating ChromaDB repository...")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="sap_intelligence"
)

for idx, row in df.iterrows():

    title = str(row.get("title", ""))
    content = str(row.get("content", ""))

    # Avoid duplicate title-content issue
    if title == content:
        text = title
    else:
        text = title + " " + content

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(idx)],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{
            "source": str(row.get("source", "")),
            "category": str(row.get("category", "")),
            "url": str(row.get("url", ""))
        }]
    )

print("Knowledge Repository Created Successfully")
print("Indexed Documents:", len(df))