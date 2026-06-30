import ollama


# ==========================================================
# Strategic Intelligence Generator
# ==========================================================

def generate_intelligence(
    question,
    evidence_documents,
    analysis_type
):

    # ======================================================
    # Remove Low Value Documents
    # ======================================================

    blocked_keywords = [

        "career",
        "consultant",
        "job",
        "salary",
        "student",
        "training",
        "certification",
        "reddit",
        "freelance"

    ]

    filtered_documents = []

    for item in evidence_documents:

        document = item.get(
            "document",
            ""
        )

        if any(
            keyword in document.lower()
            for keyword in blocked_keywords
        ):
            continue

        filtered_documents.append(item)

    # ======================================================
    # Build Evidence Context
    # ======================================================

    evidence = ""

    for i, item in enumerate(
        filtered_documents[:6],
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
        )[:500]

        evidence += f"""

==================================================
TITLE:
{title}

SOURCE:
{source}

CONTENT:
{document}

"""

    # ======================================================
    # Decide Required Analysis
    # ======================================================

    if analysis_type == "opportunity":

        required_output = """
Return EXACTLY THREE Opportunities.

Do NOT generate Risks.

Do NOT generate Trends.

Return ONLY this format.

==================================================
OPPORTUNITIES
==================================================

Title:
Description:
Impact Level:
Supporting Evidence:
Confidence Score:

Title:
Description:
Impact Level:
Supporting Evidence:
Confidence Score:

Title:
Description:
Impact Level:
Supporting Evidence:
Confidence Score:

"""

    elif analysis_type == "risk":

        required_output = """

Return EXACTLY THREE Risks.

Do NOT generate Opportunities.

Do NOT generate Trends.

Return ONLY this format.

==================================================
RISKS
==================================================

Title:
Description:
Risk Category:
Severity Level:
Supporting Evidence:
Confidence Score:

Title:
Description:
Risk Category:
Severity Level:
Supporting Evidence:
Confidence Score:

Title:
Description:
Risk Category:
Severity Level:
Supporting Evidence:
Confidence Score:

"""

    elif analysis_type == "trend":

        required_output = """

Return EXACTLY THREE Trends.

Do NOT generate Opportunities.

Do NOT generate Risks.

Return ONLY this format.

==================================================
TRENDS
==================================================

Title:
Description:
Supporting Evidence:
Confidence Score:

Title:
Description:
Supporting Evidence:
Confidence Score:

Title:
Description:
Supporting Evidence:
Confidence Score:

"""

    else:

        required_output = """

Return EXACTLY

THREE Opportunities

THREE Risks

THREE Emerging Trends

"""

    # ======================================================
    # Prompt
    # ======================================================

    prompt = f"""
You are an Executive Strategic Intelligence Analyst.

Analyse ONLY the supplied evidence.

Never invent facts.

{required_output}

Rules

1. Use ONLY supplied evidence.

2. Never invent companies.

3. Never invent article titles.

4. Supporting Evidence MUST contain the EXACT article title and source.

Example

SAP ramps up push to bring AI agents to finance teams (CFO Dive)

Do NOT write

Article 1

Article 2

Evidence 1

5. Keep descriptions under 35 words.

6. Confidence Score must be between 0 and 100.

Question

{question}

==================================================
EVIDENCE
==================================================

{evidence}

"""

    # ======================================================
    # LLM Call
    # ======================================================
    print("\n========== DEBUG ==========")
    print("Question:", question)
    print("Analysis Type:", analysis_type)
    print("Evidence Length:", len(evidence))
    print("===========================\n")

    response = ollama.chat(

        model="qwen3:8b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={

            "temperature": 0.1,

            "num_predict": 900

        }

    )

    content = response["message"]["content"]
    
    print("\nReturned characters:", len(content))

    print("\n==============================")
    print("RAW INTELLIGENCE OUTPUT")
    print("==============================")
    print(content)

    # ======================================================
    # Parse Output
    # ======================================================

    opportunities = []

    risks = []

    trends = []

    current_section = None

    current = None

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        upper = (
            line.upper()
            .replace("*", "")
            .replace("#", "")
            .replace("=", "")
            .replace(":", "")
            .strip()
        )

        # --------------------------------------------------

        if upper == "OPPORTUNITIES":

            if current:

                if current_section == "opportunities":
                    opportunities.append(current)

                elif current_section == "risks":
                    risks.append(current)

                elif current_section == "trends":
                    trends.append(current)

            current = None

            current_section = "opportunities"

            continue

        # --------------------------------------------------

        if upper == "RISKS":

            if current:

                if current_section == "opportunities":
                    opportunities.append(current)

                elif current_section == "risks":
                    risks.append(current)

                elif current_section == "trends":
                    trends.append(current)

            current = None

            current_section = "risks"

            continue

        # --------------------------------------------------

        if upper == "TRENDS":

            if current:

                if current_section == "opportunities":
                    opportunities.append(current)

                elif current_section == "risks":
                    risks.append(current)

                elif current_section == "trends":
                    trends.append(current)

            current = None

            current_section = "trends"

            continue

        # --------------------------------------------------

        if line.startswith("Title:"):

            if current:

                if current_section == "opportunities":
                    opportunities.append(current)

                elif current_section == "risks":
                    risks.append(current)

                elif current_section == "trends":
                    trends.append(current)

            current = {

                "title": line.replace(
                    "Title:",
                    ""
                ).strip()

            }

            continue

        if current is None:
            continue

        # --------------------------------------------------

        if line.startswith("Description:"):

            current["description"] = line.replace(
                "Description:",
                ""
            ).strip()

        elif line.startswith("Impact Level:"):

            current["impact"] = line.replace(
                "Impact Level:",
                ""
            ).strip()

        elif line.startswith("Risk Category:"):

            current["category"] = line.replace(
                "Risk Category:",
                ""
            ).strip()

        elif line.startswith("Severity Level:"):

            current["severity"] = line.replace(
                "Severity Level:",
                ""
            ).strip()

        elif line.startswith("Supporting Evidence:"):

            current["evidence"] = line.replace(
                "Supporting Evidence:",
                ""
            ).strip()

        elif line.startswith("Confidence Score:"):

            score = (
                line.replace(
                    "Confidence Score:",
                    ""
                )
                .replace("%", "")
                .strip()
            )

            try:

                current["confidence"] = int(score)

            except:

                current["confidence"] = 75

    # ======================================================
    # Append Final Record
    # ======================================================

    if current:

        if current_section == "opportunities":
            opportunities.append(current)

        elif current_section == "risks":
            risks.append(current)

        elif current_section == "trends":
            trends.append(current)

    # ======================================================
    # Remove Empty Items
    # ======================================================

    opportunities = [
        item for item in opportunities
        if item.get("title")
    ]

    risks = [
        item for item in risks
        if item.get("title")
    ]

    trends = [
        item for item in trends
        if item.get("title")
    ]

    # ======================================================
    # Debug
    # ======================================================

    print("\n==============================")
    print("PARSED RESULTS")
    print("==============================")
    print("Analysis Type :", analysis_type)
    print("Opportunities :", len(opportunities))
    print("Risks         :", len(risks))
    print("Trends        :", len(trends))

    # ======================================================
    # Return
    # ======================================================

    return {

        "opportunities": opportunities,

        "risks": risks,

        "trends": trends,

        "raw_output": content

    }


# ==========================================================
# Standalone Test
# ==========================================================

if __name__ == "__main__":

    print(
        "Run this module from strategic_agent.py"
    )