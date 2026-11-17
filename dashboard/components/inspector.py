from typing import Any
import pandas as pd
import streamlit as st

def render_pill_tags(text: Any, delimiter: str = ",", badge_color: str = "#2b313e") -> None:
    """Render a comma-separated string as styled inline pill badges."""
    if not isinstance(text, str) or not text.strip():
        st.write("*(None)*")
        return

    tokens = [t.strip() for t in text.split(delimiter) if t.strip() and t.strip() != "None"]
    if not tokens:
        st.write("*(None)*")
        return

    html_pills = " ".join(
        f'<span style="background-color: {badge_color}; color: #e0e0e0; padding: 3px 8px; '
        f'border-radius: 12px; margin-right: 5px; font-size: 0.85em; display: inline-block; '
        f'margin-bottom: 4px; border: 1px solid #4a5568;">{token}</span>'
        for token in tokens
    )
    st.markdown(html_pills, unsafe_allow_html=True)

def render_character_inspector(
    df: pd.DataFrame,
    game: str,
    id_col: str = "id",
    name_col: str = "name",
) -> None:
    """Render a detailed character inspector panel with attribute cards and badge pills."""
    if df.empty:
        st.info("No characters match the current filter selection.")
        return

    st.subheader("🔍 Character Inspector")
    names = df[name_col].dropna().tolist()
    selected_name = st.selectbox("Select Character to Inspect:", options=names)

    if not selected_name:
        return

    char = df[df[name_col] == selected_name].iloc[0]

    with st.container(border=True):
        header_cols = st.columns([3, 1])
        with header_cols[0]:
            rarity_display = f"{char.get('rarity', '')}★" if str(char.get('rarity', '')).isdigit() else str(char.get('rarity', ''))
            st.markdown(f"### {char[name_col]} <span style='color: #ecc94b;'>({rarity_display})</span>", unsafe_allow_html=True)
        with header_cols[1]:
            if "id" in char and pd.notna(char["id"]):
                st.caption(f"Database ID: `{char['id']}`")

        # Game-specific attribute layouts
        if game == "gi":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Element:** `{char.get('element', 'N/A')}`")
                st.markdown(f"**Weapon:** `{char.get('weapon_type', 'N/A')}`")
                st.markdown(f"**Region:** `{char.get('region', 'N/A')}`")
            with c2:
                st.markdown(f"**Max HP (Lv 90):** `{char.get('hpMax', 'N/A'):,}`" if pd.notna(char.get('hpMax')) else "**Max HP:** N/A")
                st.markdown(f"**Max ATK (Lv 90):** `{char.get('atkMax', 'N/A'):,}`" if pd.notna(char.get('atkMax')) else "**Max ATK:** N/A")
                st.markdown(f"**Max DEF (Lv 90):** `{char.get('defMax', 'N/A'):,}`" if pd.notna(char.get('defMax')) else "**Max DEF:** N/A")
            with c3:
                st.markdown(f"**Ascension Stat:** `{char.get('special_stat', 'N/A')}`")
                st.markdown(f"**Burst Energy Cost:** `{char.get('ultimate_cost', 'N/A')}`")
                st.markdown(f"**Release Date:** `{char.get('release', 'N/A')}`")

            st.divider()
            p1, p2, p3 = st.columns(3)
            with p1:
                st.markdown(f"**Japanese VA:** `{char.get('jp_va', 'N/A')}`")
            with p2:
                st.markdown(f"**Title:** *{char.get('info.title', 'N/A')}*")
            with p3:
                st.markdown(f"**Birthday:** `{char.get('birthday', 'N/A')}`")

        elif game == "zzz":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Code Name:** `{char.get('code_name', 'N/A')}`")
                st.markdown(f"**Faction:** `{char.get('faction.name', 'N/A')}`")
                st.markdown(f"**Specialty:** `{char.get('specialty.name', 'N/A')}`")
            with c2:
                st.markdown(f"**Element:** `{char.get('element.name', 'N/A')}`")
                st.markdown(f"**Attack Type:** `{char.get('attack_type.name', 'N/A')}`")
                st.markdown(f"**Assist Type:** `{char.get('assist_type', 'N/A')}`")
            with c3:
                st.markdown(f"**Max HP (Lv 60):** `{char.get('hpMax', 'N/A'):,}`" if pd.notna(char.get('hpMax')) else "**Max HP:** N/A")
                st.markdown(f"**Max ATK (Lv 60):** `{char.get('atkMax', 'N/A'):,}`" if pd.notna(char.get('atkMax')) else "**Max ATK:** N/A")
                st.markdown(f"**Max DEF (Lv 60):** `{char.get('defMax', 'N/A'):,}`" if pd.notna(char.get('defMax')) else "**Max DEF:** N/A")

            st.divider()
            t1, t2 = st.columns(2)
            with t1:
                st.markdown("**Team Conditions:**")
                for i in range(1, 4):
                    cond = char.get(f"team_condition_{i}")
                    if pd.notna(cond) and cond != "None":
                        st.markdown(f"- `{cond}`")
            with t2:
                st.markdown("**Ascension Bonus Stats:**")
                stat1 = char.get("ascension_stat_1")
                stat2 = char.get("ascension_stat_2")
                if pd.notna(stat1) and stat1 != "None":
                    st.markdown(f"- `{stat1}`")
                if pd.notna(stat2) and stat2 != "None":
                    st.markdown(f"- `{stat2}`")

        elif game == "fgo":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Class:** `{char.get('className', 'N/A')}`")
                st.markdown(f"**Attribute:** `{char.get('attribute', 'N/A')}`")
                st.markdown(f"**Cost:** `{char.get('cost', 'N/A')}` | **Max Lv:** `{char.get('lvMax', 'N/A')}`")
            with c2:
                st.markdown(f"**Max ATK:** `{char.get('atkMax', 'N/A'):,}`" if pd.notna(char.get('atkMax')) else "**Max ATK:** N/A")
                st.markdown(f"**Max HP:** `{char.get('hpMax', 'N/A'):,}`" if pd.notna(char.get('hpMax')) else "**Max HP:** N/A")
                st.markdown(f"**Growth Curve:** `{char.get('growthCurve', 'N/A')}`")
            with c3:
                st.markdown(f"**Card Deck:** `{char.get('cardDeck', 'N/A')}`")
                st.markdown(f"**Star Absorb / Gen:** `{char.get('starAbsorb', 'N/A')}` / `{char.get('starGen', 'N/A')}`")
                st.markdown(f"**Death Chance:** `{char.get('instantDeathChance', 'N/A')}`")

            st.divider()
            st.markdown("##### 💫 Noble Phantasm & Combat Profile")
            n1, n2, n3 = st.columns(3)
            with n1:
                st.markdown(f"**NP Card:** `{char.get('npCards', 'N/A')}`")
                st.markdown(f"**Rank:** `{char.get('rank', 'N/A')}`")
            with n2:
                st.markdown(f"**Type:** `{char.get('type', 'N/A')}`")
                st.markdown(f"**Target:** `{char.get('targetType', 'N/A')}`")
            with n3:
                st.markdown(f"**Hit Counts:** Arts `{char.get('artsHitCount', '-')}` | Buster `{char.get('busterHitCount', '-')}` | Quick `{char.get('quickHitCount', '-')}` | Extra `{char.get('addattackHitCount', '-')}`")

            st.divider()
            st.markdown("##### 🏷️ Servant Traits")
            render_pill_tags(char.get("traits", ""))

            st.markdown("##### ⚡ Skill & NP Effect Tags")
            s1, s2 = st.columns(2)
            with s1:
                st.caption("Skill Tags:")
                render_pill_tags(char.get("skillTags", ""))
            with s2:
                st.caption("Noble Phantasm Tags:")
                render_pill_tags(char.get("npTags", ""))

        elif game == "umamusu":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Title:** *{char.get('item_data.title', 'N/A')}*")
                st.markdown(f"**Version:** `{char.get('item_data.version', 'N/A')}`")
                st.markdown(f"**CV (English):** `{char.get('char_data.va_en', 'N/A')}`")
            with c2:
                st.markdown(f"**Birthday:** `{char.get('birthday', 'N/A')}`")
                st.markdown(f"**Height:** `{char.get('char_data.height', 'N/A')} cm`")
                b = char.get('char_data.three_sizes.b', '-')
                w = char.get('char_data.three_sizes.w', '-')
                h = char.get('char_data.three_sizes.h', '-')
                st.markdown(f"**Three Sizes:** `B{b} / W{w} / H{h}`")
            with c3:
                st.markdown("**Stat Growth Bonuses:**")
                st.markdown(f"Spd: `+{char.get('speed_bonus', 0)}%` | Sta: `+{char.get('stamina_bonus', 0)}%` | Pow: `+{char.get('power_bonus', 0)}%`")
                st.markdown(f"Guts: `+{char.get('guts_bonus', 0)}%` | Wit: `+{char.get('wit_bonus', 0)}%`")

            st.divider()
            st.markdown("##### 🏇 Track & Strategy Aptitudes")
            a1, a2, a3 = st.columns(3)
            with a1:
                st.caption("Surface:")
                st.markdown(f"Turf: `{char.get('turf_aptitude', '-')}` | Dirt: `{char.get('dirt_aptitude', '-')}`")
            with a2:
                st.caption("Distance:")
                st.markdown(f"Sprint: `{char.get('sprint_aptitude', '-')}` | Mile: `{char.get('mile_aptitude', '-')}` | Medium: `{char.get('medium_aptitude', '-')}` | Long: `{char.get('long_aptitude', '-')}`")
            with a3:
                st.caption("Strategy:")
                st.markdown(f"Front: `{char.get('front_aptitude', '-')}` | Pace: `{char.get('pace_aptitude', '-')}` | Late: `{char.get('late_aptitude', '-')}` | End: `{char.get('end_aptitude', '-')}`")
