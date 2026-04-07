import pandas as pd

def clean_text(df, columns, title=True, na_on_empty=True):
    """
    Standardizes text columns using pandas nullable string dtype.
    Strips whitespace and optionally applies title casing.
    
    Args:
        df (pd.DataFrame): The DataFrame to process.
        columns (list): List of column names to clean.
        title (bool): Whether to apply .str.title(). Defaults to True.
        na_on_empty (bool): Whether to convert empty strings to pd.NA. Defaults to True.
        
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    for col in columns:
        if col in df.columns:
            # 1. Convert to nullable string dtype (handles pd.NA naturally)
            df[col] = df[col].astype("string")
            
            # 2. Vectorized operations propagate NA automatically
            df[col] = df[col].str.strip()
            
            if title:
                df[col] = df[col].str.title()
            
            # 3. Handle empty strings
            if na_on_empty:
                df[col] = df[col].replace("", pd.NA)
                
    return df
