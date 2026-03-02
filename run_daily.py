import argparse
import os
from src.pipeline import run_daily_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Run the Healthcare Admin Automation Pipeline (synthetic data)."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV (e.g., Data/sample_input.csv)"
    )
    args = parser.parse_args()

    # Make path safe if user gives relative path
    input_path = args.input

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    result = run_daily_pipeline(input_path)

    print("\n✅ Pipeline completed successfully")
    print("📄 Report saved to:", result["report_path"])
    print("📊 Patient table saved to:", result["patient_table_path"])
    print("📈 Priority summary saved to:", result["priority_summary_path"])

    if result.get("alerts"):
        print("\n⚠️ Alerts:")
        for a in result["alerts"]:
            print("-", a)
    else:
        print("\nNo alerts triggered.")


if __name__ == "__main__":
    main()
    