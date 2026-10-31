import streamlit as st

st.set_page_config(page_title = "EcoSim, a Climate Simulation Game", page_icon = "🌱", layout = "wide")

if "initialized" not in st.session_state:
    st.session_state.budget = 10000
    st.session_state.water_supply = 1000
    st.session_state.temp_reduction = 0
    st.session_state.solar_kwh = 0
    st.session_state.trees_planted = 0
    st.session_state.solar_panels = 0
    st.session_state.turn = 1
    st.session_state.grid = {i: "Empty Plot" for i in range (1, 10)}
    st.session_state.initialized = True

st.title("🌱 EcoSim, Climate Management MVP")
st.markdown("Manage neighborhood resources, fight urban heat, and balance the budget before resources run out!")

st.sidebar.header("📊 Neighborhood Status")
st.sidebar.metric("💰 Budget", f"${st.session_state.budget:,.2f}")
st.sidebar.metric("💧 Water Supply", f"{st.session_state.water_supply} Units")

st.sidebar.markdown("---")
st.sidebar.header("🌍 Climate Impact")
st.sidebar.metric("🌡️ Heat Island Reduction", f"{st.session_state.temp_reduction:.1f} °C")
st.sidebar.metric("⚡ Solar Energy Generated", f"{st.session_state.solar_kwh} kWh")

col1, col2 = st.columns(2)
st.subheader("🗺️ Neighborhood Zoning Grid (3x3)")
cols = st.columns(3)

for idx, tile_id in enumerate(st.session_state.grid.keys()):
    col = cols[idx % 3]
    with col:
        current_status = st.session_state.grid[tile_id]
        st.markdown(f"**Plot {tile_id}")
        st.info(current_status)

        if current_status == "Empty Plot":
            if st.button(f"Plant Trees (Plot {tile_id})", key = f"tree_{tile_id}"):
                if st.session_state.budget >= 500 and st.session_state.water_supply >= 50:
                    st.session_state.budget -= 500
                    st.session_state.water_supply -= 50
                    st.session_state.temp_reduction += 0.3
                    st.session_state.grid[tile_id] = "🌳 Tree Canopy"
                    st.rerun()
                else:
                    st.error("Check your budget and water!")

            if st.button(f"Install Solar (Plot {tile_id})", key = f"solar_{tile_id}"):
                if st.session_state.budget >= 1200:
                    st.session_state.budget -= 1200
                    st.session_state.solar_kwh += 450
                    st.session_state.grid[tile_id] = "☀️ Solar Roof"
                    st.rerun()
                else:
                    st.error("Check your budget!")

st.markdown("---")

if st.button(" Advance Simulation Turn (Next Year)"):
    st.session_state.turn += 1
    st.session_state.budget += 1500
    st.session_state.water_supply += 200
    st.info(f"Advanced to Year {st.session_state.turn}. Received $1,500 municipal grant and seasonal water replenishment.")
    st.rerun()

