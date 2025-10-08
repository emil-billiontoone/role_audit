#!/usr/bin/env python3
"""
Main Runner for Role Permission Tests
======================================
Simple script to run role-based permission tests.
"""

import sys
from role_permission_tester import RolePermissionTester
from role_test_configs import ROLE_TEST_SUITES, QUICK_TEST, FULL_TEST_SUITE

def main():
    """Main entry point for role testing."""
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("\nUsage: python run_role_tests.py <role_name> [server]")
        print("\nAvailable roles:")
        for role in ROLE_TEST_SUITES.keys():
            print(f"  - {role}")
        print("\nSpecial options:")
        print("  - quick  : Run quick test suite")
        print("  - full   : Run full test suite")
        print("\nExamples:")
        print("  python run_role_tests.py Editor")
        print("  python run_role_tests.py Editor dev")
        print("  python run_role_tests.py quick")
        sys.exit(1)
    
    role_name = sys.argv[1]
    server = sys.argv[2] if len(sys.argv) > 2 else "dev"
    
    # Determine which tests to run
    if role_name.lower() == "quick":
        test_suite = QUICK_TEST
        role_name = "Quick Test"
    elif role_name.lower() == "full":
        test_suite = FULL_TEST_SUITE
        role_name = "Full Test"
    elif role_name in ROLE_TEST_SUITES:
        test_suite = ROLE_TEST_SUITES[role_name]
    else:
        print(f"\nWarning: Unknown role '{role_name}'. Running default test suite.")
        test_suite = ["permissions_view", "permissions_edit_completed_steps"]
    
    # Create tester and run tests
    print(f"\nTesting role: {role_name} on server: {server}")
    tester = RolePermissionTester(server=server, role_name=role_name)
    tester.run_test_suite(test_suite)

if __name__ == "__main__":
    main()
