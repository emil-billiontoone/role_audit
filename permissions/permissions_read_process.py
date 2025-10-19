"""
Test Module: Read Process Permission
=====================================
Checks if a user with the proper role can read a process in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2

def test_read_process(page, expected=True):
    """
    Checks if role can read a process in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Read Process Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Read Process",
        "description": "Checks if role can read a process in Clarity LIMS",
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
    }

    master_step = f"{user_details['master_step']}"

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\nAttempt {attempt}: Navigating to Configuration page...")
            page.goto(f"{BASE_URL}/clarity/configuration")
            page.wait_for_timeout(2000)

            # Click User Management
            print("Checking for Lab Work tab...")
            lab_work_tab = page.locator("div.tab-title", has_text=re.compile("Lab Work", re.I))
            if lab_work_tab.count() == 0:
                raise Exception("Lab Work tab not found — permission denied or hidden.")
            lab_work_tab.first.click()
            page.wait_for_timeout(2000)

            print("Looking for 'Master Step' column header...")
            header = page.locator("div.g-col-header.master-step-column-header")
            if header.count() == 0:
                raise Exception("Master Step column header not found — permission denied or hidden.")

            print(f"Verifying that user '{master_step}' appears in the list...")
            page.locator("#configuration-app-container").get_by_text(master_step).click()
            print(f"Master Step '{master_step}' found and clicked.")

            print(f"Verifying that master step '{master_step}' is read...")
            if page.locator("div.wps-details-form.master-step-details").is_visible():
                print(f"Master Step '{master_step}' is read.")
                result["passed"] = True
                result["result"] = "pass"
                result["screenshot"], _ = capture_screenshot(page, "read_process", "pass")
            else:
                raise Exception("Master Step details form not found — permission denied or hidden.")

            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"
            result["screenshot"], _ = capture_screenshot(page, "read_process", "fail")

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
