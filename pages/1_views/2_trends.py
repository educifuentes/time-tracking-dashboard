import streamlit as st
import pandas as pd
import altair as alt

from models.marts.aggregations.agg_area_hour_per_week import agg_area_hour_per_week

from utilities.ui_components.icons import render_icon
from utilities.visulizations.charts import bar_chart_by_week

st.title(f"{render_icon('logo')} Trends")
st.markdown("Horas semanales por área")

# Load data
df = agg_area_hour_per_week()


if not df.empty:
    
    # Create tabs
    tab_all, tab_data, tab_docu, tab_matr = st.tabs(["Todas", "DATA", "DOCU", "MATR"])

    HEIGHT = 800
    
    with tab_all:
        chart_all = bar_chart_by_week(df, area_filter=None)
        if chart_all:
            st.altair_chart(chart_all, use_container_width=True, height=HEIGHT)
            
    with tab_data:
        chart_data = bar_chart_by_week(df, area_filter="DATA")
        if chart_data:
            st.altair_chart(chart_data, use_container_width=True, height=HEIGHT)
            
    with tab_docu:
        chart_docu = bar_chart_by_week(df, area_filter="DOCU")
        if chart_docu:
            st.altair_chart(chart_docu, use_container_width=True, height=HEIGHT)
            
    with tab_matr:
        chart_matr = bar_chart_by_week(df, area_filter="MATR")
        if chart_matr:
            st.altair_chart(chart_matr, use_container_width=True, height=HEIGHT)
            
else:
    st.info("No hay actividades registradas.")