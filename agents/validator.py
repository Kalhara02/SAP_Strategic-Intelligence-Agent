# ==================================================
# Recommendation Validator
# ==================================================

def validate_recommendations(
    recommendations,
    evidence_documents
):
    """
    Validate the generated recommendations using
    the retrieved evidence.

    Validation checks:
    - Recommendations exist
    - Evidence exists
    - Required recommendation sections exist
    - Recommendations reference retrieved evidence
    - Overall validation confidence
    """

    validation = {

        "is_valid": True,

        "confidence": "High",

        "validation_score": 0,

        "issues": [],

        "checks": {}

    }

    # ==================================================
    # Recommendation Exists
    # ==================================================

    if not recommendations or not recommendations.strip():

        validation["is_valid"] = False

        validation["issues"].append(
            "No recommendations were generated."
        )

        validation["checks"]["recommendations"] = False

    else:

        validation["checks"]["recommendations"] = True

    # ==================================================
    # Evidence Exists
    # ==================================================

    if not evidence_documents:

        validation["is_valid"] = False

        validation["issues"].append(
            "No supporting evidence retrieved."
        )

        validation["checks"]["evidence"] = False

    else:

        validation["checks"]["evidence"] = True

    # ==================================================
    # Required Sections
    # ==================================================

    required_sections = [

        "Recommendation",

        "Priority",

        "Supporting Evidence",

        "Expected Impact",

        "Risk Level"

    ]

    missing_sections = []

    recommendations_lower = recommendations.lower()

    for section in required_sections:

        if section.lower() not in recommendations_lower:

            missing_sections.append(section)

    if missing_sections:

        validation["is_valid"] = False

        validation["issues"].append(

            "Missing sections: "

            + ", ".join(missing_sections)

        )

        validation["checks"]["format"] = False

    else:

        validation["checks"]["format"] = True

    # ==================================================
    # Evidence Reference Validation
    # ==================================================

    matched_titles = 0

    if evidence_documents:

        for item in evidence_documents:

            metadata = item.get("metadata", {})

            title = metadata.get(
                "title",
                ""
            ).strip()

            if (
                title
                and
                title.lower() in recommendations_lower
            ):

                matched_titles += 1

    if matched_titles > 0:

        validation["checks"]["evidence_reference"] = True

    else:

        validation["checks"]["evidence_reference"] = False

        validation["issues"].append(
            "Recommendations do not reference retrieved evidence."
        )

        validation["is_valid"] = False

    # ==================================================
    # Confidence Calculation
    # ==================================================

    passed_checks = sum(

        validation["checks"].values()

    )

    total_checks = len(

        validation["checks"]

    )

    if total_checks == 0:

        score = 0

    else:

        score = passed_checks / total_checks

    validation["validation_score"] = round(
        score * 100,
        1
    )

    if score >= 0.90:

        validation["confidence"] = "High"

    elif score >= 0.70:

        validation["confidence"] = "Medium"

    else:

        validation["confidence"] = "Low"

    return validation


# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    sample_recommendation = """

Recommendation:
Expand SAP AI services.

Priority:
HIGH

Supporting Evidence:
SAP launches new AI platform (Reuters)

Expected Impact:
Revenue Growth

Risk Level:
LOW

"""

    sample_evidence = [

        {

            "metadata": {

                "title": "SAP launches new AI platform",

                "source": "Reuters"

            },

            "document": "SAP announced a new enterprise AI platform."

        }

    ]

    result = validate_recommendations(

        sample_recommendation,

        sample_evidence

    )

    print("\nValidation Result\n")
    print(result)