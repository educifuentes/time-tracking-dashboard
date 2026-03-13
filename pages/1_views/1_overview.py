import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from models.marts.fct_activities import fct_activities

from utilities.ui_components.render_model import render_model_ui
from utilities.visulizations.charts import bar_chart_by_project, bar_chart_by_day, bar_chart_by_area

from utilities.ui_components.icons import render_icon

st.title(f"{render_icon('logo')} Horas")

st.markdown("[Ir a Ghseet](https://docs.google.com/spreadsheets/d/1I-nQVWT9XP1p0DLbgvpCMWjzQ8i6CqbTM1E9g4oCzDY/edit?gid=1838766383#gid=1838766383)")
    

# Load data
df = fct_activities()

st.markdown("Date range " + f"{df['date'].min()} - {df['date'].max()}")

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

# Layout: Today and This Week in columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hoy")
    df_today = df[df["date"] == today]
    display_dashboard_section(df_today)

with col2:
    st.subheader("Semana")

    # Calculations for "This Week" (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    iso_week = today.isocalendar()[1]
    week_start_fmt = pd.Timestamp(start_of_week).strftime("%b %-d")
    week_today_fmt = pd.Timestamp(today).strftime("%b %-d")
    st.caption(f"W{iso_week} · {week_start_fmt} — {week_today_fmt}")
    
    df_week = df[(df["date"] >= start_of_week) & (df["date"] <= end_of_week)]
    
    if not df_week.empty:
        total_hours = df_week["horas"].sum()
        st.metric("Total Horas", f"{total_hours:.1f}h")
        
        tab1, tab2, tab3 = st.tabs(["by Area", "Daily", "by Project"])


        with tab1:
            chart_area = bar_chart_by_area(df_week)
            st.altair_chart(chart_area, use_container_width=True)
        
        with tab3:
            chart_daily = bar_chart_by_day(df_week, short_date_format=True)
            st.altair_chart(chart_daily, use_container_width=True)
            
        with tab2:
            chart_proj = bar_chart_by_project(df_week)
            st.altair_chart(chart_proj, use_container_width=True)

    else:
        st.info("No hay actividades registradas en la semana.")

# Layout: This Month at the bottom
st.divider()
st.subheader("Mes")
# Calculations for "This Month"
start_of_month = today.replace(day=1)
# Simple way to get end of month for sorting/filtering
next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
end_of_month = next_month - timedelta(days=1)

df_month = df[(df["date"] >= start_of_month) & (df["date"] <= end_of_month)]
display_dashboard_section(df_month)

# Layout: Dynamic chart for given history
st.divider()

st.subheader("Trends")

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
    df_history = df[(df["date"] >= start_date) & (df["date"] <= today)]
elif history_option == "Últimos 30 Días":
    start_date = today - timedelta(days=29)
    df_history = df[(df["date"] >= start_date) & (df["date"] <= today)]
else:
    df_history = df[df["date"] <= today]

if not df_history.empty:
    history_chart = bar_chart_by_day(df_history)
    st.altair_chart(history_chart, use_container_width=True)
else:
    st.info(f"No hay actividades para mostrar en {history_option.lower()}.")

