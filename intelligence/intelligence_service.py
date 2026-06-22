import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# =====================================
# Load Embedding Model
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
# Intelligence Generator
# =====================================

def generate_intelligence(question):
    question_lower = question.lower()

    retrieval_query = f"""
SAP strategy,
enterprise AI,
cloud transformation,
business software,
partnerships,
industry developments

User Question:
{question}
"""

    query_embedding = model.encode(
        retrieval_query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=30
    )

    documents_list = results["documents"][0]

    # =====================================
    # FILTER LOW-VALUE DOCUMENTS
    # =====================================

    blocked_keywords = [
    "career",
    "consultant",
    "job",
    "salary",
    "training",
    "certification",
    "reddit",
    "student",
    "freelance",
    "mdg",
    "seeker"
   ]

    filtered_docs = []

    for doc in documents_list:

        doc_lower = str(doc).lower()

        skip = False

        for keyword in blocked_keywords:

            if keyword in doc_lower:
                skip = True
                break

        if not skip:
            filtered_docs.append(doc)

    documents = "\n\n".join(
        filtered_docs[:10]
    )

    # =====================================
    # PROMPT
    # ===================================

    if "opportunit" in question_lower:

        analysis_request = """
Generate EXACTLY 3 major opportunities.

Do NOT generate more than 3.
Do NOT generate fewer than 3.

For EACH opportunity provide:

Title:
Description:
Impact Level:
Supporting Evidence:
Confidence Score:
"""

    elif "risk" in question_lower:

        analysis_request = """
Generate EXACTLY 3 major risks.

Do NOT generate more than 3.
Do NOT generate fewer than 3.

For EACH risk provide:

Title:
Risk Category:
Severity Level:
Description:
Supporting Evidence:
Confidence Score:
"""

    elif "competitor" in question_lower:

        analysis_request = """
Generate EXACTLY 3 competitor intelligence insights.

Do NOT generate more than 3.
Do NOT generate fewer than 3.

For EACH insight provide:

Competitor:
Activity:
Strategic Impact:
Supporting Evidence:
Confidence Score:
"""

    elif (
        "trend" in question_lower
        or
        "technolog" in question_lower
    ):

        analysis_request = """
Generate EXACTLY 3 technologies or trends management should monitor.

Do NOT generate more than 3.
Do NOT generate fewer than 3.

For EACH trend provide:

Title:
Description:
Supporting Evidence:
Confidence Score:
"""

    elif (
        "prioritize" in question_lower
        or
        "strategic action" in question_lower
    ):

        analysis_request = """
Generate EXACTLY 3 strategic actions SAP should prioritize.

Do NOT generate more than 3.
Do NOT generate fewer than 3.

For EACH recommendation provide:

Recommendation:
Priority:
Supporting Evidence:
Expected Impact:
Risk Level:
"""

    elif "evidence" in question_lower:

        analysis_request = """
Generate EXACTLY 3 evidence-backed findings.

Do NOT generate more than 3.
Do NOT generate fewer than 3.

For EACH finding provide:

Finding:
Supporting Evidence:
Business Impact:
Confidence Score:
"""

    else:

        analysis_request = """
Generate EXACTLY 3 opportunities,
3 risks,
and 3 trends.
"""

    prompt = f"""
You are a Strategic Intelligence Analyst.

{analysis_request}

Use ONLY the evidence below.

DO NOT generate content related to:

- jobs
- careers
- consultants
- certifications
- training
- freelance work
- salaries
- students

Focus ONLY on:

- AI
- Cloud
- Enterprise Software
- Strategic Partnerships
- Market Opportunities
- Competitive Threats
- Business Growth
- Technology Trends

Evidence:

{documents}
"""
    # =====================================
    # OLLAMA
    # =====================================

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_predict": 1200,
            "temperature": 0.3
        }
    )

    content = response["message"]["content"]

    # =====================================
    # CLEAN MARKDOWN
    # =====================================
    
    content = content.replace(
    "**Title:**",
    "Title:"
    )

    content = content.replace(
    "**Description:**",
    "Description:"
    )

    content = content.replace(
    "**Supporting Evidence:**",
    "Supporting Evidence:"
    )

    content = content.replace(
    "**Supporting, Evidence:**",
    "Supporting Evidence:"
    )

    content = content.replace(
    "**Confidence Score:**",
    "Confidence Score:"
    )

    content = content.replace(
    "**Impact Level:**",
    "Impact Level:"
    )

    content = content.replace(
    "**Risk Category:**",
    "Risk Category:"
    )

    content = content.replace(
    "**Severity Level:**",
    "Severity Level:"
    )

    content = content.replace(
    "**OPPORTUNITIES**",
    "OPPORTUNITIES"
    )

    content = content.replace(
    "**RISKS**",
    "RISKS"
    )

    content = content.replace(
    "**TRENDS**",
    "TRENDS"
    )
    
    content = content.replace(
    "**OPPORTUNITIES**",
    "OPPORTUNITIES"
    )

    content = content.replace(
    "**RISKS**",
    "RISKS"
   )

    content = content.replace(
    "**TRENDS**",
    "TRENDS"
   )

    content = content.replace(
    "**Opportunity",
    "Opportunity"
   )

    content = content.replace(
    "**Risk",
    "Risk"
   )

    content = content.replace(
    "**Trend",
    "Trend"
   )

    content = content.replace(
    "**Recommendation",
    "Recommendation"
   )

    content = content.replace(
    "**Finding",
    "Finding"
   )

    content = content.replace(
    "**",
    ""
   )

    return content


# =====================================
# Standalone Test
# =====================================

if __name__ == "__main__":

    question = input(
        "\nStrategic Question: "
    )

    print(
        "\nGenerating Intelligence...\n"
    )

    result = generate_intelligence(
        question
    )

    print(result)