# PDF Report Guide

## Quick Start

```bash
# Auto-generated after tests
python run_all_roles.py "Emil" "Test"

# Manual generation
python generate_pdf_report.py

# Custom files
python generate_pdf_report.py -i results.json -o my_report.pdf
```

## PDF Contents

### Page 1: Header
- Report title
- Server environment (dev/staging/prod)
- Test execution timestamp
- Total role configurations tested

### Pages 2-4: Permission Test Reference
**42+ tests organized by category:**
- Authentication & Access
- Project/Sample/User Management
- Quality Control & Reagents
- Process/Role/Contact Management
- System Administration

Each test includes:
- Test name
- 1-2 sentence description
- How it validates permissions

### Page 5: Summary Statistics
- Total test executions
- Pass/fail counts
- Total & average execution times

### Pages 6+: Detailed Results by Role
- Role statistics (tests, passed, failed, time)
- Test results table with:
  - Test name
  - Expected/Actual results (✓/✗)
  - Execution time
  - Status (color-coded: 🟢 PASS, 🔴 FAIL, 🟠 ERROR)
  - Screenshot filename
- Error summary (only if errors exist)

## Features

✅ **Permission Test Reference** - All tests explained  
✅ **Color-Coded Results** - Quick visual status  
✅ **Execution Time Tracking** - Performance metrics  
✅ **Screenshot Documentation** - Evidence included  
✅ **Clean Layout** - Wide columns, good spacing  
✅ **Automatic Generation** - No config needed  

## Installation

```bash
pip install reportlab
```

## Options

```bash
# Skip PDF generation
python run_all_roles.py "Emil" "Test" --no-pdf

# Regenerate from JSON
python generate_pdf_report.py

# Help
python generate_pdf_report.py --help
```

## File Location

All outputs in `test_results/`:
- `all_role_tests.json` - Source data
- `role_test_report_YYYYMMDD_HHMMSS.pdf` - Generated PDFs
- `screenshots/` - Test screenshots

## Customization

Edit `generate_pdf_report.py` to modify:
- Test descriptions in `PERMISSION_DESCRIPTIONS`
- Category organization
- Colors and styling
- Table layouts

## Troubleshooting

**Missing reportlab:**
```bash
pip install reportlab
```

**JSON file not found:**
Run tests first to generate results.

**PDF looks wrong:**
Regenerate: `python generate_pdf_report.py`

