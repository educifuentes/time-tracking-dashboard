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


# ==========================================
# Section 2: Project Detail Drill-down
# ==========================================
st.subheader("Detalle por Proyecto")

# Build sorted project list for the selectbox
summary = df.groupby(['project', 'area'], observed=False)['horas'].sum().reset_index()
summary['area_sort_idx'] = summary['area'].map(lambda x: AREA_SORTING.get(x, 99))
summary = summary.sort_values(by=['area_sort_idx', 'horas'], ascending=[True, False])

valid_projects = [
    p for p in summary['project'].tolist()
    if str(p).strip() != "" and str(p) != "nan"
]

selected_project = st.selectbox(
    "Selecciona un proyecto",
    valid_projects,
    label_visibility="collapsed"
)

if selected_project:
    df_proj = df[df["project"] == selected_project].copy()

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
            y=alt.Y("task:N", title="Tarea", sort=alt.EncodingSortField(field="horas", op="sum", order="descending")),
            x=alt.X("sum(horas):Q", title="Horas Invertidas", axis=alt.Axis(format=".1f")),
            tooltip=[
                alt.Tooltip("task:N", title="Tarea"),
                alt.Tooltip("subtask:N", title="Subtarea"),
                alt.Tooltip("sum(horas):Q", format=".1f", title="Horas"),
                alt.Tooltip("note:N", title="Nota"),
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
            y=alt.Y("task:N", sort=alt.EncodingSortField(field="horas", op="sum", order="descending")),
            x=alt.X("sum(horas):Q", stack=None),
            text=alt.Text("sum(horas):Q", format=".1f")
        )

        st.altair_chart(chart_proj + text_proj, use_container_width=True)

# ==========================================
# Section 1: Tabs per Area
# ==========================================
st.divider()

tab_labels = ["All"] + sorted(AREA_CORE, key=lambda a: AREA_SORTING.get(a, 99))
tabs = st.tabs(tab_labels)

for tab, label in zip(tabs, tab_labels):
    with tab:
        if label == "All":
            df_tab = df.copy()
        else:
            df_tab = df[df["area"] == label].copy()

        df_tab = df_tab.dropna(subset=["project"])
        df_tab = df_tab[df_tab["project"].astype(str).str.strip() != ""]

        if df_tab.empty:
            st.info("No hay actividades para esta área.")
        else:
            chart = bar_chart_by_project(df_tab, add_area_prefix=False)
            st.altair_chart(chart, use_container_width=True, height=600)

