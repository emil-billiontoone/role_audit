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
            # Navigate to home (already logged in)
            page.goto(f"{BASE_URL}/clarity")
            page.wait_for_load_state("networkidle")

            # Go to Projects & Samples
            page.get_by_role("link", name=re.compile("PROJECTS & Samples", re.I)).click()

            # Check if NEW PROJECT button exists
            page.get_by_role("textbox", name="Filter...").fill("Emil Project Test")
            new_project_btn_count = page.locator("button", has_text="NEW PROJECT").count()
            if new_project_btn_count == 0:
                raise Exception("NEW PROJECT button not found")

            # Click New Project
            page.locator("button", has_text="NEW PROJECT").click()

            # Fill project form
            page.get_by_role("textbox", name="Enter Project Name").fill(PROJECT_NAME)
            page.get_by_placeholder("Choose an account").click()
            page.get_by_text(ACCOUNT_NAME).click()
            page.get_by_placeholder("Choose a client").fill(CLIENT_NAME)
            page.get_by_placeholder("Choose a client").press("Enter")
            page.get_by_text("Standard").click()  # Priority
            page.get_by_role("button", name="Save").click()

            # Verify project exists
            page.goto(f"{BASE_URL}/clarity/samples")
            page.get_by_role("textbox", name="Filter...").fill(PROJECT_NAME)

            project_count = page.get_by_text(PROJECT_NAME).count()
            if project_count == 0:
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