import pandas as pd
from models.staging._stg_horas import stg_horas

def fct_activities():
    df = stg_horas()

    # Convert date column
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    # Numeric columns
    df["min"] = pd.to_numeric(df["min"], errors='coerce').fillna(0)
    df["horas"] = pd.to_numeric(df["horas"], errors='coerce').fillna(0)
    df["week"] = pd.to_numeric(df["week"], errors='coerce').fillna(0).astype(int)
    
    # Categorical columns
    cat_columns = ["area", "project", "task", "subtask", "dow"]
    for col in cat_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace("nan", "").astype("category")

    # Strings
    df["note"] = df["note"].astype(str).replace("nan", "")

    return df