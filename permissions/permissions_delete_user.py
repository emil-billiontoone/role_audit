"""
Test Module: Delete User Permission
=====================================
Checks if a user with the proper role can delete a user in Clarity LIMS.
Compatible with RolePermissionTester framework.

Test Flow:
1. Add System Admin (BTO) role to the test user
2. Create a test user to be deleted
3. Remove System Admin (BTO) role to test with the original role
4. Attempt to delete the test user
5. If deletion fails, add System Admin (BTO) back and clean up
6. If deletion succeeds, test passes (cleanup already done)
"""

import re
import time
from .test_utils import capture_screenshot
from change_role import modify_user_role, get_lims_connection

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
        "description": "Checks if role can delete a user in Clarity LIMS",
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
        "first_name": "Emil Delete",
        "last_name": "User Test",
        "title": "Test",
        "account": "Administrative Lab",
        "email": "edeguzman@billiontoone.com",
        "username": "EmilDeleteUserTest",
        "role": "Lab Operator (BTO)"
    }

    full_name = f"{user_details['first_name']} {user_details['last_name']}"
    user_created = False

    try:
        # Step 1: Add System Admin (BTO) role to create test user
        print("\n--- SETUP: Adding System Admin (BTO) role to create test user ---")
        lims, username = get_lims_connection()
        user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
        print(f"Current roles for {username} after adding System Admin (BTO):")
        for r in user.roles:
            print(f"  - {r.name}")

        # Step 2: Create the test user
        print(f"\n--- SETUP: Creating test user '{full_name}' ---")
        page.goto(f"{BASE_URL}/clarity/configuration")
        page.wait_for_timeout(2000)

        # Click User Management
        print("Navigating to User Management tab...")
        user_tab = page.locator("div.tab-title", has_text=re.compile("User Management", re.I))
        if user_tab.count() == 0:
            raise Exception("User Management tab not found — cannot create test user.")
        user_tab.first.click()
        page.wait_for_timeout(2000)

        # Click NEW USER
        print("Clicking 'NEW USER' button...")
        page.locator("button").filter(has_text=re.compile("NEW USER", re.I)).click()
        page.wait_for_timeout(1000)

        # Fill user details
        print("Filling user details...")
        page.get_by_role("textbox", name=re.compile("Enter First Name", re.I)).type(user_details["first_name"], delay=10)
        page.get_by_role("textbox", name=re.compile("Enter Last Name", re.I)).type(user_details["last_name"], delay=10)
        page.wait_for_timeout(500)

        page.get_by_role("textbox", name="Title").type(user_details["title"], delay=10)
        page.wait_for_timeout(500)

        # Select Account
        page.locator("#account-drp").click()
        page.wait_for_selector("ul.rw-list >> li", state="visible")
        page.locator(f"ul.rw-list >> text={user_details['account']}").click()

        # Fill Email and Username
        page.get_by_role("textbox", name="Email").type(user_details["email"], delay=10)
        page.wait_for_timeout(500)
        page.get_by_role("textbox", name="Username").type(user_details["username"], delay=10)
        page.wait_for_timeout(500)

        # Select Role
        page.locator(".rw-multiselect-wrapper").click()
        page.get_by_role("option", name=user_details["role"]).click()
        page.wait_for_timeout(1000)

        # Save User
        print("Saving test user...")
        page.locator("button").filter(has_text="Save").click()
        page.wait_for_timeout(2000)

        # Verify user was created
        page.reload()
        page.wait_for_timeout(2000)
        page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
        search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
        if not search_result.is_visible():
            raise Exception(f"Test user '{full_name}' was not created successfully.")
        
        print(f"Test user '{full_name}' created successfully.")
        user_created = True

        # Step 3: Remove System Admin (BTO) role to test with original role
        print("\n--- SETUP: Removing System Admin (BTO) role to test deletion permission ---")
        user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
        print(f"Current roles for {username} after removing System Admin (BTO):")
        for r in user.roles:
            print(f"  - {r.name}")

        # Step 4: Test deletion with the original role
        print(f"\n--- TEST: Attempting to delete user '{full_name}' with current role ---")
        
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

                print(f"Locating user '{full_name}' in the list...")
                page.locator("div.g-col-value", has_text=re.compile(full_name, re.I)).scroll_into_view_if_needed()
                search_result = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
                if not search_result.is_visible():
                    raise Exception(f"User '{full_name}' not found in user list.")
                    
                print(f"Clicking on user '{full_name}'...")
                search_result.click()
                page.wait_for_timeout(1000)

                print("Clicking 'Delete' button...")
                delete_button = page.locator("button").filter(has_text="Delete").first
                
                # Check if delete button is visible/enabled
                if delete_button.count() == 0 or not delete_button.is_visible():
                    raise Exception("Delete button not visible — permission denied.")
                
                delete_button.click()
                page.wait_for_timeout(500)

                print("Refreshing page to verify deletion...")
                page.reload()
                page.wait_for_timeout(2000)

                # Wait for the user list to finish loading
                page.wait_for_selector("div.g-col-value", state="visible", timeout=30000)

                # Check if user is gone
                search_result_after = page.locator("div.g-col-value", has_text=re.compile(full_name, re.I))
                if not search_result_after.is_visible():
                    print(f"'{full_name}' is deleted — permission confirmed.")
                    result["passed"] = True
                    result["result"] = "pass"
                    user_created = False  # Mark as cleaned up
                    
                    # Take screenshot now that the list is fully rendered
                    result["screenshot"], _ = capture_screenshot(page, "delete_user", "pass")

                    page.goto(BASE_URL)
                    page.wait_for_timeout(1000)
                    break
                else:
                    raise Exception(f"'{full_name}' is still visible after deletion attempt — permission denied.")

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
                    result["screenshot"], _ = capture_screenshot(page, "delete_user", "fail")
                    break

    except Exception as e:
        print(f"Setup or test execution failed: {e}")
        result["error"] = str(e)
        result["passed"] = False
        result["result"] = "fail"
        result["screenshot"], _ = capture_screenshot(page, "delete_user", "fail")

    finally:
        # Step 5: Cleanup - If test user still exists, add System Admin role back and delete
        if user_created:
            print("\n--- CLEANUP: Test user still exists, adding System Admin (BTO) role to clean up ---")
            try:
                lims, username = get_lims_connection()
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
                print(f"Current roles for {username} after adding System Admin (BTO) for cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

                print(f"Deleting test user '{full_name}' with System Admin privileges...")
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
                    print(f"Test user '{full_name}' cleaned up successfully.")
                
                # Remove System Admin role after cleanup
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
                print(f"Current roles for {username} after removing System Admin (BTO) after cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

            except Exception as cleanup_error:
                print(f"Cleanup encountered an issue: {cleanup_error}")
        else:
            print("\n--- CLEANUP: Test user already deleted, no cleanup needed ---")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result