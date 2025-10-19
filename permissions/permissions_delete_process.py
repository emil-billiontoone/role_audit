"""
Test Module: Delete Process Permission
=====================================
Checks if a user with the proper role can delete a process in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2

def test_delete_process(page, expected=True):
    """
    Checks if role can delete a process in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Delete Process Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Delete Process",
        "description": "Checks if role can delete a process in Clarity LIMS",
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
        "master_step": "Emil Master Step Test",
        "instrument_type": "AJ Thermocycler",
    }

    master_step = f"{user_details['master_step']}"

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\nAttempt {attempt}: Navigating to Configuration page...")
            page.goto(f"{BASE_URL}/clarity/configuration")
            page.wait_for_timeout(2000)

            # Click User Management
            print("Checking for Lab Work tab...")
            user_tab = page.locator("div.tab-title", has_text=re.compile("Lab Work", re.I))
            if user_tab.count() == 0:
                raise Exception("Lab Work tab not found — permission denied or hidden.")
            user_tab.first.click()
            page.wait_for_timeout(2000)

            print("Clicking 'Add Master Step' icon button...")
            button = page.locator("div.wps-header-button.master-step-column-header button")

            if button.count() > 0:
                print("Button found, clicking now...")
                button.first.click()
                page.wait_for_timeout(1000)
            else:
                raise Exception("Add Master Step button not found — permission denied or hidden.")

            # Delete Master Step
            print("Clicking 'Delete'...")
            page.locator("button").filter(has_text="Delete").click()
            page.wait_for_timeout(2000)

            print("Waiting for confirmation deletion dialog...")
            confirm_button = page.get_by_role("button", name=re.compile("Delete Master Step", re.I))
            confirm_button.wait_for(state="visible", timeout=5000)
            confirm_button.click()
            page.wait_for_timeout(2000)

            # Verify master step is deleted
            print("Refreshing page to see if master step is deleted...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying that master step '{master_step}' is deleted...")
            page.locator("div.g-two-sided-row", has_text=re.compile(master_step, re.I)).scroll_into_view_if_needed()
            search_result = page.locator("div.g-two-sided-row", has_text=re.compile(master_step, re.I))
            if search_result.is_visible():
                raise Exception(f"Master Step '{master_step}' is not deleted.")

            print(f"Master Step '{master_step}' successfully deleted.")
            result["passed"] = True
            result["result"] = "pass"
            result["screenshot"], _ = capture_screenshot(page, "delete_process", "pass")

            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"
            result["screenshot"], _ = capture_screenshot(page, "delete_process", "fail")

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
