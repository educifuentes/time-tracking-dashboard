import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from models.marts.fct_activities import fct_activities

from utilities.ui_components.render_model import render_model_ui
from utilities.visulizations.charts import bar_chart_by_project

from utilities.ui_components.icons import render_icon

st.title(f"{render_icon('logo')} Horas")

    

# Load data
df = fct_activities()

st.markdown("Date range " + f"{df['date'].min().date()} - {df['date'].max().date()}")

def display_dashboard_section(filtered_df, label):
    if not filtered_df.empty:
        st.subheader(f"{label}")

        total_hours = filtered_df["horas"].sum()
        st.metric("Total Horas", f"{total_hours:.1f}h")
        
        chart = bar_chart_by_project(filtered_df)
        st.altair_chart(chart, use_container_width=True)
        
        st.divider()
        with st.expander("Ver Detalle de Actividades"):
            render_model_ui(filtered_df)
    else:
        st.info(f"No hay actividades registradas para {label.lower()}.")

# Reference date (Today)
today = pd.Timestamp.now().normalize()

# Layout: Today and This Week in columns
col1, col2 = st.columns(2)

with col1:
    with st.container(height=600):
        df_today = df[df["date"].dt.date == today.date()]
        display_dashboard_section(df_today, "Hoy")

with col2:
    with st.container(height=600):
        # Calculations for "This Week" (Monday to Sunday)
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        df_week = df[(df["date"] >= start_of_week) & (df["date"] <= end_of_week)]
        display_dashboard_section(df_week, "Semana")

# Layout: This Month at the bottom
st.divider()
st.subheader("Mes")
# Calculations for "This Month"
start_of_month = today.replace(day=1)
# Simple way to get end of month for sorting/filtering
next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
end_of_month = next_month - timedelta(days=1)

df_month = df[(df["date"] >= start_of_month) & (df["date"] <= end_of_month)]
display_dashboard_section(df_month, "Este Mes")

