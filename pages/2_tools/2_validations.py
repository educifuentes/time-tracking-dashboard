import streamlit as st

from test.validate_activities import render_activities_validations

st.set_page_config(page_title="Validations", page_icon="✅")

st.markdown("# System Validations")
st.markdown("---")

render_activities_validations()
