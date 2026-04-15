import streamlit as st

from helpers.transformations.gsheet_links import add_gsheet_link

def render_troubled_rows(df, gid=None, row_indices=None, source=None):
    """
    Renders a dataframe of troubled rows.

    Args:
        df (pd.DataFrame): The dataframe containing the rows to display.
        gid (str, optional): The Google Sheet Grid ID. Required when source="gsheets".
        row_indices (pd.Series or list, optional): The original row indices for linking.
                                                   If None, tries to use df['row_index'].
        source (str, optional): Data source hint. Pass "gsheets" to show the GSheet
                                 link column. Omit (or pass None) to display the plain
                                 dataframe without a link.
    """
    if source == "gsheets" and gid is not None:
        if row_indices is None and "row_index" in df.columns:
            row_indices = df["row_index"]

        df_with_links = add_gsheet_link(df, gid, row_indices)

        display_df = df_with_links.copy()
        if "row_index" in display_df.columns:
            display_df = display_df.drop(columns=["row_index"])

        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")},
        )
    else:
        display_df = df.drop(columns=["row_index"], errors="ignore")
        st.dataframe(display_df, use_container_width=True)

import pandas as pd

def add_gsheet_link(df, gid, row_index=None):
    """
    Adds a column with a direct link to the corresponding row in Google Sheets.
    Uses 'row_index' argument to point to the specific row.
    """
    if not gid:
        return df
        
    df = df.copy()
    
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1I-nQVWT9XP1p0DLbgvpCMWjzQ8i6CqbTM1E9g4oCzDY"
    base_url = f"{spreadsheet_url}/edit#gid={gid}"
    
    if row_index is not None:
        # Range A{row_index} makes the link point directly to the row/cell
        # We cast to int because GSheets doesn't like .0 in the range parameter
        df["link"] = row_index.apply(lambda x: f"{base_url}&range=A{int(x)}" if pd.notna(x) else base_url)
    else:
        df["link"] = base_url
    
    return df
