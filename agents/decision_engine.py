# ==================================================
# Decision Engine
# ==================================================

def prioritize_findings(
    intelligence,
    sentiment
):
    """
    Prioritize strategic findings using
    intelligence analysis and sentiment analysis.
    """

    ranked_findings = []

    # Accept either a dict (from the agent) or a plain string (standalone test)
    if isinstance(intelligence, dict):
        parts = [intelligence.get("raw_output", "")]
        for key in ("opportunities", "risks", "trends"):
            for item in intelligence.get(key, []):
                parts.append(item.get("title", ""))
                parts.append(item.get("description", ""))
                parts.append(str(item.get("impact", "")))
                parts.append(str(item.get("severity", "")))
        intelligence_text = " ".join(parts).lower()
    else:
        intelligence_text = str(intelligence).lower()

    # ==================================================
    # Intelligence Score
    # ==================================================

    intelligence_score = 3

    high_keywords = [
        "high",
        "critical",
        "major",
        "significant",
        "urgent",
        "strategic",
        "leadership",
        "opportunity",
        "competitive advantage",
        "innovation",
        "investment"
    ]

    medium_keywords = [
        "medium",
        "moderate",
        "growth",
        "improve",
        "expansion",
        "partnership",
        "technology",
        "market"
    ]

    low_keywords = [
        "low",
        "minor",
        "limited"
    ]

    high_hits = sum(
        keyword in intelligence_text
        for keyword in high_keywords
    )

    medium_hits = sum(
        keyword in intelligence_text
        for keyword in medium_keywords
    )

    low_hits = sum(
        keyword in intelligence_text
        for keyword in low_keywords
    )

    if high_hits >= 3:

        intelligence_score = 5

    elif high_hits >= 1 or medium_hits >= 3:

        intelligence_score = 4

    elif medium_hits >= 1:

        intelligence_score = 3

    elif low_hits >= 1:

        intelligence_score = 2

    else:

        intelligence_score = 3

    # ==================================================
    # Sentiment Score
    # ==================================================

    sentiment_score = 3

    overall_sentiment = sentiment.get(
        "overall_sentiment",
        "Neutral"
    )

    trend = sentiment.get(
        "trend",
        "Stable"
    )

    if overall_sentiment == "Negative":

        sentiment_score = 5

    elif overall_sentiment == "Positive":

        sentiment_score = 2

    else:

        sentiment_score = 3

    # Trend Adjustment

    if trend == "Declining":

        sentiment_score += 0.5

    elif trend == "Improving":

        sentiment_score -= 0.5

    sentiment_score = max(
        1,
        min(5, sentiment_score)
    )

    # ==================================================
    # Combined Priority Score
    # ==================================================

    priority_score = round(

        (
            intelligence_score * 0.7 +
            sentiment_score * 0.3
        ),

        2

    )

    # ==================================================
    # Priority Level
    # ==================================================

    if priority_score >= 4.5:

        priority = "HIGH"

    elif priority_score >= 3:

        priority = "MEDIUM"

    else:

        priority = "LOW"

    ranked_findings.append(

        {

            "priority": priority,

            "priority_score": priority_score,

            "intelligence_score": intelligence_score,

            "sentiment_score": sentiment_score,

            "overall_sentiment": overall_sentiment,

            "trend": trend

        }

    )

    return ranked_findings


# ==================================================
# Select Top Priorities
# ==================================================

def select_top_priorities(
    ranked_findings
):
    """
    Return the highest-priority findings.
    """

    ranked_findings = sorted(

        ranked_findings,

        key=lambda x: x["priority_score"],

        reverse=True

    )

    return ranked_findings[:3]


# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    intelligence = """
    High impact opportunity identified through
    AI cloud expansion and strategic partnerships.
    """

    sentiment = {

        "overall_sentiment": "Neutral",

        "trend": "Stable"

    }

    ranked = prioritize_findings(

        intelligence,

        sentiment

    )

    print("\nRanked Findings\n")

    print(ranked)

    print("\nTop Priorities\n")

    print(

        select_top_priorities(

            ranked

        )

    )