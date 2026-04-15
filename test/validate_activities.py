import streamlit as st
import pandas as pd

from models.marts.fct_activities import fct_activities
from helpers.ui_components.render_trouble_rows import render_troubled_rows

def render_activities_validations():
    st.title("Data Validation: fct_activities")

    # Load data
    df = fct_activities()
    
    # Assume gid "0" for the main horas worksheet (update if different)
    sheet_gid = "0"

    st.markdown("### Horas that are over 4 hours")
    over_4 = df[df["horas"] > 4]
    st.write(f"Found **{len(over_4)}** records where 'horas' is over 4.")
    if not over_4.empty:
        render_troubled_rows(over_4, gid=sheet_gid, source="gsheets")

    st.markdown("### Distinct values of project")
    distinct_projects = df["project"].dropna().unique()
    st.write(f"Found **{len(distinct_projects)}** distinct projects.")
    st.dataframe(pd.DataFrame(distinct_projects, columns=["Project"]))

    st.markdown("### Rows with empty subarea or area")
    empty_area_subarea = df[df["area"].isna() | (df["area"] == "") | (df["area"] == "nan") |
                            df["subarea"].isna() | (df["subarea"] == "") | (df["subarea"] == "nan")]
    st.write(f"Found **{len(empty_area_subarea)}** records with empty area or subarea.")
    if not empty_area_subarea.empty:
        render_troubled_rows(empty_area_subarea, gid=sheet_gid, source="gsheets")

    st.markdown("### Rows with empty date")
    empty_date = df[df["date"].isna()]
    st.write(f"Found **{len(empty_date)}** records with empty date.")
    if not empty_date.empty:
        render_troubled_rows(empty_date, gid=sheet_gid, source="gsheets")

    st.markdown("### Negative or Zero Hours")
    invalid_hours = df[df["horas"] <= 0]
    st.write(f"Found **{len(invalid_hours)}** records with 0 or negative hours.")
    if not invalid_hours.empty:
        render_troubled_rows(invalid_hours, gid=sheet_gid, source="gsheets")

    st.markdown("### Missing Subtasks")
    missing_subtasks = df[df["subtask"].isna() | (df["subtask"] == "") | (df["subtask"] == "nan")]
    st.write(f"Found **{len(missing_subtasks)}** records with missing subtask.")
    if not missing_subtasks.empty:
        render_troubled_rows(missing_subtasks, gid=sheet_gid, source="gsheets")

    st.markdown("### Potential Duplicates")
    duplicates = df[df.duplicated(subset=["date", "project", "task", "min"], keep=False)]
    st.write(f"Found **{len(duplicates)}** potential duplicate entries (matching date, project, task, and min).")
    if not duplicates.empty:
        render_troubled_rows(duplicates, gid=sheet_gid, source="gsheets")

if __name__ == "__main__":
    render_activities_validations()
