import pandas as pd
import streamlit as st
from dashboard.components.metrics import render_kpi_cards
from dashboard.components.charts import plot_stat_scatter, plot_category_distribution
from dashboard.components.inspector import render_character_inspector
from dashboard.components.statistics import render_statistical_tab

def render_zzz_view(raw_df: pd.DataFrame) -> None:
    """Render the Zenless Zone Zero agent roster dashboard."""
    st.header("⚡ Zenless Zone Zero — Agent Roster")

    if raw_df.empty:
        st.warning("No Zenless Zone Zero cleaned data found. Please run `python driver.py sync zzz`.")
        return

    # Sidebar Filter Controls
    st.sidebar.markdown("### 🔍 Filter ZZZ Agents")
    search_query = st.sidebar.text_input("Search Agent Name", placeholder="e.g. Ellen, Zhu Yuan")

    all_rarities = sorted(raw_df["rarity"].dropna().unique(), reverse=True)
    selected_rarity = st.sidebar.multiselect("Rarity", options=all_rarities, default=all_rarities)

    all_elements = sorted(raw_df["element.name"].dropna().unique()) if "element.name" in raw_df.columns else []
    selected_elements = st.sidebar.multiselect("Element", options=all_elements, default=all_elements)

    all_specialties = sorted(raw_df["specialty.name"].dropna().unique()) if "specialty.name" in raw_df.columns else []
    selected_specialties = st.sidebar.multiselect("Specialty", options=all_specialties, default=all_specialties)

    all_factions = sorted(raw_df["faction.name"].dropna().unique()) if "faction.name" in raw_df.columns else []
    selected_factions = st.sidebar.multiselect("Faction", options=all_factions, default=all_factions)

    # Apply Filters
    df = raw_df.copy()
    if search_query:
        df = df[df["name"].str.contains(search_query, case=False, na=False)]
    if selected_rarity:
        df = df[df["rarity"].isin(selected_rarity)]
    if selected_elements and "element.name" in df.columns:
        df = df[df["element.name"].isin(selected_elements)]
    if selected_specialties and "specialty.name" in df.columns:
        df = df[df["specialty.name"].isin(selected_specialties)]
    if selected_factions and "faction.name" in df.columns:
        df = df[df["faction.name"].isin(selected_factions)]

    # 1. KPI Metric Cards
    render_kpi_cards(df, total_label="Filtered Agents", rarity_col="rarity", atk_col="atkMax", hp_col="hpMax")

    # Tabs for Data View vs Visual Analytics vs Statistics vs Inspector
    tab_data, tab_charts, tab_stats, tab_inspector = st.tabs([
        "📋 Data Table", "📊 Visual Analytics", "📈 Statistical Lab", "🔍 Agent Inspector"
    ])

    with tab_data:
        st.caption(f"Showing **{len(df)}** of **{len(raw_df)}** agents.")
        display_cols = [
            "id", "name", "code_name", "rarity", "element.name", "specialty.name",
            "attack_type.name", "faction.name", "atkMax", "hpMax", "defMax",
            "assist_type", "ascension_stat_1", "info.birthday"
        ]
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, height=450)

        # Download CSV
        csv_data = df[available_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_data,
            file_name="zzz_filtered_agents.csv",
            mime="text/csv",
        )

    with tab_charts:
        st.markdown("#### Combat Stats & Distribution")
        c1, c2 = st.columns([3, 2])
        with c1:
            plot_stat_scatter(
                df,
                x_col="atkMax",
                y_col="hpMax",
                color_col="specialty.name",
                title="Max ATK vs Max HP (Lv 60)",
                hover_data=["element.name", "faction.name", "rarity", "assist_type"],
            )
        with c2:
            plot_category_distribution(df, col="specialty.name", title="Specialty Distribution")

        c3, c4 = st.columns(2)
        with c3:
            plot_category_distribution(df, col="element.name", title="Element Distribution")
        with c4:
            plot_category_distribution(df, col="faction.name", title="Faction Breakdown")

    with tab_stats:
        render_statistical_tab(df, game="zzz")

    with tab_inspector:
        render_character_inspector(df, game="zzz")
