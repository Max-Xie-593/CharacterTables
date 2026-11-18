import pandas as pd
import pygwalker as pyg
from pygwalker.services.global_var import GlobalVarManager
import streamlit as st
import streamlit.components.v1 as components

# Disable telemetry and online update checks
GlobalVarManager.set_privacy("offline")

@st.cache_data(show_spinner=False)
def _generate_pygwalker_html(df: pd.DataFrame, theme: str = "dark") -> str:
    """Generate and cache the standalone Graphic Walker HTML bundle."""
    return pyg.to_html(df, theme_key=theme)

def render_pygwalker_tab(df: pd.DataFrame, game: str) -> None:
    """Render the Graphic Walker / PyGWalker drag-and-drop exploration canvas."""
    st.markdown("### 🎨 PyGWalker Visual Exploration Studio")
    st.caption(
        "A Tableau-like drag-and-drop visual exploration canvas. "
        "Drag dimensions and measures onto Rows, Columns, or Color channels to build custom charts on the fly."
    )

    if df.empty:
        st.warning("No data available to explore in PyGWalker.")
        return

    # Clean non-serializable or problematic columns for Graphic Walker
    explore_df = df.copy()
    # Strip nested or extremely long raw text to keep canvas snappy
    drop_candidates = [
        c for c in explore_df.columns
        if c.startswith("profile.comments") or c.startswith("char_data.skills")
    ]
    if drop_candidates:
        explore_df = explore_df.drop(columns=drop_candidates, errors="ignore")

    ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 3])
    with ctrl1:
        theme = st.selectbox(
            "Canvas Theme:",
            options=["dark", "light"],
            index=0,
            key=f"{game}_pyg_theme",
        )
    with ctrl2:
        canvas_height = st.slider(
            "Canvas Height (px):",
            min_value=600,
            max_value=1400,
            value=950,
            step=50,
            key=f"{game}_pyg_height",
        )
    with ctrl3:
        st.info(f"Loaded **{len(explore_df)}** records and **{len(explore_df.columns)}** fields.")

    with st.spinner("Preparing PyGWalker Studio..."):
        try:
            html_bundle = _generate_pygwalker_html(explore_df, theme=theme)
            components.html(html_bundle, height=canvas_height, scrolling=True)
        except Exception as e:
            st.error(f"Failed to render PyGWalker canvas: {e}")
