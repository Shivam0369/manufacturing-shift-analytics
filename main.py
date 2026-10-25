from pathlib import Path
from src.validator import process_shift_csv_file, export_audit_reports
from src.metrics import calculate_shift_metrics

def main():
    print("=== Manufacturing Shift Log Validator (Project A) ===")
    
    # Use Path(__file__) to make the file path robust against directory changes (M-010 fix)
    BASE_DIR = Path(__file__).parent
    input_file = BASE_DIR / "sample_shift.csv"
    
    result = process_shift_csv_file(input_file)
    metrics = calculate_shift_metrics(result["clean_records"])
    
    print(f"\nProcessing complete for: {input_file.name}")
    print(f"Total Valid Clean Records: {len(result['clean_records'])}")
    print(f"Total Quarantined/Rejected Rows: {result['rejected_count']}")
    print(f"Total Valid Actual Production: {result['total_valid_actual']}")
    
    result["shift_metrics"] = metrics
    # Export reports to disk
    export_audit_reports(result)

if __name__ == "__main__":
    main()