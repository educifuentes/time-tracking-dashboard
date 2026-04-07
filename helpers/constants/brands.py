CORPORATE_GROUPS = [
    "marcas_ccu",
    "marcas_abinbev",
    "marcas_kross",
    "marcas_otras"
]

BRAND_CORPORATE_MAPPING = {
    "ALHAMBRA": CORPORATE_GROUPS[3],
    "AUSTRAL": CORPORATE_GROUPS[0],
    "BALTICA": CORPORATE_GROUPS[1],
    "BECKER": CORPORATE_GROUPS[1],
    "BLUE MOON": CORPORATE_GROUPS[3],
    "BUDWEISER": CORPORATE_GROUPS[1],
    "CHESTER": CORPORATE_GROUPS[3],
    "CORONA": CORPORATE_GROUPS[1],
    "CRISTAL": CORPORATE_GROUPS[0],
    "CUELLO NEGRO": CORPORATE_GROUPS[3],
    "CUSQUEÑA": CORPORATE_GROUPS[1],
    "D'OLBEK": CORPORATE_GROUPS[0],
    "ERDINGER": CORPORATE_GROUPS[3],
    "ESCUDO": CORPORATE_GROUPS[0],
    "ESTRELLA DAMM": CORPORATE_GROUPS[3],
    "ESTRELLA DE GALICIA": CORPORATE_GROUPS[3],
    "GOOSE ISLAND": CORPORATE_GROUPS[1],
    "GUAYACÁN": CORPORATE_GROUPS[0],
    "HEINEKEN": CORPORATE_GROUPS[0],
    "HOEGAARDEN": CORPORATE_GROUPS[1],
    "KILOMETRO 24,7": CORPORATE_GROUPS[1],
    "KROSS": CORPORATE_GROUPS[2],
    "KUNSTMANN": CORPORATE_GROUPS[0],
    "LOA": CORPORATE_GROUPS[3],
    "MAHOU": CORPORATE_GROUPS[3],
    "MESTRA": CORPORATE_GROUPS[3],
    "PATAGONIA": CORPORATE_GROUPS[0],
    "PERONI": CORPORATE_GROUPS[3],
    "QUILMES": CORPORATE_GROUPS[1],
    "ROYAL GUARD": CORPORATE_GROUPS[0],
    "STELLA ARTOIS": CORPORATE_GROUPS[1],
    "TOTEM": CORPORATE_GROUPS[3],
    "TROPERA": CORPORATE_GROUPS[3],
    "TUBINGER": CORPORATE_GROUPS[3],
}

BRANDS = list(BRAND_CORPORATE_MAPPING.keys())

CORPORATE_GROUP_COLORS = {
    CORPORATE_GROUPS[0]: "#2ca02c",  # Green (CCU)
    CORPORATE_GROUPS[1]: "#d62728",  # Red (Abinbev) tambien CCH
    CORPORATE_GROUPS[2]: "#ff7f0e",  # Orange (Kross)
    CORPORATE_GROUPS[3]: "#7f7f7f"   # Gray (Otras)
}

BRAND_COLORS = [
    CORPORATE_GROUP_COLORS.get(BRAND_CORPORATE_MAPPING.get(brand), CORPORATE_GROUP_COLORS[CORPORATE_GROUPS[3]])
    for brand in BRAND_CORPORATE_MAPPING
]

FREE_TEXT_MAPPINGS = {
    "bloomon": "BLUE MOON",
    "bluemoon": "BLUE MOON",
    "blue moon": "BLUE MOON",
    "chester beer artesanal": "CHESTER",
    "chester beer": "CHESTER",
    "chester": "CHESTER",
    "kross": "KROSS",
    "estrella damn": "ESTRELLA DAMM",
    "estrella damm": "ESTRELLA DAMM",
    "estrella": "ESTRELLA DAMM",
    "mahou": "MAHOU",
    "mahon": "MAHOU",
    "peroni": "PERONI",
    "peronni": "PERONI",
    "peruani": "PERONI",
    "tubiinger": "TUBINGER",
    "tubinger": "TUBINGER",
    "alambra": "ALHAMBRA",
    "alhambra": "ALHAMBRA",
    "tropera": "TROPERA",
    "las troperas": "TROPERA",
}

IGNORE_FREE_TEXT = {
    "no", "ninguna", "ninguna otra", "sin comentario", "ninguna otra marca",
    "0", "no hay otra", "no tienen cervezas a la venta , estan solo las maquinas",
    "no hay", "ok", ".", "no tiene", "si. comentarios"
}
