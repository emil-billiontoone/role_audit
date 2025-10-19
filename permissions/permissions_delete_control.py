"""
Test Module: Delete Control Permission
=====================================
Checks if a user with the proper role can delete a control in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2
control_name = "Emil Control Test"

def test_delete_control(page, expected=True):
    """
    Checks if role can delete a control in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Delete Control Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Delete Control",
        "description": "Checks if role can delete a control in Clarity LIMS",
        "execution_time": 0.0,
        "expected": expected,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    start_time = time.time()
    max_attempts = 1 if not expected else (RETRIES + 1)

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

            print("Checking for 'Controls' tab...")
            controls_tab = page.locator("div.tab-title", has_text=re.compile("Controls", re.I))
            if controls_tab.count() == 0:
                raise Exception("Controls tab not found — permission denied or hidden.")

            print("Controls tab found — clicking it...")
            controls_tab.first.click()
            page.wait_for_timeout(2000)

            print("Checking for 'NEW CONTROL' button...")
            new_control_button = page.get_by_role("button", name=re.compile("NEW CONTROL", re.I))
            if not new_control_button.is_visible():
                raise Exception("NEW CONTROL button not visible — permission denied or hidden.")

            print(f"Verifying control '{control_name}' appears in the list...")
            search_result = page.get_by_text(control_name)
            if not search_result.is_visible():
                raise Exception(f"'{control_name}' not found — creation may have failed or permission denied.")

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

            print("Refreshing page to see if control is deleted...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying control '{control_name}' is deleted...")
            search_result = page.get_by_text(control_name)
            if not search_result.is_visible():
                print(f"'{control_name}' is deleted — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception(f"'{control_name}' is not deleted — permission denied.")

            # Take screenshot before leaving page
            result["screenshot"], _ = capture_screenshot(page, "delete_control", "pass")

            print("Returning to main page...")
            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break  # success, exit retry loop

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"

            result["screenshot"], _ = capture_screenshot(page, "delete_control", "fail")

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