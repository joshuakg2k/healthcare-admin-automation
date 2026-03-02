# Healthcare Admin Analytics & Reporting Pipeline (Synthetic Data)

A simple healthcare admin automation tool that processes lab-style results table (synthetic data), flags abnormalities and missing data, assigns admin priority, and exports a daily report + CSV tables.

> Administrative support only — not for clinical or diagnostic use.

## What it does
- Reads a test-level CSV (one row per test result)
- Classifies each result: LOW / NORMAL / HIGH / NO DATA
- Aggregates to patient-level workload summaries
- Assigns admin priority (HIGH / MEDIUM / LOW / NO DATA)
- Computes workload signals (review load, data quality, workload concentration)
- Exports:
  - Daily text report (email-ready)
  - Patient admin table CSV
  - Priority summary CSV

## Outputs
Generated files are written to:
- `outputs/reports/`
- `outputs/tables/`

## How to run (demo)
Install requirements:
```bash
pip install -r requirements.txt
## Run from command line (CLI)
```bash
python run_daily.py --input Data/sample_input.csv

