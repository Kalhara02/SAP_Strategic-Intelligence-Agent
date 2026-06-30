import numpy as np
from transformers import pipeline

# Load FinBERT once
sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)

def analyze_sentiment(evidence_documents):
    """
    Analyze sentiment using FinBERT with
    business-aware scoring.
    """

    positive = 0
    neutral = 0
    negative = 0

    scores = []

    document_results = []

    positive_keywords = [
        "growth",
        "innovation",
        "partnership",
        "investment",
        "expansion",
        "profit",
        "opportunity",
        "leadership",
        "success",
        "record",
        "acquisition"
    ]

    negative_keywords = [
        "risk",
        "decline",
        "lawsuit",
        "loss",
        "competition",
        "layoff",
        "delay",
        "security",
        "breach",
        "regulation",
        "uncertainty"
    ]

    for item in evidence_documents:

        document = item["document"]
        metadata = item["metadata"]

        text = str(document).strip()

        # Ignore tiny documents
        if len(text) < 80:
            continue

        prediction = sentiment_model(text[:512])[0]

        label = prediction["label"].lower()

        confidence = float(
            prediction["score"]
        )

        score = 0

        if label == "positive":

            score = confidence
            positive += 1

        elif label == "negative":

            score = -confidence
            negative += 1

        else:

            neutral += 1

        lower = text.lower()

        keyword_bonus = 0

        for word in positive_keywords:

            if word in lower:
                keyword_bonus += 0.05

        for word in negative_keywords:

            if word in lower:
                keyword_bonus -= 0.05

        score += keyword_bonus

        score = max(-1, min(score, 1))

        scores.append(score)

        document_results.append(

            {

                "title": metadata.get(
                    "title",
                    "Unknown Title"
                ),

                "source": metadata.get(
                    "source",
                    "Unknown Source"
                ),

                "sentiment": label.capitalize(),

                "confidence": round(
                    confidence * 100,
                    2
                ),

                "score": round(
                    score,
                    3
                )

            }

        )

    # --------------------------------------
    # Overall Score
    # --------------------------------------

    average_score = np.mean(scores) if scores else 0

    if average_score >= 0.15:

        overall = "Positive"

    elif average_score <= -0.15:

        overall = "Negative"

    else:

        overall = "Neutral"

    # --------------------------------------
    # Trend
    # --------------------------------------

    if len(scores) >= 3:

        first_half = np.mean(
            scores[:len(scores)//2]
        )

        second_half = np.mean(
            scores[len(scores)//2:]
        )

        if second_half > first_half + 0.05:

            trend = "Improving"

        elif second_half < first_half - 0.05:

            trend = "Declining"

        else:

            trend = "Stable"

    else:

        trend = "Stable"

    # --------------------------------------
    # News/Public Split
    # --------------------------------------

    news_scores = []
    public_scores = []

    for item, score in zip(
        evidence_documents,
        scores
    ):

        source = item["metadata"].get(
            "source",
            ""
        ).lower()

        if "reddit" in source:

            public_scores.append(score)

        else:

            news_scores.append(score)

    news_score = np.mean(news_scores) if news_scores else average_score

    public_score = np.mean(public_scores) if public_scores else average_score

    def label(score):

        if score >= 0.15:
            return "Positive"

        elif score <= -0.15:
            return "Negative"

        return "Neutral"

    return {

        "news_sentiment": label(news_score),

        "public_sentiment": label(public_score),

        "overall_sentiment": overall,

        "news_score": round(news_score, 3),

        "public_score": round(public_score, 3),

        "overall_score": round(average_score, 3),

        "trend": trend,

        "positive_articles": positive,

        "neutral_articles": neutral,

        "negative_articles": negative,

        "document_results": document_results

    }