import streamlit as st

DISTRICTS = {
    "None": {
        "desc": "Standard zoning",
        "cost": 0,
        "income_mult": 1.0,
        "env_mult": 1.0,
        "upkeep_mult": 1.0
    },
    "💻 Tech Hub": {
        "desc": "Attracts big tech corporations. Boosts commercial/industrial"
        "income by 25%, but inreases energy drain.",
        "cost": 5_000_000,
        "income_mult": 1.25,
        "env_mult": 0.9,
        "upkeep_mult": 1.15
    },
    "🌿 National Park": {
        "desc": "Natural beauty preservation. Raises env. and res. approval gains by 30%, but reduces industrial income",
        "cost": 4_000_000,
        "income_mult": 0.8,
        "env_mult": 1.30,
        "upkeep_mult": 1.0
    },
    "⚙️ Heavy Industry": {
        "desc": "Maximizes manufacturing. Doubles factory revenue, but accelerates heat buildup and angers environmentalists",
        "cost": 6_000_000,
        "income_mult": 1.5,
        "env_mult": 0.6,
        "upkeep_mult": 1.2
    }
}

def render_districts():
    st.markdown("### 🏛️ City Special Districts")
    st.markdown("Assign districts across your city to unlock benefits to your zoning choices")

    if "active_district" not in st.session_state:
        st.session_state.active_district = "None"

    current_district = st.session_state.active_district

    col_1, col_2 = st.columns([2, 1])

    with col_1:
        chosen_district = st.selectbox(
            "Select City District Designation",
            list(DISTRICTS.keys()),
            index = list(DISTRICTS.keys().index(current_district))
        )
        d_data = DISTRICTS[chosen_district]
        st.info(f"**Description:** {d_data['desc']}")
        st.caption(
            f"🔹 Designation Cost: ${d_data['cost']:,.0f} | 📈 Income Multiplier: {d_data['income_mult']}x | 🌡️ Environmental Multiplier: {d_data['env_mult']}x"
            )

    with col_2:
        st.write("")
        st.write("")
        if chosen_district != current_district:
            if st.button("⚖️ Enact District Policy", use_container_width = True):
                if st.session_state.budget >= d_data["cost"]:
                    st.session_state.budget -= d_data["cost"]
                    st.session_state.active_district = chosen_district
                    st.success(f"Successfully enacted in {chosen_district}!")
                    st.rerun()
                else:
                    st.error("Insufficient budget to create district.")
            else:
                st.success("✅ Active District")