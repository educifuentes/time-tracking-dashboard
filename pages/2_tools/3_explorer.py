import streamlit as st
from utilities.ui_components.icons import render_icon

from models.marts.fct_activities import fct_activities

st.title(f"{render_icon('logo')} Explorer")
st.markdown("Explore the data")

# Load data
df = fct_activities()

if not df.empty:
    st.subheader("Activities")
    st.dataframe(df)
else:
    st.info("No activities registered.")
