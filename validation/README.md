# Data Validation

Checks generated CSV files for required files, duplicate primary identifiers, duplicate SKUs, product foreign keys, non-negative prices/costs/stock, valid dates, and promotion discount constraints.

Run from the `Backend` directory:

```bash
python -m validation.validate_data --data ../Database/sample_data
```

The validator writes `validation_report.json` into the data directory and exits with:
- `0` when validation passes
- `1` when validation fails

Warnings are reported separately from blocking errors.
