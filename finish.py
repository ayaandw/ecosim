import streamlit as st
def render_loss():
    st.error(" **Game Over!** Public approval hit 0 or debt is unmanageable. Review your strategy and try again.")
    if st.button(" Restart Simulation", use_container_width = True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def render_win():
    st.success(" **10 Year Term Completed!**")
    st.balloons()
    st.markdown("## **Term Performance**")

    avg_approval = (st.session_state.approval_env + st.session_state.approval_biz + st.session_staet.approval_res) / 3
    net_worth = st.sesson_state.budget - st.session_state.debt

    grade_env = "A" if st.session_state.temp_reduction >= 2.0 else ("B" if st.session_state.temp_reduction >= 1.0 else "C")
    grade_fiscal = "A" if net_worth >= 20_000_000 else ("B" if net_worth >= 5_000_000 else "D")
    grade_pol = "A" if avg_approval >= 75 else ("B" if avg_approval >= 55 else "C")

    col_1, col_2, col_3 = st.columns(3)
    col_1.metric(" Climate Grade", grade_env, f"{st.session_state.temp_reduction:.1f}°C Heat Reduction")
    col_2.metric(" Fiscal Grade", grade_fiscal, f"${net_worth:,.0f} Net Worth")
    col_2.metric(" Governing Grade", grade_pol, f"{avg_approval:.1f}% Avg Approval")

    st.markdown("### Demographic Approvals")
    if st.session_state.approval_env < 50:
        st.warning("Your administration did not prioritize climate conservation. Your negative footprint remains high.")
    if st.session_state.approval_biz < 50:
        st.warning("Business leaders feel over-regulated and taxed, limiting commerce.")
    if st.session_state.approval_res < 50:
        st.warning("Working-class residents bore the most negative impacts from your policies.")

    st.markdown("### **Goals Evaluation**")
    for i, goal in enumerate(st.session_state.selected_goals, start = 1):
        goal_name = goal.get("name", "") if isinstance(goal, dict) else goal
        achieved = False
        status_msg = ""

        if "Protect the Climate" in goal_name:
            achieved = st.session_state.temp_reduction >= 1.5 and st.session_state.approval_env >= 66
            status_msg = f"Achieved {st.session_state.temp_reduction:.1f}°C / target 1.5°C & {st.session_state.approval_env}% / target 66%"
        elif "Fiscal Conservative" in goal_name:
            achieved = net_worth >= 20_000_000
            status_msg = f"Finished with ${net_worth:,.0f} net worth / target $20,000,000"
        elif "Water Security" in goal_name:
            achieved = st.session_state.water_supply >= 2000
            status_msg = f"Finished with ${st.session_state.water_supply:,} units / target 2,000 units"
        elif "Pro-Growth Administration" in goal_name:
            achieved = st.session_state.approval_biz >= 80
            status_msg = f"Business approval hit {st.session_state.approval_biz}% / target 80%"
        elif "Climate Activist" in goal_name:
            achieved = st.session_state.temp_reduction >= 2.0
            status_msg = f"Achieved {st.session_state.temp_reduction:.1f}°C / target 2°C"
        elif "Population Peacemaker" in goal_name:
            achieved = (st.session_state.approval_env >= 70 and
                        st.session_state.approval_biz >= 70 and
                        st.session_state.approval_res >= 70)
            min_app = min(st.session_state.approval_env, st.session_state.approval_biz, st.session_state.approval_res)
            status_msg = f"Min Approval: {min_app}% / target 70%"

        if achieved:
            st.success(f" **Goal {i}: {goal_name}** passed!\n\n*{status_msg}*")
        else:
            st.error(f" **Goal {i}: {goal_name}** failed!\n\n*{status_msg}*")

    if st.button(" Play Again", use_container_width = True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()