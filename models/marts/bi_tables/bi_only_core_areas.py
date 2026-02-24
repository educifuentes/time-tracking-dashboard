from models.marts.fct_activities import fct_activities
from utilities.constants.area_config import AREA_CORE


def bi_only_core_areas():
    
    df = fct_activities()
    df = df[df["area"].isin(AREA_CORE)].copy()
    
    return df
