import s4
from s4 import clarity
import os
import time
import keyring
from s4.clarity import researcher, role


SERVICE_NAME = "role_audit_app"
CLARITY_SERVERS = {
    "prod": "https://billiontoone-prod.claritylims.com/api/v2",
    "staging": "https://clarity-staging.btolims.com/api/v2",
    "dev": "https://clarity-dev.btolims.com/api/v2"
}

def get_lims_connection(account="MASTER", server="dev"):
    """Login to Clarity API using stored credentials."""
    username = keyring.get_password(SERVICE_NAME, f"USERNAME_{account}")
    password = keyring.get_password(SERVICE_NAME, username)
    lims = s4.clarity.LIMS(CLARITY_SERVERS[server], username, password)
    print(f"Connected to {server} - API version: {lims.versions[0]['major']}")
    return lims, username

def modify_user_role(lims, user_firstname, user_lastname, role_name, action="add"):
    """Add or remove a role for a given user."""
    user = lims.researchers.query(firstname=[user_firstname], lastname=user_lastname)[0]
    role_obj = lims.roles.get_by_name(role_name)
    
    if action == "add":
        user.add_role(role_obj)
        print(f"Added role '{role_name}' to {user.username}")
    elif action == "remove":
        user.remove_role(role_obj)
        print(f"Removed role '{role_name}' from {user.username}")
    else:
        raise ValueError("Action must be 'add' or 'remove'")
    
    user.commit()
    return user

lims, username = get_lims_connection()

user = modify_user_role(lims, "Emil", "Test", "System Admin (BTO)", action="remove")

print(f"Current roles for {username}:")
for r in user.roles:
    print(f"  - {r.name}")

