"""Validate generated CSV datasets for keys, relationships, ranges and dates."""
import argparse
import csv
import json
from pathlib import Path
from datetime import datetime


def load_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate(data_dir: Path):
    errors, warnings, checks = [], [], []

    required = [
        "products.csv", "cost_records.csv", "inventory_snapshots.csv",
        "competitor_observations.csv", "price_history.csv", "promotions.csv"
    ]
    data = {}
    for filename in required:
        try:
            data[filename] = load_csv(data_dir / filename)
            checks.append(f"Loaded {filename}: {len(data[filename])} rows")
        except Exception as exc:
            errors.append(str(exc))

    if errors:
        return {"status": "FAILED", "errors": errors, "warnings": warnings, "checks": checks}

    def ids(rows, field, label):
        values = [r[field] for r in rows]
        if len(values) != len(set(values)):
            errors.append(f"Duplicate {label} values found.")
        return set(values)

    products = data["products.csv"]
    product_ids = ids(products, "product_id", "products.product_id")
    ids(data["cost_records.csv"], "cost_id", "cost_records.cost_id")
    ids(data["inventory_snapshots.csv"], "inventory_id", "inventory.inventory_id")
    ids(data["competitor_observations.csv"], "observation_id", "competitor.observation_id")
    ids(data["price_history.csv"], "price_history_id", "price_history.price_history_id")
    ids(data["promotions.csv"], "promotion_id", "promotions.promotion_id")

    skus = [r["sku"] for r in products]
    if len(skus) != len(set(skus)):
        errors.append("Duplicate product SKU values found.")

    def fk_check(rows, field, label):
        for row in rows:
            if row[field] not in product_ids:
                errors.append(f"{label}: product_id {row[field]} has no matching product.")

    for filename, label in [
        ("cost_records.csv", "cost record"),
        ("inventory_snapshots.csv", "inventory snapshot"),
        ("competitor_observations.csv", "competitor observation"),
        ("price_history.csv", "price history")
    ]:
        fk_check(data[filename], "product_id", label)

    for row in products:
        if float(row["current_selling_price"]) < 0:
            errors.append(f"Product {row['sku']} has a negative selling price.")

    for row in data["cost_records.csv"]:
        if float(row["unit_cost"]) < 0:
            errors.append(f"Cost record {row['cost_id']} has a negative unit cost.")
        if row["effective_to"] and row["effective_to"] < row["effective_from"]:
            errors.append(f"Cost record {row['cost_id']} has invalid effective dates.")

    for row in data["inventory_snapshots.csv"]:
        if int(row["available_stock"]) < 0 or int(row["reserved_stock"]) < 0:
            errors.append(f"Inventory record {row['inventory_id']} has negative stock.")
        if int(row["reserved_stock"]) > int(row["available_stock"]):
            warnings.append(f"Inventory record {row['inventory_id']}: reserved stock exceeds available stock.")

    for row in data["competitor_observations.csv"]:
        if float(row["competitor_price"]) < 0:
            errors.append(f"Competitor observation {row['observation_id']} has negative price.")
        try:
            datetime.fromisoformat(row["observed_at"])
        except ValueError:
            errors.append(f"Competitor observation {row['observation_id']} has invalid observed_at.")

    for row in data["price_history.csv"]:
        if float(row["selling_price"]) < 0:
            errors.append(f"Price history {row['price_history_id']} has negative price.")
        if row["valid_to"] and row["valid_to"] < row["valid_from"]:
            errors.append(f"Price history {row['price_history_id']} has invalid validity dates.")

    for row in data["promotions.csv"]:
        if row["discount_type"] not in {"PERCENTAGE", "FIXED"}:
            errors.append(f"Promotion {row['promotion_id']} has invalid discount_type.")
        if float(row["discount_value"]) <= 0:
            errors.append(f"Promotion {row['promotion_id']} has non-positive discount.")
        if row["end_at"] < row["start_at"]:
            errors.append(f"Promotion {row['promotion_id']} ends before it starts.")
        if row["discount_type"] == "PERCENTAGE" and float(row["discount_value"]) >= 100:
            errors.append(f"Promotion {row['promotion_id']} percentage discount must be below 100.")

    report = {
        "status": "PASSED" if not errors else "FAILED",
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "row_counts": {name: len(rows) for name, rows in data.items()}
    }
    (data_dir / "validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Validate generated pricing simulation CSV data.")
    parser.add_argument("--data", type=Path, required=True, help="Directory containing generated CSV files")
    args = parser.parse_args()
    report = validate(args.data)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASSED" else 1)


if __name__ == "__main__":
    main()
