import streamlit as st
from utilities.ui_components.icons import render_icon


# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Time Tracking",
    page_icon=render_icon("logo"),
    layout="wide",
    initial_sidebar_state="expanded"
)



# Section - Reports
overview_page = st.Page("pages/1_views/1_overview.py", title="Overview", icon=render_icon("logo"))

# Section - Tools
documentation_page = st.Page("pages/2_tools/1_documentation.py", title="Documentation", icon=render_icon("documentation"))
validations_page = st.Page("pages/2_tools/2_validations.py", title="Validations", icon=render_icon("warning"))
explorer_page = st.Page("pages/2_tools/3_explorer.py", title="Explorer", icon=render_icon("search"))

# Section - Dev
staging_page = st.Page("pages/3_dev/1_staging.py", title="Staging", icon=render_icon("horas"))
intermediate_page = st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=render_icon("database"))
marts_page = st.Page("pages/3_dev/3_marts.py", title="Marts", icon=render_icon("database"))
bi_tables_page = st.Page("pages/3_dev/4_bi_tables.py", title="BI Tables", icon=render_icon("database"))

# current page
pg = st.navigation({
    "Reports": [overview_page],
    "Tools": [documentation_page, validations_page, explorer_page],
    "Dev": [staging_page, intermediate_page, marts_page, bi_tables_page]
})

# Sidebar - Utilities
with st.sidebar:
    st.divider()
    if st.button("Refresh Gsheet Data", icon=":material/refresh:", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

pg.run()
