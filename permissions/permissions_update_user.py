"""
Test Module: Update User Permission
=====================================
Checks if a user with the proper role can update a user in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2

def test_update_user(page, expected=True):
    """
    Checks if role can update a user in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Update User Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Update User",
        "description": "Checks if role can update a user in Clarity LIMS",
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
        "phone": "1234567890",
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

            # Fill Phone
            print("Filling Phone...")
            page.get_by_role("textbox", name="Phone").type(user_details["phone"], delay=100)
            page.wait_for_timeout(500)

            # Save User
            print("Clicking 'Save'...")
            page.locator("button").filter(has_text="Save").click()
            page.wait_for_timeout(2000)

            # Verify user exists
            print("Refreshing page to see if user is updated...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying that user '{full_name}' appears in the list...")
            page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
            search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
            if not search_result.is_visible():
                raise Exception(f"User '{full_name}' not found after update.")

            print(f"Verifying phone is '{user_details['phone']}'...")
            search_result.click()
            page.wait_for_timeout(1000)
            phone_text = page.get_by_role("textbox", name="Phone").input_value()
            if phone_text.strip() == user_details["phone"]:
                print("Phone is updated — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception(f"Phone is '{phone_text}' — permission denied.")

            result["screenshot"], _ = capture_screenshot(page, "update_user", "pass")

            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"
            result["screenshot"], _ = capture_screenshot(page, "update_user", "fail")

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
