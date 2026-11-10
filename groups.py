import streamlit as st
import random

QUESTS = [
    {
        "group": " Environmentalists",
        "title": "Greenifying Mandate",
        "desc": "Environmentalists demand that you build at least 2 green plots (Parks/Solar) within the next 2 years.",
        "type": "build",
        "target_types": ["🌳 Urban Park", "☀️ Solar Array"],
        "target_count": 2,
        "turns": 2,
        "reward_env": 10,
        "reward_cash": 1_500_500,
        "penalty_env": -12
    },
    {
        "group": "Business Leaders",
        "title": "Industrial Expansion",
        "desc": "Business leaders urge you to build a revenue-generating plot (Factory/Commercial) within 2 years.",
        "type": "build",
        "target_types": ["🏭 Industrial Factory", "🏢 Commercial Block"],
        "target_count": 1,
        "turns": 2,
        "reward_biz": 12,
        "reward_cash": 2_000_000,
        "penalty_biz": -15
    },
    {
        "group": "Working Class Residents",
        "title": "Water Conservation",
        "desc": "Residents require your city's water reserves to stay above 4,000 units.",
        "type": "water",
        "target_water": 4000,
        "turns": 1,
        "reward_res": 10,
        "reward_cash": 1_000_000,
        "penalty_res": -10
    }
]

def spawn():
    if "active_quest" not in st.session_state or st.session_state.active_quest is None:
        if random.random() < 0.6:
            chosen = random.choice(QUESTS)
            st.session_state.active_quest = chosen.copy()
            st.session_state.baseline = progress(chosen)

def progress(quest):
    if quest["type"] == "build":
        return sum(1 for t in st.session_state.grid.values() if t["type"] in quest["target_types"])
    return 0

def eval():
    if "active_quest" not in st.session_state or st.session_state.active_quest is None:
        return
    
    q = st.session_state.active_quest
    success = False
    if "active_quest" not in st.session_state or q is None:
        return

    if q["type"] == "build":
        count = sum(1 for t in st.session_state.grid.values() if t["type"] in q["target_types"])
        built_start = count - st.session_state.get("baseline", 0)
        if built_start >= q["target_count"]:
            success = True
    elif q["type"] == "water":
        if st.session_state.water >= q["target_water"]:
            success = True

    if success:
        st.session_state.budget += q.get("reward_cash", 0)
        if "reward_env" in q: st.session_state.approval_env += q["reward_env"]
        if "reward_biz" in q: st.session_state.approval_biz += q["reward_biz"]
        if "reward_res" in q: st.session_state.approval_res += q["reward_res"]
        st.session_state.event_log.append(f" Group Mandate Succeeded! {q['group']} rewarded your administration.")
    else:
        q["turns"] -= 1
        if q["turns"] <= 0:
            if "penalty_env" in q: st.session_state.approval_env += q["penalty_env"]
            if "penalty_biz" in q: st.session_state.approval_biz += q["penalty_biz"]
            if "penalty_res" in q: st.session_state.approval_res += q["penalty_res"]
            st.session_state.event_log.append(f"Group Mandate Failed! {q['group']} lost faith in your leadership.")
            st.session_state.active_quest = None
            return

    if success:
        st.session_state.active_quest = None

def render_quests():
    if "active_quest" in st.session_state and st.session_state.active_quest is not None:
        q = st.session_state.active_quest
        with st.container(border = True):
            st.markdown(f"** Active Mandate: {q['group']}**")
            st.write(f"*{q['title']}*")
            st.caption(f"{q['desc']} | **Turns Left:** {q['turns']}")
    else:
        st.sidebar.caption("📜 No active demands right now")