
import pandas as pd 

ABNORMAL_TESTS   =  { 'HIGH', 'LOW'}


def summarise_patients(df_with_status: pd.DataFrame) -> pd.DataFrame:
    out = df_with_status.copy()

    
    out["is_abnormal"] = out["status"].isin(ABNORMAL_TESTS)
    out["is_no_data"] = out["status"] == "NO DATA"

    # Group to patient/day level
    patient_df = (
        out.groupby(["date", "patient_id"], as_index=False)
           .agg(
               abnormal_count=("is_abnormal", "sum"),
               no_data_count=("is_no_data", "sum")
           )
    )

    # Needs review rule 
    patient_df["needs_review"] = (patient_df["abnormal_count"] >= 1) | (patient_df["no_data_count"] >= 1)

    return patient_df
def assign_priority_row(abnormal_count: int, no_data_count: int) -> str:
    if no_data_count >= 1:
        return "NO DATA"
    if abnormal_count >= 2:
        return "HIGH"
    elif abnormal_count == 1:
        return "MEDIUM"
    else:
        return "LOW"

def add_priority_column(patient_df: pd.DataFrame) -> pd.DataFrame:
    out = patient_df.copy()
    out["priority"] = out.apply(
        lambda row: assign_priority_row(int(row["abnormal_count"]), int(row["no_data_count"])),
        axis=1
    )
    return out



