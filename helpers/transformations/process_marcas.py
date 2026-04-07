import pandas as pd

from helpers.constants.brands import BRAND_CORPORATE_MAPPING, FREE_TEXT_MAPPINGS, IGNORE_FREE_TEXT
import re
import difflib

def _extract_brands_list(val):
    if pd.isna(val) or val == "":
        return []
    
    found_brands = []
    val_upper = str(val).upper()
    
    for brand in BRAND_CORPORATE_MAPPING:
        pos = val_upper.find(brand)
        if pos != -1:
            # Store (position, TitleizedBrand)
            found_brands.append((pos, brand.title()))
    
    # Sort by position to preserve original order
    found_brands.sort()
    
    # Extract only the names
    return [b[1] for b in found_brands]

def _extract_free_text_brands(val):
    if pd.isna(val) or val == "":
        return []
    
    val = str(val).lower().strip()
    if val in IGNORE_FREE_TEXT:
        return []
    
    # Split by comma or " y "
    tokens = re.split(r",|\sy\s", val)
    found = []
    for t in tokens:
        t = t.strip()
        if not t: continue
        if t in IGNORE_FREE_TEXT: continuef
        
        # Check mapping
        if t in FREE_TEXT_MAPPINGS:
            found.append(FREE_TEXT_MAPPINGS[t].title())
        else:
            # Generic title case for unmapped brands
            found.append(t.title())
            
    return found

def process_marcos_texto_libre(df):
    if "marcas_texto_libre" not in df.columns:
        return df
    
    df["marcas_texto_libre"] = df["marcas_texto_libre"].apply(_extract_free_text_brands)
    
    return df

def process_marcas(df):
    """
    Process the 'marcas' column by extracting known brands, searching both 
    the 'marcas' column and 'marcas_texto_libre' if it exists.
    Consolidates the result into a single 'marcas' column.
    """
    if "marcas" not in df.columns:
        return df

    # Extract lists of brands from the main column
    extracted_marcas = df["marcas"].apply(_extract_brands_list)
    
    # If free text column exists, extract and combine
    if "marcas_texto_libre" in df.columns:
        # We assume process_marcos_texto_libre might have already run, or we run it directly
        extracted_libre = df["marcas_texto_libre"].apply(_extract_free_text_brands)
        combined_brands = extracted_marcas + extracted_libre
    else:
        combined_brands = extracted_marcas

    # Remove duplicates (maintaining order) and join into a comma-separated string
    df["marcas"] = combined_brands.apply(
        lambda brands: ", ".join(list(dict.fromkeys(brands))) if brands else None
    )
    
    return df

def process_marcas_questionnaire_version(df):
    """
    Alternative to process_marcas that reads from specific 'P42 - Brand' indicator columns.
    If the column value is 1, the brand is considered present.
    Creates a 'marcas' column with a comma-separated list of active brands.
    """
    brand_cols = [
        "P42 - Austral", "P42 - Baltica", "P42 - Becks", "P42 - Becker", 
        "P42 - Brahma", "P42 - Bud light", "P42 - Budweiser", "P42 - Busch", 
        "P42 - Corona", "P42 - Coronita", "P42 - Cristal", "P42 - Cusquena", 
        "P42 - Dolbek", "P42 - Escudo", "P42 - Goose island", "P42 - Guayacan", 
        "P42 - Heineken", "P42 - Hoegaarden", "P42 - Kilometro 24.7", "P42 - Kuntsmann", 
        "P42 - Leffe", "P42 - Malta del sur", "P42 - Michelob ultra", "P42 - Modelo", 
        "P42 - Pacena", "P42 - Patagonia", "P42 - Pilsen", "P42 - Pilsen del sur", 
        "P42 - Quilmes", "P42 - Royal guard", "P42 - Stella artois", "P42 - Loa", 
        "P42 - Estrella de galicia", "P42 - Kross", "P42 - Mestra", "P42 - Cuello negro", 
        "P42 - Totem", "P42 - Erdinger"
    ]
    
    def get_brands_for_row(row):
        active_brands = []
        for col in brand_cols:
            if col in df.columns:
                val = row[col]
                if pd.notna(val):
                    is_present = False
                    try:
                        if float(val) > 0:
                            is_present = True
                    except ValueError:
                        if str(val).strip().lower() in ['1', '1.0', 'true', 'yes', 'si']:
                            is_present = True
                            
                    if is_present:
                        # Extract the brand name, e.g. "P42 - Austral" -> "Austral"
                        brand_name = col.replace("P42 - ", "").title()
                        active_brands.append(brand_name)
        return ", ".join(active_brands) if active_brands else None

    # We store the active brands list in "marcas"
    df["marcas"] = df.apply(get_brands_for_row, axis=1)
    
    # Process free text if it exists and append
    if "marcas_texto_libre" in df.columns:
        extracted_libre = df["marcas_texto_libre"].apply(_extract_free_text_brands)
        
        def combine_row(row):
            existing = [b.strip() for b in str(row["marcas"]).split(",")] if pd.notna(row["marcas"]) else []
            libre = row["extracted_libre"] if isinstance(row["extracted_libre"], list) else []
            combined = existing + libre
            # remove duplicates but preserve order
            combined = list(dict.fromkeys(combined))
            return ", ".join(combined) if combined else None
            
        temp_df = pd.DataFrame({
            "marcas": df["marcas"],
            "extracted_libre": extracted_libre
        })
        df["marcas"] = temp_df.apply(combine_row, axis=1)

    return df


def classify_marcas(df, marcas_col="marcas"):
    """
    Categorize entries in the marcas column into boolean columns based on corporate parent.
    Also creates '_listado' columns with comma-separated lists of the specific brands found for each category.
    """
    if marcas_col not in df.columns:
        return df
        
    def classify_row(val):
        res = {
            "marcas_abinbev": False, "marcas_kross": False, "marcas_ccu": False, "marcas_otras": False,
            "marcas_abinbev_listado": None, "marcas_kross_listado": None, "marcas_ccu_listado": None, "marcas_otras_listado": None
        }
        if pd.isna(val) or val == "":
            return pd.Series(res)
            
        brands_in_row = [b.strip() for b in str(val).split(",")]
        
        lists = {
            "marcas_abinbev": [],
            "marcas_kross": [],
            "marcas_ccu": [],
            "marcas_otras": []
        }
        
        for b in brands_in_row:
            if not b: continue
            b_upper = b.upper()
            if b_upper in BRAND_CORPORATE_MAPPING:
                target_col = BRAND_CORPORATE_MAPPING[b_upper]
                if target_col in lists:
                    lists[target_col].append(b)
                else:
                    # In case there's a mapped col not in our list
                    res[target_col] = res.get(target_col, False)
                    res[f"{target_col}_listado"] = res.get(f"{target_col}_listado", None)
                    lists[target_col] = [b]
            else:
                lists["marcas_otras"].append(b)
                
        for col_name, brand_list in lists.items():
            if brand_list:
                res[col_name] = True
                # Remove duplicates while preserving order
                unique_brands = list(dict.fromkeys(brand_list))
                res[f"{col_name}_listado"] = ", ".join(unique_brands)
                
        return pd.Series(res)

    new_cols = df[marcas_col].apply(classify_row)
    for col in new_cols.columns:
        df[col] = new_cols[col]
        
    return df
# correct brand names
def correct_brand_names(series):
    """
    Corrects brand names with typos in a pandas Series using FREE_TEXT_MAPPINGS
    and the BRANDS list as a reference for close matches.
    Overrides typos with corrected strings, but leaves valid/unmapped names as they are.
    """
    def _correct(val):
        if pd.isna(val) or val == "":
            return val
        
        val_str = str(val).strip()
        val_lower = val_str.lower()
        val_upper = val_str.upper()
        
        if val_lower in FREE_TEXT_MAPPINGS:
            return FREE_TEXT_MAPPINGS[val_lower]
            
        # Try to find a close match in the BRANDS list
        matches = difflib.get_close_matches(val_upper, list(BRAND_CORPORATE_MAPPING.keys()), n=1, cutoff=0.8)
        if matches:
            return matches[0]
            
        return val

    return series.apply(_correct)


# pending

       # Clean marcas_otras_listado: keep only brands that belong to CORPORATE_GROUPS[3] ("marcas_otras")
    # _otras_brands = {
    #     brand for brand, group in BRAND_CORPORATE_MAPPING.items()
    #     if group == CORPORATE_GROUPS[3]
    # }

    # def _filter_otras_brands(cell):
    #     if pd.isna(cell) or str(cell).strip() == "":
    #         return cell
    #     tokens = [t.strip().upper() for t in str(cell).split(",")]
    #     filtered = [t for t in tokens if t in _otras_brands]
    #     return ", ".join(filtered) if filtered else None

    # out_df["Otras (indicar cuáles)"] = (
    #     out_df["Otras (indicar cuáles)"]
    #     .str.upper()
    #     .str.strip()
    #     .apply(_filter_otras_brands)
    # )
