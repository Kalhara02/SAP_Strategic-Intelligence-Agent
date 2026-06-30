"""
=====================================================================
AI CEO — Executive Strategic Intelligence Dashboard  (v2, dark theme)
=====================================================================

Place this file at the ROOT of your project (same level as the
`agents/`, `tools/`, and `intelligence/` folders) together with the
`.streamlit/config.toml` file, then run:

    streamlit run dashboard.py

For the best visuals install Plotly (the dashboard still works without
it, falling back to native charts):

    pip install streamlit pandas plotly

It calls your existing pipeline  agents.strategic_agent.run_agent()
and renders the 7 required sections plus an explicit agent-workflow
panel (Goal -> Plan -> Retrieve -> Analyze -> Decide -> Recommend ->
Validate -> Brief).  Use "Load sample data" to preview the layout
without running the local models.
=====================================================================
"""

import os
import sys
import re
import html
import datetime

# ---------------------------------------------------------------------
# Locate the project root so `agents`, `tools`, `intelligence` import no
# matter where Streamlit is launched from -> fixes "No module named 'agents'".
# ---------------------------------------------------------------------
PKG_DIRS = ("agents", "tools", "intelligence")


def _has_packages(d):
    return all(os.path.isdir(os.path.join(d, p)) for p in PKG_DIRS)


def _find_project_root():
    here = os.path.dirname(os.path.abspath(__file__))
    # 1) this file's dir, then walk a few levels up
    d = here
    for _ in range(6):
        if _has_packages(d):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    # 2) shallow walk downward from cwd and from the file's dir
    for base in {os.getcwd(), here}:
        for root, dirs, _files in os.walk(base):
            if _has_packages(root):
                return root
            if root[len(base):].count(os.sep) >= 3:   # limit search depth
                dirs[:] = []
    return None


PROJECT_ROOT = _find_project_root()
sys.path.insert(0, PROJECT_ROOT or os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

# ---------------------------------------------------------------------
# Import the real pipeline (graceful fallback for design / preview mode)
# ---------------------------------------------------------------------
PIPELINE_OK, PIPELINE_ERROR = True, ""
try:
    from agents.strategic_agent import run_agent
    from tools.retrieval_tool import repository_statistics
except Exception as e:                                # pragma: no cover
    PIPELINE_OK, PIPELINE_ERROR = False, f"{type(e).__name__}: {e}"

    def run_agent(question):                          # type: ignore
        raise RuntimeError(PIPELINE_ERROR)

    def repository_statistics():                      # type: ignore
        return {"documents": 0, "sources": []}


# =====================================================================
# Palette
# =====================================================================
C = {
    "indigo": "#818cf8", "blue": "#60a5fa", "cyan": "#22d3ee",
    "green": "#34d399", "amber": "#fbbf24", "red": "#f87171",
    "muted": "#9aa6c0", "text": "#eef1f8",
    "grid": "rgba(255,255,255,.07)",
}

st.set_page_config(page_title="AI CEO — Strategic Intelligence",
                   page_icon="🧭", layout="wide",
                   initial_sidebar_state="expanded")

# =====================================================================
# Global styling
# =====================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stApp { font-family:'Inter',sans-serif; }

.stApp{
  background:
    radial-gradient(1200px 600px at 12% -10%, rgba(99,102,241,.18), transparent 60%),
    radial-gradient(1000px 500px at 100% 0%, rgba(34,211,238,.10), transparent 55%),
    linear-gradient(180deg,#0a0e1a 0%, #0a0e1a 100%);
  color:#eef1f8;
}
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0c1326 0%, #0a0f1f 100%);
  border-right:1px solid rgba(255,255,255,.06);
}
.block-container{ padding-top:1.2rem; padding-bottom:3.5rem; max-width:1280px;}

/* ---------- hero ---------- */
.hero{
  position:relative; overflow:hidden;
  background:linear-gradient(120deg,#1e3a8a 0%, #4f46e5 48%, #7c3aed 100%);
  border:1px solid rgba(255,255,255,.10);
  border-radius:20px; padding:26px 30px; margin-bottom:18px;
  box-shadow:0 18px 50px rgba(31,28,90,.45);
}
.hero:after{
  content:""; position:absolute; right:-60px; top:-60px; width:240px; height:240px;
  background:radial-gradient(circle, rgba(255,255,255,.18), transparent 70%);
}
.hero h1{ font-size:1.7rem; font-weight:800; margin:0 0 6px; color:#fff; letter-spacing:-.3px;}
.hero p{ margin:0; color:rgba(255,255,255,.86); font-size:.95rem;}
.hero .tagrow{ margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;}
.htag{ background:rgba(255,255,255,.14); color:#fff; border:1px solid rgba(255,255,255,.22);
       padding:4px 11px; border-radius:999px; font-size:.74rem; font-weight:600;}

/* ---------- section header (high contrast!) ---------- */
.sec{ display:flex; align-items:center; gap:12px; margin:30px 0 14px;}
.sec .bar{ width:5px; height:26px; border-radius:6px;
           background:linear-gradient(180deg,#818cf8,#22d3ee);}
.sec .num{ background:rgba(129,140,248,.18); color:#c7ccff; border:1px solid rgba(129,140,248,.35);
           font-size:.68rem; font-weight:800; letter-spacing:.6px; padding:3px 9px; border-radius:7px;}
.sec h2{ font-size:1.25rem; font-weight:700; margin:0; color:#f4f6fc;}

/* ---------- KPI tiles ---------- */
.kpi-row{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px;}
.kpi{
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
  border:1px solid rgba(255,255,255,.09); border-radius:16px; padding:16px 16px 14px;
  position:relative; overflow:hidden; min-height:104px;
}
.kpi:before{ content:""; position:absolute; left:0; top:0; height:3px; width:100%;
             background:linear-gradient(90deg,#818cf8,#22d3ee);}
.kpi .ic{ font-size:1.1rem; opacity:.9;}
.kpi .lab{ color:#9aa6c0; font-size:.74rem; font-weight:600; margin-top:6px; text-transform:uppercase; letter-spacing:.4px;}
.kpi .val{ color:#f4f6fc; font-size:1.5rem; font-weight:800; line-height:1.15; margin-top:2px;}
.kpi .val.sm{ font-size:1.02rem; font-weight:700;}
.kpi .sub{ color:#7f8aa6; font-size:.72rem; margin-top:2px;}

/* ---------- cards ---------- */
.card{
  background:linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  border:1px solid rgba(255,255,255,.09); border-radius:16px; padding:16px 18px; margin-bottom:14px;
  box-shadow:0 10px 28px rgba(0,0,0,.28); transition:transform .15s ease, border-color .15s;
}
.card:hover{ transform:translateY(-2px); border-color:rgba(129,140,248,.4);}
.card h4{ margin:0 0 8px; font-size:1.04rem; color:#f4f6fc; font-weight:700; line-height:1.35;}
.card .desc{ color:#c9d2e6; font-size:.9rem; line-height:1.55; margin:8px 0 10px;}
.card .evi{ color:#93a0bd; font-size:.8rem;}
.card .evi b{ color:#aab4cf;}

.badge{ display:inline-block; padding:3px 11px; border-radius:999px; font-size:.7rem;
        font-weight:800; letter-spacing:.4px; margin-right:6px;}
.b-high  { background:rgba(248,113,113,.16); color:#fca5a5; border:1px solid rgba(248,113,113,.32);}
.b-medium{ background:rgba(251,191,36,.15);  color:#fcd34d; border:1px solid rgba(251,191,36,.30);}
.b-low   { background:rgba(52,211,153,.15);  color:#6ee7b7; border:1px solid rgba(52,211,153,.30);}
.b-info  { background:rgba(96,165,250,.15);  color:#93c5fd; border:1px solid rgba(96,165,250,.30);}
.b-neutral{background:rgba(255,255,255,.08);  color:#c3cbe0; border:1px solid rgba(255,255,255,.14);}

.conf-wrap{ background:rgba(255,255,255,.08); border-radius:999px; height:7px; margin-top:10px;}
.conf-bar { height:7px; border-radius:999px; background:linear-gradient(90deg,#818cf8,#22d3ee);}
.conf-lab{ color:#8e99b6; font-size:.74rem; margin-top:4px;}

/* ---------- agent pipeline ---------- */
.pipe{ display:grid; grid-template-columns:repeat(8,1fr); gap:10px;}
.step{ text-align:center; border:1px solid rgba(255,255,255,.09); border-radius:13px;
       padding:13px 6px; background:rgba(255,255,255,.03);}
.step.done{ border-color:rgba(52,211,153,.45);
            background:linear-gradient(180deg, rgba(52,211,153,.12), rgba(52,211,153,.03));
            box-shadow:0 0 20px rgba(52,211,153,.12);}
.step .si{ font-size:1.25rem; display:block;}
.step .sl{ font-size:.74rem; font-weight:700; color:#dbe2f2; margin-top:4px;}
.step.done .sl{ color:#9af3cf;}
.step .sd{ font-size:.62rem; color:#7f8aa6;}

/* ---------- CEO briefing ---------- */
.brief{ background:linear-gradient(180deg,#0e1530,#0b1124);
        border:1px solid rgba(129,140,248,.22); border-radius:18px; padding:8px 26px 20px;}
.brief .blk{ padding:16px 0; border-bottom:1px dashed rgba(255,255,255,.08);}
.brief .blk:last-child{ border-bottom:none;}
.brief h4{ color:#93c5fd; margin:0 0 8px; font-size:.8rem; letter-spacing:.7px; text-transform:uppercase;}
.brief ul{ margin:0 0 0 4px; padding:0; list-style:none;}
.brief li{ margin:7px 0; padding-left:22px; position:relative; color:#dfe5f3; line-height:1.55;}
.brief li:before{ content:"▸"; position:absolute; left:2px; color:#818cf8;}

.muted{ color:#8e99b6; font-size:.82rem;}
hr{ border-color:rgba(255,255,255,.07);}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =====================================================================
# Helpers
# =====================================================================
esc = html.escape


def lvl_class(level: str) -> str:
    l = (level or "").strip().lower()
    if l in ("high", "critical", "severe", "negative"):
        return "b-high"
    if l in ("medium", "moderate"):
        return "b-medium"
    if l in ("low", "minor", "positive"):
        return "b-low"
    return "b-neutral"


def sec(num, title):
    st.markdown(
        f'<div class="sec"><span class="bar"></span>'
        f'<span class="num">SECTION {num}</span><h2>{esc(title)}</h2></div>',
        unsafe_allow_html=True)


def kpi(label, value, icon, sub="", small=False):
    cls = "val sm" if small else "val"
    return (f'<div class="kpi"><div class="ic">{icon}</div>'
            f'<div class="lab">{esc(str(label))}</div>'
            f'<div class="{cls}">{esc(str(value))}</div>'
            f'<div class="sub">{esc(str(sub))}</div></div>')


def conf_bar(score):
    try:
        s = max(0, min(100, float(score)))
    except Exception:
        s = 0
    return (f'<div class="conf-wrap"><div class="conf-bar" style="width:{s}%"></div></div>'
            f'<div class="conf-lab">Confidence {s:.0f}%</div>')


def style_fig(fig, height=260):
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=8, b=8),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#cdd5e8", family="Inter", size=12),
                      showlegend=False)
    fig.update_xaxes(gridcolor=C["grid"], zeroline=False)
    fig.update_yaxes(gridcolor=C["grid"], zeroline=False)
    return fig


def parse_recommendations(text):
    if not text or text.strip().lower().startswith("no recommendation"):
        return []
    blocks = re.split(r"(?im)^[=\s]*RECOMMENDATION[=\s]*$", text)
    label_re = re.compile(r"(?im)^\s*(Recommendation|Priority|Supporting Evidence|"
                          r"Expected Impact|Risk Level)\s*:")
    out = []
    for block in blocks:
        block = block.strip()
        m = list(label_re.finditer(block))
        if not m:
            continue
        rec = {}
        for i, mm in enumerate(m):
            key = mm.group(1).lower().replace(" ", "_")
            start = mm.end()
            end = m[i + 1].start() if i + 1 < len(m) else len(block)
            rec[key] = block[start:end].strip()
        if rec.get("recommendation") or rec.get("priority"):
            out.append(rec)
    return out


def parse_ceo_briefing(text):
    sections = {"WHAT HAPPENED?": [], "WHY DOES IT MATTER?": [],
                "WHAT SHOULD MANAGEMENT DO NEXT?": []}
    if not text:
        return sections
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        letters = re.sub(r"[^A-Z]", "", line.upper())          # header signature
        if "WHATHAPPENED" in letters:
            current = "WHAT HAPPENED?"; continue
        if "WHYDOESITMATTER" in letters:
            current = "WHY DOES IT MATTER?"; continue
        if "WHATSHOULDMANAGEMENT" in letters:
            current = "WHAT SHOULD MANAGEMENT DO NEXT?"; continue
        if re.fullmatch(r"[=\-•*~_\s]+", line):                 # skip separator rows
            continue
        if current is None:
            continue
        cleaned = line.lstrip("•-*▸ ").strip()
        if cleaned:
            sections[current].append(cleaned)
    return sections


# =====================================================================
# Sample data (matches the real result schema)
# =====================================================================
def sample_results():
    return {
        "question": "What are SAP's biggest strategic opportunities right now?",
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plan": {"goal": "Opportunity Analysis", "analysis_type": "opportunity",
                 "priority": "High", "company": "SAP",
                 "industry": "ERP & Enterprise Software",
                 "tools": ["retrieval", "intelligence", "sentiment", "decision",
                           "recommendation", "validation", "ceo_briefing"]},
        "evidence": [
            {"document": "SAP announced a new enterprise AI platform aimed at finance teams, "
                         "expanding its Business AI portfolio across cloud products.",
             "metadata": {"title": "SAP launches new AI platform for finance", "source": "Reuters"}},
            {"document": "SAP cloud revenue grew strongly as customers migrate from on-premise "
                         "ERP to RISE with SAP.",
             "metadata": {"title": "SAP cloud revenue accelerates on RISE adoption", "source": "Bloomberg"}},
            {"document": "Analysts highlight competition from Oracle and Microsoft Dynamics in the "
                         "cloud ERP market.",
             "metadata": {"title": "Cloud ERP competition intensifies", "source": "CFO Dive"}},
        ],
        "intelligence": {
            "opportunities": [
                {"title": "Embed generative AI across the ERP suite",
                 "description": "Roll out Business AI copilots inside finance and supply-chain "
                                "modules to deepen product stickiness.",
                 "impact": "High", "evidence": "SAP launches new AI platform for finance (Reuters)",
                 "confidence": 88},
                {"title": "Accelerate RISE with SAP migrations",
                 "description": "Convert the on-premise install base to cloud subscriptions to "
                                "grow recurring revenue.",
                 "impact": "High", "evidence": "SAP cloud revenue accelerates on RISE adoption (Bloomberg)",
                 "confidence": 82}],
            "risks": [
                {"title": "Intensifying cloud ERP competition",
                 "description": "Oracle and Microsoft are expanding aggressively in the same "
                                "enterprise segment.",
                 "category": "Competitive", "severity": "Medium",
                 "evidence": "Cloud ERP competition intensifies (CFO Dive)", "confidence": 76}],
            "trends": [
                {"title": "AI copilots in enterprise software",
                 "description": "Embedded AI assistants are becoming a baseline expectation "
                                "across business applications.",
                 "evidence": "SAP launches new AI platform for finance (Reuters)", "confidence": 80}],
            "raw_output": "(sample)"},
        "sentiment": {"news_sentiment": "Positive", "public_sentiment": "Neutral",
                      "overall_sentiment": "Positive", "news_score": 0.34, "public_score": 0.05,
                      "overall_score": 0.27, "trend": "Improving",
                      "positive_articles": 6, "neutral_articles": 3, "negative_articles": 1,
                      "document_results": [
                          {"title": "SAP launches new AI platform", "source": "Reuters",
                           "sentiment": "Positive", "confidence": 91.2, "score": 0.62},
                          {"title": "SAP cloud revenue accelerates", "source": "Bloomberg",
                           "sentiment": "Positive", "confidence": 87.0, "score": 0.41},
                          {"title": "Cloud ERP competition intensifies", "source": "CFO Dive",
                           "sentiment": "Negative", "confidence": 70.5, "score": -0.22}]},
        "priorities": [{"priority": "HIGH", "priority_score": 4.6, "intelligence_score": 5,
                        "sentiment_score": 2.5, "overall_sentiment": "Positive", "trend": "Improving"}],
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
        "validation": {"is_valid": True, "confidence": "High", "validation_score": 100.0,
                       "issues": [], "checks": {"recommendations": True, "evidence": True,
                                                "format": True, "evidence_reference": True}},
        "ceo_briefing": """
==================================================
WHAT HAPPENED?
==================================================
- SAP launched a finance-focused AI platform and reported accelerating cloud revenue.
- Competitive pressure in cloud ERP is rising from Oracle and Microsoft.
==================================================
WHY DOES IT MATTER?
==================================================
- AI features and cloud migration drive recurring revenue and retention.
- Losing the AI race risks ceding the enterprise platform to rivals.
==================================================
WHAT SHOULD MANAGEMENT DO NEXT?
==================================================
- Prioritise embedded AI copilots in finance and supply chain.
- Push RISE with SAP migrations and build differentiated industry bundles.
""",
    }


# =====================================================================
# Sidebar
# =====================================================================
with st.sidebar:
    st.markdown("## 🧭 AI CEO Agent")
    st.caption("Strategic Intelligence Console")

    if not PIPELINE_OK:
        st.warning("Live pipeline not importable here.\n\n"
                   f"`{PIPELINE_ERROR}`\n\nUse **Load sample data** to preview.")
        with st.expander("🔧 Fix this — import diagnostics"):
            here = os.path.dirname(os.path.abspath(__file__))
            st.markdown(f"**Detected project root:** "
                        f"`{PROJECT_ROOT or 'NOT FOUND'}`")
            st.markdown(f"**dashboard.py is in:** `{here}`")
            st.markdown(f"**Launched from (cwd):** `{os.getcwd()}`")
            st.markdown("**Needs these folders side-by-side:** "
                        + ", ".join(f"`{p}/`" for p in PKG_DIRS))
            try:
                items = sorted(os.listdir(here))
                st.markdown("**Items next to dashboard.py:**")
                st.code("  ".join(items) or "(empty)")
            except Exception:
                pass
            if PROJECT_ROOT is None:
                st.error("Could not find a folder containing all of "
                         "`agents/`, `tools/`, `intelligence/`. "
                         "Move dashboard.py into your project root (the folder "
                         "that holds those three folders), then rerun.")
            else:
                st.info("Root was found and added to the path. If the error "
                        "persists, the failure is *inside* one of your modules "
                        "(see the error message above) — e.g. ChromaDB not "
                        "built yet, or a missing package like `ollama`.")

    question = st.text_area("Strategic question",
                            value="What are SAP's biggest strategic opportunities right now?",
                            height=92)
    run_clicked = st.button("▶  Run Agent", type="primary",
                            use_container_width=True, disabled=not PIPELINE_OK)
    sample_clicked = st.button("🧪  Load sample data", use_container_width=True)

    st.divider()
    st.caption("**LLM** qwen3:8b · Ollama")
    st.caption("**Embeddings** bge-small-en-v1.5")
    st.caption("**Sentiment** ProsusAI/finbert")
    st.caption("**Vector store** ChromaDB")


# =====================================================================
# State
# =====================================================================
st.session_state.setdefault("results", None)
if sample_clicked:
    st.session_state.results = sample_results()
if run_clicked:
    with st.spinner("Agent running: plan → retrieve → analyze → decide → "
                    "recommend → validate → brief …"):
        try:
            st.session_state.results = run_agent(question)
        except Exception as e:
            st.error(f"Agent run failed: {e}")
results = st.session_state.results


# =====================================================================
# Hero
# =====================================================================
plan = (results or {}).get("plan", {}) or {}
company = plan.get("company", "SAP")
industry = plan.get("industry", "ERP & Enterprise Software")

st.markdown(
    f'<div class="hero"><h1>{esc(company)} — Executive Intelligence Dashboard</h1>'
    f'<p>“If you were the CEO today, what would you do next — and why?”</p>'
    f'<div class="tagrow"><span class="htag">🏢 {esc(company)}</span>'
    f'<span class="htag">🏭 {esc(industry)}</span>'
    f'<span class="htag">🤖 Autonomous Strategic Agent</span></div></div>',
    unsafe_allow_html=True)

if results is None:
    st.info("Enter a question and click **Run Agent**, or click "
            "**Load sample data** in the sidebar to preview the dashboard.")
    st.stop()


# =====================================================================
# Agent workflow
# =====================================================================
st.markdown("#### ⚙️ Agent Workflow")
intel = results.get("intelligence", {}) or {}
stage = {
    ("Plan", "🗺️"): bool(plan),
    ("Retrieve", "🔎"): bool(results.get("evidence")),
    ("Analyze", "🧠"): bool(intel.get("opportunities") or intel.get("risks")
                           or intel.get("trends") or results.get("sentiment")),
    ("Decide", "⚖️"): bool(results.get("priorities")),
    ("Recommend", "💡"): bool(results.get("recommendations")),
    ("Validate", "✅"): bool(results.get("validation")),
    ("Brief", "📝"): bool(results.get("ceo_briefing")),
}
pipe = '<div class="pipe">'
for (name, ic), done in stage.items():
    cls = "step done" if done else "step"
    pipe += (f'<div class="{cls}"><span class="si">{ic}</span>'
             f'<span class="sl">{name}</span>'
             f'<span class="sd">{"done" if done else "—"}</span></div>')
pipe += '<div class="step" style="visibility:hidden"></div></div>'
st.markdown(pipe, unsafe_allow_html=True)

with st.expander("📋 Execution plan (planner output)"):
    a, b, c = st.columns(3)
    a.markdown(f"**Goal**  \n{plan.get('goal','-')}")
    b.markdown(f"**Analysis type**  \n{plan.get('analysis_type','-')}")
    c.markdown(f"**Plan priority**  \n{plan.get('priority','-')}")
    st.markdown("**Tool sequence:** " + " → ".join(plan.get("tools", [])))
    if results.get("priorities"):
        p = results["priorities"][0]
        st.markdown(f"**Decision engine:** priority **{p.get('priority','-')}** "
                    f"(score {p.get('priority_score','-')}, "
                    f"intel {p.get('intelligence_score','-')}, "
                    f"sentiment {p.get('sentiment_score','-')})")


# =====================================================================
# SECTION 1 — Company Overview
# =====================================================================
sec(1, "Company Overview")
try:
    stats = repository_statistics()
except Exception:
    stats = {"documents": len(results.get("evidence", [])), "sources": []}

sources = stats.get("sources") or sorted({
    (it.get("metadata", {}) or {}).get("source", "Unknown")
    for it in results.get("evidence", [])})
doc_count = stats.get("documents") or len(results.get("evidence", []))

tiles = (kpi("Company", company, "🏢")
         + kpi("Industry", industry, "🏭", small=True)
         + kpi("Documents", doc_count, "📚")
         + kpi("Data sources", len(sources), "🌐")
         + kpi("Last update", results.get("generated_at", "-"), "🕒", small=True))
st.markdown(f'<div class="kpi-row">{tiles}</div>', unsafe_allow_html=True)
if sources:
    st.markdown('<div class="muted" style="margin-top:8px;">Sources: '
                + ", ".join(esc(str(s)) for s in sources if s) + "</div>",
                unsafe_allow_html=True)


# =====================================================================
# SECTION 2 — Market Intelligence
# =====================================================================
sec(2, "Market Intelligence")
evidence = results.get("evidence", [])
trends = intel.get("trends", [])
COMPETITORS = ["oracle", "microsoft", "workday", "salesforce", "ibm",
               "google", "infor", "servicenow", "dynamics"]

left, right = st.columns([1.45, 1])
with left:
    st.markdown("**📰 Recent News & Developments**")
    if not evidence:
        st.caption("No documents retrieved.")
    for it in evidence[:6]:
        md = it.get("metadata", {}) or {}
        title = esc(md.get("title", "Untitled"))
        source = esc(md.get("source", "Unknown"))
        snip = esc((it.get("document", "") or "").strip().replace("\n", " ")[:170])
        st.markdown(f'<div class="card"><h4>{title}</h4>'
                    f'<span class="badge b-info">{source}</span>'
                    f'<div class="desc">{snip}…</div></div>', unsafe_allow_html=True)
with right:
    st.markdown("**🚀 Emerging Technologies / Trends**")
    if trends:
        for t in trends:
            st.markdown(f'<div class="card"><h4>{esc(t.get("title",""))}</h4>'
                        f'<div class="desc">{esc(t.get("description",""))}</div></div>',
                        unsafe_allow_html=True)
    else:
        st.caption("No trend signals in this run.")
    st.markdown("**🥊 Competitor Mentions**")
    found = set()
    for it in evidence:
        blob = ((it.get("document", "") or "") + " " +
                (it.get("metadata", {}) or {}).get("title", "")).lower()
        for comp in COMPETITORS:
            if comp in blob:
                found.add(comp.title())
    if found:
        st.markdown(" ".join(f'<span class="badge b-neutral">{esc(c)}</span>'
                             for c in sorted(found)), unsafe_allow_html=True)
    else:
        st.caption("No competitor names detected in evidence.")


# =====================================================================
# SECTION 3 — Opportunity Monitor
# =====================================================================
sec(3, "Opportunity Monitor")
opportunities = intel.get("opportunities", [])
if not opportunities:
    st.caption("No opportunities generated for this question.")
else:
    cols = st.columns(2)
    for i, op in enumerate(opportunities):
        with cols[i % 2]:
            imp = op.get("impact", "Medium")
            st.markdown(
                f'<div class="card"><h4>{esc(op.get("title",""))}</h4>'
                f'<span class="badge {lvl_class(imp)}">IMPACT · {esc(imp or "—")}</span>'
                f'<div class="desc">{esc(op.get("description",""))}</div>'
                f'<div class="evi"><b>📎 Evidence:</b> {esc(op.get("evidence","—"))}</div>'
                f'{conf_bar(op.get("confidence",0))}</div>', unsafe_allow_html=True)


# =====================================================================
# SECTION 4 — Risk Monitor
# =====================================================================
sec(4, "Risk Monitor")
risks = intel.get("risks", [])
if not risks:
    st.caption("No risks generated for this question.")
else:
    cols = st.columns(2)
    for i, rk in enumerate(risks):
        with cols[i % 2]:
            sev = rk.get("severity", "Medium")
            st.markdown(
                f'<div class="card"><h4>{esc(rk.get("title",""))}</h4>'
                f'<span class="badge {lvl_class(sev)}">SEVERITY · {esc(sev or "—")}</span>'
                f'<span class="badge b-neutral">{esc(rk.get("category","General"))}</span>'
                f'<div class="desc">{esc(rk.get("description",""))}</div>'
                f'<div class="evi"><b>📎 Evidence:</b> {esc(rk.get("evidence","—"))}</div>'
                f'{conf_bar(rk.get("confidence",0))}</div>', unsafe_allow_html=True)


# =====================================================================
# SECTION 5 — Sentiment Analysis
# =====================================================================
sec(5, "Sentiment Analysis")
sent = results.get("sentiment", {}) or {}
if not sent:
    st.caption("Sentiment analysis not available for this run.")
else:
    def tone(lbl):
        return {"Positive": C["green"], "Negative": C["red"]}.get(lbl, C["amber"])

    tiles = ""
    for lab, key, sk in [("News", "news_sentiment", "news_score"),
                         ("Public", "public_sentiment", "public_score"),
                         ("Overall", "overall_sentiment", "overall_score")]:
        v = sent.get(key, "—")
        s = sent.get(sk, 0)
        tiles += (f'<div class="kpi"><div class="ic">💬</div>'
                  f'<div class="lab">{lab} sentiment</div>'
                  f'<div class="val" style="color:{tone(v)}">{esc(str(v))}</div>'
                  f'<div class="sub">score {s:+.2f}</div></div>')
    tdir = sent.get("trend", "—")
    tcol = {"Improving": C["green"], "Declining": C["red"]}.get(tdir, C["amber"])
    tiles += (f'<div class="kpi"><div class="ic">📈</div><div class="lab">Trend</div>'
              f'<div class="val" style="color:{tcol}">{esc(str(tdir))}</div>'
              f'<div class="sub">direction</div></div>')
    tiles += kpi("Articles", (sent.get("positive_articles", 0) + sent.get("neutral_articles", 0)
                              + sent.get("negative_articles", 0)), "🗂️", "analysed")
    st.markdown(f'<div class="kpi-row">{tiles}</div>', unsafe_allow_html=True)

    g1, g2, g3 = st.columns([1, 1, 1])
    pos = sent.get("positive_articles", 0)
    neu = sent.get("neutral_articles", 0)
    neg = sent.get("negative_articles", 0)
    docs = sent.get("document_results", [])

    if HAS_PLOTLY:
        with g1:
            st.markdown("**Article distribution**")
            fig = go.Figure(go.Pie(labels=["Positive", "Neutral", "Negative"],
                                   values=[pos, neu, neg], hole=.62, sort=False,
                                   marker=dict(colors=[C["green"], "#64748b", C["red"]],
                                               line=dict(color="rgba(0,0,0,0)", width=0)),
                                   textinfo="value",
                                   textfont=dict(color="#0a0e1a", size=13)))
            fig.update_layout(annotations=[dict(text=f"{pos+neu+neg}", x=.5, y=.5,
                                                 font=dict(size=22, color="#eef1f8"),
                                                 showarrow=False)])
            st.plotly_chart(style_fig(fig, 240), use_container_width=True,
                            config={"displayModeBar": False})
        with g2:
            st.markdown("**Overall score**")
            ov = sent.get("overall_score", 0)
            ga = go.Figure(go.Indicator(
                mode="gauge+number", value=ov, number={"font": {"color": "#eef1f8"}},
                gauge={"axis": {"range": [-1, 1], "tickcolor": "#9aa6c0"},
                       "bar": {"color": C["indigo"]},
                       "bgcolor": "rgba(255,255,255,.04)",
                       "borderwidth": 0,
                       "steps": [{"range": [-1, -.15], "color": "rgba(248,113,113,.25)"},
                                 {"range": [-.15, .15], "color": "rgba(148,163,184,.25)"},
                                 {"range": [.15, 1], "color": "rgba(52,211,153,.25)"}]}))
            st.plotly_chart(style_fig(ga, 240), use_container_width=True,
                            config={"displayModeBar": False})
        with g3:
            st.markdown("**Sentiment trend**")
            if docs:
                ys = [d.get("score", 0) for d in docs]
                ln = go.Figure(go.Scatter(y=ys, mode="lines+markers",
                                          line=dict(color=C["blue"], width=3, shape="spline"),
                                          marker=dict(color=C["cyan"], size=7),
                                          fill="tozeroy", fillcolor="rgba(96,165,250,.14)"))
                st.plotly_chart(style_fig(ln, 240), use_container_width=True,
                                config={"displayModeBar": False})
            else:
                st.caption("No per-document scores.")
    else:
        g1.bar_chart(pd.DataFrame({"Articles": [pos, neu, neg]},
                                  index=["Positive", "Neutral", "Negative"]), height=240)
        if docs:
            g3.line_chart(pd.DataFrame({"score": [d.get("score", 0) for d in docs]}), height=240)

    if docs:
        with st.expander("📄 Per-document sentiment table"):
            st.dataframe(pd.DataFrame(docs), use_container_width=True)


# =====================================================================
# SECTION 6 — Strategic Recommendations  (+ validation banner)
# =====================================================================
sec(6, "Strategic Recommendations")
validation = results.get("validation", {}) or {}
if validation:
    ok = validation.get("is_valid", False)
    badge = "b-low" if ok else "b-high"
    issues = "".join(f'<div class="evi" style="margin-top:6px;">⚠️ {esc(i)}</div>'
                     for i in validation.get("issues", []))
    st.markdown(
        f'<div class="card"><h4 style="margin-bottom:6px;">🛡️ Recommendation Validation</h4>'
        f'<span class="badge {badge}">{"PASSED" if ok else "ISSUES FOUND"}</span>'
        f'<span class="badge b-info">Confidence · {esc(str(validation.get("confidence","—")))}</span>'
        f'<span class="badge b-neutral">Score · {validation.get("validation_score",0)}%</span>'
        f'{issues}</div>', unsafe_allow_html=True)

recs = parse_recommendations(results.get("recommendations", ""))
if not recs:
    st.caption("No structured recommendations produced.")
    if results.get("recommendations"):
        with st.expander("Raw recommendation text"):
            st.text(results["recommendations"])
else:
    for idx, r in enumerate(recs, 1):
        prio = (r.get("priority", "—").splitlines() or ["—"])[0].strip() or "—"
        risk = (r.get("risk_level", "—").splitlines() or ["—"])[0].strip() or "—"
        evi = esc(r.get("supporting_evidence", "—")).replace("\n", "<br>")
        st.markdown(
            f'<div class="card"><h4>#{idx} · {esc(r.get("recommendation",""))}</h4>'
            f'<span class="badge {lvl_class(prio)}">PRIORITY · {esc(prio)}</span>'
            f'<span class="badge {lvl_class(risk)}">RISK · {esc(risk)}</span>'
            f'<div class="desc"><b>Expected impact:</b> {esc(r.get("expected_impact","—"))}</div>'
            f'<div class="evi"><b>Supporting evidence:</b><br>{evi}</div></div>',
            unsafe_allow_html=True)


# =====================================================================
# SECTION 7 — CEO Briefing
# =====================================================================
sec(7, "CEO Briefing")
brief = parse_ceo_briefing(results.get("ceo_briefing", ""))
if not any(brief.values()):
    st.caption("CEO briefing not available.")
    if results.get("ceo_briefing"):
        with st.expander("Raw briefing text"):
            st.text(results["ceo_briefing"])
else:
    icons = {"WHAT HAPPENED?": "📌", "WHY DOES IT MATTER?": "🎯",
             "WHAT SHOULD MANAGEMENT DO NEXT?": "🚀"}
    html_brief = '<div class="brief">'
    for header, items in brief.items():
        if items:
            html_brief += (f'<div class="blk"><h4>{icons.get(header,"")} {header}</h4><ul>'
                           + "".join(f"<li>{esc(it)}</li>" for it in items[:6])
                           + "</ul></div>")
    html_brief += "</div>"
    st.markdown(html_brief, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f'<div class="muted">Generated {results.get("generated_at","-")} · '
            f'AI CEO Strategic Intelligence Agent</div>', unsafe_allow_html=True)
