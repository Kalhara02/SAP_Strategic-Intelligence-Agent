import ollama


# ==================================================
# Strategic Recommendation Agent
# ==================================================

def generate_recommendations(
    intelligence,
    evidence_documents
):
    """
    Generate executive strategic recommendations
    using retrieved evidence and strategic intelligence.
    """

    # ==================================================
    # No Evidence
    # ==================================================

    if not evidence_documents:

        return {

            "recommendations": [],

            "raw_output": "No evidence available."

        }

    # ==================================================
    # Build Evidence Context
    # ==================================================

    evidence = ""

    for i, item in enumerate(
        evidence_documents[:10],
        start=1
    ):

        metadata = item.get(
            "metadata",
            {}
        )

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
TITLE
==================================================

{title}

SOURCE

{source}

CONTENT

{document}

"""

    # ==================================================
    # Format Intelligence Report
    # ==================================================

    intelligence_text = ""

    # ----------------------------------------------
    # Opportunities
    # ----------------------------------------------

    if intelligence.get("opportunities"):

        intelligence_text += "\nOPPORTUNITIES\n\n"

        for item in intelligence["opportunities"]:

            intelligence_text += (

                f"Title: {item.get('title','')}\n"

                f"Description: {item.get('description','')}\n"

                f"Impact: {item.get('impact','')}\n"

                f"Evidence: {item.get('evidence','')}\n"

                f"Confidence: {item.get('confidence','')}\n\n"

            )

    # ----------------------------------------------
    # Risks
    # ----------------------------------------------

    if intelligence.get("risks"):

        intelligence_text += "\nRISKS\n\n"

        for item in intelligence["risks"]:

            intelligence_text += (

                f"Title: {item.get('title','')}\n"

                f"Description: {item.get('description','')}\n"

                f"Category: {item.get('category','')}\n"

                f"Severity: {item.get('severity','')}\n"

                f"Evidence: {item.get('evidence','')}\n"

                f"Confidence: {item.get('confidence','')}\n\n"

            )

    # ----------------------------------------------
    # Trends
    # ----------------------------------------------

    if intelligence.get("trends"):

        intelligence_text += "\nTECHNOLOGY TRENDS\n\n"

        for item in intelligence["trends"]:

            intelligence_text += (

                f"Title: {item.get('title','')}\n"

                f"Description: {item.get('description','')}\n"

                f"Evidence: {item.get('evidence','')}\n"

                f"Confidence: {item.get('confidence','')}\n\n"

            )

    # ==================================================
    # Prompt
    # ==================================================

    prompt = f"""
/no_think

You are an Executive Strategic Recommendation Agent.

Your responsibility is to advise senior executives.

Use ONLY:

1. Strategic Intelligence

2. Retrieved Evidence

Never invent:

- facts

- companies

- evidence

- article titles

Generate EXACTLY THREE recommendations.

Every recommendation MUST be unique.

Every recommendation MUST include
supporting evidence.

Return EXACTLY in this format.

==================================================
RECOMMENDATION
==================================================

Recommendation:

Priority:

Supporting Evidence:

Expected Impact:

Risk Level:

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
    # Call LLM
    # ==================================================

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

    if not content:

        content = "No recommendations generated."
        
        # ==================================================
    # Clean Markdown
    # ==================================================

    replacements = {

        "**Recommendation:**": "Recommendation:",
        "**Priority:**": "Priority:",
        "**Supporting Evidence:**": "Supporting Evidence:",
        "**Expected Impact:**": "Expected Impact:",
        "**Risk Level:**": "Risk Level:",
        "**": ""

    }

    for old, new in replacements.items():

        content = content.replace(
            old,
            new
        )

    # ==================================================
    # Parse Recommendations
    # ==================================================

    recommendations = []

    current = None

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        # ---------------------------------------------

        if line.startswith("Recommendation:"):

            if current:

                recommendations.append(current)

            current = {

                "recommendation": line.replace(
                    "Recommendation:",
                    ""
                ).strip()

            }

            continue

        if current is None:
            continue

        # ---------------------------------------------

        if line.startswith("Priority:"):

            current["priority"] = line.replace(
                "Priority:",
                ""
            ).strip()

        elif line.startswith("Supporting Evidence:"):

            current["evidence"] = line.replace(
                "Supporting Evidence:",
                ""
            ).strip()

        elif line.startswith("-"):

            evidence = current.get(
                "evidence",
                ""
            )

            evidence += " " + line.replace(
                "-",
                ""
            ).strip()

            current["evidence"] = evidence.strip()

        elif line.startswith("Expected Impact:"):

            current["impact"] = line.replace(
                "Expected Impact:",
                ""
            ).strip()

        elif line.startswith("Risk Level:"):

            current["risk_level"] = line.replace(
                "Risk Level:",
                ""
            ).strip()

    # ==================================================
    # Append Final Recommendation
    # ==================================================

    if current:

        recommendations.append(current)

    # ==================================================
    # Remove Empty Recommendations
    # ==================================================

    recommendations = [

        recommendation

        for recommendation in recommendations

        if recommendation.get(
            "recommendation"
        )

    ]

    # ==================================================
    # Debug Output
    # ==================================================

    print("\n==============================")
    print("RECOMMENDATION OUTPUT")
    print("==============================")

    print(content)

    print("\n==============================")
    print("PARSED RECOMMENDATIONS")
    print("==============================")

    print(
        "Recommendations:",
        len(recommendations)
    )

    # ==================================================
    # Return Structured Results
    # ==================================================

    return {

        "recommendations": recommendations,

        "raw_output": content

    }


# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    print(
        "Run this module from strategic_agent.py"
    )
