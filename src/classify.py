# src/classify.py

import pandas as pd

VALID_STATUSES = {"LOW", "NORMAL", "HIGH", "NO DATA"}

def classify_result(value, ref_low, ref_high) -> str:
    """
    Returns one of: LOW, NORMAL, HIGH, NO DATA
    """
    if value is None or value == "" or pd.isna(value):
        return 'NO DATA'
    try:
        value = float(value)
        ref_high = float(ref_high)
        ref_low = float(ref_low)
    except(TypeError, ValueError):
        return 'NO DATA'
      
    if value > ref_high:
        return 'HIGH'
    elif value < ref_low:
        return 'LOW'
    else:
        return 'NORMAL'

def add_status_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'status' column based on value vs reference range.
    Does not modify input df in place (returns a copy).
    """    
    out = df.copy()
    out['status'] = out.apply(
        lambda row: classify_result(row['value'], row['ref_low'],row['ref_high'] ),
        axis =1)
    return out
