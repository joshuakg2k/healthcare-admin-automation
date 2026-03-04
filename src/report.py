import pandas as pd
from src.analytics import compute_basic_metrics, compute_concentration, generate_alerts
from config import THRESHOLDS
alerts = generate_alerts(metrics, concentration_pct, THRESHOLDS)

def build_summary(metrics: dict, concentration_pct: float, alerts: list, date_str: str) -> str:

    total = metrics['total_patients']
    review_count = metrics['needs_review_count']
    review_pct = metrics['needs_review_pct']

    priority_counts = metrics['priority_count']
    priority_pct = metrics['priority_pct']

    low = priority_counts.get('LOW', 0)
    medium = priority_counts.get('MEDIUM', 0)
    high = priority_counts.get('HIGH', 0)
    no_data = priority_counts.get('NO DATA', 0)

    no_data_pct = metrics['no_data_pct']

    summary = (
        f"Out of {total} patients processed on {date_str}, "
        f"{review_count} ({review_pct:.1f}%) require administrative review. "
        f"Priority distribution is {low} LOW, {medium} MEDIUM, {high} HIGH, and {no_data} NO DATA cases. "
        f"Missing data affected {no_data_pct:.1f}% of patients. "
        f"The top 20% of patients contributed {concentration_pct:.1f}% of total abnormalities."
    )

    if alerts:
        summary += " Operational alerts were triggered based on workload and data quality thresholds."

    return summary

def build_daily_report(date_str: str, patient_df: pd.DataFrame) -> dict:
     # 1) Compute metrics
    metrics = compute_basic_metrics(patient_df)

    # 2) Compute workload concentration
    concentration_pct = compute_concentration(patient_df)

    # 3) Generate alerts
    alerts = generate_alerts(metrics, concentration_pct)

    # 4) Build narrative summary
    summary = build_summary(metrics, concentration_pct, alerts, date_str)

    # 5) Disclaimer (always included)
    disclaimer = (
        "Synthetic data. Administrative support only. "
        "Not for clinical or diagnostic use."
    )

    # 6) Assemble report object
    report = {
        "date": date_str,
        "metrics": metrics,
        "concentration_pct": concentration_pct,
        "alerts": alerts,
        "summary": summary,
        "disclaimer": disclaimer,
    }

    return report