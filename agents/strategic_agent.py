from agents.planner import create_plan
from agents.decision_engine import (
    prioritize_findings,
    select_top_priorities
)
from agents.validator import validate_recommendations
from agents.memory import AgentMemory

from tools.retrieval_tool import retrieval_tool
from tools.intelligence_tool import generate_intelligence
from tools.recommendation_tool import generate_recommendations
from tools.ceo_tool import generate_ceo_briefing
from tools.sentiment_tool import sentiment_tool
from datetime import datetime


# ==================================================
# Initialize Memory
# ==================================================

memory = AgentMemory()


# ==================================================
# Strategic Agent
# ==================================================

def run_agent(question):

    print("\nCreating execution plan...")

    plan = create_plan(question)

    print("\nExecution Plan")
    print("-" * 40)
    print("Goal:", plan["goal"])
    print("Priority:", plan["priority"])
    print("Analysis:", plan["analysis_type"])
    print("Tools:", plan["tools"])
    print()

    results = {}

    evidence_documents = []
    intelligence = {
    "opportunities": [],
    "risks": [],
    "trends": [],
    "raw_output": ""
    }
    sentiment = {}
    priorities = []
    recommendations = ""
    validation = {}
    ceo_briefing = ""

    # ==================================================
    # Execute Tools
    # ==================================================

    total_steps = len(plan["tools"])

    for step, tool in enumerate(
        plan["tools"],
        start=1
    ):

        print(
            f"\nStep {step}/{total_steps} - "
            f"{tool.replace('_', ' ').title()}"
        )

# =============================================
# Retrieval
# =============================================

        if tool == "retrieval":

            try:

                evidence_documents = retrieval_tool(
                    plan["retrieval_query"],
                    n_results=10
                )

                results["evidence"] = evidence_documents

                print(
                    f"Retrieved {len(evidence_documents)} documents."
                )

                if not evidence_documents:

                    print("\nNo evidence retrieved.")

                    results["error"] = (
                        "No evidence was retrieved for the query."
                    )

                    break

            except Exception as e:

                print(
                    f"Retrieval Error: {e}"
                )

                evidence_documents = []

                results["evidence"] = []

                results["error"] = str(e)

                break

        # =============================================
        # Intelligence
        # =============================================

        elif tool == "intelligence":

            try:

                intelligence = generate_intelligence(
                    question=question,
                    evidence_documents=evidence_documents,
                    analysis_type=plan["analysis_type"]
                )

                results["intelligence"] = intelligence

                print("\nStrategic Intelligence Summary")
                print("=" * 60)
                print("Opportunities :", len(intelligence["opportunities"]))
                print("Risks         :", len(intelligence["risks"]))
                print("Trends        :", len(intelligence["trends"]))
                print("=" * 60)

            except Exception as e:

                print(f"Intelligence Error: {e}")

                intelligence = {
                    "opportunities": [],
                    "risks": [],
                    "trends": [],
                    "raw_output": ""
                }

                results["intelligence"] = intelligence

        # =============================================
        # Sentiment
        # =============================================

        elif tool == "sentiment":

            try:

                sentiment = sentiment_tool(
                    evidence_documents
                )

                results["sentiment"] = sentiment

                print("Sentiment analysis completed.")

            except Exception as e:

                print(
                    f"Sentiment Error: {e}"
                )

                sentiment = {}

        # =============================================
        # Decision Engine
        # =============================================

        elif tool == "decision":

            try:

                ranked = prioritize_findings(
                    intelligence,
                    sentiment
                )

                priorities = select_top_priorities(
                    ranked
                )

                results["priorities"] = priorities

                print("Priority ranking completed.")

            except Exception as e:

                print(
                    f"Decision Engine Error: {e}"
                )

                priorities = []

        # =============================================
        # Recommendation Agent
        # =============================================

        elif tool == "recommendation":

            try:

                recommendation_result = generate_recommendations(
                intelligence=intelligence,
                evidence_documents=evidence_documents
                )

                recommendations = recommendation_result["raw_output"]

                results["recommendations"] = recommendation_result

                print("\nDEBUG")
                print("=" * 60)
                print("Evidence documents :", len(evidence_documents))
                print("Opportunities      :", len(intelligence.get("opportunities", [])))
                print("Risks              :", len(intelligence.get("risks", [])))
                print("Trends             :", len(intelligence.get("trends", [])))
                print("=" * 60)

                print("Recommendations generated.")

            except Exception as e:

                print(f"Recommendation Error: {e}")

                recommendations = ""

                results["recommendations"] = {
                    "recommendations": [],
                    "raw_output": ""
                }

        # =============================================
        # Validation
        # =============================================

        elif tool == "validation":

            try:

                validation = validate_recommendations(
                    recommendations,
                    evidence_documents
                )

                results["validation"] = validation

                print("Recommendations validated.")

            except Exception as e:

                print(
                    f"Validation Error: {e}"
                )

                validation = {}

        # =============================================
        # CEO Briefing
        # =============================================

        elif tool == "ceo_briefing":

            try:

                ceo_briefing = generate_ceo_briefing(
                    intelligence,
                    recommendations,
                    validation
                )

                results["ceo_briefing"] = ceo_briefing

                print("CEO briefing generated.")

            except Exception as e:

                print(
                    f"CEO Briefing Error: {e}"
                )

                ceo_briefing = ""

    # ==================================================
    # Store Interaction
    # ==================================================

    memory.add_interaction(

        question=question,

        plan=plan,

        evidence=evidence_documents,

        intelligence=intelligence,

        sentiment=sentiment,

        priorities=priorities,

        recommendations=recommendations,

        validation=validation,

        ceo_briefing=ceo_briefing

    )

    # ==================================================
    # Store Results
    # ==================================================

    results["opportunities"] = intelligence.get(
        "opportunities",
        []
    )
 
    results["risks"] = intelligence.get(
        "risks",
        []
    )

    results["trends"] = intelligence.get(
        "trends",
        []
    )
    results["question"] = question

    results["plan"] = plan

    results["generated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    results["memory"] = memory.get_last_interaction()

    return results

# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    question = input(
        "\nStrategic Question: "
    )

    output = run_agent(question)

    print("\n")

    print("=" * 80)
    print("EXECUTION PLAN")
    print("=" * 80)
    print(output["plan"])

    if "sentiment" in output:

        print("\n")
        print("=" * 80)
        print("SENTIMENT ANALYSIS")
        print("=" * 80)
        print(output["sentiment"])

    if "priorities" in output:

        print("\n")
        print("=" * 80)
        print("PRIORITY DECISIONS")
        print("=" * 80)
        print(output["priorities"])

    if "intelligence" in output:

        print("\n")
        print("=" * 80)
        print("STRATEGIC INTELLIGENCE")
        print("=" * 80)
        print(output["intelligence"])

    if "recommendations" in output:

        print("\n")
        print("=" * 80)
        print("RECOMMENDATIONS")
        print("=" * 80)
        print(output["recommendations"])

    if "validation" in output:

        print("\n")
        print("=" * 80)
        print("VALIDATION")
        print("=" * 80)
        print(output["validation"])

    if "ceo_briefing" in output:

        print("\n")
        print("=" * 80)
        print("CEO BRIEFING")
        print("=" * 80)
        print(output["ceo_briefing"])

    print("\n")
    print("=" * 80)
    print("AGENT EXECUTION COMPLETE")
    print("=" * 80)