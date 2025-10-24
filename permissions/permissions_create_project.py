"""
Test Module: Create Project Permission
======================================
Checks if a user with the proper role can create a new project in Clarity LIMS.
Compatible with RolePermissionTester framework.
\n+Test Flow:
1. Test attempts to create a project with the current role
2. If creation succeeds, test passes
3. If creation fails, test fails
4. Cleanup: If project was created, add System Admin (BTO) role, delete the project, then remove System Admin (BTO)
"""

import os
import re
import time
from .test_utils import capture_screenshot
from change_role import modify_user_role, get_lims_connection

BASE_URL = "https://clarity-dev.btolims.com"
CLIENT_NAME = "Emil Test"
RETRIES = 2  # Number of retries on failure
SCREENSHOT_DIR = "test_results/screenshots"
PROJECT_NAME = "Emil Project Test"
ACCOUNT_NAME = "Administrative Lab"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_create_project(page, expected=True):
    """
    Checks if user can create a new project in Clarity LIMS
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Create Project Permission =====")

    result = {
        "test_name": "Create Project",
        "description": "Checks if user can create a new project in Clarity LIMS",
        "execution_time": 0.0,
        "expected": expected,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None
    }

    start_time = time.time()
    
    # If expected to fail, only try once (no retries)
    max_attempts = 1 if expected == False else (RETRIES + 1)

    project_created = False

    try:
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"\nAttempt {attempt}: Navigating to Projects & Samples...")
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
                filter_box = page.get_by_role("textbox", name="Filter...")
                filter_box.wait_for(state="visible", timeout=5000)
                page.wait_for_timeout(500)
                filter_box.type(PROJECT_NAME, delay=10)
                project_row_locator = page.locator(f"div.project-list-item-headline-title[data-qtip='{PROJECT_NAME}']").first
                project_row_locator.wait_for(state="visible", timeout=10000)

                if project_row_locator.count() == 0:
                    raise Exception(f"Project '{PROJECT_NAME}' not found after creation")

                print("Project created successfully!")
                project_created = True
                result["passed"] = True
                result["result"] = "pass"
                result["screenshot"], _ = capture_screenshot(page, "create_project", "pass")
                break

            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                result["error"] = str(e)
                result["passed"] = False
                result["result"] = "fail"

                if attempt < max_attempts:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print("Max retries reached. Failing test.")
                    # Take screenshot only once at the end
                    result["screenshot"], _ = capture_screenshot(page, "create_project", "fail")
                    break

            finally:
                try:
                    page.goto(BASE_URL)
                except:
                    pass

    except Exception as e:
        print(f"Test execution failed: {e}")
        result["error"] = str(e)
        result["passed"] = False
        result["result"] = "fail"
        if not result.get("screenshot"):
            result["screenshot"], _ = capture_screenshot(page, "create_project", "fail")

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    # Cleanup: if project was created, add System Admin to delete it, then remove the role
    if project_created:
        print("\n--- CLEANUP: Adding System Admin (BTO) role to delete created project ---")
        try:
            lims, username = get_lims_connection()
            user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="add")
            print(f"Current roles for {username} after adding System Admin (BTO) for cleanup:")
            for r in user.roles:
                print(f"  - {r.name}")

            print("Navigating to Projects & Samples for cleanup...")
            page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()
            page.wait_for_timeout(1000)

            print(f"Filtering for project '{PROJECT_NAME}'...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            page.wait_for_timeout(500)
            filter_box.fill("")
            filter_box.type(PROJECT_NAME, delay=10)

            print("Waiting for project row to appear...")
            project_row_locator = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row_locator.wait_for(state="visible", timeout=10000)

            if project_row_locator.count() > 0:
                print("Project found — opening details for deletion...")
                project_row_locator.click()

                print("Clicking Delete button...")
                delete_button = page.locator("#project-button-bar-delete-button-btnEl")
                delete_button.wait_for(state="visible", timeout=5000)
                delete_button.click()

                print("Waiting for confirmation dialog...")
                confirm_window = page.locator("div.x-window:has(span:text('Confirm Delete Project'))")
                confirm_window.wait_for(state="visible", timeout=5000)

                print("Clicking 'Delete Project' button in dialog...")
                delete_confirm_button = confirm_window.get_by_role("button", name=re.compile("Delete Project", re.I))
                delete_confirm_button.wait_for(state="visible", timeout=3000)
                delete_confirm_button.click()

                page.wait_for_timeout(1000)
                project_row_check = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])")
                if project_row_check.count() == 0:
                    print("Created project cleaned up successfully.")
                else:
                    print("Warning: Project still present after deletion attempt.")

            # Remove System Admin role after cleanup
            user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")
            print(f"Current roles for {username} after removing System Admin (BTO) after cleanup:")
            for r in user.roles:
                print(f"  - {r.name}")

        except Exception as cleanup_error:
            print(f"Cleanup encountered an issue: {cleanup_error}")

    print(f"\n===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    print(f"Execution time: {result['execution_time']}s")
    if result["error"]:
        print(f"Error: {result['error']}")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")
    return result