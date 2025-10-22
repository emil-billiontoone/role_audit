# Quick Start Guide

## Setup (One-Time)

```bash
cd /Users/edeguzman/projects/code/2025/role_audit

# Install dependencies
pip install -r requirements.txt

# Store credentials
python store_creds.py
```

## Run Tests

### Test All Roles (Recommended)
```bash
python run_all_roles.py "Emil" "Test"
```

This will:
- Test each MAIN role (Lab Operator, System Admin, etc.)
- Test each with ALL add-on combinations
- Auto-generate PDF report
- Save everything to `test_results/`

### Test Single Role
```bash
python run_role_tests.py "Lab Operator"
python run_role_tests.py "System Admin" --server staging
```

## Results

- **JSON**: `test_results/all_role_tests.json`
- **PDF**: `test_results/role_test_report_*.pdf`
- **Screenshots**: `test_results/screenshots/`

## Generate PDF Manually

```bash
python generate_pdf_report.py
```

## Common Options

```bash
# Different server
python run_all_roles.py "Emil" "Test" --server staging

# Skip PDF
python run_all_roles.py "Emil" "Test" --no-pdf

# Help
python run_all_roles.py --help
```

## What Gets Tested

**5 MAIN Roles:**
- Lab Operator (BTO)
- System Admin (BTO)
- Lab Admin (BTO)
- Limited (BTO)
- BTO API

**5 ADD_ON Roles:**
- Sample Creation (BTO)
- Editor
- Reagent Manufacturing (BTO)
- ReviewEscalations
- ReWork

**= 30 total combinations** (5 MAIN × 6 configs each)

## Stopping Mid-Test

Press `n` when prompted after each MAIN role completes.

## Troubleshooting

```bash
# Credentials
python store_creds.py

# Dependencies
pip install -r requirements.txt

# Check results
ls test_results/
```

## Full Documentation

See [README.md](README.md) for complete documentation.

