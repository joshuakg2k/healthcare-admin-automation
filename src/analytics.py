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

def generate_alerts(metrics: dict, concentration_pct: float) -> list:
    alerts = []
    
    if metrics['needs_review_pct'] > 60:
       alerts.append(f'Review overload: more than 60% of patients need review')
    if metrics['no_data_pct'] > 10:
        alerts.append(f'Data Quality issue: more than 10% of patients have missing data')
    if concentration_pct >= 50:
        alerts.append(f'Workload concentrated: 50% or more abnormalities contributed by 20% of patients')
    return alerts 

