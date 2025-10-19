"""
Test Module: Create Reagent Kit Permission
=====================================
Checks if a user with the proper role can create a reagent kit in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2


def test_create_reagent_kit(page, expected=True):
    """
    Checks if role can create a reagent kit in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Create Reagent Kit Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Create Reagent Kit",
        "description": "Checks if role can create a reagent kit in Clarity LIMS",
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

            print("NEW CONTROL button found — clicking it...")
            new_control_button.click()
            page.wait_for_timeout(1000)

            print("Filling out 'Control Sample Name' field...")
            control_name = "Emil Control Test"
            name_box = page.get_by_role("textbox", name=re.compile("Enter Control Sample Name", re.I))
            name_box.click()
            name_box.type(control_name, delay=100)
            page.wait_for_timeout(500)

            print("Clicking 'Save' button...")
            save_button = page.get_by_role("button", name=re.compile("Save", re.I))
            save_button.click()
            page.wait_for_timeout(2000)


            print("Refreshing page to see if control is present...")
            page.reload()
            page.wait_for_timeout(2000)

            print(f"Verifying control '{control_name}' appears in the list...")
            search_result = page.get_by_text(control_name)
            if not search_result.is_visible():
                raise Exception(f"'{control_name}' not found — creation may have failed or permission denied.")

            print(f"'{control_name}' successfully created.")
            result["passed"] = True
            result["result"] = "pass"

            # Take screenshot before leaving page
            result["screenshot"], _ = capture_screenshot(page, "create_reagent_kit", "pass")

            print("Returning to main page...")
            page.goto(BASE_URL)
            page.wait_for_timeout(1000)
            break  # success, exit retry loop

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"

            result["screenshot"], _ = capture_screenshot(page, "create_reagent_kit", "fail")

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