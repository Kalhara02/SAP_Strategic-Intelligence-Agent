# 🧠 Executive Strategic Intelligence Dashboard

---

## 📌 Overview

**Executive Strategic Intelligence Dashboard** is an AI-powered, multi-agent decision support platform built to assist executive management by analysing enterprise intelligence and generating evidence-based strategic recommendations. It combines **Retrieval-Augmented Generation (RAG)**, **Large Language Models (LLMs)**, **sentiment analysis**, and a coordinated multi-agent architecture to retrieve enterprise knowledge, surface strategic opportunities and risks, track market trends, and produce executive-ready briefings.

The platform is built to answer one defining executive challenge:

> 💬 *"What strategic actions should management prioritize next, and why?"*

It distills scattered enterprise intelligence into a single, evidence-grounded executive narrative that leadership can act on with confidence.

---

## 🎯 Project Objectives

- Collect strategic intelligence from enterprise data sources.
- Build a searchable enterprise knowledge base.
- Generate evidence-based strategic insights.
- Identify opportunities, risks, and emerging technology trends.
- Analyse market sentiment around the business.
- Produce prioritized strategic recommendations.
- Generate CEO-level executive briefings.
- Support executive decision-making through a multi-agent AI pipeline.

---

## 🏢 The Business Problem

Executives are overwhelmed by unstructured information arriving from dozens of disconnected channels:

| Source | Signal Type |
|--------|-------------|
| 📰 Company News | Announcements, product launches |
| 🏭 Industry News | Market shifts, regulatory changes |
| 🤖 Technology News | Emerging technologies & trends |
| 🥊 Competitor Activity | Competitive positioning |
| 📊 Market Reports | Macro and sector dynamics |

Reading all of it is impossible. Synthesizing it into a confident decision is harder still. **This platform automates the retrieve → analyse → decide → recommend → validate workflow**, delivering distilled, defensible intelligence to leadership instead of raw, unfiltered noise.

---

## ✨ Core Features

### 🏢 Company Overview

A high-level snapshot of the business being monitored:

- Company name
- Industry
- Number of collected documents
- Number of data sources
- Last update timestamp

### 📰 Market Intelligence

Provides enterprise intelligence including:

| Module | Output |
|--------|--------|
| Recent News | Latest relevant developments |
| Competitor Activities | Tracked competitive moves |
| Emerging Technologies | Trend radar |
| Company Announcements | Official signals |

### 🚀 Opportunity Monitor

Automatically identifies strategic opportunities, each with:

- ⭐ Opportunity title
- 📝 Description
- 📈 Impact level
- 📎 Supporting evidence
- 🎯 Confidence score

### ⚠️ Risk Monitor

Identifies strategic risks, each with:

- ⚠️ Risk title
- 🗂️ Risk category
- 🛡️ Severity level
- 📎 Supporting evidence
- 🎯 Confidence score

### 🔬 Technology & Trend Monitor

Tracks important strategic technology trends, including:

- 🔬 Technology trends
- 🤖 Emerging enterprise technologies
- 📎 Supporting evidence
- 🎯 Confidence score

### 💚 Sentiment Analysis

Uses **FinBERT** to analyse retrieved business articles:

| View | Description |
|------|-------------|
| **News Sentiment** | Derived from collected business news articles. |
| **Public Sentiment** | Derived from broader public-facing intelligence. |
| **Overall Sentiment** | Combined strategic sentiment score. |
| **Sentiment Trend** | Direction of sentiment over time. |

Visualisations include a sentiment distribution chart and a sentiment comparison chart.

### 🧩 Strategic Recommendations

Each recommendation is delivered with:

- ⭐ **Priority ranking**
- 📈 **Expected business impact**
- 📎 **Supporting evidence**
- 🛡️ **Risk level**

### 👔 CEO Briefing

A dedicated agent that automatically generates an executive summary answering:

- 💬 What happened?
- 🎯 Why does it matter?
- 🧭 What should management do next?

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A["👤 User"] --> B["🧭 Strategic Planner Agent<br/>Breaks goal into a plan"]
    B --> C["🔎 Retrieval Agent<br/>Pulls relevant enterprise data"]
    C --> D[("🗄️ ChromaDB<br/>Vector Database")]
    D --> E["🤖 Qwen3:8B via Ollama<br/>Reasoning & Synthesis"]
    E --> F["🧠 Strategic Intelligence Agent"]
    F --> G["🚀 Opportunity Detection"]
    F --> H["⚠️ Risk Detection"]
    F --> I["🔬 Trend Detection"]
    G --> J["💚 Sentiment Analysis<br/>FinBERT"]
    H --> J
    I --> J
    J --> K["⚖️ Decision Engine"]
    K --> L["🎯 Recommendation Agent"]
    L --> M["✅ Validation Agent"]
    M --> N["👔 CEO Briefing Agent"]
    N --> O["📊 Streamlit Dashboard"]

    style A fill:#6E48AA,stroke:#fff,color:#fff
    style D fill:#FF6F61,stroke:#fff,color:#fff
    style E fill:#000000,stroke:#fff,color:#fff
    style O fill:#FF4B4B,stroke:#fff,color:#fff
```

---

## 🤖 Multi-Agent Workflow

The end-to-end reasoning pipeline:

1. **Goal** — the executive question is captured
2. **Plan** — the Strategic Planner Agent breaks it into steps
3. **Retrieve** — relevant enterprise knowledge is pulled from ChromaDB
4. **Analyse** — the Strategic Intelligence Agent detects opportunities, risks, and trends
5. **Decide** — the Decision Engine weighs findings against sentiment
6. **Recommend** — the Recommendation Agent drafts prioritized actions
7. **Validate** — the Validation Agent checks evidence and accuracy
8. **Brief** — the CEO Briefing Agent composes the executive narrative
9. **Serve** — results are presented through the Streamlit dashboard

---

## 📸 Dashboard Preview

> Replace the placeholders below with screenshots from your running dashboard.

### 🏢 Company Overview
![Company Overview](https://via.placeholder.com/1000x520.png?text=Company+Overview)

<img width="1898" height="777" alt="image" src="https://github.com/user-attachments/assets/8bf12d0c-7227-42ac-ae4e-249bbbe820aa" />

### 📰 Market Intelligence
![Market Intelligence](https://via.placeholder.com/1000x520.png?text=Market+Intelligence)

<img width="1906" height="936" alt="image" src="https://github.com/user-attachments/assets/609eeef3-d011-49df-8055-65cd32566237" />

### 🚀 Opportunity & ⚠️ Risk Monitor
![Opportunity and Risk Monitor](https://via.placeholder.com/1000x520.png?text=Opportunity+%26+Risk+Monitor)

<img width="1906" height="1031" alt="image" src="https://github.com/user-attachments/assets/e7252bdc-a899-4a47-bf28-d00ddd07d5de" />

### 🎯 Strategic Recommendations
![Strategic Recommendations](https://via.placeholder.com/1000x520.png?text=Strategic+Recommendations)

<img width="1903" height="1032" alt="image" src="https://github.com/user-attachments/assets/5bf35af2-7b2a-4865-ab52-7b9dde51b07a" />

### 👔 CEO Briefing
![CEO Briefing](https://via.placeholder.com/1000x520.png?text=CEO+Briefing)

<img width="1901" height="1032" alt="image" src="https://github.com/user-attachments/assets/28a5837a-4c34-4fff-bfb4-6d8b3d91b0bd" />

### 💚 Sentiment Analysis
![Sentiment Analysis](https://via.placeholder.com/1000x520.png?text=Sentiment+Analysis)

<img width="1905" height="1030" alt="image" src="https://github.com/user-attachments/assets/e365d348-b716-4936-b8fc-8c626287f604" />

---

## 📈 Project Highlights

- 🧠 **Multi-agent architecture** — planner, retrieval, intelligence, decision, recommendation, validation, and briefing agents
- 🗄️ **ChromaDB** semantic search engine
- 🧠 **Retrieval-Augmented Generation (RAG)** architecture
- 🤖 **Qwen3:8B** local strategic reasoning via Ollama
- 💚 **FinBERT**-powered sentiment analysis
- 🎯 **Evidence-grounded recommendations**
- 👔 **Automated CEO briefing generation**
- 📊 **Interactive Streamlit dashboard**

---

## 🧰 Technology Stack

| Layer | Technology |
|-------|------------|
| 🖥️ **Frontend** | Streamlit |
| ⚙️ **Backend** | Python |
| 🧠 **AI / NLP** | Ollama · Qwen3:8B · Sentence Transformers |
| 💚 **Sentiment Analysis** | FinBERT |
| 🗄️ **Vector Database** | ChromaDB |
| 📊 **Data Processing** | Pandas |
| 📈 **Visualization** | Plotly |

---

## 📊 Dashboard Sections

| # | Section | Purpose |
|---|---------|---------|
| 1 | 🏢 **Company Overview** | High-level company snapshot |
| 2 | 📰 **Market Intelligence** | News, competitors & technology trends |
| 3 | 🚀 **Opportunity Monitor** | Evidence-backed strategic opportunities |
| 4 | ⚠️ **Risk Monitor** | Evidence-backed strategic risks |
| 5 | 🔬 **Technology & Trend Monitor** | Emerging technologies to watch |
| 6 | 🎯 **Strategic Recommendations** | Prioritized actions with impact & risk |
| 7 | 👔 **CEO Briefing** | Executive narrative & next moves |
| 8 | 💚 **Sentiment Analysis** | News, public & overall sentiment outlook |

---

## 📁 Project Structure

```
ai_ceo_agent/
│
├── agents/
│   ├── decision_engine.py          # ⚖️ Decision logic
│   ├── memory.py                   # 🧩 Agent memory
│   ├── planner.py                  # 🧭 Strategic planning agent
│   ├── recommendation_service.py   # 🎯 Recommendation generation
│   ├── strategic_agent.py          # 🧠 Opportunity / risk / trend detection
│   └── validator.py                # ✅ Evidence validation
│
├── chroma_db_clean/                # 🗄️ ChromaDB persistent vector store
│
├── dashboard/
│   └── app.py                      # 📊 Streamlit dashboard entry point
│
├── data/
│   ├── ai_articles.csv             # 🤖 AI / technology news
│   ├── clean_documents.csv         # 🧹 Cleaned, normalized corpus
│   ├── finance_articles.csv        # 💰 Finance & market news
│   ├── google_news_articles.csv    # 📰 General news
│   ├── master_documents.csv        # 📚 Merged document set
│   ├── reddit_articles.csv         # 💬 Social / community signal
│   └── sap_news_articles.csv       # 🏢 Company-specific news
│
├── intelligence/
│   ├── ingest_clean.py             # 📥 Ingests cleaned data into ChromaDB
│   ├── intelligence_service.py     # 🧭 Strategic intelligence engine
│   ├── retrieval.py                # 🔎 Semantic retrieval logic
│   └── sentiment_service.py        # 💚 FinBERT sentiment analysis
│
├── preprocessing/
│   ├── clean_data.py               # 🧹 Cleans & normalizes raw articles
│   └── merge_files.py              # 🔗 Merges source files into one corpus
│
├── scrapers/
│   ├── ai_news_scraper.py          # 🤖 AI news ingestion
│   ├── finance_scraper.py          # 💰 Finance news ingestion
│   ├── google_news_scraper.py      # 📰 General news ingestion
│   └── reddit_scraper.py           # 💬 Social signal ingestion
│
├── tools/
│   ├── ceo_tool.py                 # 👔 CEO briefing generation
│   ├── intelligence_tool.py        # 🧭 Strategic intelligence engine
│   ├── recommendation_tool.py      # 🎯 Recommendation generation
│   ├── retrieval_tool.py           # 🔎 ChromaDB retrieval
│   └── sentiment_tool.py           # 💚 FinBERT sentiment analysis
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ai_ceo_agent.git
```

Navigate into the project

```bash
cd ai_ceo_agent
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

Download Ollama from [ollama.com/download](https://ollama.com/download)

Pull the Qwen model

```bash
ollama pull qwen3:8b
```

Start Ollama

```bash
ollama serve
```

---

## ▶️ Running the Dashboard

```bash
streamlit run dashboard/new.py
```

---

## ❓ Example Questions

The dashboard can answer strategic questions such as:

- 🚀 What are the major opportunities for SAP?
- ⚠️ What are the biggest business risks?
- 🥊 What are competitors doing?
- 🔬 Which technologies should management monitor?
- 🎯 What strategic actions should be prioritised?
- 📎 What evidence supports these recommendations?

---

## ✅ Results

The Executive Strategic Intelligence Dashboard successfully transforms large volumes of enterprise intelligence into actionable executive insights.

The system produces:

- Strategic opportunities
- Strategic risks
- Technology trends
- Market intelligence
- Sentiment analysis
- Evidence-backed strategic recommendations
- CEO-level executive briefings

All outputs are generated using a **Retrieval-Augmented Generation (RAG)** pipeline and supported by evidence retrieved from the enterprise knowledge base.

---

## 👤 Author

**Kalhara**
MSc Artificial Intelligence

<div align="center">

---

⭐ *If this project sparked an idea, consider giving it a star.* ⭐

*Built with RAG, local LLMs, and a focus on decisions that matter.*

</div>

---

## 📄 License

This project is developed for academic purposes as part of an MSc research project.
