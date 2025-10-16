"""
Test Module: Delete Project Permission
======================================
Checks if a user with the proper role can delete a new project in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "Emil Project Test"
ACCOUNT_NAME = "Administrative Lab"
CLIENT_NAME = "Emil Test"
RETRIES = 2  # Number of retries on failure
SCREENSHOT_DIR = "screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_delete_project(page, expected=True):
    """
    Checks if user can delete a new project in Clarity LIMS
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Delete Project Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Delete Project",
        "description": "Checks if user can delete a new project in Clarity LIMS",
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

            print("Waiting for project row to appear...")
            project_row_locator = page.locator(f"div.project-list-item:has(div[data-qtip='{PROJECT_NAME}'])").first
            project_row_locator.wait_for(state="visible", timeout=10000)

            if project_row_locator.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found")
            else:
                print("Project found — clicking on it...")
                project_row_locator.click()

            print("Clicking Delete button...")
            delete_button = page.locator("#project-button-bar-delete-button-btnEl")
            delete_button.wait_for(state="visible", timeout=5000)
            delete_button.click()

            print("Waiting for confirmation dialog...")
            confirm_window = page.locator("div.x-window:has(span:text('Confirm Delete Project'))")
            confirm_window.wait_for(state="visible", timeout=5000)

            print("Checking confirmation message...")
            message_locator = confirm_window.locator(".isis-message-box-text")
            message_locator.wait_for(state="visible", timeout=3000)
            message_text = message_locator.inner_text().strip()
            print(f"Dialog text: {message_text}")

            expected_text_fragment = f"Are you sure you want to delete the project '{PROJECT_NAME}'"
            if expected_text_fragment not in message_text:
                raise Exception(f"Unexpected confirmation message: {message_text}")

            print("Clicking 'Delete Project' button in dialog...")
            delete_confirm_button = confirm_window.get_by_role("button", name=re.compile("Delete Project", re.I))
            delete_confirm_button.wait_for(state="visible", timeout=3000)
            delete_confirm_button.click()

            if project_row_locator.count() == 0:
                print("Project deleted successfully")
                result["passed"] = True
                result["result"] = "pass"
                break

        except Exception as e:
            timestamp = int(time.time())
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"delete_project_{timestamp}.png")
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