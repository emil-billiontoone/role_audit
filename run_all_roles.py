#!/usr/bin/env python3
"""
Role Testing Loop - Test All MAIN Roles with ADD_ON Combinations
=================================================================
This script loops through all roles in MAIN_ROLE_TEST_SUITES, testing each
MAIN role by itself first, then with each ADD_ON role from ADD_ON_ROLE_TEST_SUITES.

For each MAIN role (e.g., Lab Operator (BTO)):
  1. Test MAIN role alone (BASE)
  2. Test MAIN role + Sample Creation (BTO)
  3. Test MAIN role + Editor
  4. Test MAIN role + Reagent Manufacturing (BTO)
  5. Test MAIN role + ReviewEscalations
  6. Test MAIN role + ReWork
  7. Prompt to continue to next MAIN role

Ensures at least one role is always assigned to the user.
"""

import sys
import argparse
from role_permission_tester import RolePermissionTester
from role_test_configs import MAIN_ROLE_TEST_SUITES, ADD_ON_ROLE_TEST_SUITES
from change_role import get_lims_connection, modify_user_role
from generate_pdf_report import PDFReportGenerator


def run_all_role_tests(user_firstname, user_lastname, server="dev", account="MASTER", generate_pdf=True):
    """
    Run tests for all roles in MAIN_ROLE_TEST_SUITES.
    
    Args:
        user_firstname: First name of the user
        user_lastname: Last name of the user
        server: Server environment (dev, staging, prod)
        account: Account name for credentials (default: MASTER)
        generate_pdf: Whether to auto-generate PDF report after completion (default: True)
    """
    print("=" * 80)
    print("COMPREHENSIVE ROLE TESTING SUITE")
    print("=" * 80)
    print(f"User: {user_firstname} {user_lastname}")
    print(f"Server: {server}")
    print(f"Total roles to test: {len(MAIN_ROLE_TEST_SUITES)}")
    print("=" * 80)
    
    # Get LIMS connection
    lims, username = get_lims_connection(account=account, server=server)
    
    # Initialize user to Lab Operator (BTO) role only
    print("\n" + "=" * 80)
    print("INITIALIZING USER ROLE")
    print("=" * 80)
    
    # Get user and current roles
    user = lims.researchers.query(firstname=[user_firstname], lastname=user_lastname)[0]
    current_roles = [role.name for role in user.roles]
    
    print(f"\nCurrent roles for {user.username}:")
    for role_name in current_roles:
        print(f"  - {role_name}")
    
    # Check if user already has only Lab Operator (BTO)
    if current_roles == ["Lab Operator (BTO)"]:
        print("\n✓ User already has only 'Lab Operator (BTO)' role. Ready to start!")
    else:
        print("\n⚙ Setting user to 'Lab Operator (BTO)' role only...")
        
        # Add Lab Operator (BTO) if not already present
        if "Lab Operator (BTO)" not in current_roles:
            print("\n[1/2] Adding 'Lab Operator (BTO)' role")
            modify_user_role(lims, user_firstname, user_lastname, "Lab Operator (BTO)", action="add")
            # Refresh user to get updated roles
            user = lims.researchers.query(firstname=[user_firstname], lastname=user_lastname)[0]
            current_roles = [role.name for role in user.roles]
        else:
            print("\n[1/2] User already has 'Lab Operator (BTO)' role")
        
        # Remove all other roles
        print("\n[2/2] Removing all other roles")
        roles_to_remove = [role_name for role_name in current_roles if role_name != "Lab Operator (BTO)"]
        
        if roles_to_remove:
            for role_name in roles_to_remove:
                print(f"  Removing: {role_name}")
                modify_user_role(lims, user_firstname, user_lastname, role_name, action="remove")
        else:
            print("  No other roles to remove")
        
        # Verify final state
        user = lims.researchers.query(firstname=[user_firstname], lastname=user_lastname)[0]
        final_roles = [role.name for role in user.roles]
        print(f"\n✓ User now has only: {', '.join(final_roles)}")
    
    print("=" * 80)
    
    # Get list of MAIN roles to test
    main_role_names = list(MAIN_ROLE_TEST_SUITES.keys())
    addon_role_names = list(ADD_ON_ROLE_TEST_SUITES.keys())
    
    # Handle "Not Logged In" specially - test once without add-ons
    # This role doesn't require role assignment and won't be tested with add-ons
    if "Not Logged In" in main_role_names:
        print("\n" + "=" * 80)
        print(f"TESTING SPECIAL ROLE: Not Logged In (no add-ons)")
        print("=" * 80)
        test_suite = MAIN_ROLE_TEST_SUITES["Not Logged In"]
        tester = RolePermissionTester(server=server, role_name="Not Logged In")
        tester.run_test_suite(test_suite)
        print(f"\n✓ Completed: Not Logged In")
        
        # Remove from main list - won't be tested with add-on combinations
        main_role_names.remove("Not Logged In")
    
    # Ensure "Lab Operator (BTO)" is first in the test list (since we initialized to it)
    if "Lab Operator (BTO)" in main_role_names:
        main_role_names.remove("Lab Operator (BTO)")
        main_role_names.insert(0, "Lab Operator (BTO)")
    
    # Process each MAIN role with all ADD_ON role combinations
    total_main_roles = len(main_role_names)
    
    for main_idx, main_role in enumerate(main_role_names, start=1):
        print("\n" + "=" * 80)
        print(f"MAIN ROLE {main_idx}/{total_main_roles}: {main_role}")
        print(f"Will test: Base + {len(addon_role_names)} add-on combinations")
        print("=" * 80)
        
        # Step 1: Assign the MAIN role (remove previous MAIN role if exists)
        if main_idx == 1 and main_role == "Lab Operator (BTO)":
            print(f"\nMAIN role '{main_role}' already assigned (initialization)")
        else:
            # Add new MAIN role
            print(f"\nAssigning MAIN role: {main_role}")
            try:
                modify_user_role(lims, user_firstname, user_lastname, main_role, action="add")
            except Exception as e:
                print(f"Error adding MAIN role {main_role}: {e}")
                print("Skipping this MAIN role...")
                continue
            
            # Remove previous MAIN role (if this isn't the first one)
            if main_idx > 1:
                previous_main_role = main_role_names[main_idx - 2]
                print(f"Removing previous MAIN role: {previous_main_role}")
                try:
                    modify_user_role(lims, user_firstname, user_lastname, previous_main_role, action="remove")
                except Exception as e:
                    print(f"Warning: Could not remove previous MAIN role {previous_main_role}: {e}")
        
        # Step 2: Test the MAIN role by itself (no add-ons)
        print("\n" + "-" * 80)
        print(f"Testing: {main_role} (BASE - no add-ons)")
        print("-" * 80)
        
        main_test_suite = MAIN_ROLE_TEST_SUITES[main_role]
        tester = RolePermissionTester(server=server, role_name=f"{main_role} (BASE)")
        tester.run_test_suite(main_test_suite)
        
        print(f"\n✓ Completed: {main_role} (BASE)")
        
        # Step 3: Test MAIN role with each ADD_ON role
        previous_addon = None
        
        for addon_idx, addon_role in enumerate(addon_role_names, start=1):
            print("\n" + "-" * 80)
            print(f"Testing: {main_role} + {addon_role} ({addon_idx}/{len(addon_role_names)})")
            print("-" * 80)
            
            # Add the ADD_ON role
            print(f"\n[1/3] Adding ADD_ON role: {addon_role}")
            try:
                modify_user_role(lims, user_firstname, user_lastname, addon_role, action="add")
            except Exception as e:
                print(f"Error adding ADD_ON role {addon_role}: {e}")
                print("Skipping this add-on combination...")
                continue
            
            # Remove previous ADD_ON role (if exists)
            if previous_addon:
                print(f"[2/3] Removing previous ADD_ON role: {previous_addon}")
                try:
                    modify_user_role(lims, user_firstname, user_lastname, previous_addon, action="remove")
                except Exception as e:
                    print(f"Warning: Could not remove previous ADD_ON role {previous_addon}: {e}")
            else:
                print("[2/3] No previous ADD_ON role to remove")
            
            # Combine test suites: MAIN + ADD_ON permissions
            print(f"[3/3] Running combined permission tests")
            combined_test_suite = {}
            combined_test_suite.update(main_test_suite)  # Add MAIN role tests
            combined_test_suite.update(ADD_ON_ROLE_TEST_SUITES[addon_role])  # Add ADD_ON role tests
            
            # Run combined tests
            combined_role_name = f"{main_role} + {addon_role}"
            tester = RolePermissionTester(server=server, role_name=combined_role_name)
            tester.run_test_suite(combined_test_suite)
            
            print(f"\n✓ Completed: {main_role} + {addon_role}")
            
            # Update previous addon for next iteration
            previous_addon = addon_role
        
        # Clean up: Remove the last ADD_ON role after testing all combinations
        if previous_addon:
            print(f"\nCleaning up ADD_ON role: {previous_addon}")
            try:
                modify_user_role(lims, user_firstname, user_lastname, previous_addon, action="remove")
            except Exception as e:
                print(f"Warning: Could not remove ADD_ON role {previous_addon}: {e}")
        
        print("\n" + "=" * 80)
        print(f"COMPLETED MAIN ROLE: {main_role}")
        print(f"Tested {1 + len(addon_role_names)} combinations (BASE + {len(addon_role_names)} add-ons)")
        print("=" * 80)
        
        # Automatically continue to next MAIN role
        if main_idx < total_main_roles:
            next_main_role = main_role_names[main_idx]
            print(f"\nAutomatically continuing to next MAIN role: {next_main_role}")
            print("(Press Ctrl+C to stop if needed)")
            import time
            time.sleep(2)  # Brief pause to allow Ctrl+C if user wants to stop
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ROLE TESTING COMPLETE")
    print("=" * 80)
    print(f"Total MAIN roles tested: {main_idx}")
    print("=" * 80)
    
    # Generate PDF report if requested
    if generate_pdf:
        print("\n" + "=" * 80)
        print("GENERATING PDF REPORT")
        print("=" * 80)
        try:
            pdf_generator = PDFReportGenerator()
            pdf_file = pdf_generator.generate_pdf()
            print(f"\n✓ PDF report available at: {pdf_file}")
        except Exception as e:
            print(f"\n⚠ Warning: Could not generate PDF report: {e}")
            print("  (Test results are still saved in JSON format)")
        print("=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run permission tests for all MAIN roles with all ADD_ON role combinations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_roles.py "Emil" "Test"
  python run_all_roles.py "Emil" "Test" --server dev
  python run_all_roles.py "John" "Doe" --server staging --account MASTER
  
This script will:
  1. Initialize user to Lab Operator (BTO) role only
  2. For each MAIN role (Lab Operator, System Admin, etc.):
     a) Test MAIN role by itself (BASE)
     b) Test MAIN role + each ADD_ON role (Sample Creation, Editor, etc.)
     c) For each combination, test all permissions from both roles
     d) Prompt to continue to next MAIN role after all ADD_ONs are tested
  3. User always has at least one role assigned

Example testing flow for Lab Operator (BTO):
  - Lab Operator (BTO) (BASE)
  - Lab Operator (BTO) + Sample Creation (BTO)
  - Lab Operator (BTO) + Editor
  - Lab Operator (BTO) + Reagent Manufacturing (BTO)
  - Lab Operator (BTO) + ReviewEscalations
  - Lab Operator (BTO) + ReWork
  [PROMPT: Continue to System Admin (BTO)?]
"""
    )
    
    parser.add_argument("firstname",
                       help="First name of the user to test")
    parser.add_argument("lastname",
                       help="Last name of the user to test")
    parser.add_argument("-s", "--server",
                       default="dev",
                       choices=["dev", "staging", "prod"],
                       help="Server environment (default: dev)")
    parser.add_argument("-a", "--account",
                       default="MASTER",
                       help="Account name for credentials (default: MASTER)")
    parser.add_argument("--no-pdf",
                       action="store_true",
                       help="Skip PDF report generation (default: generate PDF)")
    
    args = parser.parse_args()
    
    run_all_role_tests(
        user_firstname=args.firstname,
        user_lastname=args.lastname,
        server=args.server,
        account=args.account,
        generate_pdf=not args.no_pdf
    )


if __name__ == "__main__":
    main()

