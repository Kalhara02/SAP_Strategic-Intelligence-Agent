import ollama
import re


# ==================================================
# CEO Briefing Generator
# ==================================================

def generate_ceo_briefing(
    intelligence,
    recommendations,
    validation
):
    """
    Generate an executive briefing using the outputs
    from the Strategic Agent.

    Inputs:
        intelligence
        recommendations
        validation

    Output:
        Executive-level briefing.
    """

    # ==================================================
    # Input Validation
    # ==================================================

    if not intelligence:

        return (
            "CEO briefing could not be generated.\n\n"
            "Reason: Strategic intelligence is unavailable."
        )

    if not recommendations:

        return (
            "CEO briefing could not be generated.\n\n"
            "Reason: Recommendations are unavailable."
        )

    # ==================================================
    # Prompt
    # ==================================================

    prompt = f"""
/no_think

You are a CEO Strategic Advisor.

Your audience is the Executive Board.

Create a concise executive briefing using ONLY the supplied information.

Rules

- Use ONLY the information provided.
- Do NOT invent facts.
- Do NOT introduce new recommendations.
- Do NOT copy the input headings.
- Do NOT output "Strategic Intelligence".
- Do NOT output "Recommendations".
- Do NOT output "Validation".
- Do NOT include evidence.
- Do NOT include confidence scores.
- Do NOT include markdown.
- Use professional executive language.
- Maximum 100 words per section.

Return ONLY the following three sections.

WHAT HAPPENED?

WHY DOES IT MATTER?

WHAT SHOULD MANAGEMENT DO NEXT?

--------------------------------------------------

INPUT INFORMATION

Strategic Intelligence

{intelligence}

Recommendations

{recommendations}

Validation

{validation}

"""

    # ==================================================
    # Generate Briefing
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
                "temperature": 0.15,
                "num_predict": 700
            }

        )

        message = response.get("message", {})

        content = message.get("content", "").strip()

        if not content:
            content = message.get("thinking", "").strip()

    except Exception as e:

        return f"CEO briefing generation failed.\n\n{e}"

    # ==================================================
    # Empty Response
    # ==================================================

    if not content:

        return (
            "CEO briefing could not be generated.\n\n"
            "The language model returned an empty response."
        )

    # ==================================================
    # Clean Output
    # ==================================================

    content = content.replace("**", "")
    content = content.replace("•", "• ")
    content = re.sub(r"=+", "", content)

    # Remove unwanted sections if model echoes them
    unwanted_sections = [

        "STRATEGIC INTELLIGENCE",
        "RECOMMENDATIONS",
        "VALIDATION"

    ]

    upper = content.upper()

    cut_position = len(content)

    for heading in unwanted_sections:

        pos = upper.find(heading)

        if pos != -1:

            cut_position = min(cut_position, pos)

    content = content[:cut_position].strip()

    # Remove duplicate blank lines
    content = re.sub(r"\n\s*\n+", "\n\n", content)

    # ==================================================
    # Debug Output
    # ==================================================

    print("\n==========================")
    print("CEO BRIEFING OUTPUT")
    print("==========================")
    print(content)

    return content


# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    print(
        "Run this module from strategic_agent.py"
    )