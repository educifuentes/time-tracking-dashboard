import pandas as pd

def yes_no_to_boolean(series):
    """
    Convierte una serie con valores 'Sí'/'No' (o 'Yes'/'No') a booleanos True/False.
    Maneja variaciones de mayúsculas/minúsculas y espacios en blanco.
    """
    # Crear un mapeo para normalizar los valores
    mapping = {
        'si': True,
        'sí': True,
        'yes': True,
        'no': False,
    }
    
    # Aplicar la transformación de forma segura
    # Usamos str.strip().str.lower() para mayor robustez
    
    series = series.astype(str).str.strip().str.lower().map(mapping)

    return series