import json
import pandas as pd
import streamlit as st
import requests

# geojson_urls = {
#     "regions": "https://raw.githubusercontent.com/gregoiredavid/france-geojson/refs/heads/master/regions-version-simplifiee.geojson",
#     "departements": "https://raw.githubusercontent.com/gregoiredavid/france-geojson/refs/heads/master/departements-version-simplifiee.geojson",
#     "arrondissements": "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/arrondissements-version-simplifiee.geojson",
#     "communes": "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes.geojson",
# }

geojson_paths = {
    "regions": "Streamlit/geojson/regions-version-simplifiee.geojson",
    "departements": "Streamlit/geojson/departements-version-simplifiee.geojson",
    "communes": "Streamlit/geojson/communes.geojson",  # We don't use small version for communes because some geometries are missing
}


@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(
        csv_path,
        dtype={
            "sale_value": "int64",
            "postal_code": "string",
            "insee_code": "string",
            "region_name": "string",
            "region_code": "string",
            "departement_name": "string",
            "department_code": "string",
            "commune_name": "string",
            "commune_code": "string",
            "property_type_label": "category",
            "property_type_code": "category",
            "built_area_sqm": "float64",
            "land_area_sqm": "float64",
            "main_rooms_count": "int64",
            "land_use": "category",
            "land_use_special": "category",
            "price_per_sqm_built": "float64",
            "price_per_sqm_land": "float64",
        },
    )

    return df


@st.cache_data
def load_geojson(path):
    path = geojson_paths.get(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_geojson_by_department(geojson, department_code):

    filtered_geojson = {"type": "FeatureCollection", "features": []}

    for feature in geojson["features"]:
        if feature["properties"]["code"].startswith(department_code):
            filtered_geojson["features"].append(feature)

    return filtered_geojson
