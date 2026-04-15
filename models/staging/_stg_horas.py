from helpers.utilities.load_gsheets import load_gsheets_worksheet
from helpers.ui_components.yaml_loader import get_table_config

def stg_horas():
    # Load configuration from YAML
    table_config = get_table_config(
        source_name="horas",
        table_name="horas",
        yaml_path="models/staging/_src_horas.yml"
    )
    
    if not table_config:
        raise ValueError("Configuration for table 'horas' not found in _src_horas.yml")
    
    worksheet = table_config.get("worksheet")
    
    df = load_gsheets_worksheet(worksheet_name=worksheet)
    return df

