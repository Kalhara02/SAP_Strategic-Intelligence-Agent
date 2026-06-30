from intelligence.intelligence_service import generate_intelligence


# ==================================================
# Intelligence Tool
# ==================================================

def intelligence_tool(
    question,
    evidence_documents
):
    """
    Generate strategic intelligence from retrieved evidence.
    """

    return generate_intelligence(
        question,
        evidence_documents
    )