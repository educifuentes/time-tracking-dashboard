import streamlit as st

from models.marts.fct_activities import fct_activities

from helpers.ui_components.icons import render_icon
from helpers.ui_components.render_model import render_model_ui

st.title(f"{render_icon('logo')} BI Tables")
st.markdown("Exploración de tablas BI")

st.subheader("fct_activities")
df = fct_activities()
if not df.empty:
    render_model_ui(df, "fct_activities")
else:
    st.info("No hay datos en esta tabla.")