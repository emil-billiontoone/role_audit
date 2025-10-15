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


def test_permissions_create_user(page):
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

    for attempt in range(1, RETRIES + 2):
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

