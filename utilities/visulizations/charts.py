import altair as alt
import pandas as pd
from utilities.constants.area_config import AREA_COLORS, AREA_SORTING
from utilities.ui_components.days_of_week import DAYS_OF_WEEK

# ==========================================
# Helpers
# ==========================================
def get_projects_ranked_by_hours(df):
    """
    Returns a list of project_display sorted by total hours.
    """
    if "project_display" not in df.columns or "horas" not in df.columns:
        return None
        
    summary = df.groupby("project_display")["horas"].sum().sort_values(ascending=False).reset_index()
    return summary["project_display"].tolist()

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
    df = df[df['project'].astype(str).str.strip() != ''].copy()
    
    # Sort DataFrame by AREA_SORTING mapping, then by total hours descending. 
    # To do this correctly: get hours per project_display, map area sorting, and sort.
    # We will build a helper dataframe for the sort order.
    df['project_display'] = df['area'].astype(str) + " - " + df['project'].astype(str)
    
    # Calculate sum per project_display for the secondary sort
    summary = df.groupby(['project_display', 'area'])['horas'].sum().reset_index()
    # Apply AREA_SORTING to get the primary sort key (default 99 if missing)
    summary['area_sort_idx'] = summary['area'].map(lambda x: AREA_SORTING.get(x, 99))
    
    # Sort by area index ascending, then by total hours descending
    summary = summary.sort_values(by=['area_sort_idx', 'horas'], ascending=[True, False])
    
    # The sorted list of project_display
    sorted_projects = summary['project_display'].tolist()
    
    # Base chart
    base = alt.Chart(df).encode(
        y=alt.Y("project_display:N", title="Project", sort=sorted_projects)
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
            legend=None
        ),
        tooltip=[
            alt.Tooltip("project_display:N", title="Project"), 
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

def bar_chart_by_day(df):
    """
    Create vertical bar chart for hours worked by date.
    
    Args:
        df: DataFrame with 'date', 'horas', and 'area' columns
    """
    
    # Clean data: drop rows with None or NaN dates
    df = df.dropna(subset=['date']).copy()
    
    # Map to "Dow - Month, Day" format using mapping
    def format_date_with_dow(dt):
        if pd.isna(dt): return ""
        dow = dt.strftime('%A')
        abreviated_dow = DAYS_OF_WEEK.get(dow, dow[:3]) # Fallback to 3 letters
        return f"{abreviated_dow} - {dt.strftime('%b, %d')}"
    
    df['date_display'] = pd.to_datetime(df['date']).apply(format_date_with_dow)
    # create original_date for proper sorting on the axis
    df['original_date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # Base chart
    base = alt.Chart(df).encode(
        x=alt.X("date_display:O", title="Date", sort=alt.SortField("original_date"))
    )
    
    # Bar layer
    bars = base.mark_bar(
        stroke="slategray",
        strokeWidth=0.5
    ).encode(
        y=alt.Y("sum(horas):Q", title="Total Hours", axis=alt.Axis(format=".1f")),
        color=alt.Color(
            "area:N",
            scale=alt.Scale(
                domain=list(AREA_COLORS.keys()),
                range=list(AREA_COLORS.values())
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("date_display:N", title="Date"),
            "area",
            alt.Tooltip("sum(horas):Q", format=".1f", title="Total Hours"),
            alt.Tooltip("count()", title="Entries")
        ]
    )
    
    return bars.properties(
        width="container",
        height=300
    )
