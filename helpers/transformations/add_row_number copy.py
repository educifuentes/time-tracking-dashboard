def add_row_number(df):
    """
    Adds a metadata row index matching the GSheet row number.
    2-indexed as row 1 is the header in Google Sheets.
    """
    df.insert(0, "row_index", df.index + 2)
    return df
