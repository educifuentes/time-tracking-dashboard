import streamlit as st

from models.marts.bi_tables.bi_only_core_areas import bi_only_core_areas

from utilities.ui_components.icons import render_icon
from utilities.ui_components.render_model import render_model_ui

st.title(f"{render_icon('logo')} BI Tables")
st.markdown("Exploración de tablas BI")

st.subheader("bi_only_core_areas")
df = bi_only_core_areas()
if not df.empty:
    render_model_ui(df)
else:
    st.info("No hay datos en esta tabla.")