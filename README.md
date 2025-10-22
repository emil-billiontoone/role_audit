# Clarity LIMS Role Permission Testing System

A comprehensive, modular testing framework for validating role-based permissions in Clarity LIMS. Automated testing of 42+ permissions across multiple user roles with expected outcome validation and professional PDF reporting.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Store credentials (one-time setup)
python store_creds.py

# Test all roles with all add-on combinations
python run_all_roles.py "Emil" "Test"

# Or test a single role
python run_role_tests.py "Lab Operator"
```

That's it! PDF report auto-generates when done.

## Project Structure

```
role_audit/
├── run_role_tests.py              # Test single role
├── run_all_roles.py               # Test all roles + add-ons
├── role_permission_tester.py      # Core framework
├── role_test_configs.py           # Test configurations
├── generate_pdf_report.py         # PDF generator
├── permissions/                   # 42+ permission tests
└── test_results/                  # All outputs
    ├── all_role_tests.json        # Test results
    ├── role_test_report_*.pdf     # PDF reports
    └── screenshots/               # Test screenshots
```

## Available Tests (42+)

### Authentication & Access
Clarity Login, API Login, URL Check, Collaborations, Operations

### Project & Sample Management
Create/Delete Projects, Create/Delete/Update Samples, Workflow Assignment, Move to Next Step, Remove from Workflow, Sample Rework, Review Escalations, Requeue

### User & Role Management
Create/Read/Update/Delete Users, Create/Update/Delete Roles

### Quality Control & Reagents
Create/Update/Delete Controls, Create/Update/Delete Reagent Kits

### Process & Contact Management
Create/Read/Update/Delete Processes, Create/Read/Update/Delete Contacts

### Workflow & System
Edit Completed Steps, Overview Dashboard, Update Configuration, E-signature, Search, Lab Link Admin

## Role Configuration

Defined in `role_test_configs.py`:

### Main Roles
- Lab Operator (BTO)
- System Admin (BTO)
- Lab Admin (BTO)
- Limited (BTO)
- BTO API
- Not Logged In

### Add-On Roles
- Sample Creation (BTO)
- Editor
- Reagent Manufacturing (BTO)
- ReviewEscalations
- ReWork

## Usage Examples

### Test All Roles (Recommended)
```bash
# Tests each MAIN role with all ADD_ON combinations
python run_all_roles.py "Emil" "Test"

# Different server
python run_all_roles.py "Emil" "Test" --server staging

# Skip PDF generation
python run_all_roles.py "Emil" "Test" --no-pdf
```

**What it does:**
1. Initializes user to Lab Operator (BTO)
2. For each MAIN role:
   - Tests BASE role alone
   - Tests with each ADD_ON role
   - Prompts before next MAIN role
3. Auto-generates PDF report

### Test Single Role
```bash
python run_role_tests.py "Lab Operator"
python run_role_tests.py "System Admin" --server dev
```

### Generate PDF Report
```bash
# Auto-generated after run_all_roles.py
# Or manually:
python generate_pdf_report.py
python generate_pdf_report.py -i custom.json -o report.pdf
```

## PDF Reports

Professional reports auto-generated with:

 **Permission Test Reference** - Descriptions of all 42+ tests organized by category  
 **Summary Statistics** - Overall results and execution times  
 **Detailed Results** - Per-role tables with screenshots  
 **Color-Coded** - Green (pass), Red (fail), Orange (error)  
 **Execution Times** - Performance metrics  
 **Screenshots** - Documented for all tests  

See [docs/PDF_GUIDE.md](docs/PDF_GUIDE.md) for details.

## Test Results

### Console Output
```
============================================================
ROLE PERMISSION TEST SUITE
Role: Lab Operator (BTO)
Server: dev
Started: 2025-10-22 14:30:45
============================================================

Running test: Clarity Login
✓ Test passed as expected (11.2s)

Running test: Create Project
✓ Test failed as expected (permission denied) (41.7s)

============================================================
TEST SUMMARY
============================================================
Total Tests: 13
Passed (as expected): 13
Failed (unexpectedly): 0

Results saved to: test_results/all_role_tests.json
PDF report: test_results/role_test_report_20251022_143045.pdf
```

### JSON Results
`test_results/all_role_tests.json`:
```json
{
  "server": "dev",
  "timestamp": "2025-10-22 14:30:45",
  "tests": {
    "Lab Operator (BTO)": [
      {
        "test_name": "Clarity Login",
        "expected": true,
        "passed": true,
        "result": "pass",
        "execution_time": 11.2,
        "screenshot": "test_results/screenshots/clarity_login_20251022_143045.png"
      }
    ]
  }
}
```

## Creating New Tests

1. **Create test file:** `permissions/permissions_your_test.py`

```python
def test_your_permission(page, expected=True):
    """Checks if user can perform your action."""
    result = {
        "test_name": "Your Test",
        "description": "What it tests",
        "passed": False,
        "result": "fail"
    }
    
    # Your test logic here
    if can_perform_action:
        result["passed"] = True
        result["result"] = "pass"
    
    return result
```

2. **Add to config:** `role_test_configs.py`

```python
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator (BTO)": {
        "permissions_your_test": False,  # Expected outcome
    },
    "System Admin (BTO)": {
        "permissions_your_test": True,   # Expected outcome
    }
}
```

3. **Run tests:**
```bash
python run_role_tests.py "Lab Operator"
```

## Configuration

### Credentials
```bash
python store_creds.py
```

Stores credentials securely in system keyring.

### Server Environments
- `dev` - Development
- `staging` - Staging
- `prod` - Production

### Role Test Suites
Edit `role_test_configs.py`:
- Enable/disable tests (set to True/False)
- Add new tests
- Create custom test suites

## Advanced Features

- **Role Loop Testing** - Automatic testing of all role combinations
- **Smart Retry Logic** - Faster execution for expected failures
- **Screenshot Capture** - Automatic for all tests
- **Expected Outcomes** - Pass/fail validation
- **PDF Auto-Generation** - Professional reports
- **Combined Role Testing** - MAIN + ADD_ON permissions

See [docs/ADVANCED.md](docs/ADVANCED.md) for details.

## Key Features

 **42+ Permission Tests** - Comprehensive coverage  
 **Modular Design** - Easy to add/modify tests  
 **Expected Outcomes** - Validates test behavior  
 **Role Combinations** - Tests MAIN + ADD_ON roles  
 **Safe Role Management** - User always has ≥1 role  
 **Auto-Generated PDFs** - Professional reports  
 **Screenshot Documentation** - Visual evidence  
 **Execution Tracking** - Performance metrics  
 **Interactive Control** - Pause/continue between roles  
 **Organized Output** - All results in `test_results/`  

## Troubleshooting

**Credentials not found:**
```bash
python store_creds.py
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**Role assignment fails:**
- Verify role names match exactly (case-sensitive)
- Check user exists in the system

**Tests timing out:**
- Check network connection
- Increase timeout in test files

**Browser issues:**
- Browser auto-closes after tests
- Press Ctrl+C if stuck

## Documentation

- **README.md** (this file) - Main documentation
- **[docs/PDF_GUIDE.md](docs/PDF_GUIDE.md)** - PDF report details
- **[docs/ADVANCED.md](docs/ADVANCED.md)** - Advanced features and configuration
- **QUICK_START.md** - Fast reference guide

## Requirements

```
playwright>=1.40.0
keyring>=23.0.0
reportlab>=4.0.0
s4 (custom Clarity LIMS API library)
```

## Recent Updates (October 2025)

- 42+ permission tests with comprehensive coverage
- Sequential role testing with safe transitions
- MAIN + ADD_ON role combination testing
- Professional PDF reports with test reference section
- Automatic screenshot capture for all tests
- Smart retry logic for faster execution
- Centralized test results in `test_results/` folder
- Expected outcome validation
- Color-coded results
- Execution time tracking

## License

Internal BTO tool for Clarity LIMS permission testing.

---

**Quick Commands:**
```bash
# Install
pip install -r requirements.txt && python store_creds.py

# Test all roles
python run_all_roles.py "Emil" "Test"

# Test one role
python run_role_tests.py "Lab Operator"

# Generate PDF
python generate_pdf_report.py
```

