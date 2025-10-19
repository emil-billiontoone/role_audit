"""
Test Module: Update Process Permission
=====================================
Checks if a user with the proper role can update a process in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2

def test_update_process(page, expected=True):
    """
    Checks if role can update a process in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Update Process Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Update Process",
        "description": "Checks if role can update a process in Clarity LIMS",
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

            print("Looking for 'Master Step' column header...")
            header = page.locator("div.g-col-header.master-step-column-header")
            if header.count() == 0:
                raise Exception("Master Step column header not found — permission denied or hidden.")

            print(f"Verifying that user '{master_step}' appears in the list...")
            page.locator("div.g-two-sided-row", has_text=re.compile(master_step, re.I)).scroll_into_view_if_needed()
            search_result = page.locator("div.g-two-sided-row", has_text=re.compile(master_step, re.I))
            if not search_result.is_visible():
                raise Exception(f"Master Step '{master_step}' not found after creation.")

            print(f"Clicking '{master_step}'...")
            search_result.click()
            page.wait_for_timeout(1000)

            # Fill Instrument Type
            print("Filling Instrument Type...")
            page.locator(".fa.fa-plus").first.click()
            page.locator("#configuration-app-container").get_by_text(user_details["instrument_type"]).click()
            page.wait_for_timeout(500)
            page.locator("div.btn-base.isis-btn.btn.only-icon.check button").click()
            page.wait_for_timeout(500)

            # Save User
            print("Clicking 'Save'...")
            page.locator("button").filter(has_text="Save").click()
            page.wait_for_timeout(2000)

            print("Refreshing page to see if instrument type is updated...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying that instrument type is '{user_details['instrument_type']}'...")

            # Locate the div containing the instrument type
            instrument_type_div = page.locator("div.g-col-value", has_text=re.compile(user_details["instrument_type"], re.I))

            if instrument_type_div.count() > 0:
                actual_value = instrument_type_div.first.inner_text().strip()
                if actual_value == user_details["instrument_type"]:
                    print("Instrument type is updated — permission confirmed.")
                    result["passed"] = True
                    result["result"] = "pass"
                else:
                    raise Exception(f"Instrument type is '{actual_value}' — permission denied.")
            else:
                raise Exception("Instrument type field not found on page.")

            result["screenshot"], _ = capture_screenshot(page, "update_process", "pass")

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
