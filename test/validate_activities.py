import streamlit as st
import pandas as pd

from models.marts.fct_activities import fct_activities

def render_activities_validations():
    st.title("Data Validation: fct_activities")

    # Load data
    df = fct_activities()

    st.markdown("### Horas that are over 4 hours")
    over_4 = df[df["horas"] > 4]
    st.write(f"Found **{len(over_4)}** records where 'horas' is over 4.")
    st.dataframe(over_4)

    st.markdown("### Distinct values of project")
    distinct_projects = df["project"].dropna().unique()
    st.write(f"Found **{len(distinct_projects)}** distinct projects.")
    st.dataframe(pd.DataFrame(distinct_projects, columns=["Project"]))

    st.markdown("### Rows with empty subarea or area")
    empty_area_subarea = df[df["area"].isna() | (df["area"] == "") | (df["area"] == "nan") |
                            df["subarea"].isna() | (df["subarea"] == "") | (df["subarea"] == "nan")]
    st.write(f"Found **{len(empty_area_subarea)}** records with empty area or subarea.")
    st.dataframe(empty_area_subarea)

    st.markdown("### Rows with empty date")
    empty_date = df[df["date"].isna()]
    st.write(f"Found **{len(empty_date)}** records with empty date.")
    st.dataframe(empty_date)

    st.markdown("### Negative or Zero Hours")
    invalid_hours = df[df["horas"] <= 0]
    st.write(f"Found **{len(invalid_hours)}** records with 0 or negative hours.")
    st.dataframe(invalid_hours)

    st.markdown("### Missing Subtasks")
    missing_subtasks = df[df["subtask"].isna() | (df["subtask"] == "") | (df["subtask"] == "nan")]
    st.write(f"Found **{len(missing_subtasks)}** records with missing subtask.")
    st.dataframe(missing_subtasks)

    st.markdown("### Potential Duplicates")
    duplicates = df[df.duplicated(subset=["date", "project", "task", "min"], keep=False)]
    st.write(f"Found **{len(duplicates)}** potential duplicate entries (matching date, project, task, and min).")
    st.dataframe(duplicates)

if __name__ == "__main__":
    render_activities_validations()
