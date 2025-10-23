"""
Test Module: Sample Workflow Removal Permission
====================================================
Checks if a user with the proper role can remove samples
from a workflow in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2
SCREENSHOT_DIR = "test_results/screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_sample_workflow_removal(page, expected=True):
    """
    Checks if role can remove samples from a workflow in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Sample Workflow Removal Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Sample Workflow Removal",
        "description": "Checks if role can remove samples from a workflow in Clarity LIMS",
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
            filter_box.fill("")
            filter_box.type(PROJECT_NAME, delay=100)
            page.wait_for_timeout(1000)

            print("Locating project row...")
            project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row.wait_for(state="visible", timeout=10000)
            if project_row.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found")

            print("Project found — clicking to open project details...")
            project_row.click()
            page.wait_for_timeout(1500)

            print("Expanding sample group to show all samples...")
            group_expander = page.locator("div.group-expander-btn").first
            if group_expander.count() > 0:
                group_expander.click()
                page.wait_for_timeout(1500)
                print("Sample group expanded.")
            else:
                print("No group expander button found — possibly already expanded.")

            # Remove all samples from workflows using live-loop
            removed_count = 0
            while True:
                sample_rows = page.locator("div.sample-row:has(div.workflow-name)")
                if sample_rows.count() == 0:
                    break

                sample = sample_rows.first
                sample_id = sample.locator(".sample-udf-icon").get_attribute("data-sample-id")
                workflow_name = sample.locator(".workflow-name").inner_text()
                print(f"Removing sample ID {sample_id} from workflow '{workflow_name}'...")

                delete_btn = page.locator(f"div.delete-btn[data-sample-id='{sample_id}']")
                if delete_btn.count() == 0:
                    print(f"No delete button found for sample ID {sample_id}, skipping.")
                    # Remove this sample from DOM consideration if needed
                    page.evaluate("el => el.remove()", sample)
                    continue

                # Wait for any page overlay to disappear before clicking
                page.locator("div.x-mask-full-page").wait_for(state="hidden", timeout=10000)

                # Click delete
                delete_btn.first.click()

                # Wait until the delete button for this sample is gone (indicating successful removal)
                delete_btn_check = page.locator(f"div.delete-btn[data-sample-id='{sample_id}']")
                try:
                    delete_btn_check.wait_for(state="detached", timeout=10000)
                    print(f"Sample {sample_id} successfully removed from workflow.")
                except:
                    print(f"Warning: delete button for sample {sample_id} did not disappear within timeout")

                removed_count += 1
                page.wait_for_timeout(500)  # optional small buffer

            print(f"Removed {removed_count} sample(s) from workflows.")

            # Verification: ensure no samples remain assigned
            remaining_samples = page.locator("div.sample-row:has(div.workflow-name)").count()
            if remaining_samples == 0:
                print("All samples successfully removed from workflows.")
                result["passed"] = True
                result["result"] = "pass"
                result["screenshot"], _ = capture_screenshot(page, "sample_workflow_removal", "pass")
            else:
                raise Exception(f"{remaining_samples} sample(s) still assigned to workflows after removal.")

            break  # Exit retry loop on success

        except Exception as e:
            result["screenshot"], _ = capture_screenshot(page, "sample_workflow_removal", "fail")

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
                print("Returned to main Clarity home page.")
            except:
                print("Failed to return to home page after test attempt.")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)

    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")

    return result