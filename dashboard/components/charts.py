import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_stat_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    color_col: str | None = None,
    hover_name: str = "name",
    hover_data: list[str] | None = None,
) -> None:
    """Render an interactive Plotly scatter plot comparing two stats."""
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        st.info("Insufficient data for stat comparison scatter plot.")
        return

    plot_df = df.copy()
    plot_df[x_col] = pd.to_numeric(plot_df[x_col], errors="coerce")
    plot_df[y_col] = pd.to_numeric(plot_df[y_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[x_col, y_col])

    if plot_df.empty:
        st.info("No numeric values available for this scatter plot.")
        return

    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        color=color_col if color_col in plot_df.columns else None,
        hover_name=hover_name if hover_name in plot_df.columns else None,
        hover_data=[c for c in (hover_data or []) if c in plot_df.columns],
        title=title,
        template="plotly_dark",
    )
    fig.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=1, color="DarkSlateGrey")))
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_category_distribution(
    df: pd.DataFrame,
    col: str,
    title: str,
    hole: float = 0.45,
) -> None:
    """Render a donut chart showing the breakdown of a categorical column."""
    if df.empty or col not in df.columns:
        st.info(f"Column '{col}' not found for distribution chart.")
        return

    counts = df[col].dropna().value_counts().reset_index()
    counts.columns = [col, "count"]

    fig = px.pie(
        counts,
        names=col,
        values="count",
        title=title,
        hole=hole,
        template="plotly_dark",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_token_frequency(
    df: pd.DataFrame,
    col: str,
    title: str,
    top_n: int = 12,
    delimiter: str = ",",
) -> None:
    """Render a horizontal bar chart counting individual tokens from a comma-delimited column."""
    if df.empty or col not in df.columns:
        st.info(f"Column '{col}' not found for token frequency.")
        return

    tokens: list[str] = []
    for item in df[col].dropna():
        if isinstance(item, str):
            for part in item.split(delimiter):
                token = part.strip()
                if token and token != "None":
                    tokens.append(token)

    if not tokens:
        st.info(f"No tokens found in '{col}'.")
        return

    counts = pd.Series(tokens).value_counts().head(top_n).reset_index()
    counts.columns = ["Token", "Frequency"]

    fig = px.bar(
        counts,
        x="Frequency",
        y="Token",
        orientation="h",
        title=title,
        template="plotly_dark",
        color="Frequency",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)
