import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
from pathlib import Path
from datetime import datetime
import sys

# ==================================================
# PATH SETUP
# ==================================================

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

# ==================================================
# IMPORT AI SERVICES
# ==================================================

from intelligence.intelligence_service import (
    generate_intelligence
)
from agents.recommendation_service import (
    generate_recommendations
)

from agents.ceo_agent_service import (
    generate_ceo_briefing
)
# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="SAP Executive Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(
    ROOT / "data" / "clean_documents.csv"
)

# ==================================================
# SESSION STATE
# ==================================================

if "recommendation_text" not in st.session_state:
    st.session_state.recommendation_text = ""

if "ceo_briefing_text" not in st.session_state:
    st.session_state.ceo_briefing_text = ""
    
if "intelligence_text" not in st.session_state:
    st.session_state.intelligence_text = ""

# ==================================================
# SENTIMENT ANALYSIS
# ==================================================

def get_sentiment(text):

    try:
        return TextBlob(
            str(text)
        ).sentiment.polarity

    except:
        return 0

df["sentiment"] = df["content"].apply(
    get_sentiment
)

# =====================================
# CURRENT INTELLIGENCE SENTIMENT
# =====================================

current_text = (
    st.session_state.intelligence_text
)

if current_text:

    current_sentiment = get_sentiment(
        current_text
    )

else:

    current_sentiment = 0
    
# ==================================================
# HEADER
# ==================================================

st.title(
    "📊 SAP Executive Intelligence Dashboard"
)

st.caption(
    "AI-Powered Strategic Decision Support System"
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header(
    "Executive Controls"
)
st.sidebar.markdown("---")

st.sidebar.caption(
    "AI-Powered Executive Decision Support"
)

run_analysis = st.sidebar.button(
    "Generate Intelligence"
)

run_recommendations = st.sidebar.button(
    "Generate Recommendations"
)

run_ceo_briefing = st.sidebar.button(
    "Generate CEO Briefing"
)

# ==================================================
# SECTION 1
# COMPANY OVERVIEW
# ==================================================

st.header(
    "🏢 Company Overview"
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Company",
    "SAP"
)

c2.metric(
    "Industry",
    "ERP & Enterprise Software"
)

c3.metric(
    "Collected Documents",
    len(df)
)

c4.metric(
    "Data Sources",
    df["source"].nunique()
)

c5.metric(
    "Last Updated",
    datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )
)

# ==================================================
# SECTION 2
# MARKET INTELLIGENCE
# ==================================================

st.header(
    "📰 Market Intelligence"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Recent News",
        "Competitor Activities",
        "Emerging Technologies",
        "Company Announcements"
    ]
)

# ------------------------------------------
# RECENT NEWS
# ------------------------------------------

with tab1:

    st.dataframe(
        df[
            ["title", "source"]
        ].tail(10),
        use_container_width=True
    )

# ------------------------------------------
# COMPETITOR ACTIVITIES
# ------------------------------------------

competitors = [
    "oracle",
    "microsoft",
    "salesforce",
    "workday"
]

competitor_df = df[
    df["content"].str.contains(
        "|".join(competitors),
        case=False,
        na=False
    )
]

with tab2:

    st.dataframe(
        competitor_df[
            ["title", "source"]
        ].head(10),
        use_container_width=True
    )

# ------------------------------------------
# EMERGING TECHNOLOGIES
# ------------------------------------------

tech_keywords = [
    "artificial intelligence",
    "ai",
    "generative ai",
    "machine learning",
    "cloud",
    "agentic"
]

tech_df = df[
    df["content"].str.contains(
        "|".join(tech_keywords),
        case=False,
        na=False
    )
]

with tab3:

    st.dataframe(
        tech_df[
            ["title", "source"]
        ].head(10),
        use_container_width=True
    )

# ------------------------------------------
# COMPANY ANNOUNCEMENTS
# ------------------------------------------

announcement_keywords = [
    "announcement",
    "announces",
    "launch",
    "launched",
    "release",
    "released",
    "introduces",
    "introduced",
    "unveils",
    "earnings",
    "quarterly results"
]

announcement_df = df[
    df["title"].str.contains(
        "|".join(announcement_keywords),
        case=False,
        na=False
    )
]

with tab4:

    st.dataframe(
        announcement_df[
            ["title", "source"]
        ].head(10),
        use_container_width=True
    )

# ==================================================
# STRATEGIC INTELLIGENCE ENGINE
# ==================================================

st.markdown("---")

st.header(
    "🎯 Strategic Intelligence Engine"
)

question = st.selectbox(
    "Choose a Strategic Question",
    [
        "What are the major opportunities for SAP?",
        "What are the biggest risks facing SAP?",
        "What are competitors doing?",
        "Which technologies or trends should management monitor?",
        "What strategic actions should SAP prioritize?",
        "What evidence supports these recommendations?"
    ]
)

# ==================================================
# AI INTELLIGENCE
# ==================================================

if run_analysis:
    st.session_state.recommendation_text = ""
    st.session_state.ceo_briefing_text = ""

    st.success(
        "Strategic Intelligence Generated"
)
    
    with st.spinner(
        "Generating Strategic Intelligence..."
    ):

        st.session_state.intelligence_text = (
            generate_intelligence(
                question
            )
        )
# ==================================================
# STRATEGIC RECOMMENDATIONS
# ==================================================

if run_recommendations:
    st.success(
        "Recommendations Generated"
)
    
    with st.spinner(
        "Generating Strategic Recommendations..."
    ):

        st.session_state.recommendation_text = (
            generate_recommendations(
                question
            )
        )

# ==================================================
# CEO BRIEFING
# ==================================================

if run_ceo_briefing:
    st.success(
        "CEO Briefing Generated"
)
    
    with st.spinner(
        "Generating CEO Briefing..."
    ):

        st.session_state.ceo_briefing_text = (
            generate_ceo_briefing(
                question
            )
        )

# ==================================================
# SECTION 3
# STRATEGIC INTELLIGENCE REPORT
# ==================================================

st.header(
    "📈 Executive Intelligence Report"
)

if st.session_state.intelligence_text:

    st.markdown(
        st.session_state.intelligence_text
    )

else:

    st.info(
        "Click 'Generate Intelligence' to generate strategic intelligence."
    )
    
# ==================================================
# SECTION 4
# STRATEGIC RECOMMENDATIONS
# ==================================================

st.header(
    "🎯 Strategic Recommendations"
)

if st.session_state.recommendation_text:
    
    recommendations = (
        st.session_state.recommendation_text
        .split(
            "=================================================="
        )
    )

    counter = 1

    for rec in recommendations:

        if "Recommendation:" not in rec:
            continue

        with st.expander(
            f"Recommendation {counter}"
        ):

            st.write(rec)

        counter += 1
else: 
    st.info(
        "Click 'Generate Recommendations' to generate strategic recommendations."
    )
# ==================================================
# SECTION 5
# CEO BRIEFING
# ==================================================

st.header(
    "👔 CEO Briefing"
)

if st.session_state.ceo_briefing_text:

    briefing = st.session_state.ceo_briefing_text

    st.subheader(
        "📌 What Happened?"
    )

    if "WHY DOES IT MATTER?" in briefing:

        happened = briefing.split(
            "WHY DOES IT MATTER?"
        )[0]

        happened = happened.replace(
            "WHAT HAPPENED?",
            ""
        )

        happened = happened.replace(
            "==================================================",
            ""
        )

        st.markdown(
            happened.strip()
        )

    st.subheader(
        "📌 Why Does It Matter?"
    )

    if (
        "WHY DOES IT MATTER?" in briefing
        and
        "WHAT SHOULD MANAGEMENT DO NEXT?" in briefing
    ):

        matter = briefing.split(
            "WHY DOES IT MATTER?"
        )[1].split(
            "WHAT SHOULD MANAGEMENT DO NEXT?"
        )[0]

        matter = matter.replace(
            "==================================================",
            ""
        )

        st.markdown(
            matter.strip()
        )

    st.subheader(
        "📌 What Should Management Do Next?"
    )

    if "WHAT SHOULD MANAGEMENT DO NEXT?" in briefing:

        next_steps = briefing.split(
            "WHAT SHOULD MANAGEMENT DO NEXT?"
        )[1]

        next_steps = next_steps.replace(
            "==================================================",
            ""
        )

        st.markdown(
            next_steps.strip()
        )

else:

    st.info(
        "Click 'Generate CEO Briefing' to generate an executive summary."
    )
# ==================================================
# SECTION 6
# SENTIMENT ANALYSIS
# ==================================================

st.header(
    "😊 SAP News Sentiment Analysis"
)

positive = len(
    df[df["sentiment"] > 0]
)

neutral = len(
    df[df["sentiment"] == 0]
)

negative = len(
    df[df["sentiment"] < 0]
)

col1, col2 = st.columns(2)

with col1:

    sentiment_df = pd.DataFrame(
        {
            "Sentiment": [
                "Positive",
                "Neutral",
                "Negative"
            ],
            "Count": [
                positive,
                neutral,
                negative
            ]
        }
    )

    fig = px.pie(
        sentiment_df,
        values="Count",
        names="Sentiment",
        title="News Sentiment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    public_sentiment = (
        df["sentiment"].mean()
    )

    st.metric(
        "Public Sentiment",
        round(
            public_sentiment,
            2
        )
    )

    st.metric(
        "Current Intelligence Sentiment",
        round(
            current_sentiment,
            2
        )
    )

    st.metric(
        "Positive Records",
        positive
    )

    st.metric(
        "Negative Records",
        negative
    )

st.subheader(
    "Sentiment Trends"
)

st.line_chart(
    df["sentiment"]
)

if current_sentiment > 0.1:
    
    st.success(
        "Positive Strategic Outlook"
    )

elif current_sentiment < -0.1:

    st.error(
        "Negative Strategic Outlook"
    )

else:

    st.warning(
        "Neutral Strategic Outlook"
    )