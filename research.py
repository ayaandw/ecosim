import streamlit as st

TREE = {
    "Grid Management AI": {
        "tier": 1,
        "cost": 3_000_000,
        "energy_req": 1000,
        "desc": "Optimizes power routing, permanently reducing grid upkeep costs by 15%",
        "unlocked": False
    },
    "Desalination Plants": {
        "tier": 1,
        "cost": 5_000_000,
        "energy_req": 2000,
        "desc": "Takes ocean water and processes it, permanently giving +1000 units per turn"
    },
    "Air Cleanup": {
        "tier": 2,
        "cost": 10_000_000,
        "energy_req": 4000,
        "desc": "Advanced carbon capture that permanently reduces heat island effect by 0.8°C.",
        "unlocked": False
    },
    "Fusion Reactor": {
        "tier": 3,
        "cost": 25_000_000,
        "energy_req": 10_000,
        "desc": "The most advanced clean energy. Solves city power needs and unlocks a victory grade boost",
        "unlocked": False
    }
}

def render_research():
    st.markdown("### 🔬 R&D Lab")
    st.markdown("💡 Invest funds and energy generation to research more advanced tech.")

    if "unlocked_tech" not in st.session_state:
        st.session_state.unlocked_tech = []

    cols = st.columns(2)

    for i, (t_name, t_data) in enumerate(TREE.items()):
        col = cols[i % 2]
        is_unlocked = t_name in st.session_state.unlocked_tech

        with col:
            with st.container(border=True):
                st.markdown(f"#### {t_name} (Tier {t_data['tier']})")
                st.write(t_data["desc"])
                st.caption(f"Cost: ${t_data['cost']:,.0f} | Required Energy: {t_data['energy_req']:,} kWh")
                if is_unlocked:
                    st.success("✅ Researched and in effect")
                else:
                    can_afford = st.session_state.budget >= t_data["cost"]
                    has_energy = st.session_state.solar_kwh >= t_data["energy_req"]

                    if st.button(f"Unlock {t_name}", key = f"tech_{i}", use_container_width = True):
                        if not can_afford:
                            st.error("❌ Insufficient budget!")
                        elif not has_energy:
                            st.error("⚡ Insufficient clean energy supply!")
                        else:
                            st.session_state.budget -= t_data["cost"]
                            st.session_state.unlocked_tech.append(t_name)
                            if t_name == "Grid Management AI":
                                pass
                            elif t_name == "Air Cleanup":
                                st.session_state.temp_reduction += 0.8
                            elif t_name == "Desalination Plants":
                                st.session_state.water += 1000
                            elif t_name == "Fusion Reactor":
                                st.session_state.solar_kwh += 5000

                            st.success(f"🎉 Research {t_name} unlocked!")
                            st.rerun()