# Advanced Features

## Role Loop Testing

### Overview
`run_all_roles.py` automatically tests all roles with all add-on combinations.

### Usage
```bash
python run_all_roles.py "Emil" "Test"
python run_all_roles.py "Emil" "Test" --server dev
```

### How It Works

**For each MAIN role:**
1. Test BASE role alone
2. Test with Sample Creation (BTO)
3. Test with Editor
4. Test with Reagent Manufacturing (BTO)
5. Test with ReviewEscalations
6. Test with ReWork
7. **PROMPT** - Continue to next MAIN role?

**Role Management:**
- User starts with Lab Operator (BTO) only
- Adds new role before removing old (always has ≥1 role)
- Tests all permissions from both MAIN + ADD_ON

### Test Flow Example

```
Initialize: Lab Operator (BTO) only

MAIN ROLE 1/5: Lab Operator (BTO)
├─ Lab Operator (BTO) [BASE]
├─ Lab Operator (BTO) + Sample Creation (BTO)
├─ Lab Operator (BTO) + Editor
├─ Lab Operator (BTO) + Reagent Manufacturing (BTO)
├─ Lab Operator (BTO) + ReviewEscalations
└─ Lab Operator (BTO) + ReWork
   → PROMPT: Continue to System Admin?

MAIN ROLE 2/5: System Admin (BTO)
├─ System Admin (BTO) [BASE]
├─ System Admin (BTO) + Sample Creation (BTO)
└─ ... (repeat for all add-ons)
```

### Total Test Runs
- **5 MAIN roles** × **6 configs each** (1 BASE + 5 ADD_ONs)
- **= 30 total test combinations**
- **4 prompts** (after each MAIN role except last)

### Key Features
✅ Safe role transitions (never 0 roles)  
✅ Combined permission testing  
✅ Interactive control (can stop anytime)  
✅ Automatic PDF generation  
✅ Comprehensive coverage  

## Test Configuration

### Main Roles
Located in `role_test_configs.py`:

```python
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator (BTO)": {
        "permissions_clarity_login": True,
        "permissions_API_login": True,
        "permissions_create_project": False,
        # ...
    },
    "System Admin (BTO)": {
        # ...
    }
}
```

### Add-On Roles
```python
ADD_ON_ROLE_TEST_SUITES = {
    "Sample Creation (BTO)": {
        "permissions_create_project": True,
        # ...
    },
    "Editor": {
        "permissions_edit_completed_steps": True,
    }
}
```

### Customization

**Add a new test:**
1. Create `permissions/permissions_your_test.py`
2. Add to `role_test_configs.py`
3. Set expected outcome (True/False)

**Modify role combinations:**
- Edit `MAIN_ROLE_TEST_SUITES` or `ADD_ON_ROLE_TEST_SUITES`
- Comment out tests you don't want to run

## Single Role Testing

```bash
# Test one role
python run_role_tests.py "Lab Operator"

# Different servers
python run_role_tests.py "System Admin" --server staging

# Quick test
python run_role_tests.py quick
```

## Results Management

### JSON Results
`test_results/all_role_tests.json`:
- Consolidated results for all roles
- Test details with expected/actual outcomes
- Execution times
- Screenshot paths
- Error messages

### PDF Reports
Auto-generated with:
- Permission test reference
- Summary statistics
- Detailed results per role
- Screenshots and errors

### Screenshots
`test_results/screenshots/`:
- Automatically captured for all tests
- Timestamped filenames
- Referenced in JSON and PDF

## Performance

### Execution Times
- Tracked per test
- Summarized per role
- Overall averages in PDF

### Smart Retry Logic
- Tests expected to pass: Retry 2x on failure
- Tests expected to fail: Run once (no retries)
- Saves time on negative tests

### Browser Control
- Headless mode available
- Configurable slow-mo
- Automatic cleanup

## Best Practices

1. **Test on dev first** - Always validate on dev before staging/prod
2. **Review prompts** - Check results before continuing
3. **Save credentials** - Run `store_creds.py` once
4. **Organize results** - Everything in `test_results/`
5. **Check PDFs** - Visual verification of results

## Troubleshooting

**Role assignment fails:**
- Verify role names match exactly (case-sensitive)
- Check user exists in the system

**Tests timing out:**
- Increase timeout values in test files
- Check network connection

**Browser not closing:**
- Automatic now (no manual prompt)
- Press Ctrl+C if needed

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

