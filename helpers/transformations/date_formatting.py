import pandas as pd

def format_date_spanish(dt):
    if pd.isna(dt):
        return "N/A"
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
              "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{months[dt.month - 1]} {dt.year}"
