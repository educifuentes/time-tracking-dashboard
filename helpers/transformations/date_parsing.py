import pandas as pd
import re
from datetime import date

def parse_spanish_month_year(series):
    """
    Parses Spanish month-year strings (e.g., 'Marzo 2025') into datetime objects.
    Handles ranges like 'Junio 2025 - Julio 2025' by taking the earliest date.
    """
    spanish_months = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    def process_val(val):
        if pd.isna(val) or str(val).strip() == '':
            return None
        
        val_str = str(val).lower().strip()
        
        # Check for range: "Mes Año - Mes Año"
        if '-' in val_str:
            parts = val_str.split('-')
            val_str = parts[0].strip()
        
        # Match "month year"
        match = re.search(r'([a-z]+)\s+(\d{4})', val_str)
        if match:
            month_str = match.group(1)
            year_int = int(match.group(2))
            
            month_int = spanish_months.get(month_str)
            if month_int:
                return date(year_int, month_int, 1)
        
        # Fallback to pandas to_datetime for standard formats
        dt = pd.to_datetime(val_str, errors='coerce')
        if pd.notna(dt):
            return dt.date()
        
        return None

    # Apply processing
    res = series.apply(process_val)
    return pd.to_datetime(res, errors='coerce').dt.date
