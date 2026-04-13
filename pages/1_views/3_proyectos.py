import streamlit as st
import pandas as pd
import altair as alt

from models.marts.fct_activities import fct_activities

from helpers.ui_components.icons import render_icon
from helpers.constants.area_config import AREA_SORTING, AREA_COLORS, AREA_CORE
from helpers.visulizations.charts import bar_chart_by_project

st.title(f"{render_icon('logo')} Proyectos")
st.markdown("Detalle del tiempo registrado por proyecto")

# Load data
df = fct_activities()

if df.empty:
    st.info("No hay actividades registradas.")
    st.stop()


# Define the areas to show in tabs
tab_areas = ["MATR", "DOCU", "DATA", "Todas"]
tabs = st.tabs(tab_areas)

for tab, current_area in zip(tabs, tab_areas):
    with tab:
        # Filter the main dataframe for the current area tab
        if current_area == "Todas":
            df_area = df.copy()
        else:
            df_area = df[df["area"] == current_area].copy()
        
        # ==========================================
        # Section: Project Detail Drill-down
        # ==========================================
        st.subheader("Detalle por Proyecto")
        
        # Build sorted project list for the selectbox
        summary = df_area.groupby('project', observed=False)['horas'].sum().reset_index()
        summary = summary.sort_values(by='horas', ascending=False)
        
        valid_projects = [
            p for p in summary['project'].tolist()
            if str(p).strip() != "" and str(p) != "nan"
        ]
        
        selected_project = st.selectbox(
            "Selecciona un proyecto",
            options=valid_projects,
            label_visibility="collapsed",
            key=f"selectbox_proj_{current_area}"
        )
        
        if selected_project:
            df_proj = df_area[df_area["project"] == selected_project].copy()
        
            if df_proj.empty:
                st.info("No hay registros para este proyecto.")
            else:
                total_hours = df_proj["horas"].sum()
                st.caption(f"Total: **{total_hours:.1f}h**")
        
                area_color = AREA_COLORS.get(df_proj['area'].iloc[0], "#888888")
        
                chart_proj = alt.Chart(df_proj).mark_bar(
                    stroke="slategray",
                    strokeWidth=0.5,
                    color=area_color
                ).encode(
                    y=alt.Y("subarea:N", title="Subárea", sort=alt.EncodingSortField(field="horas", op="sum", order="descending")),
                    x=alt.X("sum(horas):Q", title="Horas Invertidas", axis=alt.Axis(format=".1f")),
                    tooltip=[
                        alt.Tooltip("subarea:N", title="Subárea"),
                        alt.Tooltip("sum(horas):Q", format=".1f", title="Horas"),
                        alt.Tooltip("count()", title="Entradas")
                    ]
                ).properties(
                    width="container",
                    height=alt.Step(35)
                )
        
                # Text labels
                text_proj = alt.Chart(df_proj).mark_text(
                    align='left',
                    baseline='middle',
                    dx=5,
                    fontWeight='bold',
                    color='gray'
                ).encode(
                    y=alt.Y("subarea:N", sort=alt.EncodingSortField(field="horas", op="sum", order="descending")),
                    x=alt.X("sum(horas):Q", stack=None),
                    text=alt.Text("sum(horas):Q", format=".1f")
                )
        
                st.altair_chart(chart_proj + text_proj, use_container_width=True)
        
        # ==========================================
        # Section: Overview per Area
        # ==========================================
        st.divider()
        st.subheader(f"Todos los proyectos en {current_area}")
        
        df_area_clean = df_area.dropna(subset=["project"])
        df_area_clean = df_area_clean[df_area_clean["project"].astype(str).str.strip() != ""]
        
        if df_area_clean.empty:
            st.info("No hay actividades para esta área.")
        else:
            chart = bar_chart_by_project(df_area_clean, add_area_prefix=False)
            st.altair_chart(chart, use_container_width=True, height=600)

