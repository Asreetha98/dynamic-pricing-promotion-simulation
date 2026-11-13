def normalize_demand_signal(units_sold: int, baseline_units: float) -> float:
    if baseline_units <= 0:
        return 1.0
    return max(0.0, min(3.0, units_sold / baseline_units))
