# Role Testing Loop - Quick Guide

## Overview

The `run_all_roles.py` script automates comprehensive role testing by looping through all roles in `MAIN_ROLE_TEST_SUITES`, testing each one while safely managing role assignments.

## Key Features

✅ **Safe Role Transitions**: Always adds the new role before removing the old one (user never has zero roles)  
✅ **Automatic Testing**: Runs all configured tests for each role  
✅ **Progress Tracking**: Shows which role is being tested (e.g., "Role 2/5")  
✅ **Interactive Control**: Prompts before moving to next role (can exit anytime)  
✅ **Comprehensive Logging**: All results saved to consolidated JSON file  

## Basic Usage

```bash
# Test all roles for a user
python run_all_roles.py "Emil" "Test"

# Test on specific server
python run_all_roles.py "Emil" "Test" --server dev

# With specific credentials account
python run_all_roles.py "Emil" "Test" --server staging --account MASTER
```

## How It Works

### Process Flow

```
Start
  ↓
Test "Not Logged In" (if configured)
  ↓
For each remaining role:
  ├─ [1/3] Add new role → User now has both old and new roles
  ├─ [2/3] Remove old role → User now has only new role
  └─ [3/3] Run all permission tests for new role
  ↓
Prompt: Continue to next role? [Y/n]
  ↓
Next role (repeat) or End
```

### Example Execution

```
================================================================================
COMPREHENSIVE ROLE TESTING SUITE
================================================================================
User: Emil Test
Server: dev
Total roles to test: 5
================================================================================

Connected to dev - API version: 1

================================================================================
TESTING ROLE 1/5: Lab Operator (BTO)
================================================================================

[1/3] Adding role: Lab Operator (BTO)
Added role 'Lab Operator (BTO)' to emiltest

[2/3] No previous role to remove (first role in sequence)

[3/3] Running permission tests for: Lab Operator (BTO)
============================================================
ROLE PERMISSION TEST SUITE
Role: Lab Operator (BTO)
Server: dev
Started: 2025-10-22 14:30:45
============================================================

Running test: Clarity Login
----------------------------------------
✓ Test passed as expected

Running test: Api Login
----------------------------------------
✓ Test passed as expected

[... more tests ...]

============================================================
TEST SUMMARY
============================================================
Total Tests: 3
Passed (as expected): 3
Failed (unexpectedly): 0

Completed testing role 1/5: Lab Operator (BTO)

Continue to next role (System Admin (BTO))? [Y/n]: y

================================================================================
TESTING ROLE 2/5: System Admin (BTO)
================================================================================

[1/3] Adding role: System Admin (BTO)
Added role 'System Admin (BTO)' to emiltest

[2/3] Removing previous role: Lab Operator (BTO)
Removed role 'Lab Operator (BTO)' from emiltest

[3/3] Running permission tests for: System Admin (BTO)
[... tests run ...]

Continue to next role (Lab Admin (BTO))? [Y/n]: n

Stopping role testing loop as requested.

================================================================================
COMPREHENSIVE ROLE TESTING COMPLETE
================================================================================
Total roles tested: 2
Final role assigned: System Admin (BTO)
================================================================================
```

## Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `firstname` | Yes | User's first name | `"Emil"` |
| `lastname` | Yes | User's last name | `"Test"` |
| `-s, --server` | No | Server environment (default: dev) | `--server dev` |
| `-a, --account` | No | Credentials account (default: MASTER) | `--account MASTER` |

## Roles Tested

The script tests all roles configured in `MAIN_ROLE_TEST_SUITES` in `role_test_configs.py`:

1. **Not Logged In** - Tested first (if configured)
2. **Lab Operator (BTO)** - Standard lab operations
3. **System Admin (BTO)** - Full system access
4. **Lab Admin (BTO)** - Lab management
5. **Limited (BTO)** - Minimal permissions
6. **BTO API** - API-only access

## Safety Features

### Role Assignment Safety

- ✅ Always adds new role BEFORE removing old role
- ✅ User never has zero roles (maintains system access)
- ✅ Graceful error handling if role assignment fails

### Interactive Control

- ⏸️ Pauses between each role for review
- 🛑 Can stop testing at any point (press `n`)
- 📊 Shows progress (e.g., "Role 2/5")

### Error Handling

```python
try:
    modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
except Exception as e:
    print(f"Error adding role: {e}")
    print("Skipping this role...")
    continue  # Move to next role
```

## Configuration

### Customize Roles to Test

Edit `role_test_configs.py`:

```python
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator (BTO)": {
        "permissions_clarity_login": True,
        "permissions_API_login": True,
        # ... more tests
    },
    "System Admin (BTO)": {
        "permissions_clarity_login": True,
        "permissions_create_project": True,
        # ... more tests
    },
    # Add or remove roles here
}
```

### Customize Tests for Each Role

Each role maps to a dictionary of tests with expected outcomes:

```python
"Role Name": {
    "test_module_name": expected_result,  # True = should pass, False = should fail
}
```

## Results

### Console Output

Real-time progress showing:
- Which role is being tested
- Test execution status
- Pass/fail summary
- Time taken per test

### JSON Output

All results saved to `test_results/all_role_tests.json`:

```json
{
  "server": "dev",
  "timestamp": "2025-10-22 14:45:30",
  "tests": {
    "Lab Operator (BTO)": [ /* test results */ ],
    "System Admin (BTO)": [ /* test results */ ],
    "Lab Admin (BTO)": [ /* test results */ ]
  }
}
```

### Screenshots

Automatic screenshots saved to `screenshots/` directory for all tests.

## Stopping the Loop

You have three ways to stop:

1. **Press `n` at the prompt**: Safely stops after current role
2. **Press `Ctrl+C`**: Emergency stop (not recommended during role changes)
3. **Let it complete**: Runs all roles automatically

## Best Practices

1. **Start with "Not Logged In"**: This role is tested first automatically
2. **Review Results**: Check test summary before moving to next role
3. **Monitor Role Changes**: Watch console output to confirm roles are added/removed correctly
4. **Save Credentials First**: Run `python store_creds.py` before starting
5. **Test on Dev First**: Always test on dev environment before staging/prod

## Troubleshooting

### Role Assignment Fails

```
Error adding role System Admin (BTO): Role not found
Skipping this role...
```

**Solution**: Verify role name exactly matches Clarity LIMS role name (case-sensitive)

### User Not Found

```
Error: list index out of range
```

**Solution**: Verify firstname and lastname are correct and user exists in the system

### Connection Issues

```
Error: Could not connect to server
```

**Solution**: 
- Check server parameter (`dev`, `staging`, `prod`)
- Verify credentials with `python store_creds.py`
- Confirm VPN/network access

### Tests Failing Unexpectedly

**Solution**:
- Review role configuration in `role_test_configs.py`
- Check if role permissions changed in Clarity LIMS
- Verify expected outcomes are correct

## Advanced Usage

### Skip Specific Roles

Edit `role_test_configs.py` to comment out roles you don't want to test:

```python
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator (BTO)": { /* ... */ },
    # "System Admin (BTO)": { /* ... */ },  # Commented out - won't be tested
    "Lab Admin (BTO)": { /* ... */ },
}
```

### Test Subset of Permissions

For each role, enable only the permissions you want to test:

```python
"Lab Operator (BTO)": {
    "permissions_clarity_login": True,
    "permissions_API_login": True,
    # Comment out tests you don't want to run
    # "permissions_create_project": False,
}
```

## Integration with change_role.py

The loop script imports and uses functions from `change_role.py`:

```python
from change_role import get_lims_connection, modify_user_role

# Connect to LIMS
lims, username = get_lims_connection(account="MASTER", server="dev")

# Add a role
modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")

# Remove a role
modify_user_role(lims, "Emil", "Test", "Lab Operator (BTO)", action="remove")
```

This ensures consistent role management across all scripts.

## Summary

The `run_all_roles.py` script provides:

✅ Automated comprehensive role testing  
✅ Safe role transition management  
✅ Interactive control and monitoring  
✅ Detailed results and logging  
✅ Integration with existing test framework  

**Quick Start:**
```bash
python run_all_roles.py "Emil" "Test" --server dev
```

That's it! The script handles the rest automatically.

