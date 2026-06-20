import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# =====================================
# Load Embedding Model
# =====================================

print("Loading embedding model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# =====================================
# Connect to ChromaDB
# =====================================

client = chromadb.PersistentClient(
    path="chroma_db_clean"
)

collection = client.get_collection(
    "sap_intelligence"
)

# =====================================
# User Question
# =====================================

question = input(
    "\nCEO Question: "
)

# =====================================
# Retrieve Evidence
# =====================================

query_embedding = model.encode(
    question
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

# =====================================
# Build Evidence Context
# =====================================

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
{doc[:600]}

"""

# =====================================
# CEO Prompt
# =====================================

prompt = f"""
You are the CEO of SAP.

Your role is NOT to summarize news.

Your role is to:

1. Analyze collected intelligence.
2. Reason about business implications.
3. Prioritize actions.
4. Recommend strategic decisions.
5. Justify recommendations using evidence.

Based ONLY on the evidence below:

==================================================
EXECUTIVE SUMMARY
==================================================

Explain SAP's current strategic position.

==================================================
TOP STRATEGIC PRIORITIES
==================================================

Rank priorities from highest to lowest.

==================================================
STRATEGIC RECOMMENDATIONS
==================================================

For EACH recommendation provide:

Priority Level:
(HIGH / MEDIUM / LOW)

Recommendation:

Business Rationale:

Supporting Evidence:
- Cite evidence source numbers
- Mention article titles
- Mention article sources

Expected Impact:
- Revenue Growth
- Market Differentiation
- Customer Acquisition
- Operational Efficiency

Risk Assessment:
- Financial Risk
- Operational Risk
- Strategic Risk

Implementation Urgency:
- Immediate
- 6 Months
- 12 Months

==================================================
FINAL CEO DECISION
==================================================

Answer:

"If you were SAP's CEO today,
what would you do next and why?"

Choose ONE highest-priority action.

Justify it using evidence.

==================================================
EVIDENCE
==================================================

{evidence_text}
"""

# =====================================
# Generate Response
# =====================================

print("\nAnalyzing strategic situation...\n")

response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# =====================================
# Output
# =====================================

print(
    response["message"]["content"]
)