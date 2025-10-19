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
    print("\n===== TEST: Delete Reagent Kit Permission =====")
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
    user_name = "Emil User Test"

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\nAttempt {attempt}: Navigating to Configuration page...")
            page.goto(f"{BASE_URL}/clarity/configuration")
            page.wait_for_timeout(2000)

            print("Checking for 'Consumables' tab...")
            consumables_tab = page.locator("div.tab-title", has_text=re.compile("Consumables", re.I))
            if consumables_tab.count() == 0:
                raise Exception("Consumables tab not found — permission denied or hidden.")

            print("Consumables tab found — clicking it...")
            consumables_tab.first.click()
            page.wait_for_timeout(2000)

            print("Checking for 'Reagents' tab...")
            reagents_tab = page.locator("div.tab-title", has_text=re.compile("Reagents", re.I))
            if reagents_tab.count() == 0:
                raise Exception("Reagents tab not found — permission denied or hidden.")

            print("Reagents tab found — clicking it...")
            reagents_tab.first.click()
            page.wait_for_timeout(2000)

            print(f"Verifying reagent kit '{reagent_kit_name}' is present...")
            page.wait_for_timeout(2000)
            search_result = page.get_by_text(reagent_kit_name)
            if not search_result.is_visible():
                raise Exception(f"'{reagent_kit_name}' not found — delete may have failed or permission denied.")

            search_result.click()
            page.wait_for_timeout(1000)

            print("Clicking 'Delete' button...")
            delete_button = page.get_by_role("button", name=re.compile("Delete", re.I))
            delete_button.click()
            page.wait_for_timeout(1000)

            print("Waiting for confirmation dialog...")
            confirm_button = page.get_by_role("button", name=re.compile("Delete Item", re.I))
            confirm_button.wait_for(state="visible", timeout=5000)
            confirm_button.click()
            page.wait_for_timeout(2000)

            print("Refreshing page to see if reagent kit is deleted...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying reagent kit '{reagent_kit_name}' is deleted...")
            page.wait_for_timeout(2000)
            search_result = page.get_by_text(reagent_kit_name)

            if not search_result.is_visible():
                print(f"'{reagent_kit_name}' is deleted — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception(f"'{reagent_kit_name}' is not deleted — permission denied.")

            result["screenshot"], _ = capture_screenshot(page, "delete_reagent_kit", "pass")

            print("Returning to main page...")
            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break  # success, exit retry loop

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"

            result["screenshot"], _ = capture_screenshot(page, "delete_reagent_kit", "fail")

            if attempt < max_attempts:
                print("Retrying in 2 seconds...")
                try:
                    page.goto(BASE_URL)
                    page.wait_for_timeout(1000)
                except:
                    pass
                time.sleep(2)
            else:
                print("Max retries reached. Failing test.")
                break

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")

    return result




"""
Test Module: Create User Permission
=================================
Checks if a user with the proper role can create a new user in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time

BASE_URL = "https://clarity-dev.btolims.com"
RETRIES = 2
SCREENSHOT_DIR = "screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_permissions_create_user(page, expected=True):
    """
    Checks if a user with the 'permissions_create_user' role can create a new user in Clarity LIMS.
    User Management tab and user list in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Create User Permission =====")

    result = {
        "test_name": "Create User Permission",
        "description": "Checks if a user can create a new user in Clarity LIMS",
        "execution_time": 0.0,
        "expected": True,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    start_time = time.time()

    # If expected to fail, only try once (no retries)


    max_attempts = 1 if expected == False else (RETRIES + 1)


    


    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\nAttempt {attempt}: Navigating to Configuration page...")
            page.goto(f"{BASE_URL}/clarity/configuration")
            page.wait_for_timeout(2000)

            print("Checking for User Management tab...")

            # Locate the User Management tab
            user_tab = page.locator("div.tab-title", has_text=re.compile("User Management", re.I))

            if user_tab.count() == 0:
                raise Exception("User Management tab not found — permission denied or hidden.")

            print("User Management tab found — clicking it...")
            user_tab.first.click()
            page.wait_for_timeout(2000)

            print("Checking if New User button is visible...")
            new_user_button = page.locator("div.btn-base.isis-btn.btn.large.creation.add-icon.new-user")

            if new_user_button.count() > 0:
                print("New User button found — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception("New User button not found after clicking User Management tab.")

            break  # Stop retry loop if passed

        except Exception as e:
            timestamp = int(time.time())
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"create_user_permission_fail_{timestamp}.png")
            try:
                page.screenshot(path=screenshot_file)
                result["screenshot"] = screenshot_file
            except:
                result["screenshot"] = "Failed to capture screenshot"

            result["error"] = str(e)
            print(f"Attempt {attempt} failed: {e}")

            if attempt <= RETRIES:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached. Failing test.")
                break

        finally:
            try:
                page.goto(BASE_URL)
                print("Returned to main page.")
            except:
                pass

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)

    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")

    return result

