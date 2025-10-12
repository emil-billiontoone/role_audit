"""
Test Module: API Login
==========================
Self-contained test for checking if a role can login to Clarity API.
Permission: ClarityAPI
"""

import s4
from s4 import clarity
import keyring

server = 'dev'  # Change this to 'prod' or 'staging' as needed

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
except Exception as e:
    print(f'Error connecting to Clarity API: {e}')
    exit(1)