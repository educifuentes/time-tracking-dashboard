import streamlit as st
import streamlit_mermaid as st_mm

from helpers.widgets.generate_lineage_chart import generate_lineage_chart

def render_model_lineage(df):
    """
    Renders the Mermaid diagram and provides an expander for raw metadata.
    """
    st.subheader("Data Lineage")
    
    mermaid_code = generate_lineage_chart(df)
    
    st_mm.st_mermaid(mermaid_code, height=400)
    
    with st.expander("Raw Metadata"):
        st.write(df.attrs)


