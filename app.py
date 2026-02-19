import streamlit as st


# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Spendee Dashboard :material/paid:",
    page_icon=":material/paid:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Section - Reports
overview_page = st.Page("pages/1_views/1_overview.py", title="Overview", icon=":material/dashboard:")

# Section - Tools
documentation_page = st.Page("pages/2_tools/1_documentation.py", title="Documentation", icon=":material/description:")
validations_page = st.Page("pages/2_tools/2_validations.py", title="Validations", icon=":material/warning:")
explorer_page = st.Page("pages/2_tools/3_explorer.py", title="Explorer", icon=":material/search:")

# Section - Dev
staging_page = st.Page("pages/3_dev/1_staging.py", title="Staging", icon=":material/database:")
intermediate_page = st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=":material/database:")
marts_page = st.Page("pages/3_dev/3_marts.py", title="Marts", icon=":material/database:")
bi_tables_page = st.Page("pages/3_dev/4_bi_tables.py", title="BI Tables", icon=":material/database:")

# current page
pg = st.navigation({
    "Reports": [overview_page],
    "Tools": [documentation_page, validations_page, explorer_page],
    "Dev": [staging_page, intermediate_page, marts_page, bi_tables_page]
})

pg.run()
