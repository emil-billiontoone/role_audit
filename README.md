# Clarity LIMS Role Permission Testing System

## Overview
A comprehensive, modular testing framework for validating role-based permissions in Clarity LIMS. The system provides automated testing of 40+ different permissions across multiple user roles, with expected outcome validation and detailed reporting.

## Project Structure

```
role_audit/
├── run_role_tests.py              # Main CLI entry point
├── role_permission_tester.py      # Core test framework and runner
├── role_test_configs.py           # Role-specific test configurations
├── change_role.py                 # Role switching utility
├── store_creds.py                 # Secure credential storage
├── permissions/                   # Individual permission test modules (40+ tests)
│   ├── permissions_*.py           # Each file tests a specific permission
├── test_results/                  # Test execution results
│   └── all_role_tests.json        # Consolidated test results
└── screenshots/                   # Test failure screenshots

```

## Available Permission Tests

### Authentication & Access Tests
- `permissions_clarity_login` - Tests basic Clarity LIMS login
- `permissions_API_login` - Tests API authentication
- `permissions_collaborations_login` - Tests collaborations access
- `permissions_operations_login` - Tests operations module access

### Project Management
- `permissions_create_project` - Tests project creation capability
- `permissions_delete_project` - Tests project deletion rights
- `permissions_read_process` - Tests process viewing permissions
- `permissions_create_process` - Tests process creation
- `permissions_update_process` - Tests process modification

### Sample Management
- `permissions_create_sample` - Tests sample creation
- `permissions_delete_sample` - Tests sample deletion
- `permissions_update_sample` - Tests sample modification
- `permissions_sample_workflow_assignment` - Tests workflow assignment capability
- `permissions_sample_rework` - Tests sample rework permissions
- `permissions_review_escalated_samples` - Tests escalation review
- `permissions_requeue_sample` - Tests requeuing capability
- `permissions_remove_sample_from_workflow` - Tests workflow removal

### User Management
- `permissions_create_user` - Tests user creation
- `permissions_read_user` - Tests user viewing
- `permissions_update_user` - Tests user modification
- `permissions_delete_user` - Tests user deletion

### Role Management
- `permissions_create_role` - Tests role creation
- `permissions_update_role` - Tests role modification
- `permissions_delete_role` - Tests role deletion

### Contact Management
- `permissions_create_contact` - Tests contact creation
- `permissions_read_contact` - Tests contact viewing
- `permissions_update_contact` - Tests contact modification
- `permissions_delete_contact` - Tests contact deletion

### Control & Reagent Management
- `permissions_create_control` - Tests control creation
- `permissions_update_control` - Tests control modification
- `permissions_delete_control` - Tests control deletion
- `permissions_create_reagent_kit` - Tests reagent kit creation
- `permissions_update_reagent_kit` - Tests reagent kit modification
- `permissions_delete_reagent_kit` - Tests reagent kit deletion

### System Features
- `permissions_edit_completed_steps` - Tests editing completed workflow steps
- `permissions_move_to_next_step` - Tests workflow progression
- `permissions_overview_dashboard` - Tests dashboard access
- `permissions_update_configuration` - Tests configuration changes
- `permissions_esignature_signing` - Tests e-signature capability
- `permissions_search_index` - Tests search functionality
- `permissions_administer_lab_link` - Tests lab link administration

## Configuration

### Role Test Configurations
The system uses a dictionary-based configuration where each role maps to a set of tests with their expected outcomes:

```python
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator": {
        "permissions_clarity_login": True,           # Expected to pass
        "permissions_API_login": True,              # Expected to pass
        "permissions_create_project": False,        # Expected to fail (no permission)
        "permissions_delete_project": False,        # Expected to fail
        "permissions_sample_workflow_assignment": True,
        "permissions_edit_completed_steps": False,
        # ... more tests
    },
    "System Admin": {
        "permissions_clarity_login": True,
        "permissions_create_project": True,
        "permissions_delete_project": True,
        # ... more tests
    }
}
```

### Currently Configured Roles

#### Main Roles
- **Lab Operator** - Standard lab user with operational permissions
- **System Admin** - Full administrative access
- **Lab Admin** - Lab-specific administrative permissions
- **Limited** - Minimal access role
- **BTO API** - API-only access role
- **Not Logged In** - Tests for unauthenticated access

#### Add-On Roles
- **Sample Creation** - Additional sample management permissions
- **Editor** - Edit permissions for completed steps
- **Reagent Manufacturing** - Reagent-specific permissions
- **Review Escalations** - Escalation review capabilities
- **Rework** - Sample rework permissions
- **No Add-Ons** - Base role without additional permissions

## Usage

### Basic Command Line Usage

```bash
# Test a specific role
python run_role_tests.py "Lab Operator"

# Test on different servers
python run_role_tests.py "System Admin" --server dev
python run_role_tests.py "Lab Admin" --server test
python run_role_tests.py "Limited" -s prod

# Test add-on roles
python run_role_tests.py "Editor"
python run_role_tests.py "Sample Creation"

# Quick test (for development)
python run_role_tests.py quick

# Full test suite
python run_role_tests.py full

# Show available options
python run_role_tests.py --help
```

### Setting Up Credentials

Before running tests, store your credentials securely:

```bash
python store_creds.py
```

This will prompt for username and password and store them securely using the system keyring.

## Test Results

### Console Output
Tests provide real-time feedback during execution:

```
============================================================
ROLE PERMISSION TEST SUITE
Role: Lab Operator
Server: dev
Started: 2025-10-15 12:30:45
============================================================

Running test: Clarity Login
----------------------------------------
[Test execution details...]
✓ Test passed as expected

Running test: Create Project
----------------------------------------
[Test execution details...]
✓ Test failed as expected (permission denied)

============================================================
TEST SUMMARY
============================================================

Role: Lab Operator
Total Tests: 13
Passed (as expected): 13
Failed (unexpectedly): 0
Errors: 0

Test Results:
  [PASS] Clarity Login (11.2s) Expected:✓ Actual:✓
  [PASS] Api Login (0.4s) Expected:✓ Actual:✓
  [PASS] Create Project (41.7s) Expected:✗ Actual:✗
  [PASS] Delete Project (52.9s) Expected:✗ Actual:✗
  [PASS] Sample Workflow Assignment (9.7s) Expected:✓ Actual:✓
  [PASS] Edit Completed Steps (7.8s) Expected:✗ Actual:✗
  [PASS] Overview Dashboard (1.8s) Expected:✓ Actual:✓
  [PASS] Requeue Sample (5.1s) Expected:✓ Actual:✓
  [PASS] Sample Workflow Removal (53.5s) Expected:✓ Actual:✓
  [PASS] Permissions Read User (8.9s) Expected:✓ Actual:✓
  [PASS] Permissions Create User (8.1s) Expected:✓ Actual:✓
  [PASS] Permissions Update User (17.0s) Expected:✓ Actual:✓
  [PASS] Update Sample (8.9s) Expected:✓ Actual:✓

Overall Result: ALL TESTS PASSED AS EXPECTED

Results saved to: test_results/all_role_tests.json
```

### JSON Output Format

Results are saved to a consolidated JSON file (`test_results/all_role_tests.json`) that maintains history for all roles:

```json
{
  "server": "dev",
  "timestamp": "2025-10-15 00:04:11",
  "tests": {
    "Lab Operator": [
      {
        "test_name": "Clarity Login",
        "description": "Checks if user can login to Clarity LIMS",
        "execution_time": 11.2,
        "expected": true,
        "passed": true,
        "result": "pass"
      },
      {
        "test_name": "Create Project",
        "description": "Checks if user can create a new project in Clarity LIMS",
        "execution_time": 41.7,
        "expected": false,
        "passed": false,
        "result": "pass"
      }
    ],
    "System Admin": [
      {
        "test_name": "Create Project",
        "description": "Checks if user can create a new project in Clarity LIMS",
        "execution_time": 13.9,
        "expected": true,
        "passed": true,
        "result": "pass"
      }
    ]
  }
}
```

### Understanding Test Results

- **Expected**: What the test configuration says should happen (true = should pass, false = should fail)
- **Passed**: What actually happened during the test
- **Result**: 
  - `"pass"` - Test behaved as expected (whether passing or failing)
  - `"fail"` - Test did not behave as expected (unexpected pass or fail)
  - `"error"` - Test encountered an execution error

## Creating New Permission Tests

### Step 1: Create the Test Module

Create a new file in the `permissions/` directory:

```python
# permissions/permissions_your_feature.py
"""
Test Module: Your Feature Permission
=====================================
Checks if a user can perform your specific action in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import time

BASE_URL = "https://clarity-dev.btolims.com"
RETRIES = 2
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def test_permissions_your_feature(page):
    """
    Test your specific permission.
    Returns structured result dict.
    """
    print("\n===== TEST: Your Feature Permission =====")
    
    result = {
        "test_name": "Your Feature Permission",
        "description": "Checks if user can perform your action",
        "execution_time": 0.0,
        "expected": True,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }
    
    start_time = time.time()
    
    try:
        # Navigate to the relevant page
        page.goto(f"{BASE_URL}/clarity/your-page")
        page.wait_for_timeout(2000)
        
        # Check for permission-specific elements
        if page.locator("your-selector").count() > 0:
            result["passed"] = True
            result["result"] = "pass"
        else:
            raise Exception("Permission denied - element not found")
            
    except Exception as e:
        result["error"] = str(e)
        # Capture screenshot on failure
        timestamp = int(time.time())
        screenshot_file = f"screenshots/your_feature_{timestamp}.png"
        try:
            page.screenshot(path=screenshot_file)
            result["screenshot"] = screenshot_file
        except:
            pass
    
    result["execution_time"] = round(time.time() - start_time, 2)
    
    print(f"===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    return result
```

### Step 2: Add to Role Configuration

Edit `role_test_configs.py` to include your test:

```python
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator": {
        # ... existing tests ...
        "permissions_your_feature": False,  # Set expected outcome
    },
    "System Admin": {
        # ... existing tests ...
        "permissions_your_feature": True,   # Admins should have this permission
    }
}
```

### Step 3: Run the Test

```bash
python run_role_tests.py "Lab Operator"
```

## Test Module Standards

### Required Return Structure

Every test function must return a dictionary with these fields:

```python
{
    "test_name": str,        # Display name for the test
    "description": str,      # What the test validates
    "execution_time": float, # Test duration in seconds
    "expected": bool,        # Expected outcome (set by framework)
    "passed": bool,          # Actual test result
    "result": str,           # "pass", "fail", or "error"
    "error": str | None,     # Error message if applicable
    "screenshot": str | None # Path to failure screenshot
}
```

### Best Practices

1. **Consistent Naming**: Use `permissions_` prefix for all test modules
2. **Retry Logic**: Implement retries for transient failures
3. **Screenshots**: Capture screenshots on failure for debugging
4. **Clear Output**: Provide clear console output during execution
5. **Navigation Reset**: Return to main page after test completion
6. **Timeout Handling**: Use appropriate timeouts for UI elements

## Advanced Usage

### Programmatic Testing

```python
from role_permission_tester import RolePermissionTester

# Create custom test suite
tester = RolePermissionTester(server="dev", role_name="Custom Role")

# Define tests with expected outcomes
custom_tests = {
    "permissions_clarity_login": True,
    "permissions_create_project": False,
    "permissions_update_sample": True,
}

# Run the tests
tester.run_test_suite(custom_tests)
```

### Test Groups

You can define reusable test groups in `role_test_configs.py`:

```python
# Quick smoke test
QUICK_TEST = {
    "permissions_clarity_login": True,
}

# Full regression suite
FULL_TEST_SUITE = {
    "permissions_clarity_login": True,
    "permissions_create_project": True,
    "permissions_delete_project": True,
    # ... all available tests
}
```

## Architecture Benefits

1. **Modularity**: Each permission test is self-contained and independent
2. **Scalability**: Easy to add new permission tests without modifying core code
3. **Maintainability**: Clear separation between test logic and configuration
4. **Flexibility**: Tests can be mixed and matched for different roles
5. **Validation**: Expected outcomes ensure tests behave correctly
6. **Traceability**: Comprehensive logging and result storage
7. **Debugging**: Automatic screenshots on failure

## Troubleshooting

### Common Issues

#### Tests Timing Out
- Increase timeout values in wait_for_selector calls
- Add explicit waits with page.wait_for_timeout()
- Check network conditions

#### Authentication Failures
- Run `python store_creds.py` to update credentials
- Verify server URL is correct
- Check if account is locked

#### Permission Tests Passing Unexpectedly
- Verify the expected outcome in role_test_configs.py
- Check if role permissions have changed in Clarity
- Review test implementation for edge cases

#### Screenshots Not Capturing
- Ensure screenshots/ directory exists
- Check disk space
- Verify write permissions

### Debug Mode

For detailed debugging, modify the browser launch options:

```python
# In role_permission_tester.py
browser = playwright.chromium.launch(
    headless=False,  # Show browser window
    slow_mo=500,     # Slow down operations
    devtools=True    # Open developer tools
)
```

## Recent Updates (October 2025)

- **40+ Permission Tests**: Comprehensive coverage of Clarity LIMS permissions
- **Expected Outcome Validation**: Tests now validate against expected results
- **Consolidated Results**: All test results stored in single JSON file
- **Main/Add-On Role Separation**: Clear distinction between primary and supplementary roles
- **Enhanced Error Handling**: Better retry logic and screenshot capture
- **Improved Test Discovery**: Automatic function detection with naming conventions

## Future Enhancements

- [ ] Parallel test execution for faster runs
- [ ] HTML report generation
- [ ] Test scheduling and automation
- [ ] Permission change detection and alerts
- [ ] Test coverage metrics
- [ ] Integration with CI/CD pipelines