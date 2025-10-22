# permissions/permissions_move_to_next_step.py
"""
Test Module: Move To Next Step Permission
=========================================
Checks if a user can move to the next step in Clarity LIMS.
Compatible with RolePermissionTester framework.
"""

import os
import time
import json
from playwright.sync_api import TimeoutError

BASE_URL = "https://clarity-dev.btolims.com"
RETRIES = 2
SCREENSHOT_DIR = "test_results/screenshots"
RESULTS_JSON = "permissions_results.json"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_permissions_move_to_next_step(page):
    """
    Checks if a user can move to the next step in Clarity LIMS.
    Returns structured result dict and writes JSON result to file.
    """
    print("\n===== TEST: Move To Next Step Permission =====")

    result = {
        "test_name": "Permissions Move To Next Step",
        "description": "Checks if a user can move to the next step in Clarity LIMS.",
        "execution_time": 0.0,
        "expected": True,
        "passed": False,
        "result": "fail",
        "error": None,
        "screenshot": None,
    }

    start_time = time.time()

    try:
        # 1. Click on the step
        print("Locating workflow step button...")
        step_button = page.locator("div.sub-work", has_text="Aneuploidy - Plasma Isolation")
        if step_button.count() == 0:
            raise Exception("Workflow step not found")
        print("Clicking workflow step...")
        with page.expect_navigation():
            step_button.first.click()

        print("Navigated to workflow queue page.")

        # Confirm the queue page loaded
        page.wait_for_selector("div.group-header-label", timeout=20000)
        print("Page loaded, continuing test...")

        print("Expanding 'Single Well: Tube' group header...")

        # Locate the entire group header that contains the label text
        group = page.locator("div.group-header", has_text="Single Well: Tube")

        # Wait until it’s visible and attached
        group.wait_for(state="visible", timeout=10000)

        # Now find the expander button *inside* that group
        expander = group.locator(".group-expander-btn")

        # If it’s already expanded, it won’t have “collapsed” in its class list
        is_collapsed = expander.get_attribute("class")
        if "collapsed" in (is_collapsed or ""):
            expander.click()
            print("Clicked group expander...")
        else:
            print("Group already expanded.")

        # Give it a moment to load the samples
        page.wait_for_timeout(1500)

        # Optional: verify expansion
        samples_section = group.locator(".samples")
        page.wait_for_timeout(500)
        if samples_section.is_visible():
            print("Sample group expanded successfully.")
        else:
            print("Warning: Group expansion did not reveal samples.")

        # 3. Click on a sample
        print("Selecting sample...")
        sample = page.locator("span.qtip-value", has_text="V_251014L0001-5")
        sample.first.wait_for(state="visible", timeout=10000)
        sample.first.click()

        # 4. Click Options
        print("Clicking Options button...")
        options_button = page.locator("button:has-text('Options')")
        options_button.wait_for(state="visible", timeout=10000)
        options_button.click()
        page.wait_for_timeout(1000)

        # 5. Check for Move to Next Step button
        print("Checking for 'Move to the next step' option...")
        move_button = page.locator("div.menu-item-description", has_text="Move to the next step")

        if move_button.count() > 0 and move_button.first.is_visible():
            print("'Move to the next step' option is visible.")
            result["passed"] = True
            result["result"] = "pass"
        else:
            raise Exception("Permission denied - 'Move to next step' not visible")

    except TimeoutError as e:
        result["error"] = f"TimeoutError: {str(e)}"
    except Exception as e:
        result["error"] = str(e)
    finally:
        # Capture screenshot regardless of pass or fail
        timestamp = int(time.time())
        screenshot_file = f"{SCREENSHOT_DIR}/move_to_next_step_{timestamp}.png"
        try:
            page.screenshot(path=screenshot_file)
            result["screenshot"] = screenshot_file
            print(f"Screenshot saved to {screenshot_file}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

        # Add execution time
        result["execution_time"] = round(time.time() - start_time, 2)

        # Write result to JSON file
        try:
            # Load existing results if present
            if os.path.exists(RESULTS_JSON):
                with open(RESULTS_JSON, "r") as f:
                    all_results = json.load(f)
            else:
                all_results = []

            all_results.append(result)

            with open(RESULTS_JSON, "w") as f:
                json.dump(all_results, f, indent=4)
            print(f"Test result saved to {RESULTS_JSON}")
        except Exception as e:
            print(f"Failed to write JSON results: {e}")

    print(f"===== TEST RESULT: {'PASS' if result['passed'] else 'FAIL'} =====")
    return result