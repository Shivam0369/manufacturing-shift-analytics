def calculate_shift_metrics(clean_records, min_adherence = 85):
    machine_production ={}
    max_actual = -1
    top_performer_machine = None
    total_planned = 0
    total_actual = 0
    below_target_machines = []
    if not clean_records:
        return {
    "total_planned": 0,
    "total_actual": 0,
    "overall_adherence_pct": 0.0,
    "machine_production": {},
    "top_performer_machine": None,
    "below_target_machines": []
}
    else:
        for record in clean_records:
            total_planned += record["planned"]
            total_actual += record["actual"]
            machine_id = record["machine_id"]
            if record["adherence_pct"] < min_adherence and machine_id not in below_target_machines:
                below_target_machines.append(machine_id)
            if machine_id not in machine_production:
                machine_production[machine_id] = 0
            machine_production[machine_id] += record["actual"]
        if total_planned > 0:
            overall_adherence_pct = round((total_actual/total_planned)*100,2)
        for machine,actual in machine_production.items():
            if max_actual < actual:
                max_actual = actual
                top_performer_machine = machine        
    return {
        "total_planned":total_planned,
        "total_actual":total_actual,
        "overall_adherence_pct": overall_adherence_pct,
        "machine_production":machine_production,
        "top_performer_machine":top_performer_machine,
        "below_target_machines": below_target_machines
    }

if __name__ == "__main__":
    sample_clean = [
        {"machine_id": "CNC-01",  "planned": 100, "actual": 95, "adherence_pct": 95.0},
        {"machine_id": "WELD-01", "planned": 200, "actual": 150, "adherence_pct": 75.0},
        {"machine_id": "CNC-01",  "planned": 100, "actual": 85, "adherence_pct": 85.0},
    ]

    print(calculate_shift_metrics(sample_clean))
    print(calculate_shift_metrics([]))