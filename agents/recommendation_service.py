import ollama


# ==================================================
# Strategic Recommendation Agent
# ==================================================

def generate_recommendations(
    intelligence,
    evidence_documents
):
    """
    Generate strategic recommendations using
    structured intelligence and retrieved evidence.
    """

    # ==================================================
    # No Evidence
    # ==================================================

    if not evidence_documents:

        return (
            "No recommendations generated.\n\n"
            "Reason: No supporting evidence was available."
        )

    # ==================================================
    # Build Evidence Context
    # ==================================================

    evidence = ""

    for i, item in enumerate(
        evidence_documents[:10],
        start=1
    ):

        metadata = item.get("metadata", {})

        title = metadata.get(
            "title",
            "Unknown Title"
        )

        source = metadata.get(
            "source",
            "Unknown Source"
        )

        document = item.get(
            "document",
            ""
        )[:800]

        evidence += f"""

==================================================
ARTICLE {i}
==================================================

Title:
{title}

Source:
{source}

Content:
{document}

"""

    # ==================================================
    # Format Intelligence Report
    # ==================================================

    intelligence_text = ""

    # ---------------- Opportunities ----------------

    intelligence_text += "OPPORTUNITIES\n\n"

    for item in intelligence.get("opportunities", []):

        intelligence_text += (
            f"Title: {item.get('title', '')}\n"
            f"Description: {item.get('description', '')}\n"
            f"Impact Level: {item.get('impact', '')}\n"
            f"Supporting Evidence: {item.get('evidence', '')}\n"
            f"Confidence Score: {item.get('confidence', '')}\n\n"
        )

    # ---------------- Risks ----------------

    intelligence_text += "\nRISKS\n\n"

    for item in intelligence.get("risks", []):

        intelligence_text += (
            f"Title: {item.get('title', '')}\n"
            f"Description: {item.get('description', '')}\n"
            f"Risk Category: {item.get('category', '')}\n"
            f"Severity Level: {item.get('severity', '')}\n"
            f"Supporting Evidence: {item.get('evidence', '')}\n"
            f"Confidence Score: {item.get('confidence', '')}\n\n"
        )

    # ---------------- Trends ----------------

    intelligence_text += "\nTRENDS\n\n"

    for item in intelligence.get("trends", []):

        intelligence_text += (
            f"Title: {item.get('title', '')}\n"
            f"Description: {item.get('description', '')}\n"
            f"Supporting Evidence: {item.get('evidence', '')}\n"
            f"Confidence Score: {item.get('confidence', '')}\n\n"
        )

    # ==================================================
    # Prompt
    # ==================================================

    prompt = f"""
/no_think

You are SAP's Executive Strategic Recommendation Agent.

Your role is to advise senior executives.

Use ONLY:

1. Strategic Intelligence
2. Retrieved Evidence

Rules

- Generate EXACTLY THREE recommendations.
- Every recommendation must be unique.
- Use ONLY supplied evidence.
- Never invent article titles.
- Never invent companies.
- Never invent facts.
- Recommendations must be practical and actionable.

Return EXACTLY in this format.

==================================================
RECOMMENDATION
==================================================

Recommendation:

Priority:
(HIGH / MEDIUM / LOW)

Supporting Evidence:
- Exact Article Title (Source)

Expected Impact:

Risk Level:
(HIGH / MEDIUM / LOW)

==================================================
STRATEGIC INTELLIGENCE
==================================================

{intelligence_text}

==================================================
RETRIEVED EVIDENCE
==================================================

{evidence}
"""

    # ==================================================
    # Generate Recommendations
    # ==================================================

    try:

        response = ollama.chat(

            model="qwen3:8b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={
                "temperature": 0.2,
                "num_predict": 1500
            }

        )

        content = response["message"]["content"].strip()

    except Exception as e:

        return (
            "Recommendation generation failed.\n\n"
            f"{e}"
        )

    # ==================================================
    # Empty Response
    # ==================================================

    if not content:

        return (
            "No recommendations generated.\n\n"
            "The language model returned an empty response."
        )

    # ==================================================
    # Clean Markdown
    # ==================================================

    replacements = {

        "**Recommendation:**": "Recommendation:",
        "**Priority:**": "Priority:",
        "**Supporting Evidence:**": "Supporting Evidence:",
        "**Expected Impact:**": "Expected Impact:",
        "**Risk Level:**": "Risk Level:",
        "**Recommendation**": "Recommendation",
        "**Priority**": "Priority",
        "**Supporting Evidence**": "Supporting Evidence",
        "**Expected Impact**": "Expected Impact",
        "**Risk Level**": "Risk Level",
        "**": ""

    }

    for old, new in replacements.items():

        content = content.replace(
            old,
            new
        )

    # ==================================================
    # Debug Output
    # ==================================================

    print("\n==============================")
    print("RECOMMENDATION OUTPUT")
    print("==============================")

    print(content)

    return content


# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    print(
        "Run this module from the Strategic Agent."
    )