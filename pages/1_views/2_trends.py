import streamlit as st
import pandas as pd
import altair as alt

from datetime import timedelta

from models.marts.aggregations.agg_area_hour_per_week import agg_area_hour_per_week
from models.marts.fct_activities import fct_activities

from helpers.ui_components.icons import render_icon
from helpers.visulizations.charts import bar_chart_by_week, bar_chart_by_day

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

st.divider()

st.subheader("Tendencia Diaria")

# Daily Activities Data for the Daily Trends
df_act = fct_activities()
today = pd.Timestamp.now(tz='America/Santiago').date()

col_filter, col_dummy1, col_dummy2 = st.columns(3)
with col_filter:
    history_option = st.selectbox(
        "Filtro de Tiempo",
        ["Últimos 15 Días", "Últimos 30 Días", "Todo el Historial"],
        label_visibility="collapsed"
    )

st.write("") # small spacing

if history_option == "Últimos 15 Días":
    start_date = today - timedelta(days=14)
    df_history = df_act[(df_act["date"] >= start_date) & (df_act["date"] <= today)]
elif history_option == "Últimos 30 Días":
    start_date = today - timedelta(days=29)
    df_history = df_act[(df_act["date"] >= start_date) & (df_act["date"] <= today)]
else:
    df_history = df_act[df_act["date"] <= today]

if not df_history.empty:
    history_chart = bar_chart_by_day(df_history, sort_descending=True)
    st.altair_chart(history_chart, use_container_width=True)
else:
    st.info(f"No hay actividades para mostrar en {history_option.lower()}.")