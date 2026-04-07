import streamlit as st

def metrics_display(df, show_header=True, show_divider=True, max_cols=3):
    """
    Renders metrics from a DataFrame using st.metric in a columnar layout.
    
    Args:
        df (pd.DataFrame): DataFrame containing columns for metrics and 'periodo'.
        show_header (bool): Whether to show the Period header.
        show_divider (bool): Whether to show the divider after metrics.
        max_cols (int): Maximum number of columns to show per row.
    """
    if df.empty:
        st.info("No hay métricas para mostrar.")
        return

    # Ensure 'periodo' is present
    if 'periodo' not in df.columns:
        st.warning("El DataFrame de métricas debe contener una columna 'periodo'.")
        return

    # Display only columns that represent metrics (containing '#', '%', or starting with 'N ')
    metric_cols = [col for col in df.columns if col != 'periodo' and ('#' in col or '%' in col or col.startswith('N '))]

    for _, row in df.iterrows():
        # Period Header
        if show_header:
            st.markdown(f"###### Periodo: {row['periodo']}")
        
        # Chunk metrics into groups of max_cols
        for i in range(0, len(metric_cols), max_cols):
            chunk = metric_cols[i : i + max_cols]
            cols = st.columns(len(chunk))
            for j, col_name in enumerate(chunk):
                val = row[col_name]
                cols[j].metric(label=col_name, value=val)
        
        if show_divider:
            st.divider()
