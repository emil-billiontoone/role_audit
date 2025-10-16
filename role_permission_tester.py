"""
Generic Role Permission Tester
===============================
A modular system for testing various permissions for different roles.
"""

from playwright.sync_api import sync_playwright
import keyring
import json
import time
from datetime import datetime
import importlib
import sys
import os
import os

# Configuration
SERVICE_NAME = "user_tester_app"

class RolePermissionTester:
    """Generic tester for role permissions."""
    
    def __init__(self, server="dev", role_name="Unknown Role"):
        """
        Initialize the tester.
        
        Args:
            server: Server environment (dev, test, prod)
            role_name: Name of the role being tested
        """
        self.server = server
        self.role_name = role_name
        self.base_url = f"https://clarity-{server}.btolims.com"
        self.results_file = "test_results/all_role_tests.json"
        self.current_test_results = []
        self.screenshot_dir = "screenshots"
        # Ensure screenshot directory exists
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    
    def run_test(self, page, test_function, test_name=None, expected=True):
        """
        Run a specific test function.
        
        Args:
            page: Playwright page object
            test_function: Function that takes a page and returns test results
            test_name: Optional name for the test
            expected: Expected outcome (True/False)
        
        Returns:
            dict: Test results
        """
        # Format test name from function name
        raw_test_name = test_name or test_function.__name__
        # Convert from snake_case to Title Case
        formatted_name = raw_test_name.replace("test_", "").replace("_", " ").title()
        # Special replacements for common terms
        formatted_name = formatted_name.replace("Clarity Login", "Clarity Login")
        formatted_name = formatted_name.replace("Can ", "")
        
        print(f"\nRunning test: {formatted_name}")
        print("-" * 40)
        
        # Try to get test description from function docstring
        description = test_function.__doc__.strip() if test_function.__doc__ else "No description available"
        if description:
            # Take only the first line of the docstring
            description = description.split('\n')[0].strip()
        
        start_time = time.time()
        try:
            # Try to pass expected parameter to test function
            # Tests can use this to skip retries when expected=False
            import inspect
            sig = inspect.signature(test_function)
            if 'expected' in sig.parameters:
                result = test_function(page, expected=expected)
            else:
                result = test_function(page)
            execution_time = round(time.time() - start_time, 1)
            passed = result.get("passed", False)
            
            # Determine if test result matches expectation
            result_status = "pass" if passed == expected else "fail"
            
            test_result = {
                "test_name": formatted_name,
                "description": description,
                "execution_time": execution_time,
                "expected": expected,
                "passed": passed,
                "result": result_status,
                "error": result.get("error", None),
                "screenshot": result.get("screenshot", None)
            }
            
        except Exception as e:
            execution_time = round(time.time() - start_time, 1)
            test_result = {
                "test_name": formatted_name,
                "description": description,
                "execution_time": execution_time,
                "expected": expected,
                "passed": False,
                "result": "error",
                "error": str(e),
                "screenshot": None
            }
            print(f"ERROR in test: {e}")
        
        # Always capture a screenshot if not already present
        if test_result.get("screenshot") is None:
            test_result["screenshot"] = self._capture_screenshot(page, formatted_name.lower().replace(" ", "_"))
        
        self.current_test_results.append(test_result)
        return test_result
    
    def run_test_suite(self, test_modules_with_expected):
        """
        Run a suite of tests with expected outcomes.
        
        Args:
            test_modules_with_expected: Dict mapping test module/function to expected outcome.
                                        Key can be module string or (module, function) tuple.
                                        Value is expected result (True/False)
        """
        print("=" * 60)
        print(f"ROLE PERMISSION TEST SUITE")
        print(f"Role: {self.role_name}")
        print(f"Server: {self.server}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False, slow_mo=200)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                for i, (test_spec, expected) in enumerate(test_modules_with_expected.items()):
                    # Navigate back to main page before each test (except the first)
                    if i > 0:
                        print("\nNavigating back to main page...")
                        page.goto(f"{self.base_url}/clarity")
                        page.wait_for_load_state("networkidle")
                        page.wait_for_timeout(2000)
                    
                    # Determine the test function
                    if isinstance(test_spec, str):
                        module = importlib.import_module(f"permissions.{test_spec}")
                        test_funcs = [
                            getattr(module, name) for name in dir(module)
                            if name.startswith("test_") and callable(getattr(module, name))
                        ]
                        if test_funcs:
                            result = self.run_test(page, test_funcs[0], expected=expected)
                    elif isinstance(test_spec, tuple):
                        module_name, func_name = test_spec
                        module = importlib.import_module(f"permissions.{module_name}")
                        test_func = getattr(module, func_name)
                        result = self.run_test(page, test_func, expected=expected)
                    else:
                        # Direct function reference
                        result = self.run_test(page, test_spec, expected=expected)
                
                # Print summary and save
                self.print_summary()
                self.save_results()
            
            except Exception as e:
                print(f"\nCRITICAL ERROR: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                input("\nPress Enter to close browser...")
                browser.close()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.current_test_results)
        passed_tests = sum(1 for t in self.current_test_results if t.get("result") == "pass")
        failed_tests = sum(1 for t in self.current_test_results if t.get("result") == "fail")
        
        print(f"\nRole: {self.role_name}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed (as expected): {passed_tests}")
        print(f"Failed (as expected): {failed_tests}")

        print("\nTest Results:")
        for test in self.current_test_results:
            result_status = test.get("result", "unknown").upper()
            name = test.get("test_name", "Unknown")
            time_taken = test.get("execution_time", 0)
            expected = "✓" if test.get("expected") else "✗"
            passed = "✓" if test.get("passed") else "✗"
            print(f"  [{result_status}] {name} ({time_taken:.1f}s) Expected:{expected} Actual:{passed}")
            if test.get("error"):
                print(f"        Error: {test['error']}")
        
        overall = "ALL TESTS PASSED" if failed_tests == 0 and (passed_tests + failed_tests == total_tests) else "SOME TESTS FAILED"
        print(f"\nOverall Result: {overall}")
    
    def save_results(self, filename=None):
        """Save/append results to JSON file."""
        if not filename:
            filename = self.results_file
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Load existing data or create new structure
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                data = self._create_new_data_structure()
        else:
            data = self._create_new_data_structure()
        
        # Update server and timestamp
        data["server"] = self.server
        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add or update tests for this role
        if "tests" not in data:
            data["tests"] = {}
        
        # Store results under the role name
        data["tests"][self.role_name] = self.current_test_results
        
        # Save updated data
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"\nResults saved to: {filename}")
        except Exception as e:
            print(f"\nFailed to save results: {e}")
    
    def _capture_screenshot(self, page, test_name):
        """Capture a screenshot for the test."""
        try:
            timestamp = int(time.time())
            screenshot_file = os.path.join(self.screenshot_dir, f"{test_name}_{timestamp}.png")
            page.screenshot(path=screenshot_file)
            print(f"  Screenshot saved: {screenshot_file}")
            return screenshot_file
        except Exception as e:
            print(f"  Failed to capture screenshot: {e}")
            return None
    
    def _create_new_data_structure(self):
        """Create a new data structure for the JSON file."""
        return {
            "server": self.server,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tests": {}
        }


# Example usage functions
def test_editor_role():
    """Test Editor role permissions."""
    tester = RolePermissionTester(server="dev", role_name="Editor")
    
    # List of test modules to run
    test_modules = [
        "test_edit_completed_steps",  # Can edit completed steps
        # Add more test modules here as needed
        # "test_delete_permission",
        # "test_create_permission", 
    ]
    
    tester.run_test_suite(test_modules)


def test_custom_role(role_name, test_list):
    """Test a custom role with specific tests."""
    tester = RolePermissionTester(server="dev", role_name=role_name)
    tester.run_test_suite(test_list)


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        role = sys.argv[1]
        if role.lower() == "editor":
            test_editor_role()
        else:
            print(f"Testing role: {role}")
            # Default test suite for unknown roles
            test_custom_role(role, ["test_edit_completed_steps"])
    else:
        # Default: test editor role
        test_editor_role()
