import csv
import json
from pathlib import Path

def clean_shift_records(raw_records):
    rejected_count = 0
    clean_records = []
    quarantined_rows = []
    total_valid_actual = 0
    
    for record in raw_records:
        machine_id = record.get("machine_id")
        if not machine_id:
            rejected_count += 1
            quarantined_rows.append({**record, "failure_reason": "Missing machine_id"})
            continue
            
        try:
            planned = int(record.get("planned"))
            actual = int(record.get("actual"))

        except (ValueError, TypeError):
            rejected_count += 1
            quarantined_rows.append({**record, "failure_reason": "Corrupt non-integer number"})
            continue
            
        if planned <= 0 or actual < 0:
            rejected_count += 1
            quarantined_rows.append({**record, "failure_reason": "Invalid range (planned <= 0 or actual < 0)"})
            continue
        adherence_pct = round((actual / planned) * 100, 2)   
        clean_records.append({
            "machine_id": machine_id, 
            "planned": planned, 
            "actual": actual,
            "adherence_pct": adherence_pct
        })
        
    for clean_record in clean_records:
        total_valid_actual += clean_record["actual"]
        
    return {
        "clean_records": clean_records,
        "quarantined_rows": quarantined_rows,
        "rejected_count": rejected_count,
        "total_valid_actual": total_valid_actual
    }

def export_audit_reports(validation_result, output_dir="output"):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Export Clean Summary as JSON
    json_file = out_path / "clean_shift_summary.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(validation_result, f, indent=4)
        
    # 2. Export Quarantined Rows as CSV
    csv_file = out_path / "quarantined_audit_log.csv"
    quarantined = validation_result["quarantined_rows"]
    if quarantined:
        keys = quarantined[0].keys()
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(quarantined)
            
    print(f"Audit reports successfully exported to {out_path.resolve()}")

def process_shift_csv_file(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found at {path}")
        return {"error": "File not found", "clean_records": [], "rejected_count": 0,"quarantined_rows": [],"total_valid_actual": 0},

    raw_rows = []
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_rows.append(row)
            
    return clean_shift_records(raw_rows)

