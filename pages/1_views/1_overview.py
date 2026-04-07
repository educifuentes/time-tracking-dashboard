import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from models.marts.fct_activities import fct_activities

from helpers.ui_components.render_model import render_model_ui
from helpers.visulizations.charts import bar_chart_by_project, bar_chart_by_day, bar_chart_by_area
from helpers.constants.day_codes import DAYS_ES, MONTHS_ES

from helpers.ui_components.icons import render_icon

st.title(f"{render_icon('logo')} Horas")

st.markdown("[Ir a Ghseet](https://docs.google.com/spreadsheets/d/1I-nQVWT9XP1p0DLbgvpCMWjzQ8i6CqbTM1E9g4oCzDY/edit?gid=1838766383#gid=1838766383)")
    

# Load data
df = fct_activities()


def display_dashboard_section(filtered_df):
    if not filtered_df.empty:

        total_hours = filtered_df["horas"].sum()
        st.metric("Total Horas", f"{total_hours:.1f}h")
        
        chart = bar_chart_by_project(filtered_df)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No hay actividades registradas.")

# Reference date (Today)
today = pd.Timestamp.now(tz='America/Santiago').date()

# Calculations for "This Week" (Monday to Sunday)
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)
iso_week = today.isocalendar()[1]
week_start_fmt = pd.Timestamp(start_of_week).strftime("%b %-d")
week_today_fmt = pd.Timestamp(today).strftime("%b %-d")
df_week = df[(df["date"] >= start_of_week) & (df["date"] <= end_of_week)]

# Layout First Row: Hoy and Resumen Diario
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hoy")
    today_fmt = f"{DAYS_ES[today.weekday()]} {today.day}, {MONTHS_ES[today.month - 1]}"
    st.caption(today_fmt)
    df_today = df[df["date"] == today]
    display_dashboard_section(df_today)

with col2:
    st.subheader("Resumen Diario")
    st.caption(f"Semana {iso_week} · {week_start_fmt} — {week_today_fmt}")
    if not df_week.empty:
        chart_daily = bar_chart_by_day(df_week, short_date_format=True, sort_descending=True)
        st.altair_chart(chart_daily, use_container_width=True)
    else:
        st.info("No hay actividades registradas en la semana.")

st.divider()

# Layout Second Row: Semana and Mes
col3, col4 = st.columns(2)

with col3:
    st.subheader("Semana Metas")
    st.caption(f"W{iso_week} · {week_start_fmt} — {week_today_fmt}")
    
    if not df_week.empty:
        total_hours = df_week["horas"].sum()
        st.metric("Total Horas", f"{total_hours:.1f}h")
        
        tab1, tab2 = st.tabs(["by Area", "by Project"])

        with tab1:
            chart_area = bar_chart_by_area(df_week)
            st.altair_chart(chart_area, use_container_width=True)
            
        with tab2:
            chart_proj = bar_chart_by_project(df_week)
            st.altair_chart(chart_proj, use_container_width=True)
    else:
        st.info("No hay actividades registradas en la semana.")

with col4:
    st.subheader("Mes")
    # Calculations for "This Month"
    start_of_month = today.replace(day=1)
    # Simple way to get end of month for sorting/filtering
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    end_of_month = next_month - timedelta(days=1)
    
    df_month = df[(df["date"] >= start_of_month) & (df["date"] <= end_of_month)]
    display_dashboard_section(df_month)

