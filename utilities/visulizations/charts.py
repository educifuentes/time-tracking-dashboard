import altair as alt
import pandas as pd
from utilities.ui_components.colors import AREA_COLORS

# ==========================================
# Helpers
# ==========================================
def get_projects_ranked_by_hours(df):
    """
    Returns a list of projects sorted by total hours.
    """
    if "project" not in df.columns or "horas" not in df.columns:
        return None
        
    summary = df.groupby("project")["horas"].sum().sort_values(ascending=False).reset_index()
    return summary["project"].tolist()

# ==========================================
# Project & Hours Charts
# ==========================================
def bar_chart_by_project(df):
    """
    Create horizontal bar chart for hours worked by project.
    
    Args:
        df: DataFrame with 'project' and 'horas' columns
    """
    
    # Clean data: drop rows with None, NaN or empty project names
    df = df.dropna(subset=['project'])
    df = df[df['project'].astype(str).str.strip() != '']
    
    # Get unique items in the dataframe ranked by amount
    projects = get_projects_ranked_by_hours(df)
    
    # Base chart
    base = alt.Chart(df).encode(
        y=alt.Y("project:N", title="Project", sort=projects)
    )
    
    # Bar layer
    bars = base.mark_bar(
        stroke="slategray",
        strokeWidth=0.5
    ).encode(
        x=alt.X("sum(horas):Q", title="Total Hours", axis=alt.Axis(format=".1f")),
        color=alt.Color(
            "area:N",
            scale=alt.Scale(
                domain=list(AREA_COLORS.keys()),
                range=list(AREA_COLORS.values())
            ),
            legend=alt.Legend(title="Área")
        ),
        tooltip=[
            "project", 
            alt.Tooltip("sum(horas):Q", format=".1f", title="Total Hours"),
            "area",
            alt.Tooltip("count()", title="Entries")
        ]
    )
    
    # Text layer for total hours at the end of each bar
    text = base.mark_text(
        align='left',
        baseline='middle',
        dx=5,
        fontWeight='bold',
        color='gray'
    ).encode(
        x=alt.X("sum(horas):Q", stack=None),
        text=alt.Text("sum(horas):Q", format=".1f")
    )
    
    return (bars + text).properties(
        width="container",
        height=alt.Step(40), # Dynamic height based on number of projects
    )
