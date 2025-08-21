import os
import json
import time
from typing import List, Dict, Any, Optional

import streamlit as st
from pydantic import BaseModel, Field, ValidationError

# LangChain (optional if GROQ provided)
try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    LLM_AVAILABLE = True
except Exception:
    LLM_AVAILABLE = False


# ---------- Data Models ----------
class SubTask(BaseModel):
    id: int
    title: str
    owner: str = "Agent"
    status: str = "pending"   # pending | running | done | failed
    logs: List[str] = Field(default_factory=list)

class Plan(BaseModel):
    main_query: str
    subtasks: List[SubTask]


# ---------- Utilities ----------
SYSTEM_PROMPT = """You are an expert planner. Given a user's goal, break it into clear, minimal,
non-overlapping subtasks with realistic owners (e.g., Venue Agent, Email Agent, Design Agent,
Budget Agent, Procurement Agent, Marketing Agent). Return STRICT JSON only.

Schema:
{
  "subtasks": [
    { "title": "...", "owner": "..." },
    ...
  ]
}

Rules:
- 4 to 8 subtasks max, concise and actionable.
- Keep titles imperative (e.g., "Book the venue").
- Choose meaningful owners, not generic "Agent" unless necessary.
- Do NOT include commentary outside JSON.
"""

USER_PROMPT = """Goal: "{query}"

Constraints:
- college-level workshop typical logistics.
- assume internet access but we are only simulating.
- do not add costs unless essential.

Return JSON only as per schema.
"""

FALLBACK_TEMPLATES = [
    ("Clarify requirements & constraints", "Coordinator Agent"),
    ("Draft the detailed plan & timeline", "Planning Agent"),
    ("Book or reserve the venue", "Venue Agent"),
    ("Arrange speakers/mentors & finalize agenda", "Outreach Agent"),
    ("Design poster and announcement content", "Design Agent"),
    ("Set up registration form and tracking sheet", "Ops Agent"),
    ("Promote on social media & campus groups", "Marketing Agent"),
    ("Arrange equipment & logistics (audio/visual, kits)", "Logistics Agent"),
]

AGENT_SAMPLE_LOGS = {
    "Venue Agent": [
        "Shortlisted 3 halls based on capacity.",
        "Checked availability for preferred date.",
        "Drafted reservation email."
    ],
    "Design Agent": [
        "Picked brand colors matching college palette.",
        "Created poster draft v1 in Canva.",
        "Exported web & print versions."
    ],
    "Outreach Agent": [
        "Compiled list of 5 potential speakers.",
        "Sent intro emails with tentative agenda.",
        "Got 2 positive responses."
    ],
    "Marketing Agent": [
        "Scheduled teaser post.",
        "Coordinated with clubs for resharing.",
        "Prepared caption + hashtags."
    ],
    "Ops Agent": [
        "Created Google Form with QR.",
        "Linked sheet to auto-collect responses.",
        "Enabled email notifications."
    ],
    "Logistics Agent": [
        "Requested projector & mic from AV desk.",
        "Booked 2 extra extension boards.",
        "Prepared attendance sheets."
    ],
    "Planning Agent": [
        "Outlined timeline with milestones.",
        "Mapped dependencies across teams.",
        "Shared plan with stakeholders."
    ],
    "Coordinator Agent": [
        "Captured constraints (date, budget ceiling).",
        "Aligned scope and expected outcomes.",
        "Confirmed decision-makers."
    ]
}


def get_llm(groq_api_key: Optional[str], model_name: str = "llama3-8b-8192"):
    """Return a LangChain ChatGroq instance if available & key provided, else None."""
    if not LLM_AVAILABLE:
        return None
    key = groq_api_key or os.getenv("GROQ_API_KEY")
    if not key:
        return None
    try:
        llm = ChatGroq(model=model_name, groq_api_key=key, temperature=0.3)
        return llm
    except Exception:
        return None


def make_plan_with_llm(llm, query: str) -> Plan:
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("user", USER_PROMPT)]
    )
    msg = prompt.format_messages(query=query)
    resp = llm.invoke(msg)
    text = resp.content.strip()
    # Expecting strict JSON
    data = json.loads(text)
    subtasks = []
    for i, t in enumerate(data.get("subtasks", []), start=1):
        subtasks.append(SubTask(id=i, title=t["title"], owner=t.get("owner", "Agent")))
    return Plan(main_query=query, subtasks=subtasks)


def make_plan_fallback(query: str) -> Plan:
    # Simple heuristic: reuse template but stays “dynamic” by keeping user query in the plan
    subtasks = []
    for i, (title, owner) in enumerate(FALLBACK_TEMPLATES, start=1):
        subtasks.append(SubTask(id=i, title=title, owner=owner))
    return Plan(main_query=query, subtasks=subtasks)


def simulate_agent_run(subtask: SubTask, speed: float = 0.6):
    subtask.status = "running"
    logs = AGENT_SAMPLE_LOGS.get(subtask.owner, [
        "Initialized task context.",
        "Gathered necessary info.",
        "Completed draft deliverables."
    ])
    for line in logs:
        time.sleep(speed)
        subtask.logs.append(f"[{subtask.owner}] {line}")
        yield subtask
    time.sleep(speed)
    subtask.status = "done"
    subtask.logs.append(f"[{subtask.owner}] ✅ Completed: {subtask.title}")
    yield subtask


def render_badge(status: str):
    color = {"pending": "gray", "running": "orange", "done": "green", "failed": "red"}.get(status, "gray")
    return f":{color}[{status}]"


# ---------- Streamlit App ----------
st.set_page_config(page_title="Agentic Planner (Groq)", page_icon="🤖", layout="wide")

st.title("🤖 Agentic Planner — Mock Multi-Agent Flow")
st.caption("One query → smart subtasks → simulated agents with progress logs")

with st.sidebar:
    st.subheader("⚙️ Settings")
    groq_key_input = st.text_input("GROQ_API_KEY", value=os.getenv("GROQ_API_KEY", ""), type="password")
    model_name = st.selectbox(
        "Groq Model",
        ["llama3-8b-8192", "llama-3.1-8b-instant", "llama-3.1-70b-versatile"],
        index=0
    )
    speed = st.slider("Simulation speed (sec/step)", 0.1, 1.5, 0.6, 0.1)
    st.markdown("---")
    st.markdown("**Troubleshooting**")
    st.markdown("- Don’t name this file `groq.py`")
    st.markdown("- If API errors: check internet / proxy / key")

query = st.text_input("Enter your goal (e.g., “Organize a robotics workshop”)", value="")
col_run, col_clear = st.columns([1, 1], gap="small")
run_clicked = col_run.button("▶️ Plan & Simulate")
if col_clear.button("🧹 Clear"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# Store state
if "plan" not in st.session_state:
    st.session_state.plan: Optional[Plan] = None
if "run_logs" not in st.session_state:
    st.session_state.run_logs: Dict[int, List[str]] = {}
if "statuses" not in st.session_state:
    st.session_state.statuses: Dict[int, str] = {}

def ensure_status_tracking(plan: Plan):
    for s in plan.subtasks:
        st.session_state.run_logs.setdefault(s.id, [])
        st.session_state.statuses.setdefault(s.id, "pending")

if run_clicked and query.strip():
    # Build plan (LLM first, else fallback)
    llm = get_llm(groq_key_input, model_name=model_name)
    try:
        if llm:
            plan = make_plan_with_llm(llm, query.strip())
        else:
            plan = make_plan_fallback(query.strip())
    except Exception:
        plan = make_plan_fallback(query.strip())

    st.session_state.plan = plan
    ensure_status_tracking(plan)

    # Show main query
    with st.chat_message("user"):
        st.markdown(f"**Main Goal:** {plan.main_query}")

    # Simulate each subtask agent
    for sub in plan.subtasks:
        with st.expander(f"#{sub.id} {sub.title} — {sub.owner}", expanded=True):
            placeholder = st.empty()
            log_box = st.empty()

            # Update and stream logs
            for updated in simulate_agent_run(sub, speed=speed):
                st.session_state.statuses[sub.id] = updated.status
                st.session_state.run_logs[sub.id] = updated.logs.copy()
                with placeholder.container():
                    st.markdown(f"**Owner:** {updated.owner} | **Status:** {render_badge(updated.status)}")
                with log_box.container():
                    for line in updated.logs:
                        st.markdown(f"- {line}")
            st.success(f"Completed: {sub.title}")

# Render plan (if exists) with a compact summary grid
plan: Optional[Plan] = st.session_state.get("plan")
if plan:
    st.markdown("### 📋 Plan Summary")
    for sub in plan.subtasks:
        status = st.session_state.statuses.get(sub.id, "pending")
        st.markdown(f"- **{sub.title}** — _{sub.owner}_ {render_badge(status)}")

    st.markdown("### 🧾 Consolidated Logs")
    for sub in plan.subtasks:
        logs = st.session_state.run_logs.get(sub.id, [])
        with st.expander(f"Logs • #{sub.id} {sub.title}", expanded=False):
            if logs:
                for line in logs:
                    st.markdown(f"- {line}")
            else:
                st.write("No logs yet.")

st.markdown("---")
st.caption("Tip: For real actions (email/booking), replace mocks with tool integrations. This demo only simulates the flow.")
