import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# =====================================
# Load Model Once
# =====================================

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
# CEO BRIEFING
# =====================================

def generate_ceo_briefing(question):

    print("Retrieving documents...")

    query_embedding = model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

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
{doc[:200]}

"""

    prompt = f"""
You are the CEO of SAP.

IMPORTANT:

DO NOT explain your reasoning.
DO NOT show thinking.
DO NOT show analysis steps.

Return ONLY the final answer.

Analyze the evidence and create an executive briefing.

Provide EXACTLY these sections:

==================================================
WHAT HAPPENED?
==================================================

- Maximum 3 bullet points

==================================================
WHY DOES IT MATTER?
==================================================

- Maximum 3 bullet points

==================================================
WHAT SHOULD MANAGEMENT DO NEXT?
==================================================

- Maximum 3 bullet points

Use ONLY the evidence provided.

EVIDENCE:

{evidence_text}
"""

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
            "num_predict": 800
        }
    )

    print("Response received")
    
    content = response["message"]["content"]
    
    return content


# =====================================
# STANDALONE TEST
# =====================================

if __name__ == "__main__":

    question = input(
        "\nStrategic Question: "
    )

    print(
        "\nGenerating CEO Briefing...\n"
    )

    result = generate_ceo_briefing(
        question
    )

    print(result)