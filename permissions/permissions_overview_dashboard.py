"""
Test Module: Overview Dashboard Permission
====================================================
Checks if a user with the proper role can view the overview dashboard
from a workflow in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time

BASE_URL = "https://clarity-dev.btolims.com"
RETRIES = 0
SCREENSHOT_DIR = "screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_overview_dashboard(page, expected=True):
    """
    Checks if role can view the Overview Dashboard in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Overview Dashboard Permission =====")

    result = {
        "test_name": "Overview Dashboard",
        "description": "Checks if role can view the overview dashboard in Clarity LIMS",
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
            print(f"\nAttempt {attempt}: Navigating to Overview Dashboard...")

            # Try to locate the "Overview" link inside the Dashboards dropdown
            print("Checking for 'Overview' link in Dashboards dropdown...")
            dashboard_menu = page.locator("li.dropdown a.dropdown-toggle", has_text="Dashboards")
            dashboard_menu.click()
            page.wait_for_timeout(500)

            overview_link = page.get_by_role("link", name=re.compile("Overview", re.I))

            if overview_link.count() == 0:
                raise Exception("Overview link not found in Dashboards dropdown")

            # Click the Overview link
            overview_link.first.click()
            page.wait_for_url(re.compile("/clarity/overview"))

            print("Overview Dashboard accessed successfully.")
            result["passed"] = True
            result["result"] = "pass"
            break

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            result["error"] = str(e)
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"overview_dashboard_fail_{attempt}.png")
            page.screenshot(path=screenshot_path)
            result["screenshot"] = screenshot_path
            if attempt == RETRIES + 1:
                print("All attempts failed.")
            else:
                print("Retrying...")
            page.wait_for_timeout(1000)

    result["execution_time"] = round(time.time() - start_time, 2)
    return result