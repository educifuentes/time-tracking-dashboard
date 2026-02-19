import streamlit as st

from models.staging._stg_horas import stg_horas

from utilities.ui_components.render_model import render_model_ui


horas_df = stg_horas()
render_model_ui(horas_df)

