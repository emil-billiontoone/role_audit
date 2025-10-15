"""
Test Module: Update Sample Permission
=====================================
Checks if a user with the proper role can update a sample in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_update_sample(page):
    """
    Checks if role can update a sample in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Update Sample Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Update Sample",
        "description": "Checks if role can update a sample in Clarity LIMS",
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
            print(f"\nAttempt {attempt}: Navigating to Projects & Samples...")
            page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
            page.wait_for_timeout(1500)

            print(f"Filtering for project '{PROJECT_NAME}'...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            filter_box.type(PROJECT_NAME, delay=100)
            page.wait_for_timeout(1000)

            print("Waiting for project row to appear...")
            project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row.wait_for(state="visible", timeout=15000)

            if project_row.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found")

            print("Project found — clicking on it...")
            project_row.click()
            page.wait_for_timeout(1500)

            # Check for Modify Samples button
            # Locate the button
            sample_button = page.locator("#modify-sample-sheet-button a")
            sample_button.wait_for(state="visible", timeout=10000)

            # Get button text
            button_text = sample_button.inner_text().strip().upper()
            print(f"Button text found: {button_text}")

            if "MODIFY" in button_text:
                print("Modify sample button found — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            elif "DOWNLOAD" in button_text:
                print("Modify sample button not found — user only has Download Sample List permission.")
                result["passed"] = False
                result["result"] = "fail"
            else:
                raise Exception(f"Unexpected button text: '{button_text}'")

            break  # Exit retry loop if handled correctly


        except Exception as e:
            timestamp = int(time.time())
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"update_sample_fail_{timestamp}.png")
            try:
                page.screenshot(path=screenshot_file)
                result["screenshot"] = screenshot_file
            except:
                result["screenshot"] = "Failed to capture screenshot"

            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"

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