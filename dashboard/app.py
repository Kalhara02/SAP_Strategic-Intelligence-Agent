import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from datetime import datetime
import sys

# =========================================================
# Project Imports
# =========================================================

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agents.strategic_agent import run_agent

from tools.retrieval_tool import (
    retrieve_documents,
    get_repository_statistics
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(

    page_title="Executive Strategic Intelligence Dashboard",

    page_icon="📊",

    layout="wide"

)

st.markdown("""
<style>

.section-title{
    font-size:36px;
    font-weight:700;
    color:#FFFFFF !important;
    margin-top:25px;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# Executive Dashboard Styling
# =========================================================

st.markdown(
"""
<style>

/* Hide Streamlit menu */

#MainMenu {
    visibility:hidden;
}

footer {
    visibility:hidden;
}

header {
    visibility:hidden;
}

/* Main page */

.block-container{

    padding-top:2rem;
    padding-bottom:2rem;

}

/* Section Titles */

.section-title{

    font-size:30px;

    font-weight:700;

    color:#0F172A;

    margin-top:20px;

    margin-bottom:10px;

}

/* Dashboard Cards */

.metric-card{

    background:white;

    border-radius:12px;

    padding:18px;

    border:1px solid #E5E7EB;

    box-shadow:0 2px 10px rgba(0,0,0,.05);

}

/* Executive Cards */

.executive-card{

    background:#FFFFFF;

    border-left:6px solid #2563EB;

    padding:20px;

    border-radius:12px;

    margin-bottom:18px;

    box-shadow:0 2px 12px rgba(0,0,0,.08);

}

/* Dashboard Banner */

.banner{

    background:linear-gradient(
        90deg,
        #1E3A8A,
        #2563EB
    );

    color:white;

    padding:25px;

    border-radius:15px;

    margin-bottom:20px;

}

.banner h1{

    color:white;

    font-size:34px;

}

.banner p{

    font-size:17px;

}

.small-title{

    font-weight:600;

    color:#374151;

}

</style>
""",
unsafe_allow_html=True
)

# =========================================================
# Executive Header
# =========================================================

st.markdown(
"""
<div class="banner">

<h1>📊 Executive Strategic Intelligence Dashboard</h1>

<p>
AI-powered Executive Decision Support System
</p>

</div>
""",
unsafe_allow_html=True
)

# =========================================================
# Helper Functions
# =========================================================

def metric_card(label, value):

    st.metric(

        label,

        value

    )


def build_news_dataframe(results):

    rows = []

    for item in results:

        metadata = item.get("metadata", {})

        rows.append({

            "Title":

                metadata.get(

                    "title",

                    "Unknown Title"

                ),

            "Source":

                metadata.get(

                    "source",

                    "Unknown"

                )

        })

    return pd.DataFrame(rows)


def confidence_badge(score):

    try:

        score = int(score)

    except:

        return "Unknown"

    if score >= 85:

        return "🟢 High"

    elif score >= 70:

        return "🟡 Medium"

    return "🔴 Low"


def priority_color(priority):

    priority = str(priority).upper()

    if priority == "HIGH":

        return "🔴 HIGH"

    elif priority == "MEDIUM":

        return "🟡 MEDIUM"

    return "🟢 LOW"


st.divider()

# =========================================================
# SECTION 1
# Company Overview
# =========================================================

stats = get_repository_statistics()

company = "SAP"

industry = "ERP & Enterprise Software"

total_documents = stats["documents"]

data_sources = stats["sources"]

last_updated = datetime.now().strftime(
    "%d %b %Y %H:%M"
)

st.markdown(
'<div class="section-title">🏢 Company Overview</div>',
unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    metric_card(
        "Company",
        company
    )

with c2:

    metric_card(
        "Industry",
        industry
    )

with c3:

    metric_card(
        "Collected Documents",
        total_documents
    )

with c4:

    metric_card(
        "Data Sources",
        len(data_sources)
    )

with c5:

    metric_card(
        "Last Updated",
        last_updated
    )

with st.expander(
    "View Available Data Sources"
):

    for source in data_sources:

        st.write(f"• {source}")

st.divider()

# =========================================================
# SECTION 2
# Market Intelligence
# =========================================================

st.markdown(
'<div class="section-title">📰 Market Intelligence</div>',
unsafe_allow_html=True
)

st.caption(
"""
Latest strategic intelligence retrieved from the enterprise
knowledge repository.
"""
)

recent_news = retrieve_documents(
    "SAP latest enterprise software news",
    n_results=10
)

competitor_news = retrieve_documents(
    "SAP Oracle Microsoft Salesforce Workday competition",
    n_results=10
)

technology_news = retrieve_documents(
    "SAP AI Generative AI Cloud ERP Automation",
    n_results=10
)

announcement_news = retrieve_documents(
    "SAP partnership acquisition launch earnings investment",
    n_results=10
)

tab1, tab2, tab3, tab4 = st.tabs(

    [

        "📰 Recent News",

        "🏆 Competitor Activities",

        "🤖 Emerging Technologies",

        "📢 Company Announcements"

    ]

)

# =========================================================
# Recent News
# =========================================================

with tab1:

    df = build_news_dataframe(
        recent_news
    )

    if df.empty:

        st.info(
            "No recent news available."
        )

    else:

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

# =========================================================
# Competitor Activities
# =========================================================

with tab2:

    df = build_news_dataframe(
        competitor_news
    )

    if df.empty:

        st.info(
            "No competitor activities identified."
        )

    else:

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

# =========================================================
# Emerging Technologies
# =========================================================

with tab3:

    df = build_news_dataframe(
        technology_news
    )

    if df.empty:

        st.info(
            "No emerging technologies identified."
        )

    else:

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

# =========================================================
# Company Announcements
# =========================================================

with tab4:

    df = build_news_dataframe(
        announcement_news
    )

    if df.empty:

        st.info(
            "No company announcements identified."
        )

    else:

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

st.divider()

# =========================================================
# SECTION 3
# Strategic Goal
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Strategic Goal</div>',
    unsafe_allow_html=True
)

st.caption(
    """
    Define the strategic business objective to be analysed.
    The AI agent will automatically execute the workflow:
    Goal → Plan → Retrieve → Analyze → Decide → Recommend → Validate.
    """
)

goal = st.text_area(

    "Strategic Goal",

    placeholder="""
Examples

• What are SAP's major AI opportunities?

• What are SAP's biggest strategic risks?

• Which technologies should management monitor?

• What strategic actions should SAP prioritize?
""",

    height=150

)

run = st.button(

    "🚀 Execute Strategic Analysis",

    use_container_width=True,

    type="primary"

)

results = None

# =========================================================
# Execute Agent
# =========================================================

if run:

    if goal.strip() == "":

        st.warning(
            "Please enter a strategic goal."
        )

        st.stop()

    with st.spinner(

        "Executing Goal → Plan → Retrieve → Analyze → Decide → Recommend → Validate..."

    ):

        results = run_agent(goal)

# Nothing to display yet

if results is None:

    st.info(
        "Enter a strategic goal above to begin the analysis."
    )

    st.stop()

# =========================================================
# Error Handling
# =========================================================

if "error" in results:

    st.error(results["error"])

    st.stop()

# =========================================================
# Planner Information
# =========================================================

plan = results["plan"]

analysis_type = plan.get(

    "analysis_type",

    "general"

).lower()

priority = plan.get(

    "priority",

    "Normal"

)

generated_time = results.get(

    "generated_at",

    "-"

)

# =========================================================
# Dashboard Visibility
# =========================================================

show_opportunities = analysis_type in [

    "opportunity",

    "general"

]

show_risks = analysis_type in [

    "risk",

    "general"

]

show_trends = analysis_type in [

    "trend",

    "general"

]

show_recommendations = True

show_sentiment = True

show_ceo = True

# =========================================================
# SECTION 4
# Opportunity Monitor
# =========================================================

if show_opportunities:

    st.markdown(
        '<div class="section-title">📈 Opportunity Monitor</div>',
        unsafe_allow_html=True
    )

    st.caption(
        """
        Strategic opportunities identified by the Intelligence Agent
        based on the retrieved evidence. These opportunities represent
        areas where the company can gain competitive advantage or create
        additional business value.
        """
    )

    opportunities = results["intelligence"].get(
        "opportunities",
        []
    )

    if len(opportunities) == 0:

        st.info(
            "No strategic opportunities were identified."
        )

    else:

        for index, item in enumerate(
            opportunities,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"🚀 Opportunity {index}"
                )

                st.markdown(
                    f"### {item.get('title', '-')}"
                )

                description = item.get(
                    "description",
                    "-"
                )

                if description != "-":

                    st.write(description)

                st.write("")

                col1, col2 = st.columns(2)

                # -----------------------------
                # Impact
                # -----------------------------

                with col1:

                    impact = item.get(
                        "impact",
                        "-"
                    )

                    if impact.upper() == "HIGH":

                        impact = "🟢 HIGH"

                    elif impact.upper() == "MEDIUM":

                        impact = "🟡 MEDIUM"

                    elif impact.upper() == "LOW":

                        impact = "🔴 LOW"

                    st.metric(

                        "Impact Level",

                        impact

                    )

                # -----------------------------
                # Confidence
                # -----------------------------

                with col2:

                    confidence = item.get(
                        "confidence",
                        "-"
                    )

                    st.metric(

                        "Confidence Score",

                        f"{confidence}%"

                    )

                st.markdown(
                    "#### 📄 Supporting Evidence"
                )

                evidence = item.get(
                    "evidence",
                    "-"
                )

                st.info(
                    evidence
                )

                st.write("")

                st.success(
                    "Executive Insight: "
                    "This opportunity has been identified "
                    "using retrieved enterprise evidence "
                    "and AI-powered strategic analysis."
                )

    st.divider()

# =========================================================
# SECTION 5
# Risk Monitor
# =========================================================

if show_risks:

    st.markdown(
        '<div class="section-title">⚠️ Risk Monitor</div>',
        unsafe_allow_html=True
    )

    st.caption(
        """
        Strategic risks identified from the retrieved evidence.
        These risks may affect business performance,
        competitiveness, operations, or long-term growth.
        """
    )

    risks = results["intelligence"].get(
        "risks",
        []
    )

    if len(risks) == 0:

        st.info(
            "No significant strategic risks were identified."
        )

    else:

        for index, item in enumerate(
            risks,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"⚠️ Risk {index}"
                )

                st.markdown(
                    f"### {item.get('title', '-')}"
                )

                description = item.get(
                    "description",
                    "-"
                )

                if description != "-":

                    st.write(description)

                st.write("")

                col1, col2, col3 = st.columns(3)

                # ---------------------------------------
                # Risk Category
                # ---------------------------------------

                with col1:

                    category = item.get(
                        "category",
                        "-"
                    )

                    st.metric(

                        "Risk Category",

                        category

                    )

                # ---------------------------------------
                # Severity
                # ---------------------------------------

                with col2:

                    severity = item.get(
                        "severity",
                        "-"
                    )

                    if severity.upper() == "HIGH":

                        severity = "🔴 HIGH"

                    elif severity.upper() == "MEDIUM":

                        severity = "🟡 MEDIUM"

                    elif severity.upper() == "LOW":

                        severity = "🟢 LOW"

                    st.metric(

                        "Severity Level",

                        severity

                    )

                # ---------------------------------------
                # Confidence
                # ---------------------------------------

                with col3:

                    confidence = item.get(
                        "confidence",
                        "-"
                    )

                    st.metric(

                        "Confidence Score",

                        f"{confidence}%"

                    )

                st.markdown(
                    "#### 📄 Supporting Evidence"
                )

                evidence = item.get(
                    "evidence",
                    "-"
                )

                st.info(
                    evidence
                )

                st.write("")

                # ---------------------------------------
                # Executive Recommendation
                # ---------------------------------------

                severity_text = item.get(
                    "severity",
                    ""
                ).upper()

                if severity_text == "HIGH":

                    st.error(
                        "Executive Insight: "
                        "Immediate management attention is recommended "
                        "to mitigate this strategic risk."
                    )

                elif severity_text == "MEDIUM":

                    st.warning(
                        "Executive Insight: "
                        "Management should closely monitor this risk "
                        "and prepare mitigation strategies."
                    )

                else:

                    st.success(
                        "Executive Insight: "
                        "Current evidence suggests this risk is manageable, "
                        "but continued monitoring is recommended."
                    )

    st.divider()
    
# =========================================================
# Technology & Trend Monitor
# =========================================================

if show_trends:

    st.markdown(
        '<div class="section-title">🤖 Technology & Trend Monitor</div>',
        unsafe_allow_html=True
    )

    st.caption(
        """
        Emerging technologies and market trends identified from the
        retrieved evidence. These developments may influence future
        strategic planning, competitive positioning, and investment
        decisions.
        """
    )

    trends = results["intelligence"].get(
        "trends",
        []
    )

    if len(trends) == 0:

        st.info(
            "No significant technology trends were identified."
        )

    else:

        for index, item in enumerate(
            trends,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"📊 Technology Trend {index}"
                )

                st.markdown(
                    f"### {item.get('title', '-')}"
                )

                # -------------------------------------
                # Description
                # -------------------------------------

                description = item.get(
                    "description",
                    "-"
                )

                if description != "-":

                    st.write(description)

                st.write("")

                # -------------------------------------
                # Confidence
                # -------------------------------------

                confidence = item.get(
                    "confidence",
                    "-"
                )

                st.metric(

                    "Confidence Score",

                    f"{confidence}%"

                )

                # -------------------------------------
                # Supporting Evidence
                # -------------------------------------

                st.markdown(
                    "#### 📄 Supporting Evidence"
                )

                evidence = item.get(
                    "evidence",
                    "-"
                )

                st.info(
                    evidence
                )

                st.write("")

                # -------------------------------------
                # Management Insight
                # -------------------------------------

                st.success(
                    "Management Insight: "
                    "This technology or market trend may influence "
                    "future strategic priorities, innovation planning, "
                    "and competitive positioning."
                )

    st.divider()
# =========================================================
# SECTION 7
# Sentiment Analysis
# =========================================================

if show_sentiment:

    st.markdown(
        '<div class="section-title">😊 Sentiment Analysis</div>',
        unsafe_allow_html=True
    )

    st.caption(
        """
        Sentiment analysis summarises business news and public perception
        extracted from the retrieved evidence using the FinBERT
        sentiment analysis model.
        """
    )

    sentiment = results.get(
        "sentiment",
        {}
    )

    # ----------------------------------------------------
    # Values
    # ----------------------------------------------------

    news_sentiment = sentiment.get(
        "news_sentiment",
        "Unknown"
    )

    public_sentiment = sentiment.get(
        "public_sentiment",
        "Unknown"
    )

    overall_sentiment = sentiment.get(
        "overall_sentiment",
        "Unknown"
    )

    trend = sentiment.get(
        "trend",
        "Unknown"
    )

    positive = sentiment.get(
        "positive_articles",
        0
    )

    neutral = sentiment.get(
        "neutral_articles",
        0
    )

    negative = sentiment.get(
        "negative_articles",
        0
    )

    document_results = sentiment.get(
        "document_results",
        []
    )

    # =====================================================
    # KPI Cards
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "News Sentiment",
            news_sentiment
        )

    with c2:

        st.metric(
            "Public Sentiment",
            public_sentiment
        )

    with c3:

        st.metric(
            "Overall Sentiment",
            overall_sentiment
        )

    with c4:

        st.metric(
            "Sentiment Trend",
            trend
        )

    st.write("")

    # =====================================================
    # Charts
    # =====================================================

    left, right = st.columns(2)

    # ----------------------------------------------------
    # Pie Chart
    # ----------------------------------------------------

    with left:

        pie = go.Figure(

            data=[

                go.Pie(

                    labels=[

                        "Positive",

                        "Neutral",

                        "Negative"

                    ],

                    values=[

                        positive,

                        neutral,

                        negative

                    ],

                    hole=0.45

                )

            ]

        )

        pie.update_layout(

            title="Article Sentiment Distribution"

        )

        st.plotly_chart(

            pie,

            use_container_width=True

        )

    # ----------------------------------------------------
    # Bar Chart
    # ----------------------------------------------------

    with right:

        df = pd.DataFrame({

            "Sentiment": [

                "Positive",

                "Neutral",

                "Negative"

            ],

            "Articles": [

                positive,

                neutral,

                negative

            ]

        })

        fig = px.bar(

            df,

            x="Sentiment",

            y="Articles",

            text="Articles"

        )

        fig.update_layout(

            title="Sentiment by Number of Articles"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.write("")

# =========================================================
# SECTION 8
# Strategic Recommendations
# =========================================================

if show_recommendations:

    st.markdown(
        '<div class="section-title">🎯 Strategic Recommendations</div>',
        unsafe_allow_html=True
    )

    st.caption(
        """
        Evidence-based strategic recommendations generated by the
        Strategic Recommendation Agent. Each recommendation is
        prioritised according to its expected business impact,
        supporting evidence, and implementation risk.
        """
    )

    recommendation_result = results.get(
        "recommendations",
        {}
    )

    recommendations = recommendation_result.get(
        "recommendations",
        []
    )

    if not recommendations:

        st.info(
            "No strategic recommendations were generated."
        )

    else:

        for index, item in enumerate(
            recommendations,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"🎯 Recommendation {index}"
                )

                # --------------------------------------
                # Recommendation
                # --------------------------------------

                st.markdown(
                    f"### {item.get('recommendation', '-')}"
                )

                st.write("")

                # --------------------------------------
                # Priority / Risk
                # --------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    priority = item.get(
                        "priority",
                        "-"
                    ).upper()

                    if priority == "HIGH":

                        priority_display = "🔴 HIGH"

                    elif priority == "MEDIUM":

                        priority_display = "🟡 MEDIUM"

                    else:

                        priority_display = "🟢 LOW"

                    st.metric(

                        "Priority",

                        priority_display

                    )

                with col2:

                    risk = item.get(
                        "risk_level",
                        "-"
                    ).upper()

                    if risk == "HIGH":

                        risk_display = "🔴 HIGH"

                    elif risk == "MEDIUM":

                        risk_display = "🟡 MEDIUM"

                    else:

                        risk_display = "🟢 LOW"

                    st.metric(

                        "Risk Level",

                        risk_display

                    )

                st.write("")

                # --------------------------------------
                # Expected Impact
                # --------------------------------------

                st.markdown("#### 🚀 Expected Impact")

                st.markdown(
                    f"""
                    <div style="
                        background-color:#123524;
                        border-left:5px solid #22C55E;
                        padding:15px;
                        border-radius:8px;
                        color:white;
                        font-size:16px;
                        line-height:1.6;
                    ">
                    {item.get("impact", "-")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # --------------------------------------
                # Supporting Evidence
                # --------------------------------------

                st.markdown(
                    "#### 📄 Supporting Evidence"
                )

                st.info(
                    item.get(
                        "evidence",
                        "-"
                    )
                )

                st.write("")

                # --------------------------------------
                # Executive Note
                # --------------------------------------

                st.markdown(
                    """
                    **Executive Note**

                    This recommendation has been generated by combining
                    retrieved enterprise evidence with AI-driven
                    strategic analysis. Management should evaluate the
                    recommendation together with organisational priorities,
                    available resources, and business objectives.
                    """
                )

    st.divider()

# =========================================================
# SECTION 9
# CEO Briefing
# =========================================================

import re

if show_ceo:

    st.markdown(
        '<div class="section-title">📄 CEO Briefing</div>',
        unsafe_allow_html=True
    )

    st.caption(
        """
        Executive summary generated by the CEO Briefing Agent.
        This briefing provides a concise overview of the strategic
        findings, their business implications, and recommended
        management actions.
        """
    )

    briefing = results.get(
        "ceo_briefing",
        ""
    )

    if not briefing:

        st.info(
            "No CEO briefing was generated."
        )

    else:

        # ------------------------------------------------
        # Clean Output
        # ------------------------------------------------

        briefing = briefing.replace("**", "")
        briefing = briefing.replace("•", "")
        briefing = briefing.replace("#", "")

        briefing = re.sub(r"=+", "", briefing)

        sections = {

            "WHAT HAPPENED?": "",

            "WHY DOES IT MATTER?": "",

            "WHAT SHOULD MANAGEMENT DO NEXT?": ""

        }

        current = None

        for line in briefing.splitlines():

            text = line.strip()

            if not text:
                continue

            upper = text.upper()
                if (
                    "STRATEGIC INTELLIGENCE" in upper
                    or "RECOMMENDATION" in upper
                    or "RISKS" == upper
                    or "OPPORTUNITIES" == upper
                    or "TRENDS" == upper
                ):
                    current = None
                    continue

            if "WHAT HAPPENED" in upper:

                current = "WHAT HAPPENED?"
                continue

            elif "WHY DOES IT MATTER" in upper:

                current = "WHY DOES IT MATTER?"
                continue

            elif "WHAT SHOULD MANAGEMENT DO NEXT" in upper:

                current = "WHAT SHOULD MANAGEMENT DO NEXT?"
                continue

            if current:

                sections[current] += text + " "

        # ------------------------------------------------
        # Helper Function
        # ------------------------------------------------

        def executive_card(title, icon, body):

            if not body.strip():

                body = "No information available."

            st.markdown(
                f"""
                <div style="
                    border:1px solid #2f3542;
                    border-radius:12px;
                    padding:25px;
                    margin-bottom:20px;
                    background-color:#111827;
                ">

                <h2 style="margin-top:0;">
                    {icon} {title}
                </h2>

                <p style="
                    font-size:17px;
                    line-height:1.8;
                    text-align:justify;
                    color:#E5E7EB;
                    margin-top:15px;
                ">
                {body}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        # ------------------------------------------------
        # Display
        # ------------------------------------------------

        executive_card(

            "What Happened?",

            "📌",

            sections["WHAT HAPPENED?"]

        )

        executive_card(

            "Why Does It Matter?",

            "📈",

            sections["WHY DOES IT MATTER?"]

        )

        executive_card(

            "What Should Management Do Next?",

            "🚀",

            sections["WHAT SHOULD MANAGEMENT DO NEXT?"]

        )

    st.divider()

    st.caption(
        "Executive Strategic Intelligence Dashboard | "
        "MSc Project | Multi-Agent AI Decision Support System | "
        "Powered by Ollama, ChromaDB, FinBERT and Streamlit"
    )
