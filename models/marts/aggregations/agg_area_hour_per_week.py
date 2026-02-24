import pandas as pd

from models.marts.bi_tables.bi_only_core_areas import bi_only_core_areas

def agg_area_hour_per_week():
    df = bi_only_core_areas()
    
    pivot_df = df.pivot_table(
        index="week",
        columns="area",
        values="horas",
        aggfunc="sum",
        fill_value=0
    ).reset_index()
    
    return pivot_df