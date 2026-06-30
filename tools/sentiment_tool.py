from intelligence.sentiment_service import analyze_sentiment


# ==================================================
# Sentiment Tool
# ==================================================

def sentiment_tool(evidence_documents):
    """
    Run sentiment analysis on the retrieved evidence.

    Parameters
    ----------
    evidence_documents : list

    Returns
    -------
    dict
        Sentiment analysis results.
    """

    return analyze_sentiment(
        evidence_documents
    )