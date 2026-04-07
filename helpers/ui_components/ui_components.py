import streamlit as st

from helpers.transformations.gsheet_links import add_gsheet_link
from helpers.ui_components.ui_icons import ICONS

from helpers.widgets.explorer_de_datos import explorer_de_datos

def display_compliance_badge(clasificacion):
    """Displays a formatted st.badge based on the classification."""
    if clasificacion == "En regla":
        st.badge("En regla", icon=ICONS['check'], color="green")
    elif clasificacion == "No en regla":
        st.badge("No en regla", icon=ICONS['warning'], color="red")
    elif clasificacion == "No aplica":
        st.badge("No aplica", icon=ICONS['not_apply'], color="yellow")
    elif clasificacion == "Sin comodato o terminado":
        st.badge("Sin comodato o terminado", icon=ICONS['close'], color="blue")
    else:
        st.badge(clasificacion, icon="🔍")

def render_model_ui(df, table_name=None):
    """
    Renders a standard UI component for a data model summary.
    Includes shape, columns, and the dataframe.
    Optionally fetches and displays description from YAML config.
    """


    with st.expander(f"Tabla: `{table_name}`"):
        st.write(df.shape)
        with st.expander("Columnas"):
            st.code("\n".join(df.columns))
        with st.expander("Data Types"):
            dtypes_str = " | ".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
            st.code(dtypes_str)
        df = explorer_de_datos(df)
        st.dataframe(df)
    st.divider()

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

