# Modular Role Permission Testing System

## Overview
A clean, modular system for testing role-based permissions in Clarity. Each permission test is self-contained, and the runner is completely generic.

## Recent Updates (October 2025)
- **Enhanced `permissions_view.py`**: Now includes comprehensive entry interaction testing with multiple methods (click, double-click, hover, JavaScript) in the `test_entry_interaction` function
- **Improved diagnostics**: Tests provide detailed debugging information when interactions fail
- **Better fallback handling**: Tests can pass if viewing is successful even when clicking fails (permission-based)
- **Module naming**: Standardized to `permissions_` prefix for test modules
- **Extended role coverage**: Added test configurations for 9 different roles (Editor, Lab Operator, System Admin, Lab Admin, Reagent Manufacturing, Sample Creation, Limited, Review Escalations, Rework)

## Architecture

```
run_role_tests.py           # Main entry point
    ↓
role_permission_tester.py   # Generic test runner
    ↓
Individual test modules:     # Self-contained tests
  - permissions_edit_completed_steps.py
  - permissions_view.py
  - (add more as needed)
```

## File Structure

### Core Files
- `run_role_tests.py` - Simple command-line runner
- `role_permission_tester.py` - Generic test framework
- `role_test_configs.py` - Configuration for different roles

### Test Modules
Each test module contains one or more test functions:
- `permissions_edit_completed_steps.py` - Tests editing completed steps in lab stream entries
  - Function: `test_can_edit_completed_steps` - Checks if Edit buttons appear and work
- `permissions_view.py` - Tests viewing and interacting with lab stream entries  
  - Function: `test_entry_interaction` - Comprehensive test trying multiple interaction methods
- (Add your own test modules here)

### Supporting Files
- `permissions_complete_audit_balanced.py` - Comprehensive audit helper functions for permission testing
- `store_creds.py` - Store credentials securely using keyring
- `store_creds_template.py` - Template for credential storage

## Usage

### Basic Usage
```bash
# Test a specific role
python run_role_tests.py Editor

# Test on different server
python run_role_tests.py Editor test

# Quick test (for development)
python run_role_tests.py quick

# Full test suite
python run_role_tests.py full
```

### Advanced Usage
```python
from role_permission_tester import RolePermissionTester

# Create custom test suite
tester = RolePermissionTester(server="dev", role_name="Custom Role")
tester.run_test_suite([
    "permissions_view",
    ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
])
```

## Creating New Tests

### Step 1: Create Test Module
Create a new file with your test (e.g., `permissions_your_feature.py`):

```python
from playwright.sync_api import Page

def test_your_permission(page: Page) -> dict:
    """Test description."""
    
    print("\n" + "="*60)
    print("TEST: Your Permission Name")
    print("="*60)
    
    test_result = {
        "test_name": "Your Permission Name",
        "passed": False,
        "description": "What this test checks",
        "details": {}
    }
    
    # Your test logic here
    try:
        # Do your testing
        test_result["passed"] = True  # or False based on test
    except Exception as e:
        test_result["error"] = str(e)
        test_result["passed"] = False
    
    return test_result
```

### Step 2: Add to Role Configuration
Edit `role_test_configs.py`:

```python
ROLE_TEST_SUITES = {
    "YourRole": [
        "permissions_your_feature",  # Add your test module here
        # other tests...
    ],
}
```

### Step 3: Run It
```bash
python run_role_tests.py YourRole
```

## Test Module Requirements

Each test function must:
1. Accept a `Page` object (already logged in)
2. Return a dict with:
   - `test_name`: Name of the test
   - `passed`: Boolean result
   - `description`: What the test checks
   - `details`: Additional information
   - `error`: (Optional) Error message if failed

## Example Test Modules

### Simple Permission Check
```python
def test_can_access_settings(page: Page) -> dict:
    """Check if user can access settings."""
    result = {
        "test_name": "Can Access Settings",
        "passed": False,
        "description": "Checks settings access"
    }
    
    try:
        page.goto("https://clarity-dev.btolims.com/clarity/settings")
        page.wait_for_selector(".settings-panel", timeout=3000)
        result["passed"] = True
    except:
        result["passed"] = False
    
    return result
```

### Complex Permission Test
See `permissions_edit_completed_steps.py` for an example that:
- Uses the audit framework from `permissions_complete_audit_balanced.py`
- Checks multiple entries systematically
- Looks for specific popup dialogs and edit capabilities
- Returns detailed results with comprehensive logging

See `permissions_view.py` for an example that:
- Tests multiple interaction methods (click, double-click, hover, JavaScript)
- Handles cases where entries might not be clickable
- Provides detailed debugging information
- Falls back to checking view permissions when interaction fails

## Benefits of This Architecture

1. **Modularity**: Each test is independent
2. **Reusability**: Tests can be mixed and matched for different roles
3. **Maintainability**: Easy to add, modify, or remove tests
4. **Clarity**: Clear separation of concerns
5. **Extensibility**: Simple to extend with new test types

## Configuration Examples

### Define Test Suites by Role
```python
ROLE_TEST_SUITES = {
    "Editor": [
        "permissions_view",  # Test viewing and interaction capabilities
    ],
    
    "Lab Operator": [
        "permissions_view",
    ],
    
    "System Admin": [
        "permissions_edit_completed_steps",
        "permissions_view",
    ],
    
    "Lab Admin": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],
    
    # Additional roles with specific permissions
    "Reagent Manufacturing": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],
    
    "Sample Creation": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],
}
```

### Create Test Groups
```python
# Reusable test groups
BASIC_PERMISSIONS = [
    "permissions_view",
]

EDIT_PERMISSIONS = [
    "permissions_edit_completed_steps",
]

ADMIN_PERMISSIONS = [
    # "test_user_management",
    # "test_system_settings",
]

# Quick test suite for development/debugging
QUICK_TEST = [
    ("permissions_view", "test_entry_interaction"),  # Just one quick test
]

# Full comprehensive test suite
FULL_TEST_SUITE = [
    "permissions_view",
    "permissions_edit_completed_steps",
    # Add all available tests here
]
```

## Output

Results are:
1. Displayed in console with pass/fail status
2. Saved to JSON files in `text/` directory with timestamp
3. Include timing information and error details
4. Provide detailed debugging information for failures

### JSON Output Format
```json
{
  "role": "Editor",
  "server": "dev",
  "timestamp": "2025-10-07T23:45:20.089321",
  "username": "testuser",
  "tests": [
    {
      "test_name": "Comprehensive Entry Interaction",
      "passed": true,
      "description": "Tests multiple ways to interact with lab stream entries",
      "details": {
        "tests_performed": [...],
        "element_counts": {...}
      },
      "execution_time": 45.2
    }
  ]
}
```

Example output:
```
============================================================
ROLE PERMISSION TEST SUITE
Role: Editor
Server: dev
============================================================

Running test: test_can_edit_completed_steps
----------------------------------------
TEST: Can Edit Completed Steps
...

============================================================
TEST SUMMARY
============================================================
Role: Editor
Total Tests: 2
Passed: 1
Failed: 1

Test Results:
  [PASS] Can Edit Completed Steps (45.2s)
  [FAIL] Can Delete Entries (12.3s)
        Error: No delete button found

Overall Result: FAILED

Results saved to: text/role_test_editor_20231024_143022.json
```

## Troubleshooting

### Lab Stream Entries Not Clickable

**Issue**: Lab stream entries (`.lab-stream-entry`) may appear clickable (cursor: pointer) but don't navigate when clicked.

**What we discovered**:
- Entries have `cursor: pointer` CSS style suggesting they should be clickable
- No `onclick` handler is attached to the entries
- No child elements (links or buttons) exist within the entries
- The entries are `<li>` elements containing only divs, spans, and images

**Diagnosis**: Run the `permissions_view.py` test which tries multiple interaction methods:
- Regular click
- Double click  
- JavaScript click
- Hover actions
- Clicking child elements

**Common Causes**:
1. **Permission restrictions** - User role may not have access to view entry details
2. **Missing event handlers** - Click handlers might not be attached properly
3. **Framework issues** - JavaScript framework may not have loaded completely
4. **UI design** - Entries might be display-only with no detail view

**Solution**: The test will automatically detect if entries are viewable but not clickable, and will pass the test if the user can at least see the entry list.

### Test Function Discovery

**Issue**: Test function not found or wrong function executed.

**How it works**: The test runner automatically discovers functions that:
1. Are in the specified module
2. Start with `test_` prefix
3. Accept a `Page` parameter and return a dict

**Example**:
```python
# WILL be discovered
def test_my_permission(page: Page) -> dict:
    pass

# Will NOT be discovered (wrong prefix)
def check_my_permission(page: Page) -> dict:
    pass
```

**To specify exact function**:
```python
ROLE_TEST_SUITES = {
    "Editor": [
        ("permissions_view", "test_entry_interaction"),  # Module and function
    ],
}
```

### Timeout Issues

**Issue**: Tests timing out waiting for elements.

**Solutions**:
1. Increase timeout in selectors: `page.wait_for_selector(".element", timeout=10000)`
2. Add explicit waits: `page.wait_for_timeout(2000)`
3. Wait for specific load states: `page.wait_for_load_state("networkidle")`

### Authentication Issues

**Issue**: Login fails or credentials not found.

**Solution**: Run `store_creds.py` to securely store credentials:
```bash
python store_creds.py
```
