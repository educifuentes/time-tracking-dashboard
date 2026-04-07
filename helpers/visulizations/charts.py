import altair as alt
import pandas as pd
from helpers.constants.area_config import AREA_COLORS, AREA_SORTING, AREA_CORE
from helpers.ui_components.days_of_week import DAYS_OF_WEEK
from helpers.constants.day_codes import DAY_CODES
from helpers.constants.targets import HOUR_TARGET_BY_AREA

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
def bar_chart_by_project(df, add_area_prefix=True):
    """
    Create horizontal bar chart for hours worked by project.
    
    Args:
        df: DataFrame with 'project' and 'horas' columns
        add_area_prefix: If True (default), Y axis shows 'AREA - Project'. If False, shows just project name.
    """
    
    # Clean data: drop rows with None, NaN or empty project names
    df = df.dropna(subset=['project'])
    df = df[df['project'].astype(str).str.strip() != ''].copy()
    
    # Sort DataFrame by AREA_SORTING mapping, then by total hours descending. 
    # To do this correctly: get hours per project_display, map area sorting, and sort.
    # We will build a helper dataframe for the sort order.
    if add_area_prefix:
        df['project_display'] = df['area'].astype(str) + " - " + df['project'].astype(str)
    else:
        df['project_display'] = df['project'].astype(str)
    
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

def bar_chart_by_area(df):
    """
    Create horizontal bar chart for total hours per area.
    Only areas present in the input df are shown (avoids categorical bleed-through).

    Args:
        df: DataFrame with 'area' and 'horas' columns
    """
    if df.empty or "area" not in df.columns:
        return None

    # Cast to str to shed any Categorical dtype (which would preserve all levels)
    df = df.copy()
    df["area"] = df["area"].astype(str)

    summary = df.groupby("area", sort=False)["horas"].sum().reset_index()
    
    # Guarantee all core areas are present, even if they have 0 hours. Drop any non-core areas.
    all_areas_df = pd.DataFrame({"area": AREA_CORE})
    summary = all_areas_df.merge(summary, on="area", how="left").fillna({"horas": 0})
    
    # Sort areas by AREA_SORTING mapping
    summary['sort_idx'] = summary['area'].map(lambda x: AREA_SORTING.get(x, 99))
    summary = summary.sort_values('sort_idx')
    present_areas = summary["area"].tolist()

    base = alt.Chart(summary).encode(
        y=alt.Y("area:N", title="Área", sort=present_areas)
    )

    bars = base.mark_bar(
        stroke="slategray",
        strokeWidth=0.5
    ).encode(
        x=alt.X("horas:Q", title="Total Horas", scale=alt.Scale(domain=[0, 25]), axis=alt.Axis(format="d")),
        color=alt.Color(
            "area:N",
            scale=alt.Scale(
                domain=list(AREA_COLORS.keys()),
                range=list(AREA_COLORS.values())
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("area:N", title="Área"),
            alt.Tooltip("horas:Q", format=".1f", title="Total Horas")
        ]
    )

    text = base.mark_text(
        align="left",
        baseline="middle",
        dx=5,
        fontWeight="bold",
        color="gray"
    ).encode(
        x=alt.X("horas:Q", stack=None),
        text=alt.Text("horas:Q", format=".1f")
    )

    # Build a vertical tick for each present area at the target value
    targets_data = pd.DataFrame([
        {"area": a, "target": HOUR_TARGET_BY_AREA[a]}
        for a in present_areas
        if a in HOUR_TARGET_BY_AREA
    ])

    if not targets_data.empty:
        target_rules = alt.Chart(targets_data).mark_tick(
            color="red",
            thickness=2,
            strokeDash=[4, 3]
        ).encode(
            x=alt.X("target:Q"),
            y=alt.Y("area:N", sort=present_areas),
            tooltip=[alt.Tooltip("area:N", title="Área"), alt.Tooltip("target:Q", title="Objetivo")]
        )
        chart = bars + text + target_rules
    else:
        chart = bars + text

    return chart.properties(
        width="container",
        height=alt.Step(40)
    )

def bar_chart_by_day(df, short_date_format=False, area_filter=None, sort_descending=False):
    """
    Create vertical bar chart for hours worked by date.
    
    Args:
        df: DataFrame with 'date', 'horas', and 'area' columns
        short_date_format: If True, uses abbreviated format like 'Mon 12'
        area_filter: Optional string to filter by a specific area
        sort_descending: If True, sorts dates from most recent to oldest
    """
    if df.empty or "date" not in df.columns:
        return None
        
    # Clean data: drop rows with None or NaN dates
    df = df.dropna(subset=['date']).copy()
    
    if area_filter:
        df = df[df['area'] == area_filter]
    
    # Map to "Dow - Month, Day" format using mapping
    def format_date_with_dow(dt):
        if pd.isna(dt): return ""
        dow = dt.strftime('%A')
        if short_date_format:
            abreviated_dow = DAY_CODES.get(dow, dow[:3])
            return f"{abreviated_dow} {dt.day}"
        else:
            abreviated_dow = DAYS_OF_WEEK.get(dow, dow[:3]) # Fallback to 3 letters
            return f"{abreviated_dow} - {dt.strftime('%b, %d')}"
    
    df['date_display'] = pd.to_datetime(df['date']).apply(format_date_with_dow)
    # create original_date for proper sorting on the axis
    df['original_date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # Base chart
    # Sort the dataframe to get the exact order of 'date_display' we want
    sorted_df = df[['date_display', 'original_date']].drop_duplicates().sort_values('original_date', ascending=not sort_descending)
    sorted_dates = sorted_df['date_display'].tolist()
    
    base = alt.Chart(df).encode(
        y=alt.Y("date_display:O", title="Fecha", sort=sorted_dates)
    )
    
    # Bar layer
    bars = base.mark_bar(
        stroke="slategray",
        strokeWidth=0.5
    ).encode(
        x=alt.X("sum(horas):Q", title="Total Horas", axis=alt.Axis(format=".1f")),
        color=alt.Color(
            "area:N",
            scale=alt.Scale(
                domain=list(AREA_COLORS.keys()),
                range=list(AREA_COLORS.values())
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("date_display:N", title="Fecha"),
            "area",
            alt.Tooltip("sum(horas):Q", format=".1f", title="Total Horas"),
            alt.Tooltip("count()", title="Entries")
        ]
    )
    
    # Text layer for total hours at the end of each bar
    text = base.mark_text(
        align='left',
        baseline='middle',
        dx=5,
        fontWeight='bold',
        color='slategray'
    ).encode(
        x=alt.X("sum(horas):Q", stack=None),
        text=alt.Text("sum(horas):Q", format=".1f")
    )
    
    return (bars + text).properties(
        width="container",
        height=400
    )

def bar_chart_by_week(df, area_filter=None):
    """
    Create vertical bar chart for hours worked by week.
    
    Args:
        df: DataFrame pivoted by week and area
        area_filter: Optional string to filter by a specific area
    """
    if df.empty or "week" not in df.columns:
        return None
        
    areas = [col for col in df.columns if col != 'week']
    df_melted = df.melt(id_vars=['week'], value_vars=areas, var_name='area', value_name='horas')
    
    if area_filter:
        df_melted = df_melted[df_melted['area'] == area_filter]
        
    # Base chart - week on y axis
    base = alt.Chart(df_melted).encode(
        y=alt.Y("week:O", title="Semana", sort='descending')
    )
    
    # Bar layer
    bars = base.mark_bar(
        stroke="slategray",
        strokeWidth=0.5
    ).encode(
        x=alt.X("horas:Q", title="Total Horas", scale=alt.Scale(domain=[0, 50]), axis=alt.Axis(format="d")),
        color=alt.Color(
            "area:N",
            scale=alt.Scale(
                domain=list(AREA_COLORS.keys()),
                range=list(AREA_COLORS.values())
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("week:O", title="Semana"),
            "area",
            alt.Tooltip("horas:Q", format=".1f", title="Total Horas")
        ]
    )
    
    # Text layer for total hours at the end of each bar
    text = base.mark_text(
        align='left',
        baseline='middle',
        dx=5,
        fontWeight='bold',
        color='slategray'
    ).encode(
        x=alt.X("sum(horas):Q", stack=None),
        text=alt.Text("sum(horas):Q", format=".1f")
    )

    return (bars + text).properties(
        width="container",
        height=400
    )

