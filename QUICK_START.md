# Quick Start Guide

## Installation

```bash
# Install dependencies (including reportlab for PDF generation)
pip install -r requirements.txt

# Store credentials
python store_creds.py
```

## Running Tests

### Option 1: Test All Roles (Recommended)

```bash
python run_all_roles.py "Emil" "Test"
```

**This will:**
1. ✅ Initialize user to Lab Operator (BTO) only
2. ✅ Test each MAIN role (Lab Operator, System Admin, etc.)
3. ✅ For each MAIN role, test with ALL ADD_ON combinations
4. ✅ Automatically generate professional PDF report
5. ✅ Prompt after each MAIN role completes

**Example flow:**
- Lab Operator (BTO) BASE
- Lab Operator (BTO) + Sample Creation (BTO)
- Lab Operator (BTO) + Editor
- Lab Operator (BTO) + Reagent Manufacturing (BTO)
- Lab Operator (BTO) + ReviewEscalations
- Lab Operator (BTO) + ReWork
- → **PROMPT: Continue to System Admin?**
- System Admin (BTO) BASE
- ... (repeat for all MAIN roles)

### Option 2: Test Single Role

```bash
python run_role_tests.py "Lab Operator"
```

## Results

### JSON Results
Automatically saved to: `test_results/all_role_tests.json`

### PDF Reports
Automatically generated: `test_results/role_test_report_YYYYMMDD_HHMMSS.pdf`

**PDF includes:**
- 📊 Summary statistics
- 📋 Detailed results for each role
- 🎨 Color-coded pass/fail indicators
- 🔍 Error details

### Screenshots
Saved to: `screenshots/`

## Generate PDF from Existing Results

```bash
# Regenerate PDF from JSON
python generate_pdf_report.py

# Custom files
python generate_pdf_report.py -i results.json -o my_report.pdf
```

## Common Options

```bash
# Different server
python run_all_roles.py "Emil" "Test" --server staging

# Skip PDF generation
python run_all_roles.py "Emil" "Test" --no-pdf

# Help
python run_all_roles.py --help
python generate_pdf_report.py --help
```

## What Gets Tested

With 5 MAIN roles and 5 ADD_ON roles:
- **Total combinations**: 30 (5 MAIN × 6 configs each)
- **Configs per MAIN**: BASE + 5 ADD_ONs
- **Prompts**: 4 (after each MAIN role except last)

## Documentation

- **README.md** - Full documentation
- **PDF_REPORT_GUIDE.md** - PDF generation details
- **TEST_FLOW_SUMMARY.md** - Complete test sequence
- **ROLE_LOOP_GUIDE.md** - Loop functionality details

## That's It!

```bash
python run_all_roles.py "Emil" "Test"
```

Sit back and let it run. PDF report will be ready when done! ✨

