import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "patient_id",
    "test_name",
    "value",
    "ref_low",
    "ref_high",
}

def validate_input_df(df: pd.DataFrame) -> None:
    """
    Raises ValueError with a clear message if input data is invalid.
    """
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if len(df) == 0:
        raise ValueError("Input dataset is empty.")

    
    # ref_low/ref_high should be numeric where present
    for col in ["ref_low", "ref_high"]:
        if df[col].isna().all():
            raise ValueError(f"Column '{col}' is entirely empty.")

    # check impossible ranges where both are present
    bad_ranges = df.dropna(subset=["ref_low", "ref_high"])
    if not bad_ranges.empty:
        bad = bad_ranges[bad_ranges["ref_low"] > bad_ranges["ref_high"]]
        if len(bad) > 0:
            raise ValueError("Found rows where ref_low > ref_high (invalid reference range).")