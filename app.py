import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title = "EcoSim, a Climate Simulation Game", page_icon = "🌱", layout = "wide")

if "initialized" not in st.session_state:
    st.session_state.budget = 15_000_000
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
    st.session_state.event_log = ["Simulation started! Balance the environment, business, and civilian interests."]
    st.session_state.history = [{"Year": 2026, "Budget": 15_000_000, "Env Approval": 70, "Biz Approval": 60, "Res Approval": 65}]
    st.session_state.grid = {i: {"type": "Empty Plot", "upkeep_cost": 0, "upkeep_water": 0} for i in range (1, 10)}
    st.session_state.initialized = True

st.title("🏙️ EcoSim, an Urban Climate Management Simulation")
st.markdown("Manage city budgets, infrastructure upkeep, and climate challenges under strict public scrutiny.")

st.sidebar.header("📊 City Finances & Stats")
st.sidebar.metric("💰 Budget", f"${st.session_state.budget:,.0f}")
st.sidebar.metric("🏷️ Credit Rating", st.session_state.credit_rating)
st.sidebar.metric("💧 Water Reserves", f"{st.session_state.water_supply} Units")

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

st.subheader("📢 City Hall Announcements")
st.info(st.session_state.event_log[-1])

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
st.subheader("🗺️ City Zoning Grid (3x3)")
cols = st.columns(3)

ASSETS = {
    "🌳 Urban Park": {
        "cost": 2_500_000, "water_cost": 400, "upkeep_cost": 450_000, "upkeep_water":100, 
        "heat_mod": 0.6, "solar_mod": 0, "income": 0,
        "env_mod": 5, "biz_mod": -2, "res_mod": 3,
        "desc_cost": "Cost: $2.5M | Water: 400 Units",
        "desc_upkeep": "Upkeep: $450K/yr | Water Use: 100/yr",
        "desc_effect": "Effect: -0.6°C Heat | +5 Env, -2 Biz, +3 Res Approval"
        },
    "☀️ Solar Array": {
        "cost": 5_000_000, "water_cost": 0, "upkeep_cost": 200_000, "upkeep_water": 0,
        "heat_mod": 0.0, "solar_mod": 1200, "income": 600_000,
        "env_mod": 4, "biz_mod": -2, "res_mod": 2,
        "desc_cost": "Cost: $5.0M | Water: 0 Units",
        "desc_upkeep": "Upkeep: $800K/yr | Clean Energy: 1,200 kWh/yr",
        "desc_effect": "Effect: +600K/yr Income | +4 Env, -2 Biz, +2 Res Approval"
        },
    "💧 Eco Reservoir": {
        "cost": 7_500_000, "water_cost": 0, "upkeep_cost": 800_000, "upkeep_water":-1_500, 
        "heat_mod": 0.2, "solar_mod":0, "income": 0,
        "env_mod": 2, "biz_mod": -1, "res_mod": 6,
        "desc_cost": "Cost: $7.5M | Water: 0 Units",
        "desc_upkeep": "Upkeep: $800K/yr | Yields Water",
        "desc_effect": "Effect: +1,500 Water/yr | +2 Env, -1 Biz, +6 Res Approval"
        },
    "🏭 Industrial Factory": {
        "cost": 4_000_000, "water_cost": 600, "upkeep_cost": 500_000, "upkeep_water": 400, 
        "heat_mod": -0.8, "solar_mod": 0, "income": 3_200_000,
        "env_mod": -8, "biz_mod": 7, "res_mod": -4,
        "desc_cost": "Cost: $4.0M | Water: 600 Units",
        "desc_upkeep": "Upkeep: $500K/yr | Water Use: 400/yr",
        "desc_effect": "Effect: +$3.2M/yr Income, +0.8°C Heat | -8 Env, +7 Biz, -4 Res Approval"
        },
    "🏢 Commercial Block": {
        "cost": 6_000_000, "water_cost": 800, "upkeep_cost": 700_000, "upkeep_water": 300,
        "heat_mod": -0.4, "solar_mod": 0, "income": 2_100_000,
        "env_mod": -4, "biz_mod": 5, "res_mod": -2,
        "desc_cost": "Cost: $6.0M | Water: 800 Units",
        "desc_upkeep": "Upkeep: $700K/yr | Water Use: 300/yr",
        "desc_effect": "Effect: +2.1M/yr Income, +0.4°C Heat | -4 Env, +5 Biz, -2 Res Approval"
        }
}

for idx, tile_id in enumerate(st.session_state.grid.keys()):
    col = cols[idx % 3]
    with col:
        tile = st.session_state.grid[tile_id]
        st.markdown(f"**Plot {tile_id}**")
        st.caption(f"Status: {tile['type']}")

        if tile["type"] == "Empty Plot":
            chosen_asset = st.selectbox(f"Build on {tile_id}", list(ASSETS.keys()), key = f"select_{tile_id}")

            asset_data = ASSETS[chosen_asset]
            st.caption(f"🔹 {asset_data['desc_cost']}")
            st.caption(f"🔸 {asset_data['desc_upkeep']}")
            st.caption(f"⚡ {asset_data['desc_effect']}")

            if st.button(f"Construct (Plot {tile_id})", key = f"build_{tile_id}"):
                data = ASSETS[chosen_asset]
                if st.session_state.budget >= data["cost"] and st.session_state.water_supply >= data["water_cost"]:
                    st.session_state.budget -= data["cost"]
                    st.session_state.water_supply -= data["water_cost"]
                    st.session_state.temp_reduction += data["heat_mod"]
                    st.session_state.solar_kwh += data["solar_mod"]
                    st.session_state.grid[tile_id] = {
                        "type": chosen_asset,
                        "upkeep_cost": data["upkeep_cost"],
                        "upkeep_water": data["upkeep_water"]
                    }
                    st.rerun()
                else:
                    st.error("Insufficient resources!")
        elif st.button(f"Demolish Plot {tile_id} ($1M)", key = f"clear_{tile_id}"):
            if st.session_state.budget >= 1_000_000:
                st.session_state.budget -= 1_000_000
                current_type = tile["type"]
                if "Park" in current_type:
                    st.session_state.temp_reduction = max(0.0, st.session_state.temp_reduction - 0.6)
                elif "Solar" in current_type:
                    st.session_state.solar_kwh = max(0, st.session_state.solar_kwh - 1200)
                elif "Industrial" in current_type:
                    st.session_state.temp_reduction = min(4.0, st.session_state.temp_reduction + 0.8)
                elif "Commercial" in current_type:
                    st.session_state.temp_reduction = min(4.0, st.session_state.temp_reduction + 0.4)
                st.session_state.grid[tile_id] = {"type": "Empty Plot", "upkeep_cost": 0, "upkeep_water": 0}
                st.rerun()
            else:
                st.error("Insufficient budget for demolition!")

st.markdown("---")

if st.session_state.game_over:
    st.error("🚨 **Game Over!** Public approval hit 0 or debt became unmanageable. Review your strategy and try again.")
    if st.button("🔄 Restart Simulation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
elif st.session_state.victory:
    st.success("🏆 **Victory!** Your leadership stood the test for over 10 years!")
    if st.button("🔄 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
elif st.button("⏩ Advance to Next Year"):
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

