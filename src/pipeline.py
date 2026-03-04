import os
import pandas as pd

from src.classify import add_status_column
from src.aggregate import summarise_patients, add_priority_column
from src.report import build_daily_report
from src.export import export_text_report, export_patient_table, export_priority_summary
from src.validate import validate_input_df


def run_daily_pipeline(input_csv_path: str) -> dict:
    """
    End-to-end daily pipeline:
    1) Load raw test-level CSV
    2) Classify tests (LOW/NORMAL/HIGH/NO DATA)
    3) Aggregate to patient-level + assign priority
    4) Build structured report object
    5) Export report + tables to disk
    Returns a dictionary of file paths + key outputs.
    """

    # ---------- 1) Load input ----------
    df = pd.read_csv(input_csv_path)
    validate_input_df(df)
    

    # ---------- 2) Classification ----------
    df_status = add_status_column(df)

    # ---------- 3) Patient aggregation + priority ----------
    patient_df = summarise_patients(df_status)
    patient_df = add_priority_column(patient_df)

    # Determine the report date from the data (not from system clock)
    if "date" not in patient_df.columns or len(patient_df) == 0:
        raise ValueError("patient_df is empty or missing 'date' column.")
    date_str = str(patient_df["date"].iloc[0])

    # ---------- 4) Build report object ----------
    report = build_daily_report(date_str, patient_df)

    # ---------- 5) Export outputs ----------
    report_path = export_text_report(report, output_dir="outputs/reports")
    patient_table_path = export_patient_table(patient_df, date_str, output_dir="outputs/tables")
    priority_summary_path = export_priority_summary(patient_df, date_str, output_dir="outputs/tables")

    # Return useful info for notebook / automation
    return {
        "date": date_str,
        "report_path": report_path,
        "patient_table_path": patient_table_path,
        "priority_summary_path": priority_summary_path,
        "alerts": report["alerts"],
    }