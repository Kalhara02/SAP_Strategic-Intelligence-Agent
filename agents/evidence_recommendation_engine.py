import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# Load Embedding Model
print("Loading embedding model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="chroma_db_clean"
)

collection = client.get_collection(
    "sap_intelligence"
)

# User Question
question = input(
    "\nStrategic Question: "
)

# Retrieve Relevant Documents
query_embedding = model.encode(
    question
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=8
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

# Filter Irrelevant Documents
filtered_documents = []
filtered_metadatas = []

blocked_keywords = [
    "alternative",
    "alternatives",
    "replace sap",
    "sap replacement",
    "competitor comparison"
]

for doc, meta in zip(documents, metadatas):

    title = str(
        meta.get("title", "")
    ).lower()

    skip = False

    for keyword in blocked_keywords:
        if keyword in title:
            skip = True
            break

    if not skip:
        filtered_documents.append(doc)
        filtered_metadatas.append(meta)

documents = filtered_documents
metadatas = filtered_metadatas

# Build Evidence Context
evidence_text = ""

for i, (doc, meta) in enumerate(
    zip(documents, metadatas),
    start=1
):

    title = meta.get(
        "title",
        "Unknown Title"
    )

    source = meta.get(
        "source",
        "Unknown Source"
    )

    url = meta.get(
        "url",
        "N/A"
    )

    evidence_text += f"""

==================================================
EVIDENCE SOURCE {i}
==================================================

TITLE:
{title}

SOURCE:
{source}

URL:
{url}

CONTENT:
{doc[:500]}

"""

# Prompt
prompt = f"""
You are SAP's Strategic Recommendation Engine.

You are advising SAP executives.

Recommendations MUST:

- Strengthen SAP's market position
- Increase revenue growth
- Improve customer retention
- Accelerate innovation
- Expand strategic partnerships
- Improve cloud and AI adoption

Do NOT recommend:

- Replacing SAP products
- Migrating away from SAP
- Switching to competitors
- SAP alternatives

Generate exactly 3 recommendations.

For EACH recommendation use the following format:

==================================================
RECOMMENDATION
==================================================

Recommendation:
(one strategic recommendation)

Supporting Evidence:
• Evidence Source 1
• Evidence Source 2
• Evidence Source 3

Expected Impact:
• Revenue Growth
• Market Differentiation
• Customer Acquisition
• Operational Efficiency

Risk Assessment:
• Financial Risk
• Operational Risk
• Strategic Risk

Use ONLY the evidence provided.

EVIDENCE:

{evidence_text}
"""

# Generate Recommendations
print("\nGenerating recommendations...\n")

response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# Output
print(
    response["message"]["content"]
)