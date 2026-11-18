import pandas as pd
import streamlit as st
from dashboard.components.metrics import render_kpi_cards
from dashboard.components.charts import plot_stat_scatter, plot_category_distribution
from dashboard.components.inspector import render_character_inspector
from dashboard.components.statistics import render_statistical_tab
from dashboard.components.pygwalker_view import render_pygwalker_tab

def render_umamusu_view(raw_df: pd.DataFrame) -> None:
    """Render the Uma Musume Pretty Derby roster dashboard."""
    st.header("🐎 Uma Musume: Pretty Derby — Character Roster")

    if raw_df.empty:
        st.warning("No Uma Musume cleaned data found. Please run `python driver.py sync umamusu`.")
        return

    # Sidebar Filter Controls
    st.sidebar.markdown("### 🔍 Filter Uma Musume")
    search_query = st.sidebar.text_input("Search Name / Version / VA", placeholder="e.g. Special Week, Teio")

    all_rarities = sorted(raw_df["rarity"].dropna().unique(), reverse=True)
    selected_rarity = st.sidebar.multiselect("Rarity", options=all_rarities, default=all_rarities)

    all_turf = sorted(raw_df["turf_aptitude"].dropna().unique()) if "turf_aptitude" in raw_df.columns else []
    selected_turf = st.sidebar.multiselect("Turf Aptitude", options=all_turf, default=all_turf)

    all_dirt = sorted(raw_df["dirt_aptitude"].dropna().unique()) if "dirt_aptitude" in raw_df.columns else []
    selected_dirt = st.sidebar.multiselect("Dirt Aptitude", options=all_dirt, default=all_dirt)

    # Apply Filters
    df = raw_df.copy()
    if "item_data.version" in df.columns:
        df["display_name"] = df.apply(
            lambda r: f"{r['name']} ({r['item_data.version']})"
            if pd.notna(r.get("item_data.version")) and str(r.get("item_data.version")).strip() not in ("", "None")
            else r["name"],
            axis=1,
        )
    else:
        df["display_name"] = df["name"]

    if search_query:
        mask = (
            df["display_name"].str.contains(search_query, case=False, na=False) |
            df["item_data.title"].astype(str).str.contains(search_query, case=False, na=False) |
            df["char_data.va_en"].astype(str).str.contains(search_query, case=False, na=False)
        )
        df = df[mask]
    if selected_rarity:
        df = df[df["rarity"].isin(selected_rarity)]
    if selected_turf and "turf_aptitude" in df.columns:
        df = df[df["turf_aptitude"].isin(selected_turf)]
    if selected_dirt and "dirt_aptitude" in df.columns:
        df = df[df["dirt_aptitude"].isin(selected_dirt)]

    # 1. KPI Metric Cards
    render_kpi_cards(df, total_label="Filtered Uma Musume", rarity_col="rarity", atk_col="base_speed", hp_col="base_stamina")

    # Tabs for Data View vs Visual Analytics vs Statistics vs PyGWalker vs Inspector
    tab_data, tab_charts, tab_stats, tab_pyg, tab_inspector = st.tabs([
        "📋 Data Table", "📊 Visual Analytics", "📈 Statistical Lab", "🎨 PyGWalker Studio", "🔍 Uma Musume Inspector"
    ])

    with tab_data:
        st.caption(f"Showing **{len(df)}** of **{len(raw_df)}** characters.")
        display_cols = [
            "id", "name", "rarity", "item_data.version", "item_data.title",
            "base_speed", "base_stamina", "base_power", "base_guts", "base_wit",
            "turf_aptitude", "dirt_aptitude", "sprint_aptitude", "mile_aptitude",
            "medium_aptitude", "long_aptitude", "char_data.height", "char_data.va_en"
        ]
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, height=450)

        # Download CSV
        csv_data = df[available_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_data,
            file_name="umamusu_filtered_characters.csv",
            mime="text/csv",
        )

    with tab_charts:
        st.markdown("#### Base Stats & Aptitudes")
        c1, c2 = st.columns([3, 2])
        with c1:
            plot_stat_scatter(
                df,
                x_col="base_speed",
                y_col="base_stamina",
                color_col="rarity",
                title="Base Speed vs Base Stamina",
                hover_name="display_name",
                hover_data=["item_data.title", "item_data.version", "base_power", "base_guts", "base_wit"],
            )
        with c2:
            plot_category_distribution(df, col="rarity", title="Rarity Breakdown")

        c3, c4 = st.columns(2)
        with c3:
            plot_category_distribution(df, col="turf_aptitude", title="Turf Aptitude Grades")
        with c4:
            plot_category_distribution(df, col="dirt_aptitude", title="Dirt Aptitude Grades")

    with tab_stats:
        render_statistical_tab(df, game="umamusu", name_col="display_name")

    with tab_pyg:
        render_pygwalker_tab(df, game="umamusu")

    with tab_inspector:
        render_character_inspector(df, game="umamusu", name_col="display_name")
