# """
# Test Module: Clarity Login
# ======================================
# Self-contained test for checking if a role can login to Clarity.
# Permission: ClarityLogin
# Default roles with this permission: Administrator, Researcher

# Allows:
# •	Sign in to BaseSpace LIMS
# •	Access Lab View and Projects and Samples screen
# •	Access Consumables > Reagents configuration tab; view, edit, and delete reagent lots; add lots to existing kits.
# •	Access Consumables > Controls configuration tab and view control details
# •	Access Consumables > Instruments configuration tab; add, edit, delete, and activate instruments; view instrument types.

# Result of denied permission
# •	Sign In screen:Sorry, you do not have permission to sign in to Clarity LIMS.
# """

# from playwright.sync_api import Page, TimeoutError
# import time
# import re

# def test_clarity_login(page: Page) -> dict:
#     """
#     Test if the current user can login to Clarity.
    
#     Args:
#         page: Playwright page object (already logged in)
    
#     Returns:
#         dict: Test results with pass/fail status and details
#     """
    
#     # Define what we're looking for
#     CLARITY_LOGIN_CRITERIA = 
#     # Run the audit
# If we get this message "Sorry, we were not able to find a user with that username and password." then the test fails.
# If we get redirected to the Clarity dashboard, then the test passes.

# So we need to check for both of these.

    


#     print("\n" + "="*60)
#     print("TEST: Clarity Login")
#     print("="*60)
#     print("Looking for confirmation dialog when logging in to Clarity...")
    
#     results = audit_clarity_login(page, CLARITY_LOGIN_CRITERIA)
    
#     # Prepare test summary
#     test_summary = {
#         "test_name": "Clarity Login",
#         "passed": results["passed"],
#         "description": "Checks if user gets confirmation when logging in to Clarity",
#         "raw_results": results,
#         "result": results["result"] #I want this to be pass or fail
#         },

#     def login(self, page, username=None, password=None):
#         """
#         Login to the application.
        
#         Args:
#             page: Playwright page object
#             username: Username (optional, will get from keyring if not provided)
#             password: Password (optional, will get from keyring if not provided)
#         """
#         if not username:
#             username = keyring.get_password(SERVICE_NAME, "USERNAME_KEY")
#             password = keyring.get_password(SERVICE_NAME, username) if username else None
        
#         if not username or not password:
#             raise ValueError("Credentials not found. Please run store_creds.py first.")
        
#         print("\nLogging in...")
#         page.goto(f"{self.base_url}/clarity/login/auth?unauthenticated=1")
#         page.fill("#username", username)
#         page.fill("#password", password) 
#         page.click("#sign-in")
#         page.wait_for_load_state("domcontentloaded")
#         print(f"Logged in as: {username}")
        
#         # Navigate to main page
#         page.goto(f"{self.base_url}/clarity")
#         page.wait_for_load_state("networkidle")  # Wait for all network requests to finish
#         page.wait_for_timeout(2000)  # Additional wait for JavaScript rendering
        
#         # Optional: Print current URL to confirm we're on the right page
#         print(f"Currently on: {page.url}")
#         return username

#     # Print summary
#     if test_summary["passed"]:
#         print(f"\nRESULT: PASSED - User CAN login to Clarity")
#         print(f"User was redirected to the Clarity dashboard")
#     else:
#         print(f"\nRESULT: FAILED - User CANNOT login to Clarity")
#         print(f"User got the message 'Sorry, we were not able to find a user with that username and password.'")
    
#     return test_summary
# permissions_clarity_login.py

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

SERVICE_NAME = "user_tester_app"
BASE_URL = f"https://clarity-dev.btolims.com"  # Can parameterize if needed

def test_clarity_login(page: Page) -> dict:
    """
    Test if the current user can login to Clarity.
    
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
    if role_name == "Not Logged In":
        username = "  "
        password = "  "
    
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#sign-in")

    # Wait for redirects and dashboard load
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)  # Extra time for JS to render

    # Check for login success by looking for key dashboard elements
    try:
        user_visible = page.locator("span.navbar-username").is_visible()
        work_panel_visible = page.locator("#work-available-panel").is_visible()
        passed = user_visible and work_panel_visible
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