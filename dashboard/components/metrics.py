import pandas as pd
import streamlit as st

def render_kpi_cards(
    df: pd.DataFrame,
    total_label: str = "Total Characters",
    rarity_col: str = "rarity",
    atk_col: str | None = None,
    hp_col: str | None = None,
) -> None:
    """Render top KPI metric cards for the active dataframe.

    Args:
        df (pd.DataFrame): Current filtered dataframe.
        total_label (str): Label for the total count card.
        rarity_col (str): Column name containing rarity values.
        atk_col (str | None): Optional column name for ATK stat.
        hp_col (str | None): Optional column name for HP stat.
    """
    cols = st.columns(4)

    # 1. Total Characters
    with cols[0]:
        st.metric(label=total_label, value=f"{len(df):,}")

    # 2. Rarity Distribution
    with cols[1]:
        if rarity_col in df.columns and not df.empty:
            rarity_counts = df[rarity_col].value_counts().to_dict()
            rarity_summary = " | ".join(
                f"{r}★: {count}" if str(r).isdigit() else f"{r}: {count}"
                for r, count in sorted(rarity_counts.items(), key=lambda x: str(x[0]), reverse=True)[:3]
            )
            st.metric(label="Top Rarities", value=rarity_summary or "N/A")
        else:
            st.metric(label="Top Rarities", value="N/A")

    # 3. Average Max ATK (if applicable)
    with cols[2]:
        if atk_col and atk_col in df.columns and not df.empty:
            valid_atk = pd.to_numeric(df[atk_col], errors="coerce").dropna()
            avg_atk = valid_atk.mean() if not valid_atk.empty else 0
            st.metric(label="Avg Max ATK", value=f"{avg_atk:,.0f}")
        else:
            st.metric(label="Avg Max ATK", value="N/A")

    # 4. Average Max HP (if applicable)
    with cols[3]:
        if hp_col and hp_col in df.columns and not df.empty:
            valid_hp = pd.to_numeric(df[hp_col], errors="coerce").dropna()
            avg_hp = valid_hp.mean() if not valid_hp.empty else 0
            st.metric(label="Avg Max HP", value=f"{avg_hp:,.0f}")
        else:
            st.metric(label="Avg Max HP", value="N/A")
