import pandas as pd

def compute_basic_metrics(patient_df: pd.DataFrame) -> dict:
    out = {}

    out['total_patients'] = len(patient_df)

    out['needs_review_count'] = int(patient_df['needs_review'].sum())

    if out['total_patients'] > 0:
        out['needs_review_pct'] = float((
            out['needs_review_count'] / out['total_patients']
        ) * 100)
    else:
        out['needs_review_pct'] = 0

    out['abnormal_total'] = int(patient_df['abnormal_count'].sum())
    out['no_data_total'] = int(patient_df['no_data_count'].sum())
    out['no_data_pct']  = float((out['no_data_total']/ out['total_patients'])*100)

    priority_counts = patient_df['priority'].value_counts()
    out['priority_count'] = priority_counts.to_dict()

    out['priority_pct'] = (
        (priority_counts / out['total_patients']) * 100
    ).to_dict()

    return out


import pandas as pd

def compute_concentration(patient_df: pd.DataFrame) -> float:
    total_patients = len(patient_df)
    if total_patients == 0:
        return 0.0

    top_n = max(1, int(0.20 * total_patients))

    total_abnormal = patient_df["abnormal_count"].sum()
    if total_abnormal == 0:
        return 0.0

    top_abnormal = patient_df["abnormal_count"].nlargest(top_n).sum()
    top_20_share_abnormality = (top_abnormal / total_abnormal) * 100

    return round(float(top_20_share_abnormality),1)

def generate_alerts(metrics: dict, concentration_pct: float, thresholds: dict) -> list:
    alerts = []

    if metrics["needs_review_pct"] > thresholds["review_overload_pct"]:
        alerts.append(
            f"Review overload: more than {thresholds['review_overload_pct']:.0f}% of patients need review"
        )

    total_patients = metrics["total_patients"]
    no_data_pct = (metrics["no_data_total"] / total_patients) * 100 if total_patients else 0
    if no_data_pct > thresholds["no_data_pct"]:
        alerts.append(
            f"Data quality issue: more than {thresholds['no_data_pct']:.0f}% of patients have missing data"
        )

    if concentration_pct >= thresholds["concentration_pct"]:
        alerts.append(
            f"Workload concentrated: {thresholds['concentration_pct']:.0f}% or more abnormalities contributed by 20% of patients"
        )

    return alerts

