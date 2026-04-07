import plotly.express as px
from helpers.ui_components.ui_config import CLASIFICACION_COLORS

def plot_clasificacion_pie(df):
    """Generates a pie chart for classification distribution."""
    fig = px.pie(
        df,
        names='clasificacion',
        color='clasificacion',
        hole=.3,
        color_discrete_map=CLASIFICACION_COLORS,
        height=300,
        custom_data=['clasificacion'] # Optional, but good practice
    )
    fig.update_traces(
        textinfo='percent+label', 
        pull=[0.05, 0.05, 0.05, 0.05],
        hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}"
    )
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    return fig

try:
    clientes_df, censos_df, activos_df, nominas_df, contratos_df = get_generated_dataframes()
except FileNotFoundError as e:
    st.error(f"Error loading data file: {e}. Please make sure the files are in the 'data/raw/' directory.")
    st.stop()