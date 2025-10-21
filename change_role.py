import s4
from s4 import clarity
import os
import time
import keyring
from s4.clarity import researcher, role

def add_role_to_user(user, role_obj, username, role_name):
    """Add a role to a user."""   
    # Add the role
    user.add_role(role_obj)
    user.commit()
    print(f"Added {role_name} role to {username}")

def remove_role_from_user(user, role_obj, username, role_name):
    """Remove a role from a user."""
    # Remove the role
    user.remove_role(role_obj)  
    user.commit()
    print(f"Removed {role_name} role from {username}")

SERVICE_NAME = "role_audit_app"  # must match store_creds.py
server = "dev"
role_names = [f"System Admin (BTO)"]
action = "remove"

CLARITY_SERVERS = {
    "prod": "https://billiontoone-prod.claritylims.com/api/v2",
    "staging": "https://clarity-staging.btolims.com/api/v2",
    "dev": "https://clarity-dev.btolims.com/api/v2"
}

# Retrieve stored credentials
account = "MASTER" 
username = keyring.get_password(SERVICE_NAME, f"USERNAME_{account}")
password = keyring.get_password(SERVICE_NAME, username)

# Connect to Clarity API
lims = s4.clarity.LIMS(CLARITY_SERVERS[server], username, password)
print(f'Connected to {server} - API version: {lims.versions[0]["major"]}')
print(f"The username is {username}")

current_user = lims.researchers.query(**{
    'firstname': ['Emil'],
    'lastname': "Test"
})
     
print(f"Current user: {current_user[0].first_name} {current_user[0].last_name}")
print(f"Current user: {current_user[0].username}")

print(f"Current roles for {username}:")
for r in current_user[0].roles:
    print(f"  - {r.name}")


for role_name in role_names:
    role = lims.roles.get_by_name(role_name)    
    # Change the function here to add or remove the role
    if action == "add":
        add_role_to_user(current_user[0], role, username, role_name)
    else:
        remove_role_from_user(current_user[0], role, username, role_name)

print(f"Current roles for {username}:")
for r in current_user[0].roles:
    print(f"  - {r.name}")



