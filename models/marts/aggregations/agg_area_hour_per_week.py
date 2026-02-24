import pandas as pd
from models.marts.fct_activities import fct_activities

def agg_area_hour_per_week():
    df = fct_activities()
    
    pivot_df = df.pivot_table(
        index="week",
        columns="area",
        values="horas",
        aggfunc="sum",
        fill_value=0
    ).reset_index()
    
    return pivot_df