"""
Test Module: Review Escalated Samples Permission
==================================================
Checks if a user with the proper role can review escalated samples in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time
from datetime import datetime
from .test_utils import capture_screenshot
from change_role import get_lims_connection, modify_user_role

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "ED_TEST"
RETRIES = 0
SCREENSHOT_DIR = "test_results/screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# --- Helper to select an option from a react-widgets multiselect by widget id ---
def select_multiselect_option_by_id(page, widget_id, option_text, timeout=8000):
    """
    Open multiselect #<widget_id>, wait for its listbox to be visible,
    then click the li inside that listbox that matches option_text.
    """
    listbox_id = f"#{widget_id}__listbox"
    wrapper = page.locator(f"#{widget_id} .rw-multiselect-wrapper").first

    print(f"Opening multiselect {widget_id}...")
    wrapper.click()
    try:
        page.wait_for_selector(listbox_id, state="visible", timeout=timeout)
    except Exception as e:
        print(f"Timeout waiting for listbox {listbox_id} to be visible: {e}")
        return False

    print(f"Selecting option '{option_text}' inside {listbox_id}...")
    # Use a scoped locator so we only match items inside this listbox
    option = page.locator(f"{listbox_id} >> text=\"{option_text}\"").first
    try:
        option.click()
        page.wait_for_timeout(200)  # let UI settle
        print(f"Selected '{option_text}' in {widget_id}.")
        return True
    except Exception as e:
        print(f"Failed to click option '{option_text}' in {widget_id}: {e}")
        return False



def test_review_escalated_samples(page, expected=True):
    """
    Checks if role can review escalated samples in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Review Escalated Samples Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Review Escalated Samples",
        "description": "Checks if role can review escalated samples in Clarity LIMS",
        "execution_time": 0.0,
        "expected": expected,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    SAMPLE_ID = "V_251014L0001-5"
    max_attempts = 1 if expected is False else (RETRIES + 1)
    start_time = time.time()

    for attempt in range(1, max_attempts + 1):
        try:

            # Add System Admin (BTO) role to user to create test environment
            print("Adding System Admin (BTO) role to user to create test environment...")
            lims, username = get_lims_connection()
            user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
            print(f"Current roles for {username} after adding System Admin (BTO) role:")
            for r in user.roles:
                print(f"  - {r.name}")

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

            # === Begin review escalated samples steps ===
            print("\n--- Beginning review escalated samples process ---")
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

            print("Selecting same sample for review escalated samples verification...")
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

            print("Selecting same sample for review escalated samples verification...")
            page.get_by_text(SAMPLE_ID).click()
            page.wait_for_timeout(500)

            print("Adding to Ice Bucket...")
            page.locator("#ice-bucket-add-47269198").click()
            page.get_by_role("button", name="View Ice Bucket »").click()
            page.get_by_role("button", name="Begin Work »").click()
            print("Sample review escalated samples initiated successfully.")


            from playwright.sync_api import expect

            SAMPLE_ID = "V_251014L0001-5"
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
            for _ in range(60):  # wait up to ~20 seconds
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
            for _ in range(60):  # ~10 seconds if 0.5s sleep
                if "in-use-well" in target.get_attribute("class"):
                    break
                time.sleep(0.5)
            else:
                raise Exception("Drag-and-drop did not complete successfully (well not marked in-use).")

            print(f"Sample {SAMPLE_ID} successfully dragged to output well {ROW}:{COL}.")

            # Click 'Record Details »' to finalize
            print("Clicking 'Record Details »' button to confirm review escalated samples placement...")
            page.get_by_role("button", name="Record Details »").click()
            page.wait_for_timeout(1000)
            print("Sample successfully recorded in workflow.")

            print("Filling in metadata fields before finalizing review escalated samples...")

            print("Selecting 'NA, Lot: NA' from multiselect fields...")

            if not select_multiselect_option_by_id(page, "rw_1", "NA, Lot: NA"):
                # capture screenshot for debugging and raise so outer retry logic can handle it
                ss, _ = capture_screenshot(page, "multiselect_rw1_fail", "fail")
                print(f"Screenshot captured: {ss}")
                raise Exception("Could not select 'NA, Lot: NA' in rw_1")

            if not select_multiselect_option_by_id(page, "rw_2", "NA, Lot: NA"):
                ss, _ = capture_screenshot(page, "multiselect_rw2_fail", "fail")
                print(f"Screenshot captured: {ss}")
                raise Exception("Could not select 'NA, Lot: NA' in rw_2")

            # --- Simpler dropdown (fallback handling) ---
            print("Selecting 'NA' from picker #ext-gen1136...")
            try:
                page.locator("#ext-gen1136").click()
                page.wait_for_timeout(200)
                # Try to click exact option first
                page.get_by_role("option", name="NA", exact=True).click()
                print("Selected 'NA' from #ext-gen1136.")
            except Exception:
                # fallback: click visible list item text=NA
                try:
                    page.locator("ul.rw-list >> text=NA").first.click()
                    print("Fallback: clicked visible 'NA' option.")
                except Exception as e:
                    ss, _ = capture_screenshot(page, "ext-gen1136_fail", "fail")
                    print(f"Failed to select 'NA' from #ext-gen1136: {e}. Screenshot: {ss}")
                    raise

            # --- Fill textboxes using fill() (more reliable than typing) ---
            print("Filling operator and instrument textboxes...")
            textbox_fields = [
                "BSC Operator(s)",
                "Loading Operator(s)",
                "Instrument",
                "Workstation",
                "Verifying Operator(s)",
                "Comments"
            ]

            for field in textbox_fields:
                try:
                    textbox = page.get_by_role("textbox", name=field)
                    textbox.wait_for(state="visible", timeout=5000)
                    textbox.fill("N/A")
                    print(f"Filled '{field}' with 'N/A'.")
                except Exception as e:
                    print(f"Warning: could not fill textbox '{field}': {e}")

            print("All text fields populated successfully.")

            # Proceed to next step
            print("Clicking 'Next Steps »' to continue...")
            try: 
                page.get_by_role("button", name="Next Steps »").click()
            except Exception as e:
                print(f"Failed to navigate to Work Complete page: {e}")
                raise Exception(f"Failed to navigate to Work Complete page: {e}")

            # Select workflow and confirm review escalated samples
            print("Selecting workflow and verifying review escalated samples...")

            print("Waiting for page mask to clear before removing workflow...")
            for _ in range(60):  # wait up to ~20 seconds
                masks = page.locator("div.x-mask")
                if masks.count() == 0 or not masks.first.is_visible():
                    break
                time.sleep(0.5)
            else:
                raise Exception("Timed out waiting for ExtJS mask to disappear.")

            try:
                # Click the workflow in the tree view
                workflow = page.locator("#treeview-1076").get_by_text("Aneuploidy - Automated cfDNA").first
                workflow.click()
                page.wait_for_timeout(500)  # small pause for UI

                # Click the currently selected workflow to open the Select2 dropdown
                workflow.click()  # sometimes you need a second click to open dropdown

                # Wait until the dropdown is actually visible and not display:none
                dropdown = page.locator("div.select2-drop:visible")
                dropdown.wait_for(state="visible", timeout=10000)

                # Find the option inside the visible dropdown
                option = dropdown.locator("div.iconcombobox-item", has_text="Request manager review")
                option.wait_for(state="visible", timeout=5000)

                # Click it
                option.first.click()
                page.wait_for_timeout(500)
                print("Selected 'Request manager review'")
            except Exception as e:
                print(f"Failed to select workflow and verify request manager review: {e}")
                raise Exception(f"Failed to select workflow and verify request manager review: {e}")

            # 1. Open Select2 dropdown and select "Emil Test"
            # Select manager from second dropdown
            try:
                print("Selecting manager 'Emil Test' from dropdown...")
                select2 = page.locator("div.select2-container:has(span:text('Select Manager'))")
                select2.click()

                # Wait for the visible Select2 dropdown and the list items
                manager_dropdown = page.locator("div.select2-drop:visible")
                manager_dropdown.wait_for(state="visible", timeout=10000)

                # Wait specifically for the Emil Test option
                manager_option = manager_dropdown.locator("li.select2-result", has_text="Emil Test").first
                manager_option.wait_for(state="visible", timeout=10000)
                manager_option.click()
                print("Selected 'Emil Test' successfully.")

            except Exception as e:
                raise Exception(f"Failed to select manager 'Emil Test': {e}")

            # 2. Type comment in escalation textarea
            comment_box = page.locator("textarea[name='escalationComment']")
            comment_box.type("Test", delay=10)
            print("Entered comment 'Test'")

            # 3. Click Finish Step
            page.locator("button:has-text('Finish Step »')").click()
            page.wait_for_timeout(1000)  # wait for page update
            print("Clicked Finish Step »")

            # 4. Check homepage for manager notification
            print("Checking Lab View for manager notification...")
            page.get_by_role("link", name=re.compile("Lab View", re.I)).click()
            page.wait_for_timeout(1000)

            print("Removing System Admin (BTO) role to user to test role...")
            user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
            print(f"Current roles for {username} after removing System Admin (BTO) role to test role:")
            for r in user.roles:
                print(f"  - {r.name}")

            page.wait_for_timeout(2000)
            notification = page.locator("div.manager-notification-entry:has(strong:text('Emil Test'))")
            if notification.count() == 0:
                raise Exception("Notification from Emil Test not found on homepage")

            print("Found notification — clicking to open review page...")
            notification.click()

            # Give the system time to load the review page
            print("Waiting for review page to load...")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)  # small static wait, optional

            # Now wait for the escalation review comment box
            print("Waiting for escalation review comment box to appear...")
            review_box = page.locator("textarea[name='escalationReviewComment']")
            review_box.wait_for(state="visible", timeout=60000)  # wait up to 60s

            if review_box.count() == 0:
                raise Exception("User does NOT have permission to review escalated samples")
            else:
                result["passed"] = True
                result["result"] = "pass"
                result["screenshot"], _ = capture_screenshot(page, "review_escalated_samples", "pass")
                print("Test PASSED — user has permission to review escalated samples.")


            #Cleanup: Remove sample from workflow
            print("Cleaning up: Removing sample from workflow...")

            page.get_by_role("link", name="Select this sample's next step").click()
            page.get_by_role("listitem").filter(has_text="Remove from workflow").click()
            page.get_by_role("button", name="Apply").click()
            page.get_by_role("button", name="Finish Review »").click()


            page.wait_for_timeout(1000)  # wait for page update
            print("Clicked Finish Review »")

            # Wait for the confirmation popup to appear
            confirmation_popup = page.locator("div.x-window.x-message-box:has-text('Are you sure you want to remove')")
            confirmation_popup.wait_for(state="visible", timeout=5000)
            print("Confirmation popup appeared")

            # Click the OK button
            ok_button = confirmation_popup.locator("button:has-text('OK')")
            ok_button.click()
            print("Clicked OK on confirmation popup")

            # Wait for the "Executing Custom Program" message box to appear first (optional)
            execution_popup = page.locator("div.x-window.x-message-box:has-text('Executing Custom Program')")
            execution_popup.wait_for(state="visible", timeout=5000)
            print("Execution popup appeared")

            # Wait until it disappears
            execution_popup.wait_for(state="hidden", timeout=60000)  # adjust timeout if needed
            print("Execution popup has disappeared, proceeding with next steps")

            break  # exit retry loop

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            result["screenshot"], _ = capture_screenshot(page, "review_escalated_samples", "fail")

            if attempt < max_attempts:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached. Failing test.")
                break

        finally:
            # Add System Admin (BTO) role to user to clean up test environment
            user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
            print(f"Current roles for {username} after adding System Admin (BTO) role to clean up test environment:")
            for r in user.roles:
                print(f"  - {r.name}")

            print("Performing cleanup — aborting test step and returning to Lab View...")
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
                    # Only get sample rows that have an active workflow delete button
                    sample_rows = page.locator("div.sample-row:has(div.delete-btn)")
                    if sample_rows.count() == 0:
                        break

                    sample = sample_rows.first
                    sample_id = sample.locator(".sample-udf-icon").get_attribute("data-sample-id")
                    workflow_name = sample.locator(".workflow-name").inner_text()
                    print(f"Removing sample ID {sample_id} from workflow '{workflow_name}'...")

                    delete_btn = sample.locator(".delete-btn")
                    # Wait for any overlay
                    page.locator("div.x-mask-full-page").wait_for(state="hidden", timeout=10000)
                    
                    # Click delete
                    delete_btn.click()

                    # Wait until the workflow name for this sample is gone
                    workflow_locator = page.locator(f"div.sample-row[data-sample-id='{sample_id}'] div.workflow-name")
                    try:
                        workflow_locator.wait_for(state="detached", timeout=10000)
                    except:
                        print(f"Warning: workflow for sample {sample_id} did not disappear within timeout")

                    removed_count += 1
                    page.wait_for_timeout(500)

                print(f"Removed {removed_count} sample(s) from workflows.")
                # removed_count = 0
                # while True:
                #     sample_rows = page.locator("div.sample-row:has(div.workflow-name)")
                #     if sample_rows.count() == 0:
                #         break

                #     sample = sample_rows.first
                #     sample_id = sample.locator(".sample-udf-icon").get_attribute("data-sample-id")
                #     workflow_name = sample.locator(".workflow-name").inner_text()
                #     print(f"Removing sample ID {sample_id} from workflow '{workflow_name}'...")

                #     delete_btn = page.locator(f"div.delete-btn[data-sample-id='{sample_id}']")
                #     if delete_btn.count() == 0:
                #         print(f"No delete button found for sample ID {sample_id}, skipping.")
                #         # Remove this sample from DOM consideration if needed
                #         page.evaluate("el => el.remove()", sample)
                #         continue

                #     # Wait for any page overlay to disappear before clicking
                #     page.locator("div.x-mask-full-page").wait_for(state="hidden", timeout=10000)

                #     # Click delete
                #     delete_btn.first.click()

                #     # Wait until the workflow name for this sample is gone
                #     workflow_locator = page.locator(f"div.sample-row[data-sample-id='{sample_id}'] div.workflow-name")
                #     try:
                #         workflow_locator.wait_for(state="detached", timeout=10000)
                #     except:
                #         print(f"Warning: workflow for sample {sample_id} did not disappear within timeout")

                #     removed_count += 1
                #     page.wait_for_timeout(500)  # optional small buffer

                # print(f"Removed {removed_count} sample(s) from workflows.")

                # Verification: ensure no samples remain assigned
                remaining_samples = page.locator("div.sample-row:has(div.workflow-name)").count()
                if remaining_samples == 0:
                    print("All samples successfully removed from workflows.")
                else:
                    raise Exception(f"{remaining_samples} sample(s) still assigned to workflows after removal.")

                # Verification: ensure no samples remain assigned
                remaining_samples = page.locator("div.sample-row:has(div.workflow-name)").count()
                if remaining_samples == 0:
                    print("All samples successfully removed from workflows.")
                else:
                    raise Exception(f"{remaining_samples} sample(s) still assigned to workflows after removal.")
                     # Exit cleanup loop on success

                # Remove System Admin (BTO) role from user to clean up test environment
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
                print(f"Current roles for {username} after removing System Admin (BTO) role after cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

            except Exception as e:
                print(f"Cleanup encountered an issue: {e}")

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