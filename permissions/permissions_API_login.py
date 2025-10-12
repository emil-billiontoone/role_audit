"""
Test Module: API Login
==========================
Self-contained test for checking if a role can login to Clarity API.
Permission: ClarityAPI
"""

import s4
from s4 import clarity
import keyring

def test_API_login(page=None) -> dict:
    """
    Checks if user can login to Clarity API
    
    Args:
        None
    
    Returns:
        dict: Test results with pass/fail status
    """
    server = 'dev'

    CLARITY_SERVERS = {
        "dev": "https://clarity-dev.btolims.com/api/v2"
    }

    SERVICE_NAME = "role_audit_app"

    # Retrieve stored credentials
    account = "TEST"  
    username = keyring.get_password(SERVICE_NAME, f"USERNAME_{account}")
    password = keyring.get_password(SERVICE_NAME, username) if username else None

    # Connect to Clarity API
    try:
        lims = s4.clarity.LIMS(CLARITY_SERVERS[server], username, password)
        print(f'Connected to {server} - API version: {lims.versions[0]["major"]}')
        passed = True
    except Exception as e:
        print(f'Error connecting to Clarity API: {e}')
        passed = False

    test_result = {
        "test_name": "API Login",
        "passed": passed,
        "description": "Checks if user can login to Clarity API",
        "result": "pass" if passed else "fail",
    }

    if passed:
        print("\nRESULT: PASSED - User CAN login to Clarity API")
    else:
        print("\nRESULT: FAILED - User CANNOT login to Clarity API")

    return test_result