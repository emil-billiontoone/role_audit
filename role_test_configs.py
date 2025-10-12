"""
Role Test Configurations
========================
Define which tests to run for each role.
"""

# Test suite configurations for different roles
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator": {
        # "permissions_clarity_login": True,
        "permissions_API_login": True,
    },
    
    "System Admin": {
        "permissions_edit_completed_steps": True,
        "permissions_view": True,
    },
    
    "Lab Admin": {
        "permissions_view": True,
    },

    "Limited": {
        "permissions_clarity_login": True,
        "permissions_edit_completed_steps": False,
    },

    "BTO API": {
        "permissions_clarity_login": True,
    },  

    "Not Logged In": {
        "permissions_clarity_login": False,
    },
}

ADD_ON_ROLE_TEST_SUITES = {
    "Sample Creation": {
        "permissions_view": True,
    },
    
    "Editor": {
        "permissions_clarity_login": True,
        "permissions_edit_completed_steps": True,
    },

    "Reagent Manufacturing": {
        "permissions_view": True,
    },

    "Review Escalations": {
        "permissions_view": True,
    },

    "Rework": {
        "permissions_view": True,
    },

    "No Add-Ons": {
        "permissions_view": True,
    },
}

# You can also define test groups for reuse
BASIC_PERMISSIONS = [
    "permissions_view",
]

EDIT_PERMISSIONS = [
    "permissions_edit_completed_steps",
]

ADMIN_PERMISSIONS = [
    # "test_user_management",
    # "test_system_settings",
]

# Quick test suite for development/debugging
QUICK_TEST = [
    ("permissions_view", "test_can_view_entries"),  # Just one quick test
]

# Full comprehensive test suite
FULL_TEST_SUITE = [
    "permissions_view",
    "permissions_edit_completed_steps", 
    # Add all available tests here
]
