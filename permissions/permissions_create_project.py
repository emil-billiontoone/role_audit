"""
Test Module: Create Project Permission
======================================
Checks if a user with the proper role can create a new project in Clarity LIMS.
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


def test_create_project(page):
    """
    Checks if user can create a new project in Clarity LIMS
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
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

    for attempt in range(1, RETRIES + 2):
        try:

            # Go to Projects & Samples
            page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()

            # Type in filter box
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            page.wait_for_timeout(500)  # wait half a second before typing
            filter_box.type(PROJECT_NAME, delay=100)

            # # Wait for the project row to appear
            # project_row_selector = f"div.project-list-item-headline-title[data-qtip='{PROJECT_NAME}']"
            # page.wait_for_selector(project_row_selector, state="visible", timeout=10000)

            # Now click NEW PROJECT button
            new_project_btn = page.locator("button", has_text="NEW PROJECT")
            new_project_btn.wait_for(state="visible", timeout=5000)


            new_project_btn_count = page.locator("button", has_text="NEW PROJECT").count()
            if new_project_btn_count == 0:
                raise Exception("NEW PROJECT button not found")

            # Click New Project
            new_project_btn.click()

            # Fill project form
            page.get_by_role("textbox", name="Enter Project Name").fill(PROJECT_NAME)


            # Click the "Choose an account" input
            account_input = page.locator("input[placeholder='Choose an account']")
            account_input.click()

            # Wait for the dropdown to appear
            page.wait_for_selector(".x-boundlist-item", state="visible", timeout=5000)

            # Click the correct item in the dropdown
            page.locator(".x-boundlist-item", has_text="Administrative Lab").click()
            

            # Click the dropdown trigger to enable input
            trigger_button = page.locator("#ext-gen1100")  # the div with class x-form-arrow-trigger
            trigger_button.click()

            client_input = page.locator("input[placeholder='Choose a client']")
            client_input.wait_for(state="visible", timeout=10000)

            # Wait until input is enabled
            client_input = page.locator("input[placeholder='Choose a client']")
            client_input.wait_for(state="visible", timeout=10000)

            for _ in range(20):  # retry for ~4 seconds
                if client_input.is_enabled():
                    break
                page.wait_for_timeout(200)

            client_input.type("Emil Test", delay=100)

            page.locator(".x-boundlist-item", has_text="Emil Test").click()

            # Click standard drop down
            priority_trigger = page.locator("#ext-gen1106")
            priority_trigger.click()
            page.wait_for_timeout(200)  # small delay to let dropdown appear

            page.get_by_text("Standard").click()  # Priority
            page.get_by_role("button", name="Save").click()

            # Verify project exists
            page.goto(f"{BASE_URL}/clarity/samples")


            # Type in filter box
            filter_box = page.get_by_role("textbox", name="Filter...")
            filter_box.wait_for(state="visible", timeout=5000)
            page.wait_for_timeout(500)  # wait half a second before typing
            filter_box.type(PROJECT_NAME, delay=100)

            # Wait for the project row to appear
            project_row_locator = page.locator(f"div.project-list-item-headline-title[data-qtip='{PROJECT_NAME}']").first
            project_row_locator.wait_for(state="visible", timeout=10000)

            if project_row_locator.count() == 0:
                raise Exception(f"Project '{PROJECT_NAME}' not found after creation")

            # Success
            result["passed"] = True
            result["result"] = "pass"
            break

        except Exception as e:
            # Capture screenshot on failure
            timestamp = int(time.time())
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
                print("Retrying...")
                time.sleep(2)
            else:
                break

        finally:
            try:
                page.goto(BASE_URL)
            except:
                pass

    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    return result