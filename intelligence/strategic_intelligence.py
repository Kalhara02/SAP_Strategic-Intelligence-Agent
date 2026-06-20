import chromadb
import ollama
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

retrieval_query = """
SAP strategy, enterprise AI,
cloud transformation,
business software,
partnerships,
industry developments
"""

query_embedding = model.encode(
    retrieval_query
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=15
)

documents = "\n\n".join(
    results["documents"][0]
)

prompt = f"""
You are a Strategic Intelligence Analyst.

Based ONLY on the evidence below:

Identify:

1. Opportunities
2. Risks
3. Trends

For each item provide:

- Description
- Supporting Evidence

Evidence:

{documents}
"""

response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(
    response["message"]["content"]
)