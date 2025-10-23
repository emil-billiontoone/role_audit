"""
Test Module: Create User Permission
=====================================
Checks if a user with the proper role can create a user in Clarity LIMS.
Compatible with RolePermissionTester framework.

Test Flow:
1. Test attempts to create a user with the current role
2. If creation succeeds, test passes
3. If creation fails, test fails
4. Cleanup: Add System Admin (BTO) role and delete the created user (if it exists)
"""

import re
import time
from .test_utils import capture_screenshot
from change_role import modify_user_role, get_lims_connection

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
    user_created = False

    try:
        # Test: Attempt to create user with current role
        print(f"\n--- TEST: Attempting to create user '{full_name}' with current role ---")
        
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
                new_user_button = page.locator("button").filter(has_text=re.compile("NEW USER", re.I))
                if new_user_button.count() == 0 or not new_user_button.is_visible():
                    raise Exception("NEW USER button not visible — permission denied.")
                
                new_user_button.click()
                page.wait_for_timeout(1000)

                # Fill first & last name
                print("Filling first and last name...")
                page.get_by_role("textbox", name=re.compile("Enter First Name", re.I)).type(user_details["first_name"], delay=10)
                page.get_by_role("textbox", name=re.compile("Enter Last Name", re.I)).type(user_details["last_name"], delay=10)
                page.wait_for_timeout(500)

                # Fill Title
                print("Filling Title...")
                page.get_by_role("textbox", name="Title").type(user_details["title"], delay=10)
                page.wait_for_timeout(500)

                # Select Account
                print(f"Selecting account '{user_details['account']}'...")
                page.locator("#account-drp").click()
                page.wait_for_selector("ul.rw-list >> li", state="visible")
                page.locator(f"ul.rw-list >> text={user_details['account']}").click()

                # Fill Email
                print(f"Filling email '{user_details['email']}'...")
                page.get_by_role("textbox", name="Email").type(user_details["email"], delay=10)
                page.wait_for_timeout(500)

                # Fill Username
                print(f"Filling username '{user_details['username']}'...")
                page.get_by_role("textbox", name="Username").type(user_details["username"], delay=10)
                page.wait_for_timeout(500)

                # Select Role
                print(f"Selecting role '{user_details['role']}'...")
                page.locator(".rw-multiselect-wrapper").click()
                page.get_by_role("option", name=user_details["role"]).click()
                page.wait_for_timeout(1000)

                # Save User
                print("Clicking 'Save'...")
                save_button = page.locator("button").filter(has_text="Save")
                if save_button.count() == 0 or not save_button.is_visible():
                    raise Exception("Save button not visible — permission denied.")
                
                save_button.click()
                page.wait_for_timeout(2000)

                # Verify user was created
                print("Refreshing page to verify user creation...")
                page.reload()
                page.wait_for_timeout(2000)

                print(f"Verifying that user '{full_name}' appears in the list...")
                page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
                search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
                
                if search_result.is_visible():
                    print(f"User '{full_name}' successfully created — permission confirmed.")
                    result["passed"] = True
                    result["result"] = "pass"
                    user_created = True
                    result["screenshot"], _ = capture_screenshot(page, "create_user", "pass")
                    page.goto(BASE_URL)
                    page.wait_for_timeout(1000)
                    break
                else:
                    raise Exception(f"User '{full_name}' not found after creation — creation failed.")

            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                result["error"] = str(e)
                result["passed"] = False
                result["result"] = "fail"

                if attempt < max_attempts:
                    print("Retrying in 2 seconds...")
                    page.goto(BASE_URL)
                    page.wait_for_timeout(1000)
                    time.sleep(2)
                else:
                    print("Max retries reached. Failing test.")
                    # Take screenshot only once at the end
                    result["screenshot"], _ = capture_screenshot(page, "create_user", "fail")
                    break

    except Exception as e:
        print(f"Test execution failed: {e}")
        result["error"] = str(e)
        result["passed"] = False
        result["result"] = "fail"
        result["screenshot"], _ = capture_screenshot(page, "create_user", "fail")

    finally:
        # Cleanup - If user was created, delete it with System Admin privileges
        if user_created:
            print("\n--- CLEANUP: Adding System Admin (BTO) role to delete created user ---")
            try:
                lims, username = get_lims_connection()
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
                print(f"Current roles for {username} after adding System Admin (BTO) for cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

                print(f"Deleting created user '{full_name}' with System Admin privileges...")
                page.goto(f"{BASE_URL}/clarity/configuration")
                page.wait_for_timeout(2000)

                user_tab = page.locator("div.tab-title", has_text=re.compile("User Management", re.I))
                user_tab.first.click()
                page.wait_for_timeout(2000)

                page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
                search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
                
                if search_result.is_visible():
                    search_result.click()
                    page.wait_for_timeout(1000)
                    page.locator("button").filter(has_text="Delete").first.click()
                    page.wait_for_timeout(500)
                    page.reload()
                    page.wait_for_timeout(2000)
                    print(f"Created user '{full_name}' cleaned up successfully.")
                
                # Remove System Admin role after cleanup
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
                print(f"Current roles for {username} after removing System Admin (BTO) after cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

            except Exception as cleanup_error:
                print(f"Cleanup encountered an issue: {cleanup_error}")
        else:
            print("\n--- CLEANUP: User was not created, no cleanup needed ---")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result
