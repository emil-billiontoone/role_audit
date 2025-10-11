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
        self.results = {
            "role": role_name,
            "server": server,
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
    
    
    def run_test(self, page, test_function, test_name=None):
        """
        Run a specific test function.
        
        Args:
            page: Playwright page object
            test_function: Function that takes a page and returns test results
            test_name: Optional name for the test
        
        Returns:
            dict: Test results
        """
        test_name = test_name or test_function.__name__
        print(f"\nRunning test: {test_name}")
        print("-" * 40)
        
        start_time = time.time()
        try:
            result = test_function(page)
            result["execution_time"] = time.time() - start_time
            result["error"] = None
        except Exception as e:
            result = {
                "test_name": test_name,
                "passed": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }
            print(f"ERROR in test: {e}")
        
        self.results["tests"].append(result)
        return result
    
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
        print(f"Started: {self.results['timestamp']}")
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
                            result = self.run_test(page, test_funcs[0])
                    elif isinstance(test_spec, tuple):
                        module_name, func_name = test_spec
                        module = importlib.import_module(f"permissions.{module_name}")
                        test_func = getattr(module, func_name)
                        result = self.run_test(page, test_func)
                    else:
                        # Direct function reference
                        result = self.run_test(page, test_spec)
                    
                    # Compare test result with expected
                    actual_passed = result.get("passed", False)
                    result["passed"] = actual_passed == expected  # True if matches expectation
                    result["expected"] = expected
                
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
        
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for t in self.results["tests"] if t.get("passed", False))
        failed_tests = total_tests - passed_tests
        
        print(f"\nRole: {self.role_name}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        
        print("\nTest Results:")
        for test in self.results["tests"]:
            status = "PASS" if test.get("passed", False) else "FAIL"
            name = test.get("test_name", "Unknown")
            time_taken = test.get("execution_time", 0)
            print(f"  [{status}] {name} ({time_taken:.1f}s)")
            if test.get("error"):
                print(f"        Error: {test['error']}")
        
        overall = "PASSED" if failed_tests == 0 else "FAILED"
        print(f"\nOverall Result: {overall}")
    
    def save_results(self, filename=None):
        """Save results to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"text/role_test_{self.role_name.lower().replace(' ', '_')}_{timestamp}.json"
        
        try:
            with open(filename, "w") as f:
                json.dump(self.results, f, indent=2)
            print(f"\nResults saved to: {filename}")
        except Exception as e:
            print(f"\nFailed to save results: {e}")


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
