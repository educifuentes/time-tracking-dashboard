import streamlit as st
import altair as alt
import pandas as pd


def render_trend_assets_chart(assets_history_df: pd.DataFrame) -> None:
    """
    Renders a line chart showing the temporal trend of assets
    (schoperas_ccu, salidas) for a given cliente's history DataFrame.

    Parameters
    ----------
    assets_history_df : pd.DataFrame
        Filtered DataFrame for a single cliente, sorted by fecha descending.
        Must contain columns: 'fecha', 'schoperas_ccu', 'salidas'.
    """
    if len(assets_history_df) <= 1:
        st.warning("No hay registros históricos de activos para este cliente.")
        return

    chart_data = assets_history_df.melt(
        id_vars=["fecha"],
        value_vars=["schoperas_ccu", "salidas", "coolers"],
        var_name="Activo",
        value_name="Cantidad",
    )

    line_chart = (
        alt.Chart(chart_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("fecha:T", title="Fecha", axis=alt.Axis(format="%Y-%m")),
            y=alt.Y("Cantidad:Q", title="Cantidad"),
            color="Activo:N",
            tooltip=[alt.Tooltip("fecha:T", format="%Y-%m"), "Activo", "Cantidad"],
        )
        .properties(height=250)
    )

    st.altair_chart(line_chart, use_container_width=True)
