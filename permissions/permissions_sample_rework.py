"""
Test Module: Sample Rework Permission
==================================================
Checks if a user with the proper role can rework a sample in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time
from datetime import datetime
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 2
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_sample_rework(page, expected=True):
    """
    Checks if role can rework a sample in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Sample Rework Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Sample Rework",
        "description": "Checks if role can rework a sample in Clarity LIMS",
        "execution_time": 0.0,
        "expected": expected,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    SAMPLE_ID = "V_251014L0001-4"
    max_attempts = 1 if expected is False else (RETRIES + 1)
    start_time = time.time()

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\n--- Attempt {attempt} ---")
            print("Navigating to Projects & Samples...")
            page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
            page.wait_for_timeout(1000)

            print(f"Filtering for project '{PROJECT_NAME}'...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            filter_box.type(PROJECT_NAME, delay=10)
            page.wait_for_timeout(1000)

            print("Locating project row...")
            project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row.wait_for(state="visible", timeout=10000)
            project_row.click()
            page.wait_for_timeout(1000)
            print("Project clicked successfully.")

            print("Checking for available samples...")
            sample_rows = page.locator("div.project-list-item.x-item-selected")
            if sample_rows.count() == 0:
                raise Exception("No samples found in project.")

            print("Looking for 'Select Group' button...")
            select_group_btn = page.locator("button.select-group-help", has_text="Select Group")
            select_group_btn.wait_for(state="visible", timeout=10000)

            print("Clicking 'Select Group'...")
            select_group_btn.click()
            page.wait_for_timeout(1000)

            print("Opening 'Assign To Workflow' dropdown...")
            assign_btn = page.locator("div.rw-input", has_text="Assign To Workflow")
            assign_btn.click()
            page.wait_for_timeout(500)

            print("Selecting workflow 'Aneuploidy v3.6'...")
            workflow_option = page.locator("li.rw-list-option", has_text="Aneuploidy v3.6").first
            workflow_option.wait_for(state="visible", timeout=10000)
            workflow_option.click()
            page.wait_for_timeout(500)

            print("Confirming workflow assignment...")
            workflow_name_locator = page.locator("div.workflow-name", has_text="Aneuploidy v3.6")
            if workflow_name_locator.count() == 0:
                raise Exception("Workflow assignment failed.")
            print("Workflow successfully assigned!")

            # === Begin sample rework steps ===
            print("\n--- Beginning sample rework process ---")
            page.get_by_role("link", name="Lab View").click()
            print("Navigated to Lab View.")

            print("Opening 'Step 1 » Aneuploidy - Plasma Isolation'...")
            page.get_by_text("Step 1 » Aneuploidy - Plasma Isolation").click()
            page.wait_for_timeout(1000)

            print("Expanding sample group 'Single Well: Tube'...")
            page.locator("#listbody-1014").get_by_text("Single Well: Tube").click()
            page.wait_for_timeout(500)

            print("Selecting sample in 'Waiting' status...")
            page.locator("#listbody-1014").get_by_text("Waiting").click()
            page.wait_for_timeout(500)

            print(f"Selecting sample {SAMPLE_ID}...")
            page.get_by_text(SAMPLE_ID).click()
            page.wait_for_timeout(500)

            print("Clicking Options → Move...")
            page.get_by_role("button", name="Options").click()
            page.get_by_text("Move", exact=True).click()
            page.get_by_role("button", name="OK").click()
            print("Sample moved successfully.")

            print("Navigating to next step: Plasma Verification...")
            page.get_by_role("link", name="Lab View").click()
            page.get_by_text("Step 1 » Aneuploidy - Plasma Verification").click()
            page.wait_for_timeout(1000)

            print("Expanding sample group 'Single Well: Tube'...")
            page.locator("#listbody-1014").get_by_text("Single Well: Tube").click()
            page.wait_for_timeout(500)

            print("Selecting same sample for rework verification...")
            page.get_by_text(SAMPLE_ID).click()
            page.wait_for_timeout(500)

            print("Clicking Options → Move...")
            page.get_by_role("button", name="Options").click()
            page.get_by_text("Move", exact=True).click()
            page.get_by_role("button", name="OK").click()
            print("Rework step confirmed.")

            print("Finalizing: Opening 'Step 2 » Aneuploidy - Plasma'...")
            page.get_by_role("link", name="Lab View").click()
            page.locator("#my-work-container").get_by_text("Step 2 » Aneuploidy - Plasma").click()
            page.wait_for_timeout(1000)

            print("Expanding sample group 'Single Well: Tube'...")
            page.locator("#listbody-1014").get_by_text("Single Well: Tube").click()
            page.wait_for_timeout(500)

            print("Selecting same sample for rework verification...")
            page.get_by_text(SAMPLE_ID).click()
            page.wait_for_timeout(500)

            print("Adding to Ice Bucket...")
            page.locator("#ice-bucket-add-47269197").click()
            page.get_by_role("button", name="View Ice Bucket »").click()
            page.get_by_role("button", name="Begin Work »").click()
            print("Sample rework initiated successfully.")



            from playwright.sync_api import expect

            SAMPLE_ID = "V_251014L0001-4"
            ROW = "A"
            COL = "1"

            print("Dragging sample from input to output well...")

            # Locate the source sample
            source = page.locator(f"span.qtip-value[data-qtip='{SAMPLE_ID}']")
            source.scroll_into_view_if_needed()
            source.wait_for(state="visible", timeout=40000)

            # Locate the target well
            target = page.locator(f"div.container-well-inner.cw-row-{ROW}.cw-column-{COL}")
            target.scroll_into_view_if_needed()
            target.wait_for(state="visible", timeout=40000)


            # --- Wait for ExtJS mask to disappear ---
            print("Waiting for page mask to clear before drag-and-drop...")
            for _ in range(40):  # wait up to ~20 seconds
                masks = page.locator("div.x-mask")
                if masks.count() == 0 or not masks.first.is_visible():
                    break
                time.sleep(0.5)
            else:
                raise Exception("Timed out waiting for ExtJS mask to disappear.")

            # --- Perform drag-and-drop ---
            print(f"Dragging sample {SAMPLE_ID} to output well {ROW}:{COL}...")
            page.drag_and_drop(
                f"span.qtip-value[data-qtip='{SAMPLE_ID}']",
                f"div.container-well-inner.cw-row-{ROW}.cw-column-{COL}"
            )

            # Poll for the "in-use-well" class to appear
            for _ in range(20):  # ~10 seconds if 0.5s sleep
                if "in-use-well" in target.get_attribute("class"):
                    break
                time.sleep(0.5)
            else:
                raise Exception("Drag-and-drop did not complete successfully (well not marked in-use).")

            print(f"Sample {SAMPLE_ID} successfully dragged to output well {ROW}:{COL}.")

            # Click 'Record Details »' to finalize
            print("Clicking 'Record Details »' button to confirm rework placement...")
            page.get_by_role("button", name="Record Details »").click()
            page.wait_for_timeout(1000)
            print("Sample successfully recorded in workflow.")

            # === Test success ===
            result["passed"] = True
            result["result"] = "pass"
            result["screenshot"], _ = capture_screenshot(page, "sample_rework", "pass")
            print("Test PASSED — sample successfully reworked.")
            break  # exit retry loop

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["screenshot"], _ = capture_screenshot(page, "sample_rework", "fail")

            if attempt < max_attempts:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached. Failing test.")
                break

        finally:
            try:
                page.goto(BASE_URL)
                print("Returned to main page.")
            except Exception:
                pass

    # --- Test summary ---
    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)

    print("\n===== TEST RESULT SUMMARY =====")
    print(f"Status: {'PASS' if result['passed'] else 'FAIL'}")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot saved at: {result['screenshot']}")
    print("=================================\n")

    return result