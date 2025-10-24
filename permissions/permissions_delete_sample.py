"""
Test Module: Delete Sample Permission
=====================================
Checks if a user with the proper role can delete a sample in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import re
import time
from .test_utils import capture_screenshot, clean_error_message

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2


def test_delete_sample(page, expected=True):
    """
    Checks if role can delete a sample in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Delete Sample Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Delete Sample",
        "description": "Checks if role can delete a sample in Clarity LIMS",
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
            print(f"\nAttempt {attempt}: Navigating to Projects & Samples...")
            page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
            page.wait_for_timeout(800)

            print(f"Filtering for project '{PROJECT_NAME}'...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=8000)
            filter_box.type(PROJECT_NAME, delay=50)
            page.wait_for_timeout(500)

            print("Waiting for project row to appear...")
            project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row.wait_for(state="visible", timeout=8000)

            if project_row.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found")

            print("Project found — clicking on it...")
            project_row.click()
            page.wait_for_timeout(800)

         # Check if there are samples
            sample_rows = page.locator("div.project-list-item.x-item-selected")
            if sample_rows.count() == 0:
                raise Exception("No samples found in project")

            # Deselect all samples first
            print("Looking for 'Select Group' button...")
            select_group_btn = page.locator("button.select-group-help", has_text="Select Group")
            select_group_btn.wait_for(state="visible", timeout=5000)

            if select_group_btn.count() > 0:
                print("Clicking 'Select Group'...")
                select_group_btn.click()
                page.wait_for_timeout(500)
            else:
                raise Exception("'Select Group' button not found on the page.")

            # check to see if delete button is present and clickable
            delete_button = page.locator("#delete-btn-ctrsubmitted-sample-list div.btn-base.isis-btn")

            if delete_button.count() > 0 and delete_button.first.is_visible():
                print("Delete button is visible — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception("Delete button is not visible — permission denied.")
            
            # Navigate back to base URL only on success
            try:
                page.goto(BASE_URL)
                print("Returned to main page.")
            except:
                pass
                
            break  # Exit retry loop if handled correctly


        except Exception as e:
            result["error"] = clean_error_message(e)
            result["passed"] = False
            result["result"] = "fail"

            print(f"Attempt {attempt} failed: {clean_error_message(e)}")
            
            if attempt < max_attempts:
                print("Retrying in 1 second...")
                # Navigate back to base URL before retry
                try:
                    page.goto(BASE_URL)
                    page.wait_for_timeout(500)
                except:
                    pass
                time.sleep(1)
            else:
                print("Max retries reached. Failing test.")
                break

    # Take screenshot once at the end
    if result["passed"]:
        result["screenshot"], _ = capture_screenshot(page, "delete_sample", "pass")
    else:
        result["screenshot"], _ = capture_screenshot(page, "delete_sample", "fail")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"{result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result