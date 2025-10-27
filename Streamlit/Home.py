import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(layout="wide", page_title="Home", page_icon="🏠")

if "df" not in st.session_state:
    st.session_state["df"] = load_data(
        "Streamlit/data/ValeursFoncieres-2025-S1-cleaned.csv"
    )

df = st.session_state["df"]


st.title("France Real Estate Prices - 2025 H1")
st.markdown(
    """
    **Author:** Chenchen QIU
    """
)

st.subheader("Project Overview")
st.markdown(
    """
    This Streamlit application provides an interactive analysis of the French real estate market,
    based on the ***Demandes de valeurs foncières (DVF)*** dataset for the first half of 2025.

    You can navigate through the following modules to explore market trends, price distributions, and key metrics.
    """
)

st.subheader("Get Started")
st.markdown(
    """
    - **Overview:** Explore key national real estate metrics, such as total transaction volume, average prices, and the distribution of property types.
    - **Heat Map:** Visualize average real estate prices across different regions and departments with an interactive map. Use filters to explore price variations by property type and area.
    """
)
st.divider()
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("About the Dataset")
    st.markdown(
        """
        The data used in this project is from the official French government dataset, 
        [Demandes de valeurs foncières](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/).
        This dataset, published by the French tax authority (DGFiP), contains real estate transaction information.
        """
    )

with col2:
    st.subheader("Methodology")
    st.markdown(
        """
        The data used in this dashboard has been preprocessed to clean and structure it for analysis. Key preprocessing steps include handling missing values, filtering outliers, and calculating additional metrics such as price per square meter.

        Interested in how the data was preprocessed?

        """
    )
    st.link_button(
        "Check out the data preprocessing notebook",
        "https://nbviewer.org/github/Krouvaille/DVF_2025_H1_Streamlit_App/blob/main/DVF_2025_H1_Data_Preprocessing.ipynb",  # 要打开的链接
    )
