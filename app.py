import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title = "EcoSim, a Climate Simulation Game", page_icon = "🌱", layout = "wide")

if "initialized" not in st.session_state:
    st.session_state.budget = 8000
    st.session_state.water_supply = 800
    st.session_state.temp_reduction = 0.0
    st.session_state.solar_kwh = 0
    st.session_state.turn = 0
    st.session_state.approval = 70
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.event_log = ["Simulation started! Manage your neighborhood budget and heat."]
    st.session_state.history = [{"Year": 2026, "Budget": 8000, "Water": 800, "Approval": 70, "Heat Reduction": 0.0}]
    st.session_state.grid = {i: {"type": "Empty Plot", "upkeep_cost": 0, "upkeep_water": 0} for i in range (1, 10)}
    st.session_state.initialized = True

st.title("🌱 EcoSim, a Climate Management Simulation")
st.markdown("Zone land, balance costs, and protect your city from urban climate challenges!")

st.sidebar.header("📊 City Metrics")
st.sidebar.metric("💰 Budget", f"${st.session_state.budget:,.2f}")
st.sidebar.metric("💧 Water Supply", f"{st.session_state.water_supply} Units")
st.sidebar.metric("😊 Public Approval", f"{st.session_state.approval}%")

st.sidebar.markdown("---")
st.sidebar.header("🌍 Environmental Data")
st.sidebar.metric("🌡️ Heat Island Reduction", f"{st.session_state.temp_reduction:.1f} °C")
st.sidebar.metric("⚡ Solar Energy Generated", f"{st.session_state.solar_kwh} kWh")
st.sidebar.markdown(f"**Current Year:** {2026 + st.session_state.turn}")

st.subheader("📢 Annual Event Log")
st.info(st.session_state.event_log[-1])

st.subheader("🗺️ Neighborhood Zoning Grid (3x3)")
cols = st.columns(3)

ASSETS = {
    "🌳 Urban Park": {"cost": 800, "water_cost": 80, "upkeep_cost": 100, "upkeep_water":30, "heat_mod": 0.5, "solar_mod": 0},
    "☀️ Solar Array": {"cost": 1800, "water_cost": 0, "upkeep_cost": 50, "upkeep_water": 0, "heat_mod": 0, "solar_mod": 400},
    "💧 Eco Reservoir": {"cost": 2200, "water_cost": 0, "upkeep_cost": 150, "upkeep_water":-200, "heat_mod": 0.1, "solar_mod":0}
}

for idx, tile_id in enumerate(st.session_state.grid.keys()):
    col = cols[idx % 3]
    with col:
        tile = st.session_state.grid[tile_id]
        st.markdown(f"**Plot {tile_id}**")
        st.caption(f"Status: {tile['type']}")

        if tile["type"] == "Empty Plot":
            selected_build = st.selectbox(f"Build on {tile_id}", list(ASSETS.keys()))
            if st.button(f"Construct (Plot {tile_id})", key = f"build_{tile_id}"):
                data = ASSETS[selected_build]
                if st.session_state.budget >= data["cost"] and st.session_state.water_supply >= data["water_cost"]:
                    st.session_state.budget -= data["cost"]
                    st.session_state.water_supply -= data["water_cost"]
                    st.session_state.temp_reduction += data["heat_mod"]
                    st.session_state.solar_kwh += data["solar_mod"]
                    st.session_state.grid[tile_id] = {
                        "type": selected_build,
                        "upkeep_cost": data["upkeep_cost"],
                        "upkeep_water": data["upkeep_water"]
                    }
                    st.rerun()
                else:
                    st.error("Insufficient resources!")
        elif st.button(f"Clear Plot {tile_id} ($300)", key = f"clear_{tile_id}"):
            if st.session_state.budget >= 200:
                st.session_state.budget -= 200
                current_type = tile["type"]
                if "Park" in current_type:
                    st.session_state.temp_reduction = max(0.0, st.session_state.temp_reduction - 0.5)
                elif "Solar" in current_type:
                    st.session_state.solar_kwh = max(0, st.session_state.solar_kwh - 400)
                st.session_state.grid[tile_id] = {"type": "Empty Plot", "upkeep_cost": 0, "upkeep_water": 0}
                st.rerun()
            else:
                st.error("Insufficient budget to clear plot!")

st.markdown("---")

if st.session_state.game_over:
    st.error("🚨 **Game Over!** Public approval hit 0% or bankruptcy ruined the city. Review your strategy and try again.")
    if st.button("🔄 Restart Simulation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
elif st.session_state.victory:
    st.success("🏆 **Victory!** You successfully managed your city's climate and public approval for 10 years!")
    if st.button("🔄 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    if st.button("⏩ Advance to Next Year"):
        st.session_state.turn += 1

        total_upkeep_cost = sum(t["upkeep_cost"] for t in st.session_state.grid.values())
        total_upkeep_water = sum(t["upkeep_water"] for t in st.session_state.grid.values())

        yearly_income = 1500 + (st.session_state.solar_kwh * 0.4)
        yearly_water_gain = 250

        st.session_state.budget += (yearly_income - total_upkeep_cost)
        st.session_state.water_supply += (yearly_water_gain - total_upkeep_water)

        event_roll = random.choice([
            ("normal", "Normal weather conditions throughout the year."),
            ("drought", "Severe Drought! Water supplies drained heavily."),
            ("subsidy", "Green Grant Received! +$800 bonus."),
            ("heatwave", "Intense Heatwave! Citizens are angry about rising temps (-15% approval)."),
        ])

        event_type, event_desc = event_roll
        if event_type == "drought":
            st.session_state.water_supply -= 200
            st.session_state.approval -= 5
        elif event_type == "subsidy":
            st.session_state.budget += 800
        elif event_type == "heatwave":
            st.session_state.approval -= 15

        st.session_state.event_log.append(f"Year {st.session_state.turn}: {event_desc}")

        if st.session_state.budget < 0:
            st.session_state.approval -= 20
        if st.session_state.water_supply < 0:
            st.session_state.approval -= 15
        if st.session_state.temp_reduction < 1.0:
            st.session_state.approval -= 10

        st.session_state.approval = max(0, min(100, st.session_state.approval))

        if st.session_state.approval <= 0 or st.session_state.budget < -2000:
            st.session_state.game_over = True
        elif st.session_state.turn >= 10:
            st.session_state.victory = True

        st.session_state.history.append({
            "Year": 2026 + st.session_state.turn,
            "Budget": st.session_state.budget,
            "Water": st.session_state.water_supply,
            "Approval": st.session_state.approval,
            "Heat Reduction": st.session_state.temp_reduction
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

