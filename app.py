import streamlit as st
import pandas as pd
import random
from components import ASSETS, goals
from screens import render_setup_screen, render_tutorial_screen

st.set_page_config(page_title = "EcoSim, a Climate Simulation Game", page_icon = "🌱", layout = "wide")

st.markdown("""
<style>
    .tile-card {
        border: 2px solid #333;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        background_color: #1e1e1e;
        margin-bottom: 10px;
    }
    .tile-empty { border: 2px dashed #666; background-color: #121212; }
    .tile-park { border-color: #2e7d32; background-color: #1b381e; }
    .tile-solar { border-color: #fbc02d; background-color: #38321b; }
    .tile-reservoir { border-color: #0288d1; background-color: #1b2f38; }
    .tile-factory { border-color: #d32f2f; background-color: #381b1b; }
    .tile-commercial { border-color: #7b1fa2; background-color: #2e1b38; }
</style>
""", unsafe_allow_html = True)

if "initialized" not in st.session_state:
    st.session_state.game_phase = "setup" #setup, tutorial, playing, game over, victory
    st.session_state.selected_goals = [
        {"name": "Protect the Climate", "desc": "Default goal, depends on heat reduction and environmental approval"},
        {"name": "", "desc": ""},
        {"name": "", "desc": ""}
    ]
    st.session_state.budget = 15_000_000
    st.session_state.debt = 0
    st.session_state.water_supply = 5_000
    st.session_state.temp_reduction = 0.0
    st.session_state.solar_kwh = 0
    st.session_state.turn = 0
    st.session_state.approval_env = 70 # Environmentalists
    st.session_state.approval_biz = 60 #Business People
    st.session_state.approval_res = 65 #Residents
    st.session_state.credit_rating = "AA"
    st.session_state.active_policy = "None"
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.show_tutorial = True
    st.session_state.viewing_summary = False
    st.session_state.build_mode_active = False
    st.session_state.tutorial_step = 1
    st.session_state.latest_summary = {}
    if "selected_blueprint" not in st.session_state:
        st.session_state.selected_blueprint = "🌳 Urban Park"
    st.session_state.event_log = ["Simulation started! Balance the environment, business, and civilian interests."]
    st.session_state.history = [{"Year": 2026, "Budget": 15_000_000, "Env Approval": 70, "Biz Approval": 60, "Res Approval": 65}]
    st.session_state.grid = {i: {"type": "Empty Plot", "upkeep_cost": 0, "upkeep_water": 0} for i in range (1, 17)}
    st.session_state.initialized = True

st.title("🏙️ EcoSim, an Urban Climate Management Simulation")
st.markdown("Manage city budgets, infrastructure upkeep, and climate challenges under strict public scrutiny.")

if st.session_state.game_phase == "setup":
    render_setup_screen(goals)
    st.stop()

st.markdown("---")

if st.session_state.show_tutorial:
    render_tutorial_screen()
    st.stop()

st.sidebar.header("📊 City Finances & Stats")
st.sidebar.metric("💰 Budget", f"${st.session_state.budget:,.0f}")
if st.session_state.debt > 0:
    st.sidebar.metric("📉 Outstanding Debt", f"${st.session_state.debt:,.0f}", delta_color = "inverse")
st.sidebar.metric("🏷️ Credit Rating", st.session_state.credit_rating)
st.sidebar.metric("💧 Water Reserves", f"{st.session_state.water_supply:,} Units")

st.sidebar.markdown("---")
st.sidebar.header("👥 Approval by Demographic")
st.sidebar.metric("🌿 Environmentalists", f"{st.session_state.approval_env}%")
st.sidebar.metric("💼 Business Leaders", f"{st.session_state.approval_biz}%")
st.sidebar.metric("🏡 Working Class Residents", f"{st.session_state.approval_res}%")

st.sidebar.markdown("---")
st.sidebar.header("🌍 Environmental Data")
st.sidebar.metric("🌡️ Heat Island Reduction", f"{st.session_state.temp_reduction:.1f} °C")
st.sidebar.metric("⚡ Clean Energy", f"{st.session_state.solar_kwh} kWh")
st.sidebar.markdown(f"**Current Year:** {2026 + st.session_state.turn}")
st.sidebar.markdown(f"**Active Policy:** {st.session_state.active_policy}")

st.sidebar.markdown("---")
st.sidebar.header("🎯 Active Governing Goals")

for i, goal in enumerate(st.session_state.selected_goals, start = 1):
    if isinstance(goal, dict):
        g_name = goal.get("name", "")
        g_desc = goal.get("desc", "")
        st.sidebar.markdown(f"**Goal {i}:** {g_name}")
        st.sidebar.caption(f"└ {g_desc}")
    else:
        st.sidebar.markdown(f"**Goal {i}:** {goal}")

if st.session_state.viewing_summary:
    sum_data = st.session_state.latest_summary
    st.markdown("---")
    st.error(f"📰 **YEAR {sum_data['year']} REVIEW: CITY HALL GAZETTE")
    st.info(f"**Annual Event:** {sum_data['event_desc']}")

    st.markdown(f"**Major Group Events:** \n {sum_data['faction_msg']}")

    with st.expander(" **View Itemized Approval Rating Drivers**", expanded = True):
        st.markdown(f"** Environmentalists ({sum_data['env_diff']:+d}%):**")
        for driver in sum_data['env_drivers']:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• {driver}")

        st.markdown(f"** Business Leaders ({sum_data['biz_diff']:+d}%):**")
        for driver in sum_data['biz_drivers']:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• {driver}")

        st.markdown(f"** Working Class Residents ({sum_data['res_diff']:+d}%):**")
        for driver in sum_data['res_drivers']:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• {driver}")

    with st.expander(" **View Itemized Municipal Budget Invoice**", expanded = True):
        st.markdown(f"• **Base Revenue:** +$3,500,000")
        st.markdown(f"• **Building/Asset Revenue:** +${sum_data['asset_income']:,.0f}")
        st.markdown(f"• **Solar Energy Credits:** +${sum_data['solar_income']:,.0f}")
        st.markdown(f"• **Infrastructure Upkeep Costs:** -${sum_data['upkeep_cost']:,.0f}")
        if sum_data['interest_paid'] > 0:
            st.markdown(f"• **Debt & Deficit Interest Penalty:** -${sum_data['interest_paid']:,.0f}")
        st.markdown(f"---")
        st.markdown(f"**Net Budget Shift this Year:** **${sum_data['budget_diff']:,.0f}**")

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("💰 Net Budget Change", f"${sum_data['budget_diff']:,.0f}")
    col_b.metric("🌿 Environmentalist Approval", f"{sum_data['env_curr']}%", f"{sum_data['env_diff']}%")
    col_c.metric("💼 Business Approval", f"{sum_data['biz_curr']}%", f"{sum_data['biz_diff']}%")
    col_d.metric("🏡 Resident Approval", f"{sum_data['biz_curr']}%", f"{sum_data['biz_diff']}%")

    if st.button("➡️ Close Review & Proceed"):
        st.session_state.viewing_summary = False
        st.rerun()
    st.stop()

st.subheader("📢 City Hall Announcements")
st.info(st.session_state.event_log[-1])

with st.expander("Bond and Emergency Loan Office"):
    st.markdown("Need quick cash? Issue bonds to introduce cash into your budget, but be aware of compouding interest and credit rating downgrades.")
    loan_amount = st.selectbox("Select amount", [5_000_000, 10_000_000, 20_000_000], format_func = lambda x: f"${x:,.0f}")
    if st.button("Release to Circulation"):
        st.session_state.budget += loan_amount
        st.session_state.debt += loan_amount
        st.session_state.approval_biz += 3
        st.session_state.approval_res -= 5
        st.success(f"Issued ${loan_amount:,.0f} in bonds!")
        st.rerun()

st.subheader("🏛️ Municipal Policies (Choose 1 per Term)")
policy_options = [
    "None",
    "🌿 Green Transition Mandate (+Solar Income, +Park Approval, -Budget)",
    "🏭 Industrial Deregulation (++Factory Income, --Heat and Approval)",
    "💧 Water Rationing (+Water Supply, -10% Approval)"
]
selected_policy = st.selectbox("Select Active Policy", policy_options, key = "policy_select")
st.session_state.active_policy = selected_policy

st.markdown("---")
btn_text = "❌ Close Build Mode" if st.session_state.build_mode_active else "🔨 Open Build Mode"

col_header, col_btn = st.columns([3, 1])
with col_header:
    st.subheader("🗺️ City Zoning Grid (4x4))")

with col_btn:
    if st.button(btn_text, key = "toggle_build_mode_main", type = "primary" if not st.session_state.build_mode_active else "secondary", use_container_width = True):
        st.session_state.build_mode_active = not st.session_state.build_mode_active
        st.rerun()

if "active_build_tile" not in st.session_state:
    st.session_state.active_build_tile = None

if st.session_state.build_mode_active:
    st.info("🏗️ **BUILD MODE ACTIVE:** Select a blueprint from your hotbar below, then click **[Construct]** on any empty plot!")

    hb_cols = st.columns(len(ASSETS) + 1)
    asset_keys = list(ASSETS.keys())

    for i, a_key in enumerate(asset_keys):
        a_data = ASSETS[a_key]
        is_selected = (st.session_state.selected_blueprint == a_key)
        btn_label = f"✨ [{a_key}]" if is_selected else a_key

        with hb_cols[i]:
            if st.button(btn_label, key = f"hb_{i}"):
                st.session_state.selected_blueprint = a_key
                st.rerun()
            st.caption(f"Cost: ${a_data['cost']/1_000_000:.1f}M")

    with hb_cols[-1]:
        if st.button("❌ Exit", key = "hb_close"):
            st.session_state.build_mode_active = False
            st.rerun()

    active_b = ASSETS[st.session_state.selected_blueprint]
    st.markdown(f"**Selected Blueprint:** `{st.session_state.selected_blueprint}` - *{active_b['desc_effect']}* ")

cols = st.columns(4)

for i, tile_id in enumerate(st.session_state.grid.keys()):
    col = cols[i % 4]
    tile = st.session_state.grid[tile_id]
    t_type = tile["type"]

    css_class = "tile-empty"
    icon = "🏗️"
    if "Park" in t_type: css_class, icon = "tile-park", "🌳"
    elif "Solar" in t_type: css_class, icon = "tile-solar", "☀️"
    elif "Reservoir" in t_type: css_class, icon = "tile-reservoir", "💧"
    elif "Factory" in t_type: css_class, icon = "tile-factory", "🏭"
    elif "Commercial" in t_type: css_class, icon = "tile-commercial", "🏢"

    with col:
        st.markdown(f"""
        <div class = "tile-card {css_class}">
            <h2 style = "margin:0;">{icon}</h2>
            <b>Plot {tile_id}</b><br/>
            <small>{t_type}</small>
        </div>
        """, unsafe_allow_html = True)

        if t_type == "Empty Plot" and st.session_state.build_mode_active:
            chosen_bp = st.session_state.selected_blueprint
            b_data = ASSETS[chosen_bp]

            if st.button(f"🏗️ Construct ({chosen_bp.split()[1]})", key = f"build_plot_{tile_id}"):
                will_be_deficit = (st.session_state.budget - b_data["cost"]) < 0
                if st.session_state.water_supply < b_data["water_cost"]:
                    st.error("Insufficient water!")
                elif will_be_deficit and st.session_state.budget + 25_000_000 < b_data["cost"]:
                    st.error("Budget too low for deficit!")
                else:
                    st.session_state.budget -= b_data["cost"]
                    st.session_state.water_supply -= b_data["water_cost"]
                    st.session_state.temp_reduction += b_data["heat_mod"]
                    st.session_state.solar_kwh += b_data["solar_mod"]
                    st.session_state.grid[tile_id] = {
                        "type": chosen_bp,
                        "upkeep_cost": b_data["upkeep_cost"],
                        "upkeep_water": b_data["upkeep_water"]
                    }
                    st.rerun()

        elif t_type != "Empty Plot" and st.session_state.build_mode_active:
            if st.button(f" Demolish [Plot {tile_id}]", key = f"clear_{tile_id}"):
                if st.session_state.budget >= 1_000_000:
                    st.session_state.budget -= 1_000_000
                    if "Park" in t_type: st.session_state.temp_reduction = max(0.0, st.session_state.temp_reduction - 0.6)
                    elif "Solar" in t_type: st.session_state.solar_kwh = max(0, st.session_state.solar_kwh - 1200)
                    elif "Factory" in t_type: st.session_state.temp_reduction = min(4.0, st.session_state.temp_reduction + 0.8)
                    elif "Commercial" in t_type: st.session_state.temp_reduction = min(4.0, st.session_state.temp_reduction + 0.4)
                    st.session_state.grid[tile_id] = {"type": "Empty Plot", "upkeep_cost": 0, "upkeep_water": 0}
                    st.rerun()
                else:
                    st.error("Need $1M for demolition!")

if st.session_state.active_build_tile is not None:
    t_id = st.session_state.active_build_tile
    st.markdown("---")
    st.warning(f"🏗️ **BUILD MODE ACTIVE: Constructing on Plot {t_id}")
    col_m1, col_m2 = st.columns([2, 1])

    with col_m1:
        chosen_asset = st.selectbox("Select Blueprint Option", list(ASSETS.keys()))
        asset_data = ASSETS[chosen_asset]
        st.markdown(f"**Upfront Cost:** ${asset_data['cost']:,} | **Water Needed:** {asset_data['water_cost']} Units")
        st.markdown(f"**Annual Upkeep:** ${asset_data['upkeep_cost']:,}/yr | **Environmental Effect:** {asset_data['desc_effect']}")

        will_be_deficit = (st.session_state.budget - asset_data["cost"]) < 0
        if will_be_deficit:
            st.error("⚠️ Warning: Deficit financing required! ⚠️")
            confirm_deficit = st.checkbox("Are you sure you want to go into a deficit to construct this?")
        else:
            confirm_deficit = True

    with col_m2:
        st.write("")
        st.write("")
        if st.button("✅ Confirm Blueprint Construction", key = "confirm_build_btn"):
            if not confirm_deficit and will_be_deficit:
                st.error("Authorize debt first!")
            elif st.session_state.water_supply < asset_data["water_cost"]:
                st.error("Insufficient water!")
            else:
                st.session_state.budget -= asset_data["cost"]
                st.session_state.water_supply -= asset_data["water_cost"]
                st.session_state.temp_reduction += asset_data["heat_mod"]
                st.session_state.solar_kwh += asset_data["solar_mod"]
                st.session_state.grid[t_id] = {
                    "type": chosen_asset,
                    "upkeep_cost": asset_data["upkeep_cost"],
                    "upkeep_water": asset_data["upkeep_water"]
                }
                st.session_state.active_build_tile = None
                st.rerun()

        if st.button("❌ Cancel Build Mode", key = "cancel_build_btn"):
            st.session_state.active_build_tile = None
            st.rerun()

st.markdown("---")

if st.session_state.game_over:
    st.error("🚨 **Game Over!** Public approval hit 0 or debt became unmanageable. Review your strategy and try again.")
    if st.button("🔄 Restart Simulation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
elif st.session_state.victory:
    st.success("🏆 **10-Year Mayoral Term Completed!")
    st.markdown("## **MAYORAL TERM PERFORMANCE**")

    avg_approval = (st.session_state.approval_env + st.session_state.approval_biz + st.session_state.approval_res) / 3
    net_worth = st.session_state.budget - st.session_state.debt

    grade_env = "A" if st.session_state.temp_reduction >= 2.0 else ("B" if st.session_state.temp_reduction >= 1.0 else "C")
    grade_fiscal = "A" if net_worth > 20_000_000 else ("B" if net_worth > 5_000_000 else "D")
    grade_politics = "A" if avg_approval >= 75 else ("B" if avg_approval >= 55 else "C")

    col_g1, col_g2, col_g3 = st.columns(3)
    col_g1.metric(" Climate Grade", grade_env, f"{st.session_state.temp_reduction:.1f}°C Heat Reduction")
    col_g2.metric(" Fiscal Grade", grade_fiscal, f"${net_worth:,.0f} Net Worth")
    col_g3.metric(" Governance Grade", grade_politics, f"{avg_approval:.1f}% Avg Approval")

    st.markdown("###👥 **Demographic Approval Breakdown ➡️**")
    if st.session_state.approval_env < 50:
        st.warning("⚠️ **Environmental Critique:** Your administration prioritized immediate revenue over climate conservation. Your city's carbon footprint remains high.")
    if st.session_state.approval_biz < 50:
        st.warning("💼 **Commercial Critique:** Business leaders feel over-regulated and taxed, stifling commercial expansion.")
    if st.session_state.approval_res < 50:
        st.warning("🏡 **Civilian Critique:** Working-class residents bore the brunt of negative impacts from your policies.")

    st.markdown("###🎯 **Governing Goals Evaluation**")
    for i, goal in enumerate(st.session_state.selected_goals, start = 1):
        goal_name = goal.get("name", "")
        goal_desc = goal.get("desc", "")
        achieved = False
        status_msg = ""

        if "Protect the Climate" in goal_name:
            achieved = st.session_state.temp_reduction >= 1.5 and st.session_state.approval_env >= 66
            status_msg = f"Achieved {st.session_state.temp_reduction:.1f}°C / target 1.5°C and {st.session_state.approval_env:,}% / target 66%"
        elif "Fiscal Conservative" in goal_name:
            achieved = net_worth >= 20_000_000
            status_msg = f"Finished with ${net_worth:,.0f} net worth / target $20,000,000"
        elif "Water Security" in goal_name:
            achieved = st.session_state.water_supply >= 2000
            status_msg = f"Finished with {st.session_state.water_supply:,} units / target 2,000 units"
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
            status_msg = f"Min Approval: {min(st.session_state.approval_env, st.session_state.approval_biz, st.session_state.approval_res)}% / target 70%"

        if achieved:
            st.success(f"✅ **Goal {i}: {goal_name}** PASSED!\n\n*{status_msg}")
        else:
            st.error(f"❌ **Goal {i}: {goal_name}** FAILED!\n\n*{status_msg}*")
    
    if st.button("🔄 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

elif st.button("⏩ Advance to Next Year"):
    old_budget = st.session_state.budget
    old_env = st.session_state.approval_env
    old_biz = st.session_state.approval_biz
    old_res = st.session_state.approval_res

    st.session_state.turn += 1

    total_upkeep_cost = sum(t["upkeep_cost"] for t in st.session_state.grid.values())
    total_upkeep_water = sum(t["upkeep_water"] for t in st.session_state.grid.values())
    asset_income = sum(ASSETS.get(t["type"], {}).get("income", 0) for t in st.session_state.grid.values() if t["type"] != "Empty Plot")

    env_shift = sum(ASSETS.get(t["type"], {}).get("env_mod", 0) for t in st.session_state.grid.values() if t["type"] != "Empty Plot")
    biz_shift = sum(ASSETS.get(t["type"], {}).get("biz_mod", 0) for t in st.session_state.grid.values() if t["type"] != "Empty Plot")
    res_shift = sum(ASSETS.get(t["type"], {}).get("res_mod", 0) for t in st.session_state.grid.values() if t["type"] != "Empty Plot")

    yearly_income = 3_500_000 + asset_income + (st.session_state.solar_kwh * 400)
    yearly_water_gain = 800

    st.session_state.approval_env += env_shift
    st.session_state.approval_biz += biz_shift
    st.session_state.approval_res += res_shift

    if "Green Transition Mandate" in st.session_state.active_policy:
        yearly_income -= 1_200_000
        st.session_state.approval_env += 4
        st.session_state.approval_biz -= 3
    elif "Industrial Deregulation" in st.session_state.active_policy:
        yearly_income += 3_500_000
        st.session_state.approval_biz += 6
        st.session_state.approval_env -= 7
        st.session_state.temp_reduction -= 0.4
    elif "Water Rationing" in st.session_state.active_policy:
        yearly_water_gain += 1_500
        st.session_state.approval_res -= 6

    net_cash_flow = yearly_income - total_upkeep_cost
    if st.session_state.budget < 0:
        interest_penalty = abs(st.session_state.budget) * 0.08
        net_cash_flow -= interest_penalty
        st.session_state.approval_res -= 8
    
    st.session_state.budget += net_cash_flow
    st.session_state.water_supply += (yearly_water_gain - total_upkeep_water)

    faction_msg = ""

    faction_messages = []

    if st.session_state.approval_env >= 85:
        st.session_state.budget += 1_000_000
        faction_messages.append("Environmentalists staged a clean-energy charity auction (+$1M)!")
    elif st.session_state.approval_env < 40:
        st.session_state.approval_res -= 5
        faction_messages.append("Environmentalists are staging massive climate protests (-5% resident morale).")

    if st.session_state.approval_biz >= 85:
        st.session_state.budget += 1_500_500
        faction_messages.append("Business leaders invested heavily in bonds (+$1.5M)!")
    elif st.session_state.approval_biz < 40:
        yearly_income -= 1_000_000
        faction_messages.append(" Chamber of Commerce initiated a corporate tax strike ($1M).")

    if st.session_state.approval_res >= 85:
        st.session_state.water_supply += 500
        faction_messages.append("Residents launched a community-led water saving campaign (+500 Water)!")
    elif st.session_state.approval_res < 40:
        st.session_state.approval_env -= 5
        st.session_state.approval_biz -= 5
        faction_messages.append("Working class citizens are rioting over costs in the city (-5 of all approvals).")

    faction_msg = "  \n".join(faction_messages) if faction_messages else "No major group events this year."

    if st.session_state.budget > 10_000_000:
        st.session_state.credit_rating = "AAA"
    elif st.session_state.budget > 2_000_000:
        st.session_state.credit_rating = "AA"
    elif st.session_state.budget >= 0:
        st.session_state.credit_rating = "BBB"
    elif st.session_state.budget > -15_000_000:
        st.session_state.credit_rating = "B (Junk)"
    else:
        st.session_state.credit_rating = "Default"

    st.session_state.approval_env = max(0, min(100, st.session_state.approval_env))
    st.session_state.approval_biz = max(0, min(100, st.session_state.approval_biz))
    st.session_state.approval_res = max(0, min(100, st.session_state.approval_res))

    event_roll = random.choice([
        ("normal", "Stable year for the city."),
        ("drought", "Severe Drought! Water reserves drained heavily (-800 Units)"),
        ("grant", "Federal Grant Awarded! +$2.5M added to budget."),
        ("heatwave", "Intense Heatwave! Citizens are suffering (-15% approval)."),
    ])

    event_type, event_desc = event_roll
    if event_type == "drought":
        st.session_state.water_supply -= 800
        st.session_state.approval_res -= 4
        st.session_state.approval_env -= 4
        st.session_state.approval_biz -= 4
    elif event_type == "grant":
        st.session_state.budget += 2_500_000
        st.session_state.approval_biz += 4
    elif event_type == "heatwave":
        st.session_state.approval_env -= 7
        st.session_state.approval_res -= 7
        st.session_state.approval_biz -= 7

    st.session_state.event_log.append(f"Year {st.session_state.turn}: {event_desc}")

    if st.session_state.budget < 0:
        st.session_state.approval_res -= 8
        st.session_state.approval_biz -= 12
    if st.session_state.water_supply < 0:
        st.session_state.approval_res -= 15
    if st.session_state.temp_reduction < 1.5:
        st.session_state.approval_env -= 10

    if (st.session_state.approval_env <= 0 or
        st.session_state.approval_biz <= 0 or
        st.session_state.approval_res <= 0 or
        st.session_state.budget < -25_000_000):
        st.session_state.game_over = True
    elif st.session_state.turn >= 10:
        st.session_state.victory = True

    st.session_state.latest_summary = {
        "year": 2026 + st.session_state.turn,
        "event_desc": event_desc,
        "faction_msg": faction_msg,
        "budget_diff": st.session_state.budget - old_budget,
        "base_income": 3_500_000,
        "asset_income": asset_income,
        "solar_income": st.session_state.solar_kwh * 400,
        "upkeep_cost": total_upkeep_cost,
        "interest_paid": (abs(old_budget) * 0.08) if old_budget < 0 or st.session_state.debt > 0 else 0,
        "env_curr": st.session_state.approval_env,
        "env_diff": st.session_state.approval_env - old_env,
        "env_drivers": [
            f"Zoning Grid: {env_shift:+d}%",
            f"Policy Impact: {'+4%' if 'Green' in st.session_state.active_policy else ('-7%' if 'Industrial' in st.session_state.active_policy else '0%')}",
            f"Event Penalty: {('-4%' if event_type in ['drought', 'heatwave'] else '0%')}",
            f"Heat Penalty: {'-10%' if st.session_state.temp_reduction < 1.5 else 'None'}",
            f"Protest Effects: {'-5%' if st.session_state.approval_res < 40 else 'None'}"
        ],
        "biz_curr": st.session_state.approval_biz,
        "biz_diff": st.session_state.approval_biz - old_biz,
        "biz_drivers": [
            f"Zoning Grid: {biz_shift:+d}%",
            f"Policy Impact: {'+6%' if 'Industrial' in st.session_state.active_policy else ('-3%' if 'Green' in st.session_state.active_policy else '0%')}",
            f"Deficit Penalty: {'-12%' if old_budget < 0 else 'None'}",
            f"Event Penalty: {('-4%' if event_type in ['drought', 'heatwave'] else '0%')}",
            f"Protest Effects: {'-5%' if st.session_state.approval_res < 40 else 'None'}"
        ],
        "res_curr": st.session_state.approval_res,
        "res_diff": st.session_state.approval_res - old_res,
        "res_drivers": [
            f"Zoning Grid: {res_shift:+d}%",
            f"Policy Impact: {'-6%' if 'Water' in st.session_state.active_policy else '0%'}",
            f"Deficit Penalty: {'-8%' if old_budget < 0 else 'None'}",
            f"Event Penalty: {'-4' if event_type in ['drought', 'heatwave'] else '0%'}",
            f"Water Penalty: {'-15%' if st.session_state.water_supply < 0 else 'None'}",
            f"Protest Effects: {'-5%' if st.session_state.approval_env < 40 else 'None'}"
        ],
        "credit": st.session_state.credit_rating
    }
    st.session_state.viewing_summary = True

    st.session_state.history.append({
        "Year": 2026 + st.session_state.turn,
        "Budget": st.session_state.budget,
        "Water": st.session_state.water_supply,
        "Env Approval": st.session_state.approval_env,
        "Biz Approval": st.session_state.approval_biz,
        "Res Approval": st.session_state.approval_res
    })

    st.rerun()

st.markdown("### 📈 Municipal Climate Data & Export")
if len(st.session_state.history) > 0:
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history, width='stretch')

    csv_data = df_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label = "📥 Download City Performance Report (CSV)",
        data = csv_data,
        file_name = "ecosim_performance_report.csv",
        mime = "text/csv",
    )

