from helpers.utilities.yaml_loader import load_yaml_config

def get_source_metadata(table_name: str, yaml_path: str):
    """
    Looks up a table in the given YAML configuration.
    Returns a tuple of (file_path, sheet_name).
    """
    config = load_yaml_config(yaml_path)
    sources_dict_or_list = config.get("sources", [])
    
    # Support both list of sources and dict of sources (e.g. keyed by schema)
    if isinstance(sources_dict_or_list, dict):
        sources = sources_dict_or_list.values()
    else:
        sources = sources_dict_or_list
        
    file_path = None
    sheet_name = None
    for source in sources:
        for table in source.get("tables", []):
            if table.get("name") == table_name:
                file_path = table.get("path")
                break
        if file_path:
            break
            
    if not file_path:
        raise ValueError(f"Table '{table_name}' not found in {yaml_path}")
        
    return file_path
