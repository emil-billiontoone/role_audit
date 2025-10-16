"""
Test Module: Create Project Permission
======================================
Checks if a user with the proper role can create a new project in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time
from datetime import datetime

BASE_URL = "https://clarity-dev.btolims.com"
PROJECT_NAME = "Emil Project Test"
ACCOUNT_NAME = "Administrative Lab"
CLIENT_NAME = "Emil Test"
RETRIES = 2  # Number of retries on failure
SCREENSHOT_DIR = "screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_create_project(page, expected=True):
    """
    Checks if user can create a new project in Clarity LIMS
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Create Project Permission =====")
    print(f"Project: {PROJECT_NAME}")

    result = {
        "test_name": "Create Project",
        "description": "Checks if user can create a new project in Clarity LIMS",
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

            print(f"Typing project name '{PROJECT_NAME}' in filter box...")
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            page.wait_for_timeout(500)
            filter_box.type(PROJECT_NAME, delay=100)

            print("Clicking 'NEW PROJECT' button...")
            new_project_btn = page.locator("button", has_text="NEW PROJECT")
            new_project_btn.wait_for(state="visible", timeout=5000)
            if new_project_btn.count() == 0:
                raise Exception("NEW PROJECT button not found")
            new_project_btn.click()

            print("Filling in project form...")
            page.get_by_role("textbox", name="Enter Project Name").fill(PROJECT_NAME)

            print(f"Selecting account '{ACCOUNT_NAME}'...")
            account_input = page.locator("input[placeholder='Choose an account']")
            account_input.click()
            page.wait_for_selector(".x-boundlist-item", state="visible", timeout=5000)
            page.locator(".x-boundlist-item", has_text=ACCOUNT_NAME).click()

            print(f"Selecting client '{CLIENT_NAME}'...")
            trigger_button = page.locator("#ext-gen1100")  # dropdown trigger
            trigger_button.click()
            client_input = page.locator("input[placeholder='Choose a client']")
            client_input.wait_for(state="visible", timeout=10000)
            for _ in range(20):
                if client_input.is_enabled():
                    break
                page.wait_for_timeout(200)
            client_input.type(CLIENT_NAME, delay=100)
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
            filter_box.type(PROJECT_NAME, delay=100)
            project_row_locator = page.locator(f"div.project-list-item-headline-title[data-qtip='{PROJECT_NAME}']").first
            project_row_locator.wait_for(state="visible", timeout=10000)

            if project_row_locator.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found after creation")
            else:
                print("Project created successfully!")

            result["passed"] = True
            result["result"] = "pass"
            break

        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # readable
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"create_project_{timestamp}.png")
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