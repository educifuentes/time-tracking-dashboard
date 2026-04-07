import streamlit as st
import pandas as pd
from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.constants.brands import BRANDS, BRAND_COLORS

def display_df_censos(df: pd.DataFrame):
    config = {
        col: st.column_config.Column(
            col.replace("_", " ").title()
        ) for col in df.columns
    }
    
    config["marcas"] = st.column_config.MultiselectColumn(
        "Marcas",
        help="Marcas",
        options=[brand.title() for brand in BRANDS],
        color=BRAND_COLORS,
    )
    
    config["clasificacion"] = st.column_config.MultiselectColumn(
        "Clasificación",
        help="Clasificación",
        options=list(CLASIFICACION_COLORS.keys()),
        color=list(CLASIFICACION_COLORS.values()),
    )
    
    st.dataframe(df, width='stretch', hide_index=True, column_config=config)
