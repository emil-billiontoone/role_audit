#!/usr/bin/env python3
"""
Main Runner for Role Permission Tests
======================================
Simple script to run role-based permission tests.
"""

import sys
import argparse
from role_permission_tester import RolePermissionTester
from role_test_configs import MAIN_ROLE_TEST_SUITES, ADD_ON_ROLE_TEST_SUITES

def main():
    """Main entry point for role testing."""
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Run role-based permission tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available roles:
{}

Special options:
  quick  : Run quick test suite
  full   : Run full test suite

Examples:
  python run_role_tests.py "Lab Operator"
  python run_role_tests.py "Lab Operator" --server dev
  python run_role_tests.py "System Admin" -s test
""".format("\n".join(f"  - {role}" for role in MAIN_ROLE_TEST_SUITES.keys()))
    )
    
    parser.add_argument("role", 
                       help="Role name to test (use quotes for names with spaces)")
    parser.add_argument("-s", "--server", 
                       default="dev",
                       choices=["dev", "test", "prod", "stage"],
                       help="Server environment (default: dev)")
    
    args = parser.parse_args()
    
    role_name = args.role
    server = args.server
    
    # Determine which tests to run
    if role_name in MAIN_ROLE_TEST_SUITES:
        test_suite = MAIN_ROLE_TEST_SUITES[role_name]
    elif role_name in ADD_ON_ROLE_TEST_SUITES:
        test_suite = ADD_ON_ROLE_TEST_SUITES[role_name]
    else:
        print(f"\nWarning: Unknown role '{role_name}'. Running default test suite.")
        # Ensure it's a dict with expected outcomes
        test_suite = {"permissions_clarity_login": True}
    
    # Create tester and run tests
    print(f"\nTesting role: {role_name} on server: {server}")
    tester = RolePermissionTester(server=server, role_name=role_name)
    tester.run_test_suite(test_suite)

if __name__ == "__main__":
    main()
