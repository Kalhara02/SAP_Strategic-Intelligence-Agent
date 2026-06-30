"""
=====================================================================
AI CEO — Executive Strategic Intelligence Dashboard
=====================================================================

Place this file at the ROOT of your project (the same level as the
`agents/`, `tools/`, and `intelligence/` folders) and run:

    streamlit run dashboard.py

It calls your existing agent pipeline:

    agents.strategic_agent.run_agent(question)

and renders the 7 required sections plus an explicit agent-workflow
panel (Goal -> Plan -> Retrieve -> Analyze -> Decide -> Recommend ->
Validate) so the agent behaviour is visible during the demo.

A "Load sample data" button is provided so you can see / screenshot
the full layout without running the heavy local models.
=====================================================================
"""

import re
import datetime
import streamlit as st

# ---------------------------------------------------------------------
# Optional plotting (falls back to Streamlit-native charts if missing)
# ---------------------------------------------------------------------
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

import pandas as pd


# ---------------------------------------------------------------------
# Try to import the real pipeline. If it fails (e.g. models not loaded
# while you are just designing the UI), the dashboard still renders and
# you can use the sample-data button.
# ---------------------------------------------------------------------
PIPELINE_OK = True
PIPELINE_ERROR = ""
try:
    from agents.strategic_agent import run_agent
    from tools.retrieval_tool import repository_statistics
except Exception as e:                       # pragma: no cover
    PIPELINE_OK = False
    PIPELINE_ERROR = str(e)

    def run_agent(question):                 # type: ignore
        raise RuntimeError(PIPELINE_ERROR)

    def repository_statistics():             # type: ignore
        return {"documents": 0, "sources": []}


# =====================================================================
# Page configuration + styling
# =====================================================================
st.set_page_config(
    page_title="AI CEO — Strategic Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root{
  --bg-card:#ffffff;
  --line:#e6e8ee;
  --ink:#1d2433;
  --muted:#6b7280;
  --accent:#3b5bdb;
}
html, body, [class*="css"]  { font-family: 'Inter', 'Segoe UI', sans-serif; }

.block-container { padding-top: 1.4rem; padding-bottom: 3rem; }

.hero{
  background: linear-gradient(120deg,#0b1f4d 0%,#243b78 55%,#3b5bdb 100%);
  color:#fff; padding:22px 26px; border-radius:16px; margin-bottom:14px;
}
.hero h1{ font-size:1.55rem; margin:0 0 4px 0; font-weight:700;}
.hero p{ margin:0; opacity:.85; font-size:.92rem;}

.section-head{
  display:flex; align-items:center; gap:10px;
  border-left:4px solid var(--accent); padding-left:12px;
  margin:26px 0 10px 0;
}
.section-head h2{ font-size:1.18rem; margin:0; color:var(--ink);}
.section-num{
  background:var(--accent); color:#fff; font-size:.72rem; font-weight:700;
  border-radius:6px; padding:2px 8px;
}

.card{
  background:var(--bg-card); border:1px solid var(--line);
  border-radius:14px; padding:16px 18px; margin-bottom:14px;
  box-shadow:0 1px 2px rgba(16,24,40,.04);
}
.card h4{ margin:0 0 6px 0; font-size:1.02rem; color:var(--ink);}
.card .desc{ color:#374151; font-size:.9rem; margin:6px 0 10px 0; line-height:1.5;}
.card .evi{ color:var(--muted); font-size:.82rem; }

.badge{ display:inline-block; padding:3px 10px; border-radius:999px;
        font-size:.72rem; font-weight:700; letter-spacing:.3px;}
.b-high  { background:#fde8e8; color:#c0341d;}
.b-medium{ background:#fff4e0; color:#b26a00;}
.b-low   { background:#e6f6ec; color:#1f7a45;}
.b-neutral{background:#eef0f4; color:#4b5563;}
.b-info  { background:#e7edff; color:#2b46b3;}

.conf-wrap{ background:#eef0f4; border-radius:999px; height:8px; width:100%; margin-top:8px;}
.conf-bar { background:var(--accent); height:8px; border-radius:999px;}

.pipe{ display:flex; gap:8px; flex-wrap:wrap; }
.pipe .step{
  flex:1; min-width:120px; text-align:center; border:1px solid var(--line);
  border-radius:10px; padding:10px 6px; background:#fff; font-size:.8rem;
}
.pipe .step.done{ border-color:#1f7a45; background:#f1faf4;}
.pipe .step.done .ic{ color:#1f7a45;}
.pipe .step .ic{ font-size:1.1rem; display:block; margin-bottom:2px; color:#9aa3b2;}
.pipe .step .lbl{ font-weight:600; color:var(--ink);}

.brief{ background:#0f172a; color:#e2e8f0; border-radius:14px; padding:18px 22px;}
.brief h4{ color:#93c5fd; margin:14px 0 6px 0; text-transform:uppercase;
           font-size:.82rem; letter-spacing:.6px;}
.brief ul{ margin:0 0 4px 18px;} .brief li{ margin:3px 0; line-height:1.5;}

.small-muted{ color:var(--muted); font-size:.8rem;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =====================================================================
# Helpers
# =====================================================================
def badge_class(level: str) -> str:
    l = (level or "").strip().lower()
    if l in ("high", "critical", "severe", "negative"):
        return "b-high"
    if l in ("medium", "moderate"):
        return "b-medium"
    if l in ("low", "minor", "positive"):
        return "b-low"
    return "b-neutral"


def section_head(num: int, title: str):
    st.markdown(
        f'<div class="section-head"><span class="section-num">SECTION {num}</span>'
        f'<h2>{title}</h2></div>',
        unsafe_allow_html=True,
    )


def confidence_bar(score) -> str:
    try:
        s = float(score)
    except Exception:
        s = 0
    s = max(0, min(100, s))
    return (
        f'<div class="conf-wrap"><div class="conf-bar" style="width:{s}%"></div></div>'
        f'<div class="small-muted" style="margin-top:3px;">Confidence: {s:.0f}%</div>'
    )


REC_LABELS = ("Recommendation", "Priority", "Supporting Evidence",
              "Expected Impact", "Risk Level")


def parse_recommendations(text: str):
    """Turn the LLM recommendation text into a list of structured dicts."""
    if not text or text.strip().lower().startswith("no recommendation"):
        return []
    # split into blocks at each standalone RECOMMENDATION header line
    blocks = re.split(r"(?im)^[=\s]*RECOMMENDATION[=\s]*$", text)
    recs = []
    label_re = re.compile(
        r"(?im)^\s*(Recommendation|Priority|Supporting Evidence|"
        r"Expected Impact|Risk Level)\s*:",
    )
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        matches = list(label_re.finditer(block))
        if not matches:
            continue
        rec = {}
        for i, m in enumerate(matches):
            key = m.group(1).lower().replace(" ", "_")
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
            rec[key] = block[start:end].strip()
        if rec.get("recommendation") or rec.get("priority"):
            recs.append(rec)
    return recs


def parse_ceo_briefing(text: str):
    sections = {
        "WHAT HAPPENED?": [],
        "WHY DOES IT MATTER?": [],
        "WHAT SHOULD MANAGEMENT DO NEXT?": [],
    }
    if not text:
        return sections
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        header = line.upper().replace("=", "").replace("*", "").replace("#", "").strip()
        if header in sections:
            current = header
            continue
        if current is None:
            continue
        # treat bullets and plain content lines as items
        cleaned = line.lstrip("•-*").strip()
        if cleaned:
            sections[current].append(cleaned)
    return sections


# =====================================================================
# Sample data (so the layout renders without running local models)
# =====================================================================
def sample_results():
    return {
        "question": "What are SAP's biggest strategic opportunities right now?",
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plan": {
            "goal": "Opportunity Analysis",
            "analysis_type": "opportunity",
            "priority": "High",
            "company": "SAP",
            "industry": "ERP & Enterprise Software",
            "tools": ["retrieval", "intelligence", "sentiment",
                      "decision", "recommendation", "validation", "ceo_briefing"],
        },
        "evidence": [
            {"document": "SAP announced a new enterprise AI platform aimed at finance teams, "
                         "expanding its Business AI portfolio across cloud products.",
             "metadata": {"title": "SAP launches new AI platform for finance",
                          "source": "Reuters", "url": "https://example.com/1"}},
            {"document": "SAP cloud revenue grew strongly as customers migrate from "
                         "on-premise ERP to RISE with SAP.",
             "metadata": {"title": "SAP cloud revenue accelerates on RISE adoption",
                          "source": "Bloomberg", "url": "https://example.com/2"}},
            {"document": "Analysts highlight competition from Oracle and Microsoft Dynamics "
                         "in the cloud ERP market.",
             "metadata": {"title": "Cloud ERP competition intensifies",
                          "source": "CFO Dive", "url": "https://example.com/3"}},
        ],
        "intelligence": {
            "opportunities": [
                {"title": "Embed generative AI across the ERP suite",
                 "description": "Roll out Business AI copilots inside finance and "
                                "supply-chain modules to deepen product stickiness.",
                 "impact": "High",
                 "evidence": "SAP launches new AI platform for finance (Reuters)",
                 "confidence": 88},
                {"title": "Accelerate RISE with SAP migrations",
                 "description": "Convert the on-premise install base to cloud "
                                "subscriptions to grow recurring revenue.",
                 "impact": "High",
                 "evidence": "SAP cloud revenue accelerates on RISE adoption (Bloomberg)",
                 "confidence": 82},
            ],
            "risks": [
                {"title": "Intensifying cloud ERP competition",
                 "description": "Oracle and Microsoft are expanding aggressively in "
                                "the same enterprise segment.",
                 "category": "Competitive", "severity": "Medium",
                 "evidence": "Cloud ERP competition intensifies (CFO Dive)",
                 "confidence": 76},
            ],
            "trends": [
                {"title": "AI copilots in enterprise software",
                 "description": "Embedded AI assistants are becoming a baseline "
                                "expectation across business applications.",
                 "evidence": "SAP launches new AI platform for finance (Reuters)",
                 "confidence": 80},
            ],
            "raw_output": "(sample)",
        },
        "sentiment": {
            "news_sentiment": "Positive", "public_sentiment": "Neutral",
            "overall_sentiment": "Positive",
            "news_score": 0.34, "public_score": 0.05, "overall_score": 0.27,
            "trend": "Improving",
            "positive_articles": 6, "neutral_articles": 3, "negative_articles": 1,
            "document_results": [
                {"title": "SAP launches new AI platform", "source": "Reuters",
                 "sentiment": "Positive", "confidence": 91.2, "score": 0.62},
                {"title": "SAP cloud revenue accelerates", "source": "Bloomberg",
                 "sentiment": "Positive", "confidence": 87.0, "score": 0.41},
                {"title": "Cloud ERP competition intensifies", "source": "CFO Dive",
                 "sentiment": "Negative", "confidence": 70.5, "score": -0.22},
            ],
        },
        "priorities": [
            {"priority": "HIGH", "priority_score": 4.6, "intelligence_score": 5,
             "sentiment_score": 2.5, "overall_sentiment": "Positive", "trend": "Improving"}
        ],
        "recommendations": """
==================================================
RECOMMENDATION
==================================================
Recommendation:
Embed generative-AI copilots across the core finance and supply-chain modules.
Priority:
HIGH
Supporting Evidence:
- SAP launches new AI platform for finance (Reuters)
Expected Impact:
Higher product stickiness and incremental subscription revenue.
Risk Level:
MEDIUM
==================================================
RECOMMENDATION
==================================================
Recommendation:
Accelerate RISE with SAP migrations for the on-premise install base.
Priority:
HIGH
Supporting Evidence:
- SAP cloud revenue accelerates on RISE adoption (Bloomberg)
Expected Impact:
Growth in recurring cloud revenue and improved retention.
Risk Level:
LOW
==================================================
RECOMMENDATION
==================================================
Recommendation:
Differentiate against Oracle and Microsoft with industry-specific cloud bundles.
Priority:
MEDIUM
Supporting Evidence:
- Cloud ERP competition intensifies (CFO Dive)
Expected Impact:
Defended market share in contested enterprise segments.
Risk Level:
MEDIUM
""",
        "validation": {
            "is_valid": True, "confidence": "High", "validation_score": 100.0,
            "issues": [],
            "checks": {"recommendations": True, "evidence": True, "format": True,
                       "evidence_reference": True},
        },
        "ceo_briefing": """
==================================================
WHAT HAPPENED?
==================================================
• SAP launched a finance-focused AI platform and reported accelerating cloud revenue.
• Competitive pressure in cloud ERP is rising from Oracle and Microsoft.
==================================================
WHY DOES IT MATTER?
==================================================
• AI features and cloud migration drive recurring revenue and retention.
• Losing the AI race risks ceding the enterprise platform to rivals.
==================================================
WHAT SHOULD MANAGEMENT DO NEXT?
==================================================
• Prioritise embedded AI copilots in finance and supply chain.
• Push RISE with SAP migrations and build differentiated industry bundles.
""",
    }


# =====================================================================
# Sidebar — controls
# =====================================================================
with st.sidebar:
    st.markdown("### 🧭 AI CEO Agent")
    st.caption("Strategic Intelligence Console")

    if not PIPELINE_OK:
        st.warning(
            "Live pipeline not importable in this environment.\n\n"
            f"`{PIPELINE_ERROR}`\n\n"
            "Use **Load sample data** to preview the dashboard."
        )

    question = st.text_area(
        "Strategic question",
        value="What are SAP's biggest strategic opportunities right now?",
        height=90,
    )

    run_clicked = st.button("▶  Run Agent", use_container_width=True,
                            type="primary", disabled=not PIPELINE_OK)
    sample_clicked = st.button("🧪  Load sample data", use_container_width=True)

    st.divider()
    st.caption("**Model:** qwen3:8b (Ollama)  ·  **Embeddings:** bge-small-en-v1.5")
    st.caption("**Sentiment:** ProsusAI/finbert  ·  **Store:** ChromaDB")


# =====================================================================
# Run / load state
# =====================================================================
if "results" not in st.session_state:
    st.session_state.results = None

if sample_clicked:
    st.session_state.results = sample_results()

if run_clicked:
    with st.spinner("Agent running:  plan → retrieve → analyze → decide → "
                    "recommend → validate → brief …"):
        try:
            st.session_state.results = run_agent(question)
        except Exception as e:
            st.error(f"Agent run failed: {e}")

results = st.session_state.results


# =====================================================================
# Hero header
# =====================================================================
plan = (results or {}).get("plan", {}) or {}
company = plan.get("company", "SAP")
industry = plan.get("industry", "ERP & Enterprise Software")

st.markdown(
    f'<div class="hero"><h1>{company} — Executive Intelligence Dashboard</h1>'
    f'<p>“If you were the CEO today, what would you do next — and why?”</p></div>',
    unsafe_allow_html=True,
)

if results is None:
    st.info("Enter a strategic question and click **Run Agent**, "
            "or click **Load sample data** in the sidebar to preview the layout.")
    st.stop()


# =====================================================================
# Agent workflow panel (demonstrates agent behaviour for the examiner)
# =====================================================================
st.markdown("#### Agent Workflow")
executed_tools = set(plan.get("tools", []))
# also infer execution from which result keys are populated
stage_done = {
    "Plan":      bool(plan),
    "Retrieve":  bool(results.get("evidence")),
    "Analyze":   bool(results.get("intelligence", {}).get("opportunities")
                      or results.get("intelligence", {}).get("risks")
                      or results.get("intelligence", {}).get("trends")
                      or results.get("sentiment")),
    "Decide":    bool(results.get("priorities")),
    "Recommend": bool(results.get("recommendations")),
    "Validate":  bool(results.get("validation")),
    "Brief":     bool(results.get("ceo_briefing")),
}
icons = {"Plan": "🗺️", "Retrieve": "🔎", "Analyze": "🧠", "Decide": "⚖️",
         "Recommend": "💡", "Validate": "✅", "Brief": "📝"}
steps_html = '<div class="pipe">'
for name, done in stage_done.items():
    cls = "step done" if done else "step"
    steps_html += (f'<div class="{cls}"><span class="ic">{icons[name]}</span>'
                   f'<span class="lbl">{name}</span></div>')
steps_html += "</div>"
st.markdown(steps_html, unsafe_allow_html=True)

with st.expander("Execution plan (planner output)"):
    c1, c2, c3 = st.columns(3)
    c1.write(f"**Goal:** {plan.get('goal','-')}")
    c2.write(f"**Analysis type:** {plan.get('analysis_type','-')}")
    c3.write(f"**Plan priority:** {plan.get('priority','-')}")
    st.write(f"**Tool sequence:** {' → '.join(plan.get('tools', []))}")
    st.caption(f"Question: {results.get('question','')}")


# =====================================================================
# SECTION 1 — Company Overview
# =====================================================================
section_head(1, "Company Overview")

try:
    stats = repository_statistics()
except Exception:
    stats = {"documents": len(results.get("evidence", [])),
             "sources": []}

# derive sources from evidence if repository stats unavailable
sources = stats.get("sources") or sorted({
    (it.get("metadata", {}) or {}).get("source", "Unknown")
    for it in results.get("evidence", [])
})
doc_count = stats.get("documents") or len(results.get("evidence", []))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Company", company)
c2.metric("Industry", industry)
c3.metric("Collected documents", doc_count)
c4.metric("Data sources", len(sources))
c5.metric("Last update", results.get("generated_at", "-"))

if sources:
    st.caption("Sources: " + ", ".join(str(s) for s in sources if s))


# =====================================================================
# SECTION 2 — Market Intelligence
# =====================================================================
section_head(2, "Market Intelligence")
evidence = results.get("evidence", [])
intel = results.get("intelligence", {}) or {}
trends = intel.get("trends", [])

COMPETITORS = ["oracle", "microsoft", "workday", "salesforce", "ibm",
               "google", "infor", "servicenow", "dynamics"]

left, right = st.columns([1.4, 1])

with left:
    st.markdown("**Recent News & Developments**")
    if not evidence:
        st.caption("No documents retrieved.")
    for it in evidence[:6]:
        md = it.get("metadata", {}) or {}
        title = md.get("title", "Untitled")
        source = md.get("source", "Unknown")
        snippet = (it.get("document", "") or "").strip().replace("\n", " ")[:180]
        st.markdown(
            f'<div class="card"><h4>{title}</h4>'
            f'<span class="badge b-info">{source}</span>'
            f'<div class="desc">{snippet}…</div></div>',
            unsafe_allow_html=True,
        )

with right:
    st.markdown("**Emerging Technologies / Trends**")
    if trends:
        for t in trends:
            st.markdown(
                f'<div class="card"><h4>{t.get("title","")}</h4>'
                f'<div class="desc">{t.get("description","")}</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No trend signals in this run.")

    st.markdown("**Competitor Mentions**")
    found = set()
    for it in evidence:
        blob = ((it.get("document", "") or "") + " " +
                (it.get("metadata", {}) or {}).get("title", "")).lower()
        for comp in COMPETITORS:
            if comp in blob:
                found.add(comp.title())
    if found:
        st.markdown(" ".join(
            f'<span class="badge b-neutral">{c}</span>' for c in sorted(found)),
            unsafe_allow_html=True)
    else:
        st.caption("No competitor names detected in evidence.")


# =====================================================================
# SECTION 3 — Opportunity Monitor
# =====================================================================
section_head(3, "Opportunity Monitor")
opportunities = intel.get("opportunities", [])
if not opportunities:
    st.caption("No opportunities generated for this question.")
else:
    cols = st.columns(2)
    for i, op in enumerate(opportunities):
        with cols[i % 2]:
            impact = op.get("impact", "Medium")
            st.markdown(
                f'<div class="card"><h4>{op.get("title","")}</h4>'
                f'<span class="badge {badge_class(impact)}">IMPACT: {impact or "—"}</span>'
                f'<div class="desc">{op.get("description","")}</div>'
                f'<div class="evi">📎 {op.get("evidence","—")}</div>'
                f'{confidence_bar(op.get("confidence", 0))}</div>',
                unsafe_allow_html=True,
            )


# =====================================================================
# SECTION 4 — Risk Monitor
# =====================================================================
section_head(4, "Risk Monitor")
risks = intel.get("risks", [])
if not risks:
    st.caption("No risks generated for this question.")
else:
    cols = st.columns(2)
    for i, rk in enumerate(risks):
        with cols[i % 2]:
            sev = rk.get("severity", "Medium")
            st.markdown(
                f'<div class="card"><h4>{rk.get("title","")}</h4>'
                f'<span class="badge {badge_class(sev)}">SEVERITY: {sev or "—"}</span> '
                f'<span class="badge b-neutral">{rk.get("category","General")}</span>'
                f'<div class="desc">{rk.get("description","")}</div>'
                f'<div class="evi">📎 {rk.get("evidence","—")}</div>'
                f'{confidence_bar(rk.get("confidence", 0))}</div>',
                unsafe_allow_html=True,
            )


# =====================================================================
# SECTION 5 — Sentiment Analysis
# =====================================================================
section_head(5, "Sentiment Analysis")
sent = results.get("sentiment", {}) or {}

if not sent:
    st.caption("Sentiment analysis not available for this run.")
else:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("News sentiment", sent.get("news_sentiment", "—"),
              f"{sent.get('news_score', 0):+.2f}")
    m2.metric("Public sentiment", sent.get("public_sentiment", "—"),
              f"{sent.get('public_score', 0):+.2f}")
    m3.metric("Overall sentiment", sent.get("overall_sentiment", "—"),
              f"{sent.get('overall_score', 0):+.2f}")
    m4.metric("Trend", sent.get("trend", "—"))

    g1, g2 = st.columns(2)

    # Article distribution
    with g1:
        st.markdown("**Article distribution**")
        dist = pd.DataFrame({
            "Sentiment": ["Positive", "Neutral", "Negative"],
            "Articles": [sent.get("positive_articles", 0),
                         sent.get("neutral_articles", 0),
                         sent.get("negative_articles", 0)],
        }).set_index("Sentiment")
        st.bar_chart(dist, height=240)

    # Per-document score trend
    with g2:
        st.markdown("**Sentiment trend across documents**")
        docs = sent.get("document_results", [])
        if docs:
            trend_df = pd.DataFrame(
                {"score": [d.get("score", 0) for d in docs]}
            )
            st.line_chart(trend_df, height=240)
        else:
            st.caption("No per-document scores available.")

    docs = sent.get("document_results", [])
    if docs:
        with st.expander("Per-document sentiment table"):
            st.dataframe(pd.DataFrame(docs), use_container_width=True)


# =====================================================================
# SECTION 6 — Strategic Recommendations (+ validation banner)
# =====================================================================
section_head(6, "Strategic Recommendations")

validation = results.get("validation", {}) or {}
if validation:
    vc = validation.get("confidence", "—")
    vs = validation.get("validation_score", 0)
    ok = validation.get("is_valid", False)
    badge = "b-low" if ok else "b-high"
    st.markdown(
        f'<div class="card"><b>Validation</b> &nbsp;'
        f'<span class="badge {badge}">{"VALID" if ok else "ISSUES FOUND"}</span> '
        f'<span class="badge b-info">Confidence: {vc}</span> '
        f'<span class="badge b-neutral">Score: {vs}%</span>'
        + ("".join(f'<div class="evi">⚠️ {i}</div>'
                   for i in validation.get("issues", [])))
        + "</div>",
        unsafe_allow_html=True,
    )

recs = parse_recommendations(results.get("recommendations", ""))
if not recs:
    st.caption("No structured recommendations produced.")
    if results.get("recommendations"):
        with st.expander("Raw recommendation text"):
            st.text(results["recommendations"])
else:
    for idx, r in enumerate(recs, 1):
        prio = r.get("priority", "").splitlines()[0].strip() if r.get("priority") else "—"
        risk = r.get("risk_level", "").splitlines()[0].strip() if r.get("risk_level") else "—"
        st.markdown(
            f'<div class="card"><h4>#{idx} — {r.get("recommendation","")}</h4>'
            f'<span class="badge {badge_class(prio)}">PRIORITY: {prio}</span> '
            f'<span class="badge {badge_class(risk)}">RISK: {risk}</span>'
            f'<div class="desc"><b>Expected impact:</b> {r.get("expected_impact","—")}</div>'
            f'<div class="evi"><b>Supporting evidence:</b><br>{r.get("supporting_evidence","—")}</div>'
            "</div>",
            unsafe_allow_html=True,
        )


# =====================================================================
# SECTION 7 — CEO Briefing
# =====================================================================
section_head(7, "CEO Briefing")
brief = parse_ceo_briefing(results.get("ceo_briefing", ""))
if not any(brief.values()):
    st.caption("CEO briefing not available.")
    if results.get("ceo_briefing"):
        with st.expander("Raw briefing text"):
            st.text(results["ceo_briefing"])
else:
    html = '<div class="brief">'
    for header, items in brief.items():
        if items:
            html += f"<h4>{header}</h4><ul>"
            html += "".join(f"<li>{it}</li>" for it in items[:6])
            html += "</ul>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)
st.caption(f"Generated at {results.get('generated_at','-')}  ·  "
           f"AI CEO Strategic Intelligence Agent")
