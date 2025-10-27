from utils import load_data
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Overview")

if "df" not in st.session_state:
    st.session_state["df"] = load_data(
        "Streamlit/data/ValeursFoncieres-2025-S1-cleaned.csv"
    )

df = st.session_state["df"]

st.title("France Real Estate Prices - 2025 H1 - Overview")

st.markdown("### National Key Metrics")

# Create three columns
col1, col2, col3 = st.columns([1, 1, 1.5])

# Column 1
col1.metric("Total Transactions", df.shape[0])
col1.metric("Average Price per sqm", round(df["price_per_sqm_built"].mean(), 2))

# Column 2
col2.metric("Total Sales Value (€)", f"{df['sale_value'].sum():,.0f}")
col2.metric("Median Price per sqm", round(df["price_per_sqm_built"].median(), 2))

# Column 3
fig_pie = px.pie(df, names="property_type_label", title="Distribution by Property Type")
fig_pie.update_layout(
    height=200,
    margin=dict(l=0, r=0, t=30, b=30),
)
col3.plotly_chart(fig_pie, config={"width": "stretch"})

st.divider()

# ----- Correlation Plot -----
st.subheader("Correlation between Built Area and Price per Square Meter")

df_no_outliers = df[
    df["price_per_sqm_built"] < df["price_per_sqm_built"].quantile(0.9995)
]


# Polynomial Line Regression
@st.cache_data
def polynomial_fit(df, degree=7):
    x = df["built_area_sqm"]
    y = df["price_per_sqm_built"]
    p = np.polyfit(x, y, deg=degree)
    poly_func = np.poly1d(p)
    x_trend = np.linspace(df["built_area_sqm"].min(), df["built_area_sqm"].max(), 200)
    y_trend = poly_func(x_trend)
    return x_trend, y_trend


x_trend, y_trend = polynomial_fit(df_no_outliers, degree=7)
# p = np.polyfit(
#     df_no_outliers["built_area_sqm"], df_no_outliers["price_per_sqm_built"], deg=7
# )
# poly_func = np.poly1d(p)
# x_trend = np.linspace(
#     df_no_outliers["built_area_sqm"].min(), df_no_outliers["built_area_sqm"].max(), 200
# )
# y_trend = poly_func(x_trend)

# Plotting
df_sampled = df_no_outliers.sample(frac=0.5, random_state=42)  # Sample for performance
trace_scatter = go.Scattergl(
    x=df_sampled["built_area_sqm"],
    y=df_sampled["price_per_sqm_built"],
    mode="markers",
    name="Transactions",
    marker=dict(color="skyblue", opacity=0.1, size=3),
    showlegend=False,
)

trace_halo = go.Scattergl(
    x=x_trend,
    y=y_trend,
    mode="lines",
    name="Halo",
    line=dict(color="white", width=8),  # Wider line for border effect
    showlegend=False,
)

trace_trendline = go.Scattergl(
    x=x_trend,
    y=y_trend,
    mode="lines",
    name="Polynomial Fit",
    line=dict(color="red", width=4),
)

fig = go.Figure(data=[trace_scatter, trace_halo, trace_trendline])

fig.update_layout(
    height=350,
    xaxis_title="Built Area (sqm)",
    yaxis_title="Price per Square Meter (€)",
    template="plotly_white",
    legend_title_text="Legend",
    legend=dict(
        orientation="h",  # Make the legend horizontal
        yanchor="bottom",
        y=0.75,
        xanchor="right",
        x=1,
        bgcolor="rgba(255, 255, 255, 0.5)",  # Add a semi-transparent background
        bordercolor="Black",
        borderwidth=1,
    ),
    margin=dict(l=100, r=100, t=0, b=0),
)

st.plotly_chart(fig, config={"width": "stretch"})
