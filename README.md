**France Real Estate Prices - 2025 H1 Analysis**

This project provides an interactive dashboard to analyze and visualize real estate data from the first half of 2025 in France. Built with Streamlit, it offers insights into market trends, price distributions, and geographical variations.

**✨ Features**

- **National Key Metrics:** Get a high-level overview of the French real estate market with key metrics such as total transaction volume, average prices, and the distribution of property types.

- **Interactive HeatMap:** Visualize average real estate prices across different regions and departments with an interactive map. Use filters to explore price variations by property type and area.

- **Correlation Analysis:** Explore the relationship between built area and price per square meter.


**🗃️ Dataset**

The data used in this project is from the official French government dataset, [Demandes de valeurs foncières](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/) for the first half of 2025. This dataset, published by the French tax authority (DGFIP), contains real estate transaction information.

The raw data has been preprocessed to clean and structure it for analysis. Key preprocessing steps include handling missing values, filtering outliers, and calculating additional metrics such as price per square meter.

**🚀 Getting Started**

```
git clone https://github.com/your-username/france-real-estate-2025-h1.git
cd DVF_Streamlit_App
pip install -r requirements.txt
streamlit run Streamlit/Home.py
```

The application will be available at http://localhost:8501.

**📂 File Structure**
```
├── DVF_2025_H1_Data_Preprocessing.ipynb
├── geojson_perf_test.ipynb
├── notice-descriptive-du-fichier-dvf-20221017.pdf
├── requirements.txt
├── Streamlit
│  ├── data
│  ├── geojson
│  ├── Home.py
│  ├── pages
│  │  ├── 1_Overview.py
│  │  └── 2_HeatMap.py
│  └── utils.py
├── ValeursFoncieres-2025-S1-cleaned.csv
└── ValeursFoncieres-2025-S1.txt
```


**🌐 Deployment**

The application is deployed and accessible at the following URL:

https://chenchen-qiu-dvf-dashboard.streamlit.app/HeatMap
