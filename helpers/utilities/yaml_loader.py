import yaml
import os

def load_yaml_config(file_path):
    """
    Loads a YAML configuration file.
    """
    # If the path is relative, assume it's from the project root
    if not os.path.isabs(file_path):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        file_path = os.path.join(project_root, file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML file not found at: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_table_config(source_name, table_name, yaml_path='models/sources/_src_reportes_ccu.yml'):
    """
    Retrieves the configuration for a specific table from a YAML source file.
    """
    config = load_yaml_config(yaml_path)
    
    # Get the sources part of the config
    sources_data = config if isinstance(config, list) else config.get('sources', {})
    
    # If sources_data is a dictionary, convert it to a lookable structure
    if isinstance(sources_data, dict):
        # If it's a dict like {'censos': {...}}, check if source_name is a key
        if source_name in sources_data:
            source = sources_data[source_name]
            # Some structures might have 'tables' directly under the source key
            for table in source.get('tables', []):
                if table.get('name') == table_name:
                    return table
        # Also handle if it's a dict where values have 'name' attribute (less common but possible)
        for _, source in sources_data.items():
            if isinstance(source, dict) and source.get('name') == source_name:
                for table in source.get('tables', []):
                    if table.get('name') == table_name:
                        return table
    elif isinstance(sources_data, list):
        for source in sources_data:
            if isinstance(source, dict) and source.get('name') == source_name:
                for table in source.get('tables', []):
                    if table.get('name') == table_name:
                        return table
                        
    return None
