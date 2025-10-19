"""
Test Module: Create User Permission
=====================================
Checks if a user with the proper role can create a user in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2

def test_create_user(page, expected=True):
    """
    Checks if role can create a user in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Create User Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Create User",
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
        "title": "Test",
        "account": "Administrative Lab",
        "email": "edeguzman@billiontoone.com",
        "username": "EmilCreateUserTest",
        "role": "Lab Operator (BTO)"
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

            # Click NEW USER
            print("Clicking 'NEW USER' button...")
            page.locator("button").filter(has_text=re.compile("NEW USER", re.I)).click()
            page.wait_for_timeout(1000)

            # Fill first & last name
            print("Filling first and last name...")
            page.get_by_role("textbox", name=re.compile("Enter First Name", re.I)).type(user_details["first_name"], delay=100)
            page.get_by_role("textbox", name=re.compile("Enter Last Name", re.I)).type(user_details["last_name"], delay=100)
            page.wait_for_timeout(500)

            # Fill Title
            print("Filling Title...")
            page.get_by_role("textbox", name="Title").type(user_details["title"], delay=100)
            page.wait_for_timeout(500)

            # Select Account
            print(f"Selecting account '{user_details['account']}'...")
            page.locator("#account-drp").click()
            page.wait_for_selector("ul.rw-list >> li", state="visible")
            page.locator(f"ul.rw-list >> text={user_details['account']}").click()

            # Fill Email
            print(f"Filling email '{user_details['email']}'...")
            page.get_by_role("textbox", name="Email").type(user_details["email"], delay=100)
            page.wait_for_timeout(500)

            # Fill Username
            print(f"Filling username '{user_details['username']}'...")
            page.get_by_role("textbox", name="Username").type(user_details["username"], delay=100)
            page.wait_for_timeout(500)

            # Select Role
            print(f"Selecting role '{user_details['role']}'...")
            page.locator(".rw-multiselect-wrapper").click()
            page.get_by_role("option", name=user_details["role"]).click()
            page.wait_for_timeout(1000)
            print(f"Role '{user_details['role']}' selected successfully.")

            # Save User
            print("Clicking 'Save'...")
            page.locator("button").filter(has_text="Save").click()
            page.wait_for_timeout(2000)

            # Verify user exists
            print("Refreshing page to see if user is created...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying that user '{full_name}' appears in the list...")
            page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
            search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
            if not search_result.is_visible():
                raise Exception(f"User '{full_name}' not found after creation.")

            print(f"User '{full_name}' successfully created.")
            result["passed"] = True
            result["result"] = "pass"
            result["screenshot"], _ = capture_screenshot(page, "create_user", "pass")

            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"
            result["screenshot"], _ = capture_screenshot(page, "create_user", "fail")

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
