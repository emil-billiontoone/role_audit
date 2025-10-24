"""
Test Module: Delete Project Permission
======================================
Checks if a user with the proper role can delete a project in Clarity LIMS.
Compatible with RolePermissionTester framework.

Test Flow:
1. Add System Admin (BTO) role to the test user
2. Create "Emil Project Test" as a test project
3. Remove System Admin (BTO) role to test with the original role
4. Attempt to delete the test project
5. If deletion fails, add System Admin (BTO) back and clean up
6. If deletion succeeds, test passes (cleanup already done)
"""

import re
import time
from .test_utils import capture_screenshot
from change_role import modify_user_role, get_lims_connection

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "Emil Project Test"
ACCOUNT_NAME = "Administrative Lab"
CLIENT_NAME = "Emil Test"
RETRIES = 1  # Reduced retries for faster test

def test_delete_project(page, expected=True):
    """
    Checks if role can delete a project in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Delete Project Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Delete Project",
        "description": "Checks if role can delete a project in Clarity LIMS",
        "execution_time": 0.0,
        "expected": expected,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    start_time = time.time()
    max_attempts = 1 if not expected else (RETRIES + 1)

    project_created = False

    try:
        # Step 1: Add System Admin (BTO) role to create test project
        print("\n--- SETUP: Adding System Admin (BTO) role to create test project ---")
        lims, username = get_lims_connection()
        user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
        print(f"Current roles for {username} after adding System Admin (BTO):")
        for r in user.roles:
            print(f"  - {r.name}")

        # Step 2: Create the test project
        print(f"\n--- SETUP: Creating test project '{PROJECT_NAME}' ---")
        page.goto(f"{BASE_URL}/clarity/samples")
        page.wait_for_timeout(2000)

        print(f"\nNavigating to Projects & Samples...")
        page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
        page.wait_for_timeout(1000)

        print(f"Typing project name '{PROJECT_NAME}' in filter box...")
        filter_box = page.get_by_role("textbox", name="Filter...")
        filter_box.wait_for(state="visible", timeout=5000)
        page.wait_for_timeout(500)
        filter_box.type(PROJECT_NAME, delay=10)

        print("Clicking 'NEW PROJECT' button...")
        new_project_btn = page.locator("button", has_text="NEW PROJECT")
        if new_project_btn.count() == 0 or not new_project_btn.is_visible():
            raise Exception("NEW PROJECT button not visible — permission denied.")
        new_project_btn.click()

        print("Filling in project form...")
        page.get_by_role("textbox", name="Enter Project Name").fill(PROJECT_NAME)

        print(f"Selecting account '{ACCOUNT_NAME}'...")
        account_input = page.locator("input[placeholder='Choose an account']")
        account_input.click()
        page.wait_for_selector(".x-boundlist-item", state="visible", timeout=5000)
        page.locator(".x-boundlist-item", has_text=ACCOUNT_NAME).click()

        print(f"Selecting client '{CLIENT_NAME}'...")
        trigger_button = page.locator("#ext-gen1100")
        trigger_button.click()
        client_input = page.locator("input[placeholder='Choose a client']")
        client_input.wait_for(state="visible", timeout=10000)
        for _ in range(20):
            if client_input.is_enabled():
                break
            page.wait_for_timeout(200)
        client_input.type(CLIENT_NAME, delay=10)
        client_input.press("Enter")

        print("Setting priority to 'Standard' and saving project...")
        priority_trigger = page.locator("#ext-gen1106")
        priority_trigger.click()
        page.wait_for_timeout(200)
        page.get_by_text("Standard").click()
        page.get_by_role("button", name="Save").click()

        print("Verifying project creation...")
        page.goto(f"{BASE_URL}/clarity/samples")
        page.wait_for_timeout(1000)
        filter_box = page.get_by_role("textbox", name="Filter...")
        filter_box.wait_for(state="visible", timeout=5000)
        page.wait_for_timeout(500)
        filter_box.type(PROJECT_NAME, delay=10)
        project_row_locator = page.locator(f"div.project-list-item-headline-title[data-qtip='{PROJECT_NAME}']").first
        project_row_locator.wait_for(state="visible", timeout=10000)

        if project_row_locator.count() == 0:
            raise Exception(f"Test project '{PROJECT_NAME}' was not created successfully.")
        
        print(f"Test project '{PROJECT_NAME}' created successfully.")
        project_created = True

        # Step 3: Remove System Admin (BTO) role to test with original role
        print("\n--- SETUP: Removing System Admin (BTO) role to test deletion permission ---")
        user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
        print(f"Current roles for {username} after removing System Admin (BTO):")
        for r in user.roles:
            print(f"  - {r.name}")

        # Step 4: Test deletion with the original role
        print(f"\n--- TEST: Attempting to delete project '{PROJECT_NAME}' with current role ---")
        
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"\nAttempt {attempt}: Navigating to Projects & Samples...")
                page.goto(f"{BASE_URL}/clarity/samples")
                page.wait_for_timeout(1000)
                page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
                page.wait_for_timeout(1000)

                print(f"Filtering for project '{PROJECT_NAME}'...")
                filter_box = page.get_by_role("textbox", name="Filter...")
                filter_box.wait_for(state="visible", timeout=5000)
                page.wait_for_timeout(500)
                filter_box.type(PROJECT_NAME, delay=10)

                print("Waiting for project row to appear...")
                project_row_locator = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
                project_row_locator.wait_for(state="visible", timeout=10000)

                if project_row_locator.count() == 0:
                    raise Exception(f"Project '{PROJECT_NAME}' not found")
                
                print("Project found — clicking on it...")
                project_row_locator.click()
                page.wait_for_timeout(1000)

                print("Checking for Delete button...")
                delete_button = page.locator("#project-button-bar-delete-button-btnEl")
                
                # Check if delete button is visible/enabled
                if delete_button.count() == 0 or not delete_button.is_visible():
                    raise Exception("Delete button not visible — permission denied.")
                
                print("Clicking Delete button...")
                delete_button.click()

                print("Waiting for confirmation dialog...")
                confirm_window = page.locator("div.x-window:has(span:text('Confirm Delete Project'))")
                confirm_window.wait_for(state="visible", timeout=5000)

                print("Clicking 'Delete Project' button in dialog...")
                delete_confirm_button = confirm_window.get_by_role("button", name=re.compile("Delete Project", re.I))
                delete_confirm_button.wait_for(state="visible", timeout=3000)
                delete_confirm_button.click()

                # Wait for deletion to complete
                page.wait_for_timeout(2000)

                # Verify project is deleted
                print("Verifying deletion...")
                page.goto(f"{BASE_URL}/clarity/samples")
                page.wait_for_timeout(1000)
                filter_box = page.get_by_role("textbox", name="Filter...")
                filter_box.wait_for(state="visible", timeout=5000)
                page.wait_for_timeout(500)
                filter_box.type(PROJECT_NAME, delay=10)
                page.wait_for_timeout(1000)

                project_row_check = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])")
                if project_row_check.count() == 0:
                    print(f"'{PROJECT_NAME}' is deleted — permission confirmed.")
                    result["passed"] = True
                    result["result"] = "pass"
                    project_created = False  # Mark as cleaned up
                    
                    # Take screenshot showing project is gone
                    result["screenshot"], _ = capture_screenshot(page, "delete_project", "pass")

                    page.goto(BASE_URL)
                    page.wait_for_timeout(1000)
                    break
                else:
                    raise Exception(f"'{PROJECT_NAME}' is still visible after deletion attempt — permission denied.")

            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                result["error"] = str(e)
                result["passed"] = False
                result["result"] = "fail"

                if attempt < max_attempts:
                    print("Retrying in 2 seconds...")
                    page.goto(BASE_URL)
                    page.wait_for_timeout(1000)
                    time.sleep(2)
                else:
                    print("Max retries reached. Failing test.")
                    # Take screenshot only once at the end - showing delete button missing or project still there
                    result["screenshot"], _ = capture_screenshot(page, "delete_project", "fail")
                    break

    except Exception as e:
        print(f"Setup or test execution failed: {e}")
        result["error"] = str(e)
        result["passed"] = False
        result["result"] = "fail"
        result["screenshot"], _ = capture_screenshot(page, "delete_project", "fail")

    finally:
        # Step 5: Cleanup - If test project still exists, add System Admin role back and delete
        if project_created:
            print("\n--- CLEANUP: Test project still exists, adding System Admin (BTO) role to clean up ---")
            try:
                lims, username = get_lims_connection()
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
                print(f"Current roles for {username} after adding System Admin (BTO) for cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

                print(f"Deleting test project '{PROJECT_NAME}' with System Admin privileges...")
                page.goto(f"{BASE_URL}/clarity/samples")
                page.wait_for_timeout(1000)
                page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
                page.wait_for_timeout(1000)

                filter_box = page.get_by_role("textbox", name="Filter...")
                filter_box.wait_for(state="visible", timeout=5000)
                page.wait_for_timeout(500)
                filter_box.type(PROJECT_NAME, delay=10)

                project_row_locator = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
                project_row_locator.wait_for(state="visible", timeout=10000)

                if project_row_locator.count() > 0:
                    project_row_locator.click()
                    page.wait_for_timeout(1000)

                    delete_button = page.locator("#project-button-bar-delete-button-btnEl")
                    delete_button.wait_for(state="visible", timeout=5000)
                    delete_button.click()

                    confirm_window = page.locator("div.x-window:has(span:text('Confirm Delete Project'))")
                    confirm_window.wait_for(state="visible", timeout=5000)

                    delete_confirm_button = confirm_window.get_by_role("button", name=re.compile("Delete Project", re.I))
                    delete_confirm_button.wait_for(state="visible", timeout=3000)
                    delete_confirm_button.click()

                    page.wait_for_timeout(2000)
                    print(f"Test project '{PROJECT_NAME}' cleaned up successfully.")
                
                # Remove System Admin role after cleanup
                user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
                print(f"Current roles for {username} after removing System Admin (BTO) after cleanup:")
                for r in user.roles:
                    print(f"  - {r.name}")

            except Exception as cleanup_error:
                print(f"Cleanup encountered an issue: {cleanup_error}")
        else:
            print("\n--- CLEANUP: Test project already deleted, no cleanup needed ---")
        
        # ALWAYS remove System Admin role at the end, regardless of test outcome
        print("\n--- FINAL CLEANUP: Removing System Admin (BTO) role ---")
        try:
            lims, username = get_lims_connection()
            user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
            print(f"Removed System Admin (BTO) role")
            print(f"Current roles for {username}:")
            for r in user.roles:
                print(f"  - {r.name}")
        except Exception as e:
            print(f"Warning: Could not remove System Admin (BTO) role: {e}")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    if result["error"]:
        print(f"{result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result