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


def generate_recommendations(question):

    print("Retrieving documents...")

    retrieval_query = f"""
SAP strategy,
enterprise AI,
cloud transformation,
business growth,
strategic partnerships,
industry developments,
market opportunities,
competitive advantage

User Question:
{question}
"""

    query_embedding = model.encode(
        retrieval_query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=15
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # =====================================
    # Filter Low-Value Documents
    # =====================================

    filtered_documents = []
    filtered_metadatas = []

    blocked_keywords = [
        "alternative",
        "alternatives",
        "replace sap",
        "sap replacement",
        "competitor comparison",
        "freelance",
        "career",
        "consultant",
        "student",
        "job",
        "salary",
        "training",
        "certification"
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

    documents = filtered_documents[:5]
    metadatas = filtered_metadatas[:5]

    # =====================================
    # Build Evidence Context
    # =====================================

    print("Building evidence context...")

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

        evidence_text += f"""
==================================================
ARTICLE {i}
==================================================

TITLE:
{title}

SOURCE:
{source}

CONTENT:
{doc[:200]}

"""

    # =====================================
    # Prompt
    # =====================================

    prompt = f"""
You are SAP's Strategic Recommendation Engine.

You are advising SAP executives.

Your recommendations MUST:

- Strengthen SAP's market position
- Increase revenue growth
- Accelerate AI adoption
- Increase cloud adoption
- Improve customer retention
- Expand strategic partnerships
- Improve competitive advantage

Do NOT recommend:

- SAP alternatives
- Replacing SAP
- Career advice
- Freelance opportunities
- Student opportunities
- Job opportunities

Generate EXACTLY 3 recommendations.

Use ONLY the evidence provided.

For EACH recommendation use EXACTLY this format:

==================================================
RECOMMENDATION
==================================================

Recommendation:
(one recommendation)

Priority:
(HIGH / MEDIUM / LOW)

Supporting Evidence:
- Exact Article Title (Source)
- Exact Article Title (Source)
- Exact Article Title (Source)

Expected Impact:
- Revenue Growth
- Market Differentiation
- Customer Acquisition
- Operational Efficiency

Risk Level:
(HIGH / MEDIUM / LOW)

IMPORTANT:

- Use ONLY article titles provided in the evidence.
- Include the source in brackets.
- Example:
  SAP cloud revenues rise as AI drives demand (Reuters)
- Do NOT use "Evidence Source 1", "Evidence Source 2", etc.
- Do NOT invent article titles.
- Do NOT repeat article content.
- Do NOT output URLs.
- Output recommendations only.

EVIDENCE:

{evidence_text}
"""

    print("Prompt length:", len(prompt))
    print("Sending prompt to Ollama...")

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": "/no_think\n" + prompt
            }
        ],
        options={
            "num_predict": 1200
        }
    )

    print("Response received")
    
    content = response["message"]["content"]

    return content


# =====================================
# Standalone Test
# =====================================

if __name__ == "__main__":

    question = input(
        "\nStrategic Question: "
    )

    print(
        "\nGenerating recommendations...\n"
    )

    result = generate_recommendations(
        question
    )

    print(result)