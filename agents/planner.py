# ==================================================
# Strategic Planner
# ==================================================

def create_plan(question):
    """
    Creates an execution plan for the Strategic Agent.

    Responsibilities:
    - Understand the user's intent
    - Select the analysis type
    - Set execution priority
    - Select which tools to execute

    The planner DOES NOT perform reasoning.
    The original user question is passed to the
    retrieval tool for semantic search.
    """

    question_lower = question.lower()

    goal = "General Strategic Intelligence"
    analysis_type = "general"
    priority = "Medium"

    # ==========================================
    # Opportunity Analysis
    # ==========================================

    if (
        "opportunity" in question_lower
        or
        "opportunities" in question_lower
    ):

        goal = "Opportunity Analysis"
        analysis_type = "opportunity"
        priority = "High"

    # ==========================================
    # Risk Analysis
    # ==========================================

    elif (
        "risk" in question_lower
        or
        "risks" in question_lower
        or
        "threat" in question_lower
        or
        "threats" in question_lower
    ):

        goal = "Risk Analysis"
        analysis_type = "risk"
        priority = "High"

    # ==========================================
    # Competitor Analysis
    # ==========================================

    elif (

        "competitor" in question_lower

        or

        "competition" in question_lower

    ):

        goal = "Competitor Analysis"
        analysis_type = "competitor"
        priority = "High"

    # ==========================================
    # Technology Trends
    # ==========================================

    elif (

        "trend" in question_lower

        or

        "trends" in question_lower

        or

        "technology" in question_lower

        or

        "technologies" in question_lower

        or

        "innovation" in question_lower

    ):

        goal = "Technology Trend Analysis"
        analysis_type = "trend"
        priority = "Medium"

    # ==========================================
    # Strategic Recommendations
    # ==========================================

    elif (

        "recommend" in question_lower

        or

        "strategy" in question_lower

        or

        "prioritize" in question_lower

        or

        "next" in question_lower

    ):

        goal = "Strategic Recommendation"
        analysis_type = "strategy"
        priority = "High"

    # ==========================================
    # Build Plan
    # ==========================================

    plan = {

        "goal": goal,

        # Use the original question for semantic retrieval
        "retrieval_query": question,

        "analysis_type": analysis_type,

        "priority": priority,

        "tools": [

            "retrieval",

            "intelligence",

            "sentiment",

            "decision",

            "recommendation",

            "validation",

            "ceo_briefing"

        ],
        
        "company": "SAP",

        "industry": "ERP & Enterprise Software"

    }

    return plan