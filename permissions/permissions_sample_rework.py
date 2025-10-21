# """
# Test Module: Sample Rework Permission
# ==================================================
# Checks if a user with the proper role can rework a sample in Clarity LIMS.
# Compatible with RolePermissionTester framework.
# """

# import os
# import re
# import time
# from .test_utils import capture_screenshot

# BASE_URL = "https://clarity-dev.btolims.com"
# PROJECT_NAME = "ED_TEST"
# RETRIES = 2
# SCREENSHOT_DIR = "screenshots"

# os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# def test_sample_rework(page, expected=True):
#     """
#     Checks if role can rework a sample in Clarity LIMS.
#     Accepts a Playwright 'page' object from the test framework.
#     Returns structured JSON result.
#     """
#     print("\n===== TEST: Sample Rework Permission =====")
#     print(f"Project: {PROJECT_NAME}")

#     result = {
#         "test_name": "Sample Rework",
#         "description": "Checks if role can rework a sample in Clarity LIMS",
#         "execution_time": 0.0,
#         "expected": True,
#         "passed": False,
#         "result": "fail",
#         "error": None,
#         "screenshot": None
#     }

#     start_time = time.time()

#     # If expected to fail, only try once (no retries)

#     SAMPLE_ID = "V_251014L0001-4"


#     max_attempts = 1 if expected == False else (RETRIES + 1)



    


#     for attempt in range(1, max_attempts + 1):
#         try:
#             print(f"\nAttempt {attempt}: Navigating to Projects & Samples...")
#             page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
#             page.wait_for_timeout(1000)

#             print(f"Filtering for project '{PROJECT_NAME}'...")
#             filter_box = page.get_by_role("textbox", name="Filter...")
#             filter_box.wait_for(state="visible", timeout=5000)
#             page.wait_for_timeout(500)
#             filter_box.type(PROJECT_NAME, delay=10)
#             page.wait_for_timeout(1000)

#             project_row = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
#             project_row.wait_for(state="visible", timeout=10000)

#             if project_row.count() == 0:
#                 raise Exception(f"Project '{PROJECT_NAME}' not found")
#             print("Project found — clicking on it...")
#             project_row.click()
#             page.wait_for_timeout(1000)

#             # Check if there are samples
#             sample_rows = page.locator("div.project-list-item.x-item-selected")
#             if sample_rows.count() == 0:
#                 raise Exception("No samples found in project")

#             # Deselect all samples first
#             print("Looking for 'Select Group' button...")
#             select_group_btn = page.locator("button.select-group-help", has_text="Select Group")
#             select_group_btn.wait_for(state="visible", timeout=10000)  # wait up to 10 seconds

#             if select_group_btn.count() > 0:
#                 print("Clicking 'Select Group'...")
#                 select_group_btn.click()
#                 page.wait_for_timeout(1000)
#             else:
#                 raise Exception("'Select Group' button not found on the page.")

#             # Click Assign to Workflow
#             assign_btn = page.locator("div.rw-input", has_text="Assign To Workflow")
#             assign_btn.click()
#             page.wait_for_timeout(500)

#             # Select workflow from dropdown
#             workflow_option = page.locator("li.rw-list-option", has_text="Aneuploidy v3.6").first
#             workflow_option.wait_for(state="visible", timeout=10000)  # wait for dropdown item
#             workflow_option.click()
#             page.wait_for_timeout(500)
#             print(f"Selected workflow: {workflow_option.text_content()}")

#             # Confirm workflow assigned
#             workflow_name_locator = page.locator(
#                 "div.workflow-name", has_text="Aneuploidy v3.6"
#             )
#             if workflow_name_locator.count() > 0:
#                 print("Workflow successfully assigned")
#                 result["passed"] = True
#                 result["result"] = "pass"
#                 result["screenshot"], _ = capture_screenshot(page, "sample_rework", "pass")
#             else:
#                 raise Exception("Workflow assignment failed")

#             # Clean up: unassign workflow
#             sample_id = sample_rows.first.get_attribute("data-sample-id")
#             if sample_id:
#                 delete_btn = page.locator(f"div.delete-btn[data-sample-id='{sample_id}']")
#                 if delete_btn.count() > 0:
#                     print("Cleaning up: unassigning workflow...")
#                     delete_btn.first.click()
#                     page.wait_for_timeout(500)


#             # Move to the Aneuploidy v3.6 workflow
#             print("Moving to the Aneuploidy v3.6 workflow...")
#             page.goto(f"{BASE_URL}/clarity/")
#             page.wait_for_timeout(1000)

#             # 1. Click on the step
#             print("Locating workflow step button...")
#             step_button = page.locator("div.sub-work", has_text="Aneuploidy - Plasma Isolation")
#             if step_button.count() == 0:
#                 raise Exception("Workflow step not found")
#             print("Clicking workflow step...")
#             with page.expect_navigation():
#                 step_button.first.click()

#             print("Navigated to workflow queue page.")

#             # Confirm the queue page loaded
#             page.wait_for_selector("div.group-header-label", timeout=20000)
#             print("Page loaded, continuing test...")

#             print("Expanding 'Single Well: Tube' group header...")

#             # Locate the entire group header that contains the label text
#             group = page.locator("div.group-header", has_text="Single Well: Tube")

#             # Wait until it’s visible and attached
#             group.wait_for(state="visible", timeout=10000)

#             # Now find the expander button *inside* that group
#             expander = group.locator(".group-expander-btn")

#             # If it’s already expanded, it won’t have “collapsed” in its class list
#             is_collapsed = expander.get_attribute("class")
#             if "collapsed" in (is_collapsed or ""):
#                 expander.click()
#                 print("Clicked group expander...")
#             else:
#                 print("Group already expanded.")

#             # Give it a moment to load the samples
#             page.wait_for_timeout(1500)

#             # Optional: verify expansion
#             samples_section = group.locator(".samples")
#             page.wait_for_timeout(500)
#             if samples_section.is_visible():
#                 print("Sample group expanded successfully.")
#             else:
#                 print("Warning: Group expansion did not reveal samples.")

#             # 3. Click on a sample
#             print("Selecting sample...")
#             sample = page.locator("span.qtip-value", has_text=SAMPLE_ID)
#             sample.first.wait_for(state="visible", timeout=10000)
#             sample.first.click()

#             # 4. Click Options
#             print("Clicking Options button...")
#             options_button = page.locator("button:has-text('Options')")
#             options_button.wait_for(state="visible", timeout=10000)
#             options_button.click()
#             page.wait_for_timeout(1000)

#             # 5. Check for Move to Next Step button
#             print("Clicking 'Move to the next step' button...")
#             move_button = page.locator("div.menu-item-description", has_text="Move to the next step")
#             move_button.click()
#             page.wait_for_timeout(1000)

#             result["passed"] = True
#             result["result"] = "pass"
#             result["screenshot"], _ = capture_screenshot(page, "sample_rework", "pass")

#             break  # Exit retry loop if successful

#         except Exception as e:
#             result["screenshot"], _ = capture_screenshot(page, "sample_rework", "fail")

#             result["error"] = str(e)
#             result["passed"] = False
#             result["result"] = "fail"

#             print(f"Attempt {attempt} failed: {e}")
#             if attempt <= RETRIES:
#                 print("Retrying in 2 seconds...")
#                 time.sleep(2)
#             else:
#                 print("Max retries reached. Failing test.")
#                 break

#         finally:
#             try:
#                 page.goto(BASE_URL)
#                 print("Returned to main page.")
#             except:
#                 pass

#     end_time = time.time()
#     result["execution_time"] = round(end_time - start_time, 2)
#     print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
#     print(f"Execution time: {result['execution_time']}s")
#     if result["error"]:
#         print(f"Error: {result['error']}")
#     if result["screenshot"]:
#         print(f"Screenshot: {result['screenshot']}")
#     return 

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

            # Perform drag-and-drop
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


                # SAMPLE_ID = "V_251014L0001-4"
            # ROW = "A"
            # COL = "1"

            # print(f"Dragging sample {SAMPLE_ID} to well {ROW}:{COL}...")

            # # --- Step 1: locate source and target ---
            # source = page.locator(f"span.qtip-value[data-qtip='{SAMPLE_ID}']")
            # target = page.locator(f"div.container-well-inner.cw-row-{ROW}.cw-column-{COL}")

            # # Wait until both are visible
            # source.scroll_into_view_if_needed()
            # source.wait_for(state="visible", timeout=40000)
            # target.scroll_into_view_if_needed()
            # target.wait_for(state="visible", timeout=40000)

            # # --- Step 2: get bounding boxes for precise drag ---
            # source_box = source.bounding_box()
            # target_box = target.bounding_box()

            # if not source_box or not target_box:
            #     raise Exception("Cannot determine position of source or target for drag-and-drop.")

            # # --- Step 3: perform manual drag-and-drop ---
            # page.mouse.move(source_box["x"] + source_box["width"]/2, source_box["y"] + source_box["height"]/2)
            # page.mouse.down()
            # page.mouse.move(target_box["x"] + target_box["width"]/2, target_box["y"] + target_box["height"]/2, steps=15)
            # page.mouse.up()

            # # --- Step 4: verify the sample landed in the target well ---
            # target_sample = page.locator(
            #     f"div.container-well-inner.cw-row-{ROW}.cw-column-{COL} span.qtip-value[data-qtip='{SAMPLE_ID}']"
            # )

            # try:
            #     target_sample.wait_for(state="visible", timeout=10000)
            #     print(f"Sample {SAMPLE_ID} successfully dragged to well {ROW}:{COL}.")
            # except:
            #     raise Exception(f"Drag-and-drop failed: Sample {SAMPLE_ID} not found in target well {ROW}:{COL}.")
