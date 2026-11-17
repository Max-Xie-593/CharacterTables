import pandas as pd
import streamlit as st
from dashboard.data_loader import extract_unique_tokens
from dashboard.components.metrics import render_kpi_cards
from dashboard.components.charts import plot_stat_scatter, plot_category_distribution, plot_token_frequency
from dashboard.components.inspector import render_character_inspector
from dashboard.components.statistics import render_statistical_tab

def render_fgo_view(raw_df: pd.DataFrame) -> None:
    """Render the Fate/Grand Order servant roster dashboard."""
    st.header("⚔️ Fate/Grand Order — Servant Roster")

    if raw_df.empty:
        st.warning("No Fate/Grand Order cleaned data found. Please run `python driver.py sync fgo`.")
        return

    # Sidebar Filter Controls
    st.sidebar.markdown("### 🔍 Filter FGO Servants")
    search_query = st.sidebar.text_input("Search Servant / CV / Illustrator", placeholder="e.g. Artoria, Takeuchi, Rie")

    all_rarities = sorted(raw_df["rarity"].dropna().unique(), reverse=True)
    selected_rarity = st.sidebar.multiselect("Rarity", options=all_rarities, default=all_rarities)

    all_classes = sorted(raw_df["className"].dropna().unique()) if "className" in raw_df.columns else []
    selected_classes = st.sidebar.multiselect("Class", options=all_classes, default=all_classes)

    all_attributes = sorted(raw_df["attribute"].dropna().unique()) if "attribute" in raw_df.columns else []
    selected_attributes = st.sidebar.multiselect("Attribute", options=all_attributes, default=all_attributes)

    # Tokenized multi-select filters for comma-delimited columns
    all_traits = extract_unique_tokens(raw_df["traits"]) if "traits" in raw_df.columns else []
    selected_traits = st.sidebar.multiselect("Filter by Traits", options=all_traits, help="Matches servants possessing ANY of the selected traits")

    all_skill_tags = extract_unique_tokens(raw_df["skillTags"]) if "skillTags" in raw_df.columns else []
    selected_skill_tags = st.sidebar.multiselect("Filter by Skill Tags", options=all_skill_tags, help="Matches servants possessing ANY of the selected skill tags")

    # Apply Filters
    df = raw_df.copy()
    if "className" in df.columns:
        df["display_name"] = df.apply(
            lambda r: f"{r['name']} ({r['className']})" if pd.notna(r.get("className")) else r["name"],
            axis=1,
        )
    else:
        df["display_name"] = df["name"]

    if search_query:
        mask = (
            df["display_name"].str.contains(search_query, case=False, na=False) |
            df["profile.cv"].str.contains(search_query, case=False, na=False) |
            df["profile.illustrator"].str.contains(search_query, case=False, na=False)
        )
        df = df[mask]
    if selected_rarity:
        df = df[df["rarity"].isin(selected_rarity)]
    if selected_classes and "className" in df.columns:
        df = df[df["className"].isin(selected_classes)]
    if selected_attributes and "attribute" in df.columns:
        df = df[df["attribute"].isin(selected_attributes)]
    if selected_traits and "traits" in df.columns:
        df = df[df["traits"].apply(lambda s: isinstance(s, str) and any(t in s for t in selected_traits))]
    if selected_skill_tags and "skillTags" in df.columns:
        df = df[df["skillTags"].apply(lambda s: isinstance(s, str) and any(t in s for t in selected_skill_tags))]

    # 1. KPI Metric Cards
    render_kpi_cards(df, total_label="Filtered Servants", rarity_col="rarity", atk_col="atkMax", hp_col="hpMax")

    # Tabs for Data View vs Visual Analytics vs Statistics vs Inspector
    tab_data, tab_charts, tab_stats, tab_inspector = st.tabs([
        "📋 Data Table", "📊 Visual Analytics", "📈 Statistical Lab", "🔍 Servant Inspector"
    ])

    with tab_data:
        st.caption(f"Showing **{len(df)}** of **{len(raw_df)}** servants.")
        display_cols = [
            "collectionNo", "name", "className", "rarity", "attribute", "cost", "lvMax",
            "atkMax", "hpMax", "cardDeck", "npCards", "rank", "type", "targetType",
            "profile.cv", "profile.illustrator"
        ]
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, height=450)

        # Download CSV
        csv_data = df[available_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_data,
            file_name="fgo_filtered_servants.csv",
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
                color_col="className",
                title="Max ATK vs Max HP",
                hover_name="display_name",
                hover_data=["rarity", "cardDeck", "npCards", "targetType"],
            )
        with c2:
            plot_category_distribution(df, col="className", title="Class Distribution")

        c3, c4 = st.columns(2)
        with c3:
            plot_token_frequency(df, col="traits", title="Top 15 Most Common Traits", top_n=15)
        with c4:
            plot_token_frequency(df, col="skillTags", title="Top 15 Most Common Skill Tags", top_n=15)

    with tab_stats:
        render_statistical_tab(df, game="fgo", name_col="display_name")

    with tab_inspector:
        render_character_inspector(df, game="fgo", name_col="display_name")
