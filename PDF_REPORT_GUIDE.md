# PDF Report Generation Guide

## Overview

The `generate_pdf_report.py` script creates comprehensive, professional PDF reports from your test results JSON file.

## Installation

First, install the required dependency:

```bash
pip install reportlab
# Or install all requirements:
pip install -r requirements.txt
```

## Automatic Generation

**By default, PDF reports are automatically generated** after running the complete test suite:

```bash
python run_all_roles.py "Emil" "Test"
```

This will:
1. Run all tests
2. Save results to JSON
3. **Automatically generate a PDF report** at the end

### Skip PDF Generation

If you want to skip automatic PDF generation:

```bash
python run_all_roles.py "Emil" "Test" --no-pdf
```

## Manual Generation

You can also generate PDF reports manually from existing JSON results:

### Basic Usage

```bash
# Generate from default JSON file
python generate_pdf_report.py

# This reads: test_results/all_role_tests.json
# Creates: test_results/role_test_report_YYYYMMDD_HHMMSS.pdf
```

### Custom Input/Output

```bash
# Specify custom input file
python generate_pdf_report.py --input custom_results.json

# Specify custom output file
python generate_pdf_report.py --output my_report.pdf

# Both
python generate_pdf_report.py -i results.json -o report.pdf
```

## PDF Report Contents

### 📄 Page 1: Overview & Header

**Header Section:**
- Report title
- Server environment (dev/staging/prod)
- Test execution timestamp
- Total role configurations tested

### 📖 Pages 2-4: Permission Test Reference

**Comprehensive test descriptions organized by category:**
- **Authentication & Access** - Login and access control tests
- **Project Management** - Project creation and deletion
- **Sample Management** - Sample lifecycle operations
- **Workflow Operations** - Workflow and step management
- **User Management** - User account operations
- **Quality Control** - Control sample management
- **Reagent Management** - Reagent kit operations
- **Process Management** - Process definition operations
- **Role Management** - Role and permission management
- **Contact Management** - Contact record operations
- **System Administration** - Configuration and admin functions

**For each test:**
- Test name in bold
- 1-2 sentence description of what it tests
- Explanation of how it validates permissions

### 📊 Page 5: Summary Statistics

- Role configurations tested
- Total test executions
- Tests passed (as expected)
- Tests failed (unexpected)
- Errors encountered
- **Total execution time**
- **Average time per test**

### 📄 Subsequent Pages: Detailed Results

**For Each Role Configuration:**
- Role name (e.g., "Lab Operator (BTO) + Editor")
- Quick statistics (total, passed, failed, errors)
- **Execution time summary** (total time, average per test)
- Detailed test table with **wider columns** for better readability:
  - Test name
  - Expected result (✓/✗)
  - Actual result (✓/✗)
  - Execution time (seconds)
  - Status (PASS/FAIL/ERROR) - color coded
    - 🟢 Green = PASS
    - 🔴 Red = FAIL
    - 🟠 Orange = ERROR
  - **Screenshot filename**

**Error Summary (if any):**
- Only shown when errors occur
- Test name and error message
- Concise format

## PDF Features

✅ **Professional Layout** - Clean, organized, easy to read  
✅ **Permission Test Reference** - Comprehensive descriptions of all 42+ permission tests organized by category  
✅ **Color-Coded Results** - Quick visual identification of issues  
✅ **Comprehensive Data** - All test information included  
✅ **Summary Statistics** - High-level overview at a glance  
✅ **Execution Time Tracking** - Total and average times per role and overall  
✅ **Screenshot Documentation** - Filename in table for quick reference  
✅ **Categorized Tests** - Tests organized by functional area (Authentication, Samples, Users, etc.)  
✅ **Test Explanations** - 1-2 sentence descriptions of what each test validates and how  
✅ **Error Details** - Full error messages for debugging  
✅ **Timestamped** - Auto-generated filenames with date/time  
✅ **Table of Results** - Organized by role configuration  

## Example Output Structure

```
role_test_report_20251022_143045.pdf

┌─────────────────────────────────────────────────┐
│  Role Permission Test Report                    │
│                                                  │
│  Server:                    dev                 │
│  Test Date:                 2025-10-22 14:30:45 │
│  Total Role Configurations: 30                  │
└─────────────────────────────────────────────────┘

[PAGE BREAK]

┌─────────────────────────────────────────────────┐
│  Permission Test Reference                      │
│                                                  │
│  This section provides detailed descriptions... │
│                                                  │
│  Authentication & Access                        │
│  ┌──────────────┬──────────────────────────┐   │
│  │ Clarity Login│ Tests ability to authen- │   │
│  │              │ ticate and access the... │   │
│  ├──────────────┼──────────────────────────┤   │
│  │ Api Login    │ Tests ability to authen- │   │
│  │              │ ticate and connect to... │   │
│  └──────────────┴──────────────────────────┘   │
│                                                  │
│  Sample Management                              │
│  ┌───────────────┬─────────────────────────┐   │
│  │ Create Sample │ Tests permission to...  │   │
│  │ Delete Sample │ Tests permission to...  │   │
│  │ Update Sample │ Tests permission to...  │   │
│  └───────────────┴─────────────────────────┘   │
│                                                  │
│  [... more categories ...]                      │
└─────────────────────────────────────────────────┘

[PAGE BREAK]

┌─────────────────────────────────────────────────┐
│  Summary Statistics                             │
│  ┌──────────────────────────────┬─────────┐    │
│  │ Metric                       │ Count   │    │
│  ├──────────────────────────────┼─────────┤    │
│  │ Role Configurations Tested   │ 30      │    │
│  │ Total Test Executions        │ 95      │    │
│  │ Tests Passed (as expected)   │ 92      │    │
│  │ Tests Failed (unexpected)    │ 3       │    │
│  │ Errors Encountered           │ 0       │    │
│  │ Total Execution Time         │ 285.4s  │    │
│  │ Average Time per Test        │ 3.0s    │    │
│  └──────────────────────────────┴─────────┘    │
└─────────────────────────────────────────────────┘

[PAGE BREAK]

┌─────────────────────────────────────────────────┐
│  Detailed Test Results by Role                  │
│                                                  │
│  Role: Lab Operator (BTO) (BASE)                │
│  Tests: 2 | Passed: 2 | Failed: 0 | Errors: 0  │
│  Total Execution Time: 11.6s | Average: 5.8s   │
│                                                  │
│  ┌───────────────┬────┬────┬──────┬──────┬──────────────┐
│  │ Test Name     │Exp │Res │Time  │Status│Screenshot    │
│  ├───────────────┼────┼────┼──────┼──────┼──────────────┤
│  │ Clarity Login │ ✓  │ ✓  │11.2s │PASS  │clarity_...png│
│  │ Api Login     │ ✓  │ ✓  │ 0.4s │PASS  │api_login...  │
│  └───────────────┴────┴────┴──────┴──────┴──────────────┘
│                                                  │
│  [No errors - error section not shown]          │
│                                                  │
│  Role: Lab Operator (BTO) + Sample Creation...  │
│  Tests: 3 | Passed: 2 | Failed: 1 | Errors: 0  │
│  Total Execution Time: 53.3s | Average: 17.8s  │
│                                                  │
│  ┌───────────────┬────┬────┬──────┬──────┬──────────────┐
│  │ Test Name     │Exp │Res │Time  │Status│Screenshot    │
│  ├───────────────┼────┼────┼──────┼──────┼──────────────┤
│  │ Clarity Login │ ✓  │ ✓  │11.2s │PASS  │clarity_...png│
│  │ Api Login     │ ✓  │ ✓  │ 0.4s │PASS  │api_login...  │
│  │ Create Project│ ✗  │ ✗  │41.7s │PASS  │create_pro... │
│  └───────────────┴────┴────┴──────┴──────┴──────────────┘
│                                                  │
│  [No errors - all tests behaved as expected]    │
│                                                  │
│  [... more roles ...]                           │
└─────────────────────────────────────────────────┘
```

## Use Cases

### After Full Test Run

```bash
# Run all tests and auto-generate PDF
python run_all_roles.py "Emil" "Test"

# PDF is automatically created at the end
# Location shown in output
```

### Regenerate PDF from Existing Results

```bash
# Maybe you updated the formatting - regenerate PDF
python generate_pdf_report.py

# Creates new timestamped PDF from existing JSON
```

### Create Custom Report

```bash
# Generate PDF from specific test results
python generate_pdf_report.py \
  --input test_results/backup_20251020.json \
  --output reports/october_audit.pdf
```

### Share Results

The PDF format is perfect for:
- 📧 **Email attachments** - Share with team/stakeholders
- 📊 **Documentation** - Archive test results
- 🖨️ **Printing** - Physical copies for review meetings
- 💼 **Presentations** - Professional format for reports

## Troubleshooting

### "Module reportlab not found"

Install reportlab:
```bash
pip install reportlab
```

### "JSON file not found"

Make sure you've run tests first:
```bash
python run_all_roles.py "Emil" "Test"
```

### PDF looks wrong or incomplete

Regenerate the PDF:
```bash
python generate_pdf_report.py
```

### Want to customize the PDF

Edit `generate_pdf_report.py`:
- Modify colors in `_setup_custom_styles()`
- Change table layouts in `_create_role_section()`
- Adjust page sizes/margins in `generate_pdf()`

## File Locations

```
role_audit/
├── generate_pdf_report.py          # PDF generator script
├── test_results/
│   ├── all_role_tests.json         # Source data
│   └── role_test_report_*.pdf      # Generated PDFs (timestamped)
```

## Tips

💡 **Automatic is Best** - Let `run_all_roles.py` auto-generate the PDF after tests  
💡 **Keep JSON** - Always keep the JSON file as your source of truth  
💡 **Timestamped Files** - Each PDF has a unique timestamp, won't overwrite  
💡 **Custom Names** - Use `--output` for specific filenames when needed  
💡 **Batch Processing** - Generate PDFs from multiple JSON files in a loop  

## Summary

**Quick Start:**
```bash
# Just run your tests - PDF is created automatically!
python run_all_roles.py "Emil" "Test"
```

**Manual Generation:**
```bash
# Generate PDF from existing results
python generate_pdf_report.py
```

That's it! Your professional PDF reports are ready to share! 📄✨

