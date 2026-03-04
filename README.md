# Healthcare Admin Analytics & Reporting Pipeline (Synthetic Data)
---

A simple healthcare admin automation tool that processes lab-style tabular results (synthetic data), flags abnormalities and missing data, assigns administrative priority, and exports a structured daily report and CSV tables.

> Administrative support only — not for clinical or diagnostic use.

---

## What It Does

- Reads a test-level CSV (one row per test result)
- Classifies each result: LOW / NORMAL / HIGH / NO DATA
- Aggregates results to patient-level workload summaries
- Assigns administrative priority (HIGH / MEDIUM / LOW / NO DATA)
- Computes workload signals:
  - Review load percentage
  - Missing data rate
  - Workload concentration (top 20% abnormality share)
- Generates operational alerts based on configurable thresholds
- Exports:
  - Daily text report (email-ready format)
  - Patient-level admin CSV table
  - Priority summary CSV

---
## Pipeline Overview

```
Input CSV
   ↓
Validate Input Data
   ↓
Classify Test Results
   ↓
Aggregate Patient Results
   ↓
Compute Analytics Metrics
   ↓
Generate Operational Alerts
   ↓
Build Executive Summary
   ↓
Export Reports & Tables
```
---

## Outputs

Generated files are written to:

- `outputs/reports/`
- `outputs/tables/`

Outputs include:
- Daily healthcare admin text report
- Patient-level prioritisation table
- Priority distribution summary

---


## Configurable Alert Thresholds

Alert thresholds are configurable in:
- config.py

You can modify:
- Review overload percentage threshold

- Missing data percentage threshold

- Workload concentration threshold
---
## Example Output

A sample report excerpt is available here:
- docs/sample_report_excerpt.txt
---

## Project Structure

```
healthcare-admin-automation/
│
├── Data/                    # Example synthetic dataset
│
├── Notebook/                # Exploration and demo notebooks
│   ├── 01_exploration.ipynb
│   └── demo_run.ipynb
│
├── src/                     # Core pipeline modules
│   ├── classify.py
│   ├── aggregate.py
│   ├── analytics.py
│   ├── report.py
│   ├── export.py
│   └── pipeline.py
│
├── outputs/                 # Generated outputs (ignored in git)
│   ├── reports/
│   └── tables/
│
├── docs/
│   └── sample_report_excerpt.txt
│
├── run_daily.py             # CLI entry point
├── requirements.txt
└── README.md
```

---
## How to Run
### Install Requirements

```bash
pip install -r requirements.txt
```

### Run the Pipeline from Command Line (CLI)

```bash
python run_daily.py --input Data/sample_input.csv
```

What Happens When You Run It

The pipeline will:

- Validate the input dataset
- Classify lab results (LOW / NORMAL / HIGH / NO DATA)
- Aggregate patient-level workload metrics
- Generate operational alerts
- Export:
  - Daily text report → outputs/reports/
  - Patient admin table → outputs/tables/
  - Priority summary → outputs/tables/
