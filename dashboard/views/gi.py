import pandas as pd
import streamlit as st
from dashboard.components.metrics import render_kpi_cards
from dashboard.components.charts import plot_stat_scatter, plot_category_distribution
from dashboard.components.inspector import render_character_inspector
from dashboard.components.statistics import render_statistical_tab

def render_gi_view(raw_df: pd.DataFrame) -> None:
    """Render the Genshin Impact character roster dashboard."""
    st.header("✨ Genshin Impact — Character Roster")

    if raw_df.empty:
        st.warning("No Genshin Impact cleaned data found. Please run `python driver.py sync gi`.")
        return

    # Sidebar Filter Controls
    st.sidebar.markdown("### 🔍 Filter Genshin Characters")
    search_query = st.sidebar.text_input("Search Character Name", placeholder="e.g. Raiden, Hu Tao")

    all_rarities = sorted(raw_df["rarity"].dropna().unique(), reverse=True)
    selected_rarity = st.sidebar.multiselect("Rarity", options=all_rarities, default=all_rarities)

    all_elements = sorted(raw_df["element"].dropna().unique())
    selected_elements = st.sidebar.multiselect("Element", options=all_elements, default=all_elements)

    all_weapons = sorted(raw_df["weapon_type"].dropna().unique())
    selected_weapons = st.sidebar.multiselect("Weapon Type", options=all_weapons, default=all_weapons)

    all_regions = sorted(raw_df["region"].dropna().unique())
    selected_regions = st.sidebar.multiselect("Region", options=all_regions, default=all_regions)

    # Apply Filters
    df = raw_df.copy()
    df["display_name"] = df.apply(
        lambda r: f"{r['name']} ({r['element']})"
        if str(r.get("name")).strip() == "Traveler" and pd.notna(r.get("element"))
        else r["name"],
        axis=1,
    )

    if search_query:
        df = df[df["display_name"].str.contains(search_query, case=False, na=False)]
    if selected_rarity:
        df = df[df["rarity"].isin(selected_rarity)]
    if selected_elements:
        df = df[df["element"].isin(selected_elements)]
    if selected_weapons:
        df = df[df["weapon_type"].isin(selected_weapons)]
    if selected_regions:
        df = df[df["region"].isin(selected_regions)]

    # 1. KPI Metric Cards
    render_kpi_cards(df, total_label="Filtered Characters", rarity_col="rarity", atk_col="atkMax", hp_col="hpMax")

    # Tabs for Data View vs Visual Analytics vs Statistics vs Inspector
    tab_data, tab_charts, tab_stats, tab_inspector = st.tabs([
        "📋 Data Table", "📊 Visual Analytics", "📈 Statistical Lab", "🔍 Character Inspector"
    ])

    with tab_data:
        st.caption(f"Showing **{len(df)}** of **{len(raw_df)}** characters.")
        display_cols = [
            "id", "name", "rarity", "element", "weapon_type", "region",
            "hpMax", "atkMax", "defMax", "special_stat", "ultimate_cost",
            "birthday", "jp_va", "release"
        ]
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, height=450)

        # Download CSV
        csv_data = df[available_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_data,
            file_name="gi_filtered_characters.csv",
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
                color_col="element",
                title="Max ATK vs Max HP (Lv 90)",
                hover_name="display_name",
                hover_data=["weapon_type", "region", "rarity", "special_stat"],
            )
        with c2:
            plot_category_distribution(df, col="element", title="Element Distribution")

        c3, c4 = st.columns(2)
        with c3:
            plot_category_distribution(df, col="weapon_type", title="Weapon Type Breakdown")
        with c4:
            plot_category_distribution(df, col="region", title="Region Breakdown")

    with tab_stats:
        render_statistical_tab(df, game="gi", name_col="display_name")

    with tab_inspector:
        render_character_inspector(df, game="gi", name_col="display_name")
