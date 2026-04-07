import pandas as pd
from typing import List

def safe_concat_with_columns(dfs: List[pd.DataFrame], selected_columns: List[str]) -> pd.DataFrame:
    """
    Checks if all input DataFrames have the selected_columns before concatenation.
    If a column is missing, it creates it with None values.
    Returns the concatenated DataFrame sliced to the selected columns.
    """
    aligned_dfs = []
    for df in dfs:
        df_copy = df.copy()
        for col in selected_columns:
            if col not in df_copy.columns:
                df_copy[col] = None
        aligned_dfs.append(df_copy[selected_columns])
        
    return pd.concat(aligned_dfs, ignore_index=True)
