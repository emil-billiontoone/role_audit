import s4
from s4 import clarity
import os
import time
import keyring
from s4.clarity import researcher, role

SERVICE_NAME = "role_audit_app"  
server = "dev"

CLARITY_SERVERS = {
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



