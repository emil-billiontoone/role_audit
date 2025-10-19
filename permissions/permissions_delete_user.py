"""
Test Module: Delete User Permission
=====================================
Checks if a user with the proper role can delete a user in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2

def test_delete_user(page, expected=True):
    """
    Checks if role can delete a user in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Delete User Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Delete User",
        "description": "Checks if role can create a user in Clarity LIMS",
        "execution_time": 0.0,
        "expected": expected,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    start_time = time.time()
    max_attempts = 1 if not expected else (RETRIES + 1)

    user_details = {
        "first_name": "Emil Create",
        "last_name": "User Test",
    }

    full_name = f"{user_details['first_name']} {user_details['last_name']}"

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\nAttempt {attempt}: Navigating to Configuration page...")
            page.goto(f"{BASE_URL}/clarity/configuration")
            page.wait_for_timeout(2000)

            # Click User Management
            print("Checking for User Management tab...")
            user_tab = page.locator("div.tab-title", has_text=re.compile("User Management", re.I))
            if user_tab.count() == 0:
                raise Exception("User Management tab not found — permission denied or hidden.")
            user_tab.first.click()
            page.wait_for_timeout(2000)

            print(f"Verifying that user '{full_name}' appears in the list...")
            page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
            search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
            if not search_result.is_visible():
                raise Exception(f"User '{full_name}' not found after creation.")
                
            print(f"Deleting user '{full_name}'...")
            search_result.click()
            page.wait_for_timeout(1000)

            print("Clicking 'Delete' button...")
            page.locator("button").filter(has_text="Delete").first.click()
            page.wait_for_timeout(500)

            print("Refreshing page to see if user is deleted...")
            page.reload()
            page.wait_for_timeout(2000)

            # Wait for the user list to finish loading
            page.wait_for_selector("div.g-col-value", state="visible", timeout=30000)

            if not search_result.is_visible():
                print(f"'{full_name}' is deleted — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
                
                # Take screenshot now that the list is fully rendered
                result["screenshot"], _ = capture_screenshot(page, "delete_user", "pass")

                page.goto(BASE_URL)
                page.wait_for_timeout(1000)
                break
            else:
                raise Exception(f"'{full_name}' is not deleted — permission denied.")

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"
            result["screenshot"], _ = capture_screenshot(page, "delete_user", "fail")

            if attempt < max_attempts:
                print("Retrying in 2 seconds...")
                page.goto(BASE_URL)
                page.wait_for_timeout(1000)
                time.sleep(2)
            else:
                print("Max retries reached. Failing test.")
                break

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result