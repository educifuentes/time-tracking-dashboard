ICONS = {
    # source: https://fonts.google.com/icons
    # branding
    "logo": "timer",
    
    # tables
    "horas": "timer",
    # VALIDATIONS   
    "check": "check_box",
    "warning": "warning",
    "close": "close",
    # otros
    "documentation": "article",
    "search": "search",
    "database": "database",
    "metrics": "calculate",
    "not_apply": "circle"
}

def render_icon(icon_key: str) -> str:
    """
    Returns the streamlit material icon format for a given key.
    """
    icon_name = ICONS.get(icon_key, "help")
    return f":material/{icon_name}:"