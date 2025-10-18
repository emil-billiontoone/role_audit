"""
Role Test Configurations
========================
Define which tests to run for each role.
"""

# Test suite configurations for different roles
MAIN_ROLE_TEST_SUITES = {
    "Lab Operator": {
        "permissions_clarity_login": True,
        "permissions_API_login": True,
        "permissions_create_project": False, 
        "permissions_delete_project": False, 
        "permissions_sample_workflow_assignment": True, 
        "permissions_move_to_next_step": True, 
        "permissions_remove_sample_from_workflow": True,
        "permissions_edit_completed_steps": False,
        "permissions_overview_dashboard": True, 
        "permissions_requeue_sample": True,
        "permissions_read_user": True, 
        "permissions_create_user": True, 
        "permissions_update_user": True, 
        "permissions_update_sample": True, 
    },
    
    "System Admin": {
        "permissions_clarity_login": True,
        # "permissions_edit_completed_steps": True,
        # "permissions_API_login": True,
        # "permissions_collaborations_login": True, # Don't worry about this test
        # "permissions_operations_login": True, # Don't worry about this test
        # "permissions_create_project": True, 
        # "permissions_delete_project": True, 
        # "permissions_create_sample": True, 
        # "permissions_delete_sample": True, 
        # "permissions_sample_workflow_assignment": True, 
        # "permissions_sample_rework": True, # still need to create this test ???
        # "permissions_review_escalated_samples": True, # still need to create this test ???
        # "permissions_move_to_next_step": True, 
        "permissions_create_control": True,
        "permissions_update_control": True,
        "permissions_delete_control": True, 
        # "permissions_create_reagent_kit": True, # still need to create this test
        # "permissions_update_reagent_kit": True, # still need to create this test
        # "permissions_delete_reagent_kit": True, # still need to create this test
        # "permissions_overview_dashboard": True, 
        # "permissions_update_configuration": True, # still need to create this test ???
        # "permissions_requeue_sample": True,
        # "permissions_remove_sample_from_workflow": True, 
        # "permissions_read_user": True,
        # "permissions_create_user": True, 
        # "permissions_update_user": True,
        # "permissions_delete_user": True, # still need to create this test
        # "permissions_read_process": True, # still need to create this test
        # "permissions_create_process": True, # still need to create this test
        # "permissions_update_process": True, # still need to create this test
        # "permissions_esignature_signing": True, # still need to create this test ???
        # "permissions_create_role": True, # still need to create this test
        # "permissions_update_role": True, # still need to create this test
        # "permissions_delete_role": True, # still need to create this test
        # "permissions_search_index": True, # still need to create this test ???
        # "permissions_update_sample": True, 
        # "permissions_create_contact": True, # still need to create this test
        # "permissions_read_contact": True, # still need to create this test
        # "permissions_update_contact": True, # still need to create this test
        # "permissions_delete_contact": True, # still need to create this test
        # "permissions_administer_lab_link": True, # still need to create this test???
    },
    
    "Lab Admin": {
        "permissions_clarity_login": True,
        # "permissions_edit_completed_steps": False,
        # "permissions_API_login": True,
        # "permissions_create_project": False, 
        # "permissions_delete_project": False, 
        # "permissions_create_sample": True, # still need to create this test
        # "permissions_delete_sample": True, # still need to create this test
        # "permissions_sample_workflow_assignment": True, 
        # "permissions_sample_rework": True, # still need to create this test
        # "permissions_review_escalated_samples": True, # still need to create this test
        # "permissions_move_to_next_step": True, # still need to create this test
        # "permissions_create_control": True, # still need to create this test
        # "permissions_update_control": True, # still need to create this test
        # "permissions_delete_control": True, # still need to create this test
        # "permissions_create_reagent_kit": True, # still need to create this test
        # "permissions_update_reagent_kit": True, # still need to create this test
        # "permissions_delete_reagent_kit": True, # still need to create this test
        # "permissions_overview_dashboard": 
        # "permissions_requeue_sample": True,
        # "permissions_remove_sample_from_workflow": True, # still need to create this test
        # "permissions_read_user": True,
        # "permissions_create_user": True, # still need to create this test
        # "permissions_update_user": True, # still need to create this test
        # "permissions_read_process": True, # still need to create this test
        # "permissions_update_sample": True, # still need to create this test
    },

    "Limited": {
        "permissions_clarity_login": True,
        # "permissions_edit_completed_steps": False,
        # "permissions_API_login": False,
        # "permissions_create_project": False, 
        # "permissions_sample_workflow_assignment": False,
        # "permissions_sample_rework": True, # still need to create this test
        # "permissions_review_escalated_samples": True, # still need to create this test
        # "permissions_create_control": True, # still need to create this test
        # "permissions_update_control": True, # still need to create this test
        # "permissions_create_reagent_kit": True, # still need to create this test
        # "permissions_update_reagent_kit": True, # still need to create this test
        # "permissions_update_configuration": True, # still need to create this test
        # "permissions_requeue_sample": False,
        # "permissions_remove_sample_from_workflow": True, # still need to create this test
        # "permissions_read_process": True, # still need to create this test
        # "permissions_create_process": True, # still need to create this test
        # "permissions_update_process": True, # still need to create this test
        # "permissions_overview_dashboard": False, 
        # "permissions_read_user": False, 
        # "permissions_create_user": False,
        # "permissions_update_user": False,
        # "permissions_update_sample": False, 
        # "permissions_move_to_next_step": False, 
        # "permissions_create_sample": False, 
        # "permissions_delete_sample": False, 
        # "permissions_create_control": False,
        "permissions_create_control": True,
        "permissions_update_control": True,
        "permissions_delete_control": True, 
    },

    "BTO API": {
        "permissions_clarity_login": False,
        "permissions_edit_completed_steps": False,
        "permissions_API_login": True,
        "permissions_overview_dashboard": False, 
    },  

    "Not Logged In": {
        "permissions_clarity_login": False,
        "permissions_edit_completed_steps": False,
        "permissions_API_login": True,
        "permissions_overview_dashboard": False, 
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
