import pandas as pd

REGION_MAP = {
    # 1 - Tarapacá
    "Tarapacá": "1 - Tarapaca",
    "Tarapaca": "1 - Tarapaca",

    # 2 - Antofagasta
    "Antofagasta": "2 - Antofagasta",

    # 3 - Atacama
    "Atacama": "3 - Atacama",

    # 4 - Coquimbo
    "Coquimbo": "4 - Coquimbo",

    # 5 - Valparaíso
    "Valparaíso": "5 - Valparaiso",
    "Valparaiso": "5 - Valparaiso",

    # 6 - O’Higgins
    "O'Higgins": "6 - O'Higgins",
    "Libertador Bernardo O'Higgins": "6 - O'Higgins",

    # 7 - Maule
    "Maule": "7 - Maule",

    # 8 - Biobío
    "Biobío": "8 - Biobio",
    "Biobio": "8 - Biobio",
    "Bio Bio": "8 - Biobio",

    # 9 - La Araucanía
    "La Araucanía": "9 - La Araucania",
    "Araucanía": "9 - La Araucania",
    "La Araucania": "9 - La Araucania",

    # 10 - Los Lagos
    "Los Lagos": "10 - Los Lagos",

    # 11 - Aysén
    "Aysén": "11 - Aysen",
    "Aysen": "11 - Aysen",

    # 12 - Magallanes
    "Magallanes": "12 - Magallanes",
    "Magallanes Y De La Antártica Chilena": "12 - Magallanes",

    # 13 - Metropolitana
    "Metropolitana": "13 - Metropolitana",
    "Metropolitana De Santiago": "13 - Metropolitana",

    # 14 - Los Ríos
    "Los Ríos": "14 - Los Rios",
    "Los Rios": "14 - Los Rios",

    # 15 - Arica y Parinacota
    "Arica Y Parinacota": "15 - Arica y Parinacota",
    "Arica y Parinacota": "15 - Arica y Parinacota",

    # 16 - Ñuble
    "Ñuble": "16 - Ñuble",
}

# Add integer mappings mapping '1' and 1 to '1 - Tarapaca'
_extra_mappings = {}
for val in REGION_MAP.values():
    num_str = val.split(" - ")[0]
    _extra_mappings[int(num_str)] = val
    _extra_mappings[num_str] = val
REGION_MAP.update(_extra_mappings)

def clean_region(df):
    """
    Cleans the region column in a DataFrame using the REGION_MAP.
    Ensures NaN values are transformed to None.
    """
    if "region" not in df.columns:
        return df

    def normalize_region(val):
        if pd.isna(val):
            return None
            
        # Try direct match
        if val in REGION_MAP:
            return REGION_MAP[val]
            
        # Clean string variations
        if isinstance(val, str):
            val = val.strip()
            # Strip trailing .0 if it represents a float
            if val.endswith(".0"):
                val = val[:-2]
            
            if val in REGION_MAP:
                return REGION_MAP[val]
                
        # Handle floats/strings that can be cast to int
        try:
            val_int = int(float(val))
            if val_int in REGION_MAP:
                return REGION_MAP[val_int]
        except (ValueError, TypeError):
            pass
            
        # Fallback to returning original value if no mapping found
        return val
        
    df["region"] = df["region"].apply(normalize_region)
    
    # Convert remaining NaN explicitly to None
    df["region"] = df["region"].where(df["region"].notna(), None)
    
    return df