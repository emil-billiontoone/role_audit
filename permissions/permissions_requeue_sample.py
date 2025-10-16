"""
Test Module: Requeue Sample Permission
======================================
Checks if a user with the proper role can see the Requeue button for a sample in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import re
import time

BASE_URL = "https://clarity-dev.btolims.com"
RETRIES = 1
SCREENSHOT_DIR = "screenshots"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_requeue_sample(page, expected=True):
    """
    Checks if a user can see the Requeue button for a sample in Clarity LIMS.
    Accepts a Playwright 'page' object from the test framework.
    Returns structured JSON result.
    """
    print("\n===== TEST: Requeue Sample Permission =====")

    result = {
        "test_name": "Requeue Sample",
        "description": "Checks if user can see the Requeue button for a sample in Clarity LIMS",
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
            print(f"\nAttempt {attempt}: Navigating to Sample and Container Search page...")
            page.goto(f"{BASE_URL}/clarity/search?query=Emil%20Test&offset=0&scope=Process")
            page.wait_for_timeout(1500)

            print("Expanding sample details...")
            # Expand the search result to show project/sample details
            page.locator("div.detail-toggle").first.click()
            page.wait_for_timeout(1000)

            print("Looking for sample project row...")
            sample_row = page.locator("div.project-name a", has_text=re.compile("1428460L1954-1", re.I))
            if sample_row.count() == 0:
                raise Exception("Sample project not found in search results.")

            print("Checking for Requeue button visibility...")

            # Locate the requeue icon/container
            requeue_button = page.locator("div.requeue.active")

            if requeue_button.count() > 0:
                print("Requeue button is present — permission confirmed.")
                result["passed"] = True
                result["result"] = "pass"
            else:
                raise Exception("Requeue button not found — permission denied or hidden.")

            break

        except Exception as e:
            timestamp = int(time.time())
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"requeue_sample_fail_{timestamp}.png")
            try:
                page.screenshot(path=screenshot_file)
                result["screenshot"] = screenshot_file
            except:
                result["screenshot"] = "Failed to capture screenshot"

            result["error"] = str(e)
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