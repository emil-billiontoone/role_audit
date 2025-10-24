"""
Test Module: Sample Workflow Assignment Permission
==================================================
Checks if a user with the proper role can assign a sample to a workflow in Clarity LIMS.
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
            page.wait_for_timeout(800)

            print(f"Filtering for project '{PROJECT_NAME}'...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=8000)
            filter_box.type(PROJECT_NAME, delay=50)
            page.wait_for_timeout(500)

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

            # Click Assign to Workflow
            assign_btn = page.locator("div.rw-input", has_text="Assign To Workflow")
            assign_btn.click()
            page.wait_for_timeout(300)

            # Select workflow from dropdown
            workflow_option = page.locator("li.rw-list-option", has_text="Aneuploidy v3.6").first
            workflow_option.wait_for(state="visible", timeout=5000)
            workflow_option.click()
            page.wait_for_timeout(300)
            print(f"Selected workflow: {workflow_option.text_content()}")

            # Confirm workflow assigned
            workflow_name_locator = page.locator(
                "div.workflow-name", has_text="Aneuploidy v3.6"
            )
            if workflow_name_locator.count() > 0:
                print("Workflow successfully assigned")
                result["passed"] = True
                result["result"] = "pass"
                result["screenshot"], _ = capture_screenshot(page, "sample_workflow_assignment", "pass")
            else:
                raise Exception("Workflow assignment failed")

            break  # Exit retry loop if successful

        except Exception as e:
            result["error"] = str(e)
            result["passed"] = False
            result["result"] = "fail"
            result["screenshot"], _ = capture_screenshot(page, "sample_workflow_assignment", "fail")

            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                print("Retrying in 1 second...")
                time.sleep(1)
            else:
                print("Max retries reached. Failing test.")
                break

    # Cleanup: Remove all samples from workflows (runs once after all attempts)
    try:
        print("\n--- CLEANUP: Removing all samples from workflows ---")
        page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
        page.wait_for_timeout(800)

        print(f"Filtering for project '{PROJECT_NAME}'...")
        filter_box = page.get_by_role("textbox", name="Filter...")
        filter_box.wait_for(state="visible", timeout=5000)
        page.wait_for_timeout(300)
        filter_box.fill("")
        filter_box.type(PROJECT_NAME, delay=50)
        page.wait_for_timeout(500)

        print("Locating project row...")
        project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
        project_row.wait_for(state="visible", timeout=8000)
        if project_row.count() == 0:
            print(f"Warning: Project '{PROJECT_NAME}' not found for cleanup")
        else:
            print("Project found — clicking to open project details...")
            project_row.click()
            page.wait_for_timeout(1000)

            print("Expanding sample group to show all samples...")
            group_expander = page.locator("div.group-expander-btn").first
            if group_expander.count() > 0:
                group_expander.click()
                page.wait_for_timeout(1000)
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
                try:
                    page.locator("div.x-mask-full-page").wait_for(state="hidden", timeout=5000)
                except:
                    pass  # No overlay present

                # Click delete
                delete_btn.first.click()

                # Wait until the delete button for this sample is gone (indicating successful removal)
                delete_btn_check = page.locator(f"div.delete-btn[data-sample-id='{sample_id}']")
                try:
                    delete_btn_check.wait_for(state="detached", timeout=8000)
                    print(f"Sample {sample_id} successfully removed from workflow.")
                except:
                    print(f"Warning: delete button for sample {sample_id} did not disappear within timeout")

                removed_count += 1
                page.wait_for_timeout(300)

            print(f"Removed {removed_count} sample(s) from workflows.")

            # Verification: ensure no samples remain assigned
            remaining_samples = page.locator("div.sample-row:has(div.workflow-name)").count()
            if remaining_samples == 0:
                print("All samples successfully removed from workflows.")
            else:
                print(f"Warning: {remaining_samples} sample(s) still assigned to workflows after removal.")

        # Navigate back to base URL
        page.goto(BASE_URL)
        print("Returned to main page.")
    except Exception as cleanup_error:
        print(f"Cleanup encountered an issue: {cleanup_error}")
        result["screenshot"], _ = capture_screenshot(page, "sample_workflow_assignment", "fail")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"{result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result