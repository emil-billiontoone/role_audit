"""
Test Module: Clarity Login
==========================
Self-contained test for checking if a role can login to Clarity.
Permission: ClarityLogin
"""

from asyncio import Server
from playwright.sync_api import Page
import keyring
import time
from datetime import datetime

SERVICE_NAME = "role_audit_app"
BASE_URL = f"https://clarity-dev.btolims.com"  # Can parameterize if needed

def test_clarity_login(page: Page) -> dict:
    """
    Checks if user can login to Clarity LIMS
    
    Args:
        page: Playwright page object
    
    Returns:
        dict: Test results with pass/fail status
    """

    # Get credentials
    account = "TEST"  
    username = keyring.get_password(SERVICE_NAME, f"USERNAME_{account}")
    password = keyring.get_password(SERVICE_NAME, username) if username else None

    if not username or not password:
        raise ValueError("Credentials not found. Please run store_creds.py first.")

    # Go to login page and submit credentials
    page.goto(f"{BASE_URL}/clarity/login/auth?unauthenticated=1")
    # if role_name == "Not Logged In":
    #     username = "  "
    #     password = "  "
    
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#sign-in")

    # Wait for redirects and dashboard load
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(5000)  # Extra time for JS to render

    # Check for login success by looking for key dashboard elements
    try:
        page.wait_for_selector("span.navbar-username", timeout=5000)
        page.wait_for_selector("#work-available-panel", timeout=5000)
        passed = True
    except:
        passed = False

    # Also check for known login error message just in case
    try:
        error_visible = page.locator(
            "text=Sorry, we were not able to find a user with that username and password."
        ).is_visible()
        if error_visible:
            passed = False
    except:
        pass  # ignore if error message not found

    # Build standardized result
    test_result = {
        "test_name": "Clarity Login",
        "passed": passed,
        "description": "Checks if user can login to Clarity LIMS",
        "result": "pass" if passed else "fail",
    }

    # Print summary
    if passed:
        print(f"\nRESULT: PASSED - User CAN login to Clarity")
    else:
        print(f"\nRESULT: FAILED - User CANNOT login to Clarity")

    return test_result