"""
Test Module: URL Access Permission
=====================================
Checks that a user without access is redirected to the login page for all
Clarity LIMS protected URLs.
Compatible with RolePermissionTester framework.
"""

import time
from .test_utils import capture_screenshot

BASE_URL = "https://clarity-dev.btolims.com"
UNAUTH_URL = f"{BASE_URL}/clarity/login/auth?unauthenticated=1"

# All URLs to test
URLS_TO_TEST = [
    f"{BASE_URL}/clarity/",
    f"{BASE_URL}/clarity/configuration",
    f"{BASE_URL}/clarity/overview",
    f"{BASE_URL}/clarity/projects",
    f"{BASE_URL}/clarity/samples",
    f"{BASE_URL}/clarity/configuration/consumables/reagents",
    f"{BASE_URL}/clarity/configuration/lab-work",
    f"{BASE_URL}/clarity/configuration/custom-fields/global-fields",
    f"{BASE_URL}/clarity/configuration/user-management/users",
    f"{BASE_URL}/clarity/configuration/automation/step-automation",
    f"{BASE_URL}/clarity/profile",
]

def test_url_check(page, expected_fail=True):
    """
    For each URL:
      - Navigate to it.
      - If redirected to unauthenticated login page → PASS.
      - If the page loads directly (no redirect) → FAIL.
    """
    print("\n===== TEST: URL Access Permission =====")
    results = []
    start_time = time.time()

    for url in URLS_TO_TEST:
        print(f"\nVisiting: {url}")
        single_result = {"url": url, "passed": False, "error": None}

        try:
            page.goto(url, timeout=20000)
            page.wait_for_timeout(1000)

            current_url = page.url
            print(f"Current URL: {current_url}")

            if current_url.startswith(UNAUTH_URL):
                print("Redirected to unauthenticated page — as expected.")
                single_result["passed"] = True
            else:
                print("Unexpected access — page did not redirect to login.")
                single_result["error"] = f"Expected redirect to {UNAUTH_URL}, got {current_url}"

            # # Take a screenshot for each URL
            # screenshot_name = f"url_check_{int(time.time())}"
            # single_result["screenshot"], _ = capture_screenshot(page, screenshot_name, "pass" if single_result["passed"] else "fail")

        except Exception as e:
            single_result["error"] = str(e)
            print(f"Error visiting {url}: {e}")
            single_result["screenshot"], _ = capture_screenshot(page, "url_check_error", "fail")

        results.append(single_result)

    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    # Determine overall test result
    all_passed = all(r["passed"] for r in results)
    print("\n===== TEST RESULT SUMMARY =====")
    print(f"Status: {'PASS' if all_passed else 'FAIL'}")
    print(f"Execution time: {total_time}s")

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  {status} - {r['url']}")
        if r["error"]:
            print(f"    → {r['error']}")

    # Return structured summary
    return {
        "test_name": "URL Access Permission",
        "description": "Checks that protected URLs redirect to unauthenticated login",
        "execution_time": total_time,
        "passed": all_passed,
        "details": results,
    }