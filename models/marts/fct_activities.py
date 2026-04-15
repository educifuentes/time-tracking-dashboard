import pandas as pd
from models.staging._stg_horas import stg_horas

def fct_activities():
    df = stg_horas()

    # Convert date column to temporary datetime series and drop nulls
    dt_series = pd.to_datetime(df["date"], errors='coerce')
    
    # Drop rows where date is NaT to prevent comparing a date with float later
    df = df[dt_series.notna()].copy()
    dt_series = dt_series.dropna()
    
    # extra date columns
    df["year"] = dt_series.dt.year
    df["month"] = dt_series.dt.month
    df["dow"] = dt_series.dt.dayofweek
    week_start = dt_series - pd.to_timedelta(dt_series.dt.dayofweek, unit='d')
    
    # Format week strings using year-Wweek (e.g. 2024-W42 - Oct 14)
    iso_year = dt_series.dt.isocalendar().year.astype(str)
    iso_week = dt_series.dt.isocalendar().week.astype(str).str.zfill(2)
    df["week"] = iso_year + "-W" + iso_week + " - " + week_start.dt.strftime('%b %d')
    
    # Finally, set the date column to only store dates
    df["date"] = dt_series.dt.date
    
    # Numeric columns
    df["min"] = pd.to_numeric(df["min"], errors='coerce')
    df["horas"] = pd.to_numeric(df["horas"], errors='coerce')

    
    # Categorical columns
    cat_columns = ["area", "project", "task", "subtask"]
    for col in cat_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace("nan", "").astype("category")

    # Strings
    df["note"] = df["note"].astype(str).replace("nan", "")

    # Clean empty areas
    df["area"] = df["area"].astype(str).replace(["", "nan"], "MISC")
    df["area"] = df["area"].astype("category")

    # clean
    

    # reorder columns
    df = df[["date",
             "year", 
             "month", 
             "dow", 
             "week", 
             "area", 
             "subarea",
             "project", 
             "task", 
             "subtask", 
             "min", 
             "horas", 
             "note"]]


    return df