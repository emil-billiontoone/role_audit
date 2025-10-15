"""
Test Module: Update User Permission
===================================
Checks if a user with the proper role can update a user in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://clarity-dev.btolims.com"
RETRIES = 0
USER_NAME = "Emil Test"
SCREENSHOT_DIR = "screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_permissions_update_user(page):
    """
    Checks if a user can update a user in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Update User Permission =====")

    result = {
        "test_name": "Update User Permission",
        "description": "Checks if a user can update a user in Clarity LIMS",
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

            print("Waiting for User Management tab...")
            user_tab = page.locator("div.tab-title", has_text=re.compile("User Management", re.I))
            user_tab.wait_for(state="visible", timeout=5000)  

            print("User Management tab found — clicking it...")
            user_tab.first.click()

            print("Waiting for user list to appear...")
            user_list = page.locator("div.g-table.user-list")
            user_list.wait_for(state="visible", timeout=15000)

            print(f"Searching for user: {USER_NAME}...")
            user_entry = page.locator("div.g-col-value", has_text=re.compile(USER_NAME, re.I))
            user_entry.wait_for(state="visible", timeout=15000)

            print(f"User '{USER_NAME}' found — clicking entry...")
            user_entry.first.click()

            print("Waiting for Fax input field...")
            fax_input = page.locator("input#fax")
            fax_input.wait_for(state="visible", timeout=15000)

            print("Entering 'TEST' in Fax field to trigger Save button...")
            fax_input.fill("TEST")

            print("Waiting for Save button to become active...")
            save_button_active = page.locator(
                "div.btn-base.isis-btn.btn.action.undefined button:not(.disabled)",
                has_text=re.compile("Save", re.I)
            )
            save_button_active.wait_for(state="visible", timeout=15000)

            print("Save button is active — user can update details.")
            result["passed"] = True
            result["result"] = "pass"
            break  # test passed, exit retry loop

        except PlaywrightTimeoutError as e:
            result["error"] = f"Timeout waiting for element: {e}"
            print(f"Attempt {attempt} failed: {result['error']}")

        except Exception as e:
            result["error"] = str(e)
            print(f"Attempt {attempt} failed: {result['error']}")

        finally:
            timestamp = int(time.time())
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"update_user_permission_fail_{timestamp}.png")
            try:
                page.screenshot(path=screenshot_file)
                result["screenshot"] = screenshot_file
            except:
                result["screenshot"] = "Failed to capture screenshot"

            if attempt <= RETRIES and not result["passed"]:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached or test passed.")

            try:
                page.goto(BASE_URL)
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