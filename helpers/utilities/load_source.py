import pandas as pd

def load_source(file_path: str, format: str = "csv", sheet_name: str = None, **kwargs) -> pd.DataFrame:
    """
    Loads a source file into a pandas DataFrame using its file path.
    Supports 'csv' (default), 'excel', and will auto-detect '.parquet' files based on extension.
    """
    if format == "excel":
        if 'nrows' in kwargs and kwargs['nrows'] is not None:
            return pd.read_excel(file_path, sheet_name=sheet_name, nrows=kwargs['nrows'])
        return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        
    if file_path.endswith(".parquet"):
        return pd.read_parquet(file_path, **kwargs)
        
    return pd.read_csv(file_path, **kwargs)
