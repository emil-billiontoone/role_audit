"""
Role Test Configurations
========================
Define which tests to run for each role.
"""

# Test suite configurations for different roles
MAIN_ROLE_TEST_SUITES = {
    "Editor": [
        "permissions_edit_completed_steps",
    ],
    
    "Lab Operator": [
        "permissions_view",
    ],
    
    "System Admin": [
        "permissions_edit_completed_steps",
        "permissions_view",
    ],
    
    "Lab Admin": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],

    "Reagent Manufacturing": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],

    "Sample Creation": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],
# This is a test to see if branch works
    "Limited": [
        "clarity_login",
    ],

    "Review Escalations": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],

    "Rework": [
        "permissions_view",
        ("permissions_edit_completed_steps", "test_can_edit_completed_steps"),
    ],

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
