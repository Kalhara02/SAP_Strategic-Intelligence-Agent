import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

client = chromadb.PersistentClient(
    path="chroma_db_clean"
)

collection = client.get_collection(
    "sap_intelligence"
)

query = input(
    "Enter question: "
)

query_embedding = model.encode(
    query
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\nTOP DOCUMENTS\n")

for i, doc in enumerate(
    results["documents"][0],
    start=1
):
    print("=" * 50)
    print(f"DOCUMENT {i}")
    print(doc[:1000])
    print()