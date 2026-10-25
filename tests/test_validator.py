from src.validator import clean_shift_records
from src.metrics import calculate_shift_metrics

def test_clean_shift_records_filters_bad_rows():
    shift_records = [{"machine_id": "CNC-01", "planned": "100", "actual": "90"},
                    {"machine_id": "CNC-01", "planned": "130", "actual": "N/A"},
                    {"machine_id": "", "planned": "100", "actual": "90"}
                    ]
    res = clean_shift_records(shift_records)
    assert res["rejected_count"] == 2
    assert res["total_valid_actual"] == 90
    assert len(res["clean_records"]) == 1

def test_calculate_shift_metrics_normal():
    sample_clean = [
        {"machine_id": "CNC-01",  "planned": 100, "actual": 95, "adherence_pct": 95.0},
        {"machine_id": "WELD-01", "planned": 200, "actual": 150, "adherence_pct": 75.0},
        {"machine_id": "CNC-01",  "planned": 100, "actual": 85, "adherence_pct": 85.0},
    ]
    res = calculate_shift_metrics(sample_clean)
    assert res["total_planned"] == 400

    assert res["total_actual"] == 330

    assert res["overall_adherence_pct"] == 82.5

    assert res["machine_production"]["CNC-01"] == 180

    assert res["top_performer_machine"] == "CNC-01"

    assert res["below_target_machines"] == ["WELD-01"]

def test_calculate_shift_metrics_empty():
    res = calculate_shift_metrics([])

    assert res["total_planned"] == 0 
    assert res["overall_adherence_pct"] == 0.0
    assert res["top_performer_machine"] ==  None

def test_below_target_machines_no_duplicates():
    sample_clean = [
        {"machine_id": "CNC-01",  "planned": 100, "actual": 95, "adherence_pct": 95.0},
        {"machine_id": "WELD-01", "planned": 200, "actual": 150, "adherence_pct": 75.0},
        {"machine_id": "WELD-01", "planned": 200, "actual": 150, "adherence_pct": 75.0},
        {"machine_id": "CNC-01",  "planned": 100, "actual": 85, "adherence_pct": 85.0},
    ]

    res = calculate_shift_metrics(sample_clean)

    assert res["below_target_machines"] == ["WELD-01"]