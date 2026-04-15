import streamlit as st
import importlib.util
import os
import sys

# Dynamically import the local test/validate_activities.py to avoid conflicting 
# with the Python standard library's 'test' module
spec = importlib.util.spec_from_file_location(
    "local_validate_activities",
    os.path.join(os.getcwd(), "test", "validate_activities.py")
)
validate_activities = importlib.util.module_from_spec(spec)
sys.modules["local_validate_activities"] = validate_activities
spec.loader.exec_module(validate_activities)

st.set_page_config(page_title="Validations", page_icon="✅")

st.markdown("# System Validations")
st.markdown("---")

validate_activities.render_activities_validations()
