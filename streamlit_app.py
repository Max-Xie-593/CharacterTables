import streamlit as st
from dashboard.data_loader import GAMES, load_cleaned_data
from dashboard.views.gi import render_gi_view
from dashboard.views.zzz import render_zzz_view
from dashboard.views.fgo import render_fgo_view
from dashboard.views.umamusu import render_umamusu_view

def main() -> None:
    # 1. Page Configuration
    st.set_page_config(
        page_title="CharacterTables Roster Explorer",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 2. Custom CSS Styling
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            background: linear-gradient(90deg, #3182ce, #805ad5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sub-header {
            color: #a0aec0;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 3. Header Banner
    st.markdown('<div class="main-header">🎮 CharacterTables Roster Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Interactive data explorer, stat visualizer, and character inspector across supported games.</div>',
        unsafe_allow_html=True,
    )

    # 4. Sidebar Navigation
    st.sidebar.title("🎮 Select Game")
    game_options = {game_id: f"{icon} {title}" for game_id, title, icon in GAMES}
    selected_game = st.sidebar.radio(
        "Game",
        options=list(game_options.keys()),
        format_func=lambda x: game_options[x],
        label_visibility="collapsed",
    )

    st.sidebar.divider()

    # 5. Load Data & Render Appropriate View
    df = load_cleaned_data(selected_game)

    if selected_game == "gi":
        render_gi_view(df)
    elif selected_game == "zzz":
        render_zzz_view(df)
    elif selected_game == "fgo":
        render_fgo_view(df)
    elif selected_game == "umamusu":
        render_umamusu_view(df)

    # 6. Footer
    st.divider()
    st.caption(
        "Powered by **CharacterTables** data pipeline. Data is extracted and automatically synced via scheduled GitHub Actions."
    )

if __name__ == "__main__":
    main()
