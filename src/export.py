import pandas as pd
import os

def build_text_report(report: dict) -> str:
    lines = []
    lines.append("DAILY HEALTHCARE ADMIN REPORT")
    lines.append(f"Date: {report['date']}")
    lines.append("-" * 50)

    # Key metrics
    lines.append("Key metrics:")
    lines.append(f"- Total patients processed: {report['metrics']['total_patients']}")
    lines.append(
        f"- Patients needing review: {report['metrics']['needs_review_count']} "
        f"({report['metrics']['needs_review_pct']:.1f}%)"
    )
    lines.append(
        f"- Missing data rate (NO DATA): {report['metrics']['no_data_pct']:.1f}%"
    )

    # Priority breakdown
    lines.append("")
    lines.append("Priority breakdown:")
    priority_counts = report["metrics"]["priority_count"]
    for p in ["HIGH", "MEDIUM", "LOW", "NO DATA"]:
        lines.append(f"- {p}: {priority_counts.get(p, 0)}")

    # Concentration
    lines.append("")
    lines.append(
        f"Workload concentration:"
        f"\n- Top 20% share of abnormalities: {report['concentration_pct']:.1f}%"
    )

    # Alerts
    lines.append("")
    lines.append("Alerts:")
    if report["alerts"]:
        for a in report["alerts"]:
            lines.append(f"- {a}")
    else:
        lines.append("- None")

    # Summary
    lines.append("")
    lines.append("Executive summary:")
    lines.append(report["summary"])

    # Safety
    lines.append("")
    lines.append(report["disclaimer"])

    return "\n".join(lines)




# ---------- TXT EXPORT ----------

def export_text_report(report: dict, output_dir: str = "outputs/reports") -> str:
   
   
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_output_dir = os.path.join(BASE_DIR, output_dir)

    os.makedirs(full_output_dir, exist_ok=True)

    

    date_str = report["date"]
    filename = f"daily_admin_report_{date_str.replace('-', '')}.txt"
    path = os.path.join(full_output_dir, filename)

    text = build_text_report(report)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


# ---------- PATIENT TABLE CSV EXPORT ----------

def export_patient_table(patient_df: pd.DataFrame, date_str: str, output_dir: str = "outputs/tables") -> str:
    """
    Exports a patient-level admin review table to CSV.
    Returns the saved file path.
    """
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_output_dir = os.path.join(BASE_DIR, output_dir)

    os.makedirs(full_output_dir, exist_ok=True)

    
    

    # Select + sort for admin readability
    admin_table = patient_df[[
        "date", "patient_id", "priority", "abnormal_count", "no_data_count", "needs_review"
    ]].copy()

    priority_order = ["HIGH", "MEDIUM", "LOW", "NO DATA"]
    admin_table["priority"] = pd.Categorical(
        admin_table["priority"], categories=priority_order, ordered=True
    )

    admin_table = admin_table.sort_values(
        by=["priority", "abnormal_count"], ascending=[True, False]
    ).reset_index(drop=True)

    filename = f"daily_admin_table_{date_str.replace('-', '')}.csv"
    path = os.path.join(full_output_dir, filename)

    admin_table.to_csv(path, index=False, encoding="utf-8")
    return path


# ---------- PRIORITY SUMMARY CSV EXPORT ----------

def export_priority_summary(patient_df: pd.DataFrame, date_str: str, output_dir: str = "outputs/tables") -> str:
    """
    Exports a 1-row-per-priority summary table to CSV.
    Columns: priority, patient_count, pct_of_total
    Returns the saved file path.
    """
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_output_dir = os.path.join(BASE_DIR, output_dir)

    os.makedirs(full_output_dir, exist_ok=True)

    
   

    total = len(patient_df)
    priority_order = ["HIGH", "MEDIUM", "LOW", "NO DATA"]

    summary = (
        patient_df.groupby("priority")
        .size()
        .reindex(priority_order, fill_value=0)
        .reset_index(name="patient_count")
    )

    if total > 0:
        summary["pct_of_total"] = (summary["patient_count"] / total) * 100
    else:
        summary["pct_of_total"] = 0.0

    filename = f"daily_priority_summary_{date_str.replace('-', '')}.csv"
    path = os.path.join(full_output_dir, filename)

    summary.to_csv(path, index=False, encoding="utf-8")
    return path