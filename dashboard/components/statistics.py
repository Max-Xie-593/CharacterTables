import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def _get_numeric_cols(df: pd.DataFrame) -> list[str]:
    """Return clean numeric stat columns excluding IDs and non-stat numbers."""
    ignored = {"id", "collectionNo", "illustrator_id", "cv_id", "series_id"}
    cols = []
    for c in df.columns:
        if c in ignored or c.endswith("_id"):
            continue
        # Check if numeric or convertible
        if pd.api.types.is_numeric_dtype(df[c]):
            cols.append(c)
        else:
            converted = pd.to_numeric(df[c], errors="coerce")
            if converted.notna().sum() > len(df) * 0.5:
                cols.append(c)
    return cols

def _get_categorical_cols(df: pd.DataFrame) -> list[str]:
    """Return categorical columns suitable for grouping (2-30 unique values)."""
    ignored_prefixes = ("profile.", "char_data.skills", "char_data.passives", "char_data.three_sizes")
    cols = []
    for c in df.columns:
        if any(c.startswith(p) for p in ignored_prefixes) or c.endswith("_id") or c in ("id", "collectionNo"):
            continue
        # Consider string/object dtypes or low-cardinality integer categories like rarity
        if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == "object" or c == "rarity":
            nunique = df[c].nunique(dropna=True)
            if 2 <= nunique <= 30:
                cols.append(c)
    return cols

def render_statistical_tab(df: pd.DataFrame, game: str, name_col: str = "name") -> None:
    """Render an advanced statistical analysis laboratory tab."""
    if df.empty:
        st.info("No data available to compute statistics.")
        return

    numeric_cols = _get_numeric_cols(df)
    categorical_cols = _get_categorical_cols(df)

    if not numeric_cols:
        st.warning("No numeric columns found for statistical analysis.")
        return

    st.markdown("### 📈 Statistical Laboratory")
    st.caption("Perform exploratory data analysis, correlation discovery, distribution profiling, and group comparisons.")

    sub_tabs = st.tabs([
        "📊 Distributions & Summary",
        "🔥 Correlation Matrix",
        "📉 Bivariate & Regression",
        "⚖️ Group Comparisons",
    ])

    # -------------------------------------------------------------
    # Sub-Tab 1: Distributions & Summary
    # -------------------------------------------------------------
    with sub_tabs[0]:
        st.markdown("#### 1. Parametric & Non-Parametric Summary")
        selected_stats = st.multiselect(
            "Select metrics to summarize:",
            options=numeric_cols,
            default=numeric_cols[:min(8, len(numeric_cols))],
            key=f"{game}_summary_metrics",
        )

        if selected_stats:
            num_df = df[selected_stats].apply(pd.to_numeric, errors="coerce")
            summary = num_df.describe(percentiles=[0.05, 0.25, 0.50, 0.75, 0.95]).T
            summary["skew"] = num_df.skew()
            summary["kurtosis"] = num_df.kurtosis()
            summary = summary.rename(columns={
                "count": "Count",
                "mean": "Mean",
                "std": "Std Dev",
                "min": "Min",
                "5%": "P5",
                "25%": "Q1 (25%)",
                "50%": "Median",
                "75%": "Q3 (75%)",
                "95%": "P95",
                "max": "Max",
                "skew": "Skewness",
                "kurtosis": "Kurtosis",
            })
            st.dataframe(summary.style.format("{:.2f}", na_rep="-"), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 2. Distribution & Outlier Profiler")
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        with col_ctrl1:
            dist_metric = st.selectbox("Metric to profile:", options=numeric_cols, key=f"{game}_dist_metric")
        with col_ctrl2:
            group_options = ["None (Overall)"] + categorical_cols
            dist_group = st.selectbox("Group by category:", options=group_options, key=f"{game}_dist_group")
        with col_ctrl3:
            plot_type = st.radio("Plot Type:", ["Box Plot", "Violin Plot", "Histogram / KDE"], horizontal=True, key=f"{game}_plot_type")

        clean_plot_df = df.copy()
        clean_plot_df[dist_metric] = pd.to_numeric(clean_plot_df[dist_metric], errors="coerce")
        clean_plot_df = clean_plot_df.dropna(subset=[dist_metric])

        # Outlier calculation (IQR rule)
        q25 = clean_plot_df[dist_metric].quantile(0.25)
        q75 = clean_plot_df[dist_metric].quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outliers = clean_plot_df[(clean_plot_df[dist_metric] < lower_bound) | (clean_plot_df[dist_metric] > upper_bound)]

        # KPI chips for selected metric
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Mean", f"{clean_plot_df[dist_metric].mean():.1f}")
        m2.metric("Median", f"{clean_plot_df[dist_metric].median():.1f}")
        m3.metric("Std Dev", f"{clean_plot_df[dist_metric].std():.1f}")
        m4.metric("IQR", f"{iqr:.1f}")
        m5.metric("Outliers (>1.5×IQR)", f"{len(outliers)}")

        group_col = None if dist_group == "None (Overall)" else dist_group

        if plot_type == "Box Plot":
            fig = px.box(
                clean_plot_df,
                x=group_col,
                y=dist_metric,
                color=group_col,
                points="all",
                hover_name=name_col if name_col in clean_plot_df.columns else None,
                template="plotly_dark",
                title=f"Box Plot of {dist_metric}" + (f" by {dist_group}" if group_col else ""),
            )
        elif plot_type == "Violin Plot":
            fig = px.violin(
                clean_plot_df,
                x=group_col,
                y=dist_metric,
                color=group_col,
                box=True,
                points="all",
                hover_name=name_col if name_col in clean_plot_df.columns else None,
                template="plotly_dark",
                title=f"Violin Plot of {dist_metric}" + (f" by {dist_group}" if group_col else ""),
            )
        else:
            fig = px.histogram(
                clean_plot_df,
                x=dist_metric,
                color=group_col,
                marginal="box",
                barmode="overlay",
                opacity=0.75,
                template="plotly_dark",
                title=f"Histogram / Density of {dist_metric}",
            )

        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

        if not outliers.empty:
            with st.expander(f"⚠️ View Detected Outliers for {dist_metric} ({len(outliers)} characters)"):
                cols_to_show = [c for c in [name_col, dist_metric, group_col] if c and c in outliers.columns]
                st.dataframe(outliers[cols_to_show].sort_values(by=dist_metric, ascending=False), use_container_width=True)

    # -------------------------------------------------------------
    # Sub-Tab 2: Correlation Matrix
    # -------------------------------------------------------------
    with sub_tabs[1]:
        st.markdown("#### 1. Correlation Matrix Heatmap")
        corr_c1, corr_c2 = st.columns([3, 1])
        with corr_c1:
            corr_cols = st.multiselect(
                "Select numeric metrics to correlate:",
                options=numeric_cols,
                default=numeric_cols[:min(10, len(numeric_cols))],
                key=f"{game}_corr_cols",
            )
        with corr_c2:
            corr_method = st.radio("Correlation Method:", ["pearson", "spearman"], index=0, key=f"{game}_corr_method")

        if len(corr_cols) >= 2:
            corr_df = df[corr_cols].apply(pd.to_numeric, errors="coerce").corr(method=corr_method)

            fig_corr = px.imshow(
                corr_df,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                template="plotly_dark",
                title=f"{corr_method.capitalize()} Correlation Heatmap",
            )
            fig_corr.update_layout(margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_corr, use_container_width=True)

            # Discover strongest correlations (excluding self-correlation)
            corr_pairs = []
            for i in range(len(corr_cols)):
                for j in range(i + 1, len(corr_cols)):
                    c1, c2 = corr_cols[i], corr_cols[j]
                    val = corr_df.loc[c1, c2]
                    if pd.notna(val):
                        corr_pairs.append((c1, c2, val))

            if corr_pairs:
                corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
                st.markdown("##### 🔍 Strongest Observed Relationships:")
                top_cols = st.columns(min(3, len(corr_pairs)))
                for idx, (c1, c2, val) in enumerate(corr_pairs[:3]):
                    with top_cols[idx]:
                        label = "Positive" if val > 0 else "Negative"
                        st.info(f"**{c1}** ↔ **{c2}**\n\n**r = {val:.2f}** ({label})")
        else:
            st.info("Please select at least 2 metrics to compute correlations.")

    # -------------------------------------------------------------
    # Sub-Tab 3: Bivariate & Regression
    # -------------------------------------------------------------
    with sub_tabs[2]:
        st.markdown("#### 1. Linear Regression & Trendline Analysis")
        reg_c1, reg_c2, reg_c3 = st.columns(3)
        with reg_c1:
            x_col = st.selectbox("Independent Variable (X):", options=numeric_cols, index=0, key=f"{game}_reg_x")
        with reg_c2:
            default_y = 1 if len(numeric_cols) > 1 else 0
            y_col = st.selectbox("Dependent Variable (Y):", options=numeric_cols, index=default_y, key=f"{game}_reg_y")
        with reg_c3:
            reg_color = st.selectbox("Color by category:", options=["None"] + categorical_cols, key=f"{game}_reg_color")

        if x_col != y_col:
            reg_df = df.copy()
            reg_df[x_col] = pd.to_numeric(reg_df[x_col], errors="coerce")
            reg_df[y_col] = pd.to_numeric(reg_df[y_col], errors="coerce")
            reg_df = reg_df.dropna(subset=[x_col, y_col])

            if len(reg_df) > 2:
                # Calculate OLS Regression using numpy
                x_vals = reg_df[x_col].values
                y_vals = reg_df[y_col].values
                slope, intercept = np.polyfit(x_vals, y_vals, deg=1)
                y_pred = slope * x_vals + intercept
                ss_res = np.sum((y_vals - y_pred) ** 2)
                ss_tot = np.sum((y_vals - np.mean(y_vals)) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

                # Regression metrics banner
                r1, r2, r3 = st.columns(3)
                r1.metric("Slope (m)", f"{slope:.4f}")
                r2.metric("Intercept (b)", f"{intercept:.2f}")
                r3.metric("R² (Fit Quality)", f"{r_squared:.3f}")

                color_arg = None if reg_color == "None" else reg_color
                fig_reg = px.scatter(
                    reg_df,
                    x=x_col,
                    y=y_col,
                    color=color_arg,
                    hover_name=name_col if name_col in reg_df.columns else None,
                    template="plotly_dark",
                    title=f"Scatter & OLS Trendline: {y_col} vs {x_col}",
                )

                # Add regression line
                x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
                y_line = slope * x_line + intercept
                fig_reg.add_trace(
                    go.Scatter(
                        x=x_line,
                        y=y_line,
                        mode="lines",
                        name=f"OLS Trendline (R²={r_squared:.2f})",
                        line=dict(color="#FF4B4B", width=2, dash="dash"),
                    )
                )

                fig_reg.update_layout(margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig_reg, use_container_width=True)
            else:
                st.info("Insufficient numeric data points to fit a regression line.")
        else:
            st.warning("Please choose two distinct metrics for X and Y.")

    # -------------------------------------------------------------
    # Sub-Tab 4: Group Comparisons
    # -------------------------------------------------------------
    with sub_tabs[3]:
        st.markdown("#### 1. Categorical Group Aggregations & Disparities")
        grp_c1, grp_c2 = st.columns(2)
        with grp_c1:
            grp_cat = st.selectbox("Category to compare:", options=categorical_cols, key=f"{game}_grp_cat")
        with grp_c2:
            grp_metric = st.selectbox("Target metric to evaluate:", options=numeric_cols, key=f"{game}_grp_metric")

        if grp_cat and grp_metric:
            grp_df = df.copy()
            grp_df[grp_metric] = pd.to_numeric(grp_df[grp_metric], errors="coerce")
            grp_df = grp_df.dropna(subset=[grp_cat, grp_metric])

            # Group aggregation stats
            agg_table = grp_df.groupby(grp_cat)[grp_metric].agg(
                Count="count",
                Mean="mean",
                Std="std",
                Median="median",
                Min="min",
                Max="max",
            ).reset_index()

            st.dataframe(agg_table.style.format({
                "Mean": "{:.2f}",
                "Std": "{:.2f}",
                "Median": "{:.2f}",
                "Min": "{:.2f}",
                "Max": "{:.2f}",
            }, na_rep="-"), use_container_width=True)

            # Bar chart with error bars
            fig_bar = px.bar(
                agg_table,
                x=grp_cat,
                y="Mean",
                error_y="Std",
                color=grp_cat,
                title=f"Mean {grp_metric} by {grp_cat} (with ±1 Std Dev error bars)",
                template="plotly_dark",
            )
            fig_bar.update_layout(margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
