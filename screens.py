import streamlit as st
import random

def render_setup_screen(goals):
    st.markdown("---")
    st.subheader("🎯 Governing goals will guide you as you play. ➡️")
    st.markdown("Before taking oath, select your administration's core priorities. A climate improvement goal is permanently locked in.")

    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        st.markdown("### Goal 1 ➡️")
        st.info("**Protect the Climate**  \n(Locked Mandatory Goal)  \nHave 1.5°C heat reduction and 66% environmental approval at end of term")

    with col_g2:
        st.markdown("### Goal 2 ➡️")
        goal_choice_2 = st.selectbox(
            "Select Secondary Goal",
            goals,
            format_func = lambda g: f"{g['name']}\n | {g['desc']}",
            key = "setup_goal_2"
        )

    with col_g3:
        st.markdown("### Goal 3 ➡️")
        available_3 = [g for g in goals if g["name"] != goal_choice_2["name"]]
        goal_choice_3 = st.selectbox(
            "Select Tertiary Goal",
            available_3,
            format_func = lambda g: f"{g['name']}\n | {g['desc']}",
            key = "setup_goal_3"
        )

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)

    if col_btn1.button("Random Council-Appointed Goals ➡️"):
        rand_pick = random.sample(goals, 2)
        st.session_state.selected_goals = [
            {"name": "Protect the Climate", "desc": "Have 1.5°C heat reduction and 66% environmental approval at end of term"},
            rand_pick[0],
            rand_pick[1]
        ]
        st.session_state.game_phase = "playing"
        st.rerun()

    if col_btn2.button("Let's Go! ➡️"):
        st.session_state.selected_goals = [
            {"name": "Protect the Climate", "desc": "Achieve climate stability"},
            goal_choice_2,
            goal_choice_3
        ]
        st.session_state.game_phase = "playing"
        st.rerun()

def render_tutorial_screen():
    st.markdown("---")
    st.warning(f"**Welcome, Mayor! This is a tutorial for Ecoim (Step {st.session_state.tutorial_step})**")

    if st.session_state.tutorial_step == 1:
        st.markdown("""
        ### Step 1: Three Demographics of People
        In **EcoSim**, you cannot please everybody. Look at your sidebar (once you enter office) to monitor three groups:
        * 🌿 **Environmentalists:** Want green infrastructure and low heat.
        * 💼 **Business Leaders:** Want commerce and revenue.
        * 🏡 **Working Class Residents:** Care about water security and avoiding debt.
        """)

        if st.button("Next: Finances ➡️"):
            st.session_state.tutorial_step = 2
            st.rerun()

    elif st.session_state.tutorial_step == 2:
        st.markdown("""
        ### Step 2: Budgets & Debt
        You start with **$15,000,000**. Infrastructure has heavy annual upkeep costs.
        * If your budget dips below $0, you will face compouding interest penalties and credit rating drops.
        * You can issue bonds if you need cash, but residents will grow unhappy with the burden of debt.
        """)
        col_t1, col_t2 = st.columns(2)
        if col_t1.button("⬅️ Back"):
            st.session_state.tutorial_step = 1
            st.rerun()
        elif col_t2.button("Next: Zoning & Infrastructure ➡️"):
            st.session_state.tutorial_step = 3
            st.rerun()

    elif st.session_state.tutorial_step == 3:
        st.markdown("""
        ### Step 3: The 4x4 Zoning Grid
        Your city is represented by a 4x4 grid. Open Build Mode to construct Parks, Solar Plots, Reservoirs, Factories, and Commercial Blocks.
        """)
        col_t1, col_t2 = st.columns(2)
        if col_t1.button("⬅️ Back"):
            st.session_state.tutorial_step = 2
            st.rerun()
        if col_t2.button(" Next: Policies and Crises ➡️"):
            st.session_state.tutorial_step = 4
            st.rerun()

    elif st.session_state.tutorial_step == 4:
        st.markdown("""
        ### Step 4: City Policies and Annual Events
        * **Policies:** At the start of each year, choose 1 executive policy to alter your city's rules
        * **Random Events:** Each year brings unpredictable events which will put your leadership to the test.
        """)
        col_t1, col_t2 = st.columns(2)
        if col_t1.button("⬅️ Back"):
            st.session_state.tutorial_step = 3
            st.rerun()
        if col_t2.button("Next: The Final Goal ➡️"):
            st.session_state.tutorial_step = 5
            st.rerun()

    elif st.session_state.tutorial_step == 5:
        st.markdown("""
        ### Step 5: Winning & The Year-End Gazette
        * **Your Objective:** Survive the full 10 years while keeping all the demographics happy and your budget high.
        * **Yearly Review:** Every time you advance to the next year, a newspaper shows stats for that year.
        """)
        col_t1, col_t2 = st.columns(2)
        if col_t1.button("⬅️ Back"):
            st.session_state.tutorial_step = 4
            st.rerun()
        if col_t2.button("Finish Tutorial & Begin! ➡️"):
            st.session_state.show_tutorial = False
            st.rerun()