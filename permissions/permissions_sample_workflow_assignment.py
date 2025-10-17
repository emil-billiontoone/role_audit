"""
Test Module: Sample Workflow Assignment Permission
==================================================
Checks if a user with the proper role can assign a sample to a workflow in Clarity LIMS.
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

def test_sample_workflow_assignment(page, expected=True):
    """
    Checks if role can assign a sample to a workflow in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Sample Workflow Assignment Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Sample Workflow Assignment",
        "description": "Checks if role can assign a sample to a workflow in Clarity LIMS",
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
            page.wait_for_timeout(1000)

            print(f"Filtering for project '{PROJECT_NAME}'...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            page.wait_for_timeout(500)
            filter_box.type(PROJECT_NAME, delay=100)
            page.wait_for_timeout(1000)

            project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row.wait_for(state="visible", timeout=10000)

            if project_row.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found")
            print("Project found — clicking on it...")
            project_row.click()
            page.wait_for_timeout(1000)

            # Check if there are samples
            sample_rows = page.locator("div.project-list-item.x-item-selected")
            if sample_rows.count() == 0:
                raise Exception("No samples found in project")

            # Deselect all samples first
            print("Looking for 'Select Group' button...")
            select_group_btn = page.locator("button.select-group-help", has_text="Select Group")
            select_group_btn.wait_for(state="visible", timeout=10000)  # wait up to 10 seconds

            if select_group_btn.count() > 0:
                print("Clicking 'Select Group'...")
                select_group_btn.click()
                page.wait_for_timeout(1000)
            else:
                raise Exception("'Select Group' button not found on the page.")

            # Click Assign to Workflow
            assign_btn = page.locator("div.rw-input", has_text="Assign To Workflow")
            assign_btn.click()
            page.wait_for_timeout(500)

            # Select workflow from dropdown
            workflow_option = page.locator("li.rw-list-option", has_text="Aneuploidy v3.6").first
            workflow_option.wait_for(state="visible", timeout=10000)  # wait for dropdown item
            workflow_option.click()
            page.wait_for_timeout(500)
            print(f"Selected workflow: {workflow_option.text_content()}")

            # Confirm workflow assigned
            workflow_name_locator = page.locator(
                "div.workflow-name", has_text="Aneuploidy v3.6"
            )
            if workflow_name_locator.count() > 0:
                print("Workflow successfully assigned")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception("Workflow assignment failed")

            # Clean up: unassign workflow
            sample_id = sample_rows.first.get_attribute("data-sample-id")
            if sample_id:
                delete_btn = page.locator(f"div.delete-btn[data-sample-id='{sample_id}']")
                if delete_btn.count() > 0:
                    print("Cleaning up: unassigning workflow...")
                    delete_btn.first.click()
                    page.wait_for_timeout(500)

            break  # Exit retry loop if successful

        except Exception as e:
            timestamp = int(time.time())
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"sample_workflow_{timestamp}.png")
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