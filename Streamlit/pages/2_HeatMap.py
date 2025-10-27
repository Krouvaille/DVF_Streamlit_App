from utils import load_data
from utils import load_geojson
from utils import filter_geojson_by_department
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(layout="wide", page_title="French Real Estate - Heat Map")

if "df" not in st.session_state:
    st.session_state["df"] = load_data(
        "Streamlit/data/ValeursFoncieres-2025-S1-cleaned.csv"
    )

df = st.session_state["df"]

# ------------------ Sidebar (Filters) ------------------
st.sidebar.title("Filters")

# View Mode
view_mode = st.sidebar.pills(
    "View Mode", options=["Global", "Specific"], default="Global"
)

if view_mode == "Global":
    selected_level = st.sidebar.radio(
        "Geographic Level", options=["Regions", "Departments"]
    )
elif view_mode == "Specific":
    options = list(
        df[["department_name", "department_code"]]
        .drop_duplicates()
        .set_index("department_name")["department_code"]
        .to_dict()
        .items()
    )
    selected_department_name, selected_department_code = st.sidebar.selectbox(
        "Department",
        options=options,
        format_func=lambda x: x[0],
        index=0,
    )
# Property Type
property_type = st.sidebar.radio(
    "Property Type",
    options=["All", "Appartement", "Maison", "Locaux"],
)

# Built Area Range
min_area, max_area = st.sidebar.slider(
    "Built Area (m²)",
    min_value=int(df["built_area_sqm"].min()),
    max_value=int(df["built_area_sqm"].max()),
    value=(int(df["built_area_sqm"].min()), int(df["built_area_sqm"].max())),
    step=1,
)

# ------------------ Mapping Dicts ------------------

st.title("France Real Estate Prices - 2025 H1 - Heat Map")

property_type_mapping = {
    "All": ["1", "2", "3", "4"],
    "Maison": ["1"],
    "Appartement": ["2"],
    "Locaux": ["4"],
}


# ------------------ Filter Data ------------------
filtered_df = df[
    (df["property_type_code"].isin(property_type_mapping.get(property_type)))
    & (df["built_area_sqm"].between(min_area, max_area))
]


# ------------------ Aggregation on filtered data ------------------
if view_mode == "Global":
    if selected_level == "Regions":
        geojson_data = load_geojson("regions")
        grouped_df = (
            filtered_df.groupby("region_code")
            .agg(
                region_name=("region_name", "first"),
                avg_price_sqm=("price_per_sqm_built", "mean"),
            )
            .round(2)
            .reset_index()
        )
        locations = "region_code"
        labels = "region_name"
    elif selected_level == "Departments":
        geojson_data = load_geojson("departements")
        grouped_df = (
            filtered_df.groupby("department_code")
            .agg(
                department_name=("department_name", "first"),
                avg_price_sqm=("price_per_sqm_built", "mean"),
            )
            .round(2)
            .reset_index()
        )
        locations = "department_code"
        labels = "department_name"
elif view_mode == "Specific":
    geojson_data = load_geojson("communes")
    geojson_data = filter_geojson_by_department(geojson_data, selected_department_code)

    grouped_df = (
        filtered_df[filtered_df["department_code"] == selected_department_code]
        .groupby("insee_code")
        .agg(
            commune_name=("commune_name", "first"),
            avg_price_sqm=("price_per_sqm_built", "mean"),
        )
        .round(2)
        .reset_index()
    )
    locations = "insee_code"
    labels = "commune_name"


main, rightbar = st.columns([3, 1.2])


# ------------------ Main Page ------------------
with main:
    # Choropleth Map
    grouped_df["log_price_sqm"] = np.log10(grouped_df["avg_price_sqm"]).round(2)

    fig = px.choropleth(
        grouped_df,
        geojson=geojson_data,
        locations=locations,
        featureidkey="properties.code",
        color="log_price_sqm" if view_mode == "Global" else "avg_price_sqm",
        color_continuous_scale="Viridis",
        custom_data=[labels, "avg_price_sqm", locations],
    )
    fig.update_geos(
        projection_type="mercator",
        fitbounds="locations",
        visible=False,
    )
    fig.update_layout(
        dragmode=False,
        height=750,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={
            "title": "Price / m²",
            "tickprefix": "€",
            "tickvals": np.log10([2500, 5000, 7500, 10000, 15000, 20000]),
            "ticktext": [
                "2.5k",
                "5k",
                "7.5k",
                "10k",
                "15k",
                "20k",
            ],
            "orientation": "h",
            "y": -0.1,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        hoverlabel=dict(
            bgcolor="rgba(0, 0, 0, 0.1)",
            font_size=12,
            font_color="black",
            font_family="Arial",
            bordercolor="black",
        ),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br><br>"
            + "Avg. Price: €%{customdata[1]:,.0f}<br>"
            + "Department Code: %{customdata[2]}"
            + "<extra></extra>"
        )
    )
    st.plotly_chart(fig, config={"width": "stretch"})
# ------------------ Right Bar ------------------
with rightbar:
    # --- Statistics ---
    st.subheader("Top Areas")
    st.dataframe(
        grouped_df[[labels, "avg_price_sqm"]]
        .sort_values("avg_price_sqm", ascending=False)
        .head(10),
        width="stretch",
        hide_index=True,
    )
