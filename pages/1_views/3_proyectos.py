import streamlit as st
import pandas as pd
import altair as alt

from models.marts.fct_activities import fct_activities
from utilities.ui_components.render_model import render_model_ui
from utilities.ui_components.icons import render_icon
from utilities.constants.area_config import AREA_SORTING

st.title(f"{render_icon('logo')} Proyectos")
st.markdown("Detalle del tiempo registrado por proyecto")

# Load data
df = fct_activities()

if df.empty:
    st.info("No hay actividades registradas.")
    st.stop()

# Create a display name for the project, adding a prefix of the adhoc area
df['project_display'] = df['area'].astype(str) + " - " + df['project'].astype(str)

# Calculate sum per project_display
summary = df.groupby(['project_display', 'area'], observed=False)['horas'].sum().reset_index()

# Apply AREA_SORTING to get the primary sort key (default 99 if missing)
summary['area_sort_idx'] = summary['area'].map(lambda x: AREA_SORTING.get(x, 99))

# Sort by area index ascending, then by total hours descending
summary = summary.sort_values(by=['area_sort_idx', 'horas'], ascending=[True, False])

# The sorted list of project_display
projects_sorted = summary['project_display'].tolist()

for proj_disp in projects_sorted:
    if str(proj_disp).strip() == "" or str(proj_disp).endswith("nan") or str(proj_disp).endswith(" - "):
        continue
    
    df_proj = df[df["project_display"] == proj_disp].copy()
    if df_proj.empty:
        continue
        
    total_hours = df_proj["horas"].sum()
    st.subheader(f"{proj_disp} - {total_hours:.1f}h")
    
    # Altair chart: task on Y-axis and hours on X-axis, stacking automatically to show individual entries in tooltip
    chart = alt.Chart(df_proj).mark_bar(
        stroke="slategray",
        strokeWidth=0.5
    ).encode(
        y=alt.Y("task:N", title="Tarea", sort=alt.EncodingSortField(field="horas", op="sum", order="descending")),
        x=alt.X("horas:Q", title="Horas Invertidas"),
        color=alt.Color("task:N", legend=None),
        tooltip=[
            alt.Tooltip("task:N", title="Tarea"),
            alt.Tooltip("subtask:N", title="Subtarea"),
            alt.Tooltip("horas:Q", format=".1f", title="Horas"),
            alt.Tooltip("note:N", title="Nota"),
            alt.Tooltip("date:T", title="Fecha", format="%Y-%m-%d")
        ]
    ).properties(
        width="container"
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    with st.expander(f"Ver Registros: {proj_disp}"):
        render_model_ui(df_proj)
    
    st.divider()