import streamlit as st
from components import ASSETS, get_neighbors

def render_inspector():
    st.markdown("### 🔍 Grid Tile Inspector")

    if "inspected_id" not in st.session_state:
        st.session_state.inspected_id = 1

    col_select, col_details = st.columns([1, 2])

    with col_select:
        st.session_state.inspected_id = st.selectbox(
            "Inspect Plot Number",
            options = list(st.session_state.grid.keys()),
            format_func = lambda x: f"Plot {x}: {st.session_state.grid[x]['type']}"
        )
    t_id = st.session_state.inspected_id
    tile = st.session_state.grid[t_id]
    t_type = tile["type"]

    with col_details:
        with st.container(border = True):
            st.markdown(f"**Plot {t_id} Status:** `{t_type}`")

            if t_type == "Empty Plot":
                st.caption("🌱 Ready for construction in Build Mode.")
            else:
                asset_info = ASSETS.get(t_type, {})
                st.write(f"💸 **Annual Upkeep:** ${asset_info.get('upkeep_cost', 0):,.0f}/yr")
                st.write(f"💧 **Water Use:** {asset_info.get('upkeep_water', 0):,}/yr")

                neighbors = get_neighbors(t_id)
                neighbor_t = [st.session_state.grid[n]["type"] for n in neighbors]

                if "Park" in t_type and any("Commercial" in n for n in neighbor_t):
                    st.success("✨ **Active Synergy:** Adjacent to commercial area (+2 Res Approval)")
                elif "Factory" in t_type and any("Park" in n or "Resevoir" in n for n in neighbor_t):
                    st.error("⚠️ **Negative Synergy:** Adjacent to green/water plot (-3 Env Approval)")
                else:
                    st.caption("No active synergies for this plot.")
                