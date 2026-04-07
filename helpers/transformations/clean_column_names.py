def clean_column_name(df):
    """
    Strips whitespace from the beginning and end of all column names in the DataFrame.
    """
    df.columns = df.columns.str.strip()
    return df
