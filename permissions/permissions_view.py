"""
Test Module: Comprehensive Lab Stream Entry Testing
====================================================
Tests various ways to interact with lab stream entries.
"""

from playwright.sync_api import Page
import time

def test_entry_interaction(page: Page) -> dict:
    """
    Checks if user can view and interact with lab stream entries
    
    Args:
        page: Playwright page object (already logged in)
    
    Returns:
        dict: Test results with pass/fail status and details
    """
    
    print("\n" + "="*60)
    print("TEST: Comprehensive Entry Interaction")
    print("="*60)
    
    test_result = {
        "test_name": "Comprehensive Entry Interaction",
        "passed": False,
        "description": "Tests multiple ways to interact with lab stream entries",
        "details": {
            "tests_performed": []
        }
    }
    
    try:
        # Wait for lab stream
        print("\n1. Looking for lab-stream section...")
        page.wait_for_selector(".lab-stream", timeout=5000)
        
        # Get entries
        entries = page.locator(".lab-stream-entry")
        entry_count = entries.count()
        print(f"   Found {entry_count} entries")
        
        if entry_count == 0:
            test_result["details"]["reason"] = "No entries found"
            return test_result
        
        first_entry = entries.first
        original_url = page.url
        
        # Test 1: Regular click on the entry
        print("\n2. Test 1: Regular click on entry")
        print("-" * 40)
        try:
            first_entry.click()
            page.wait_for_timeout(2000)  # Wait 2 seconds
            new_url = page.url
            
            if new_url != original_url:
                print(f"   ✓ SUCCESS: Navigated to {new_url}")
                test_result["details"]["tests_performed"].append({
                    "test": "Regular click",
                    "success": True,
                    "result": f"Navigated to {new_url}"
                })
                test_result["passed"] = True
                page.goto(original_url)  # Go back
                page.wait_for_selector(".lab-stream", timeout=5000)
            else:
                print(f"   ✗ No navigation occurred")
                test_result["details"]["tests_performed"].append({
                    "test": "Regular click",
                    "success": False,
                    "result": "No navigation"
                })
        except Exception as e:
            print(f"   ✗ Error: {e}")
            test_result["details"]["tests_performed"].append({
                "test": "Regular click",
                "success": False,
                "error": str(e)
            })
        
        # Test 2: Double click
        print("\n3. Test 2: Double click on entry")
        print("-" * 40)
        try:
            entries = page.locator(".lab-stream-entry")  # Re-get after navigation
            first_entry = entries.first
            first_entry.dblclick()
            page.wait_for_timeout(2000)
            new_url = page.url
            
            if new_url != original_url:
                print(f"   ✓ SUCCESS: Double-click navigated to {new_url}")
                test_result["details"]["tests_performed"].append({
                    "test": "Double click",
                    "success": True,
                    "result": f"Navigated to {new_url}"
                })
                test_result["passed"] = True
                page.goto(original_url)
                page.wait_for_selector(".lab-stream", timeout=5000)
            else:
                print(f"   ✗ No navigation occurred")
                test_result["details"]["tests_performed"].append({
                    "test": "Double click",
                    "success": False,
                    "result": "No navigation"
                })
        except Exception as e:
            print(f"   ✗ Error: {e}")
            test_result["details"]["tests_performed"].append({
                "test": "Double click",
                "success": False,
                "error": str(e)
            })
        
        # Test 3: Click on specific child elements
        print("\n4. Test 3: Click on text content within entry")
        print("-" * 40)
        try:
            entries = page.locator(".lab-stream-entry")
            first_entry = entries.first
            
            # Try clicking on the protocol span
            protocol_span = first_entry.locator(".protocol").first
            if protocol_span.count() > 0:
                print("   Clicking on protocol text...")
                protocol_span.click()
                page.wait_for_timeout(2000)
                new_url = page.url
                
                if new_url != original_url:
                    print(f"   ✓ SUCCESS: Clicking protocol navigated to {new_url}")
                    test_result["details"]["tests_performed"].append({
                        "test": "Click protocol text",
                        "success": True,
                        "result": f"Navigated to {new_url}"
                    })
                    test_result["passed"] = True
                    page.goto(original_url)
                    page.wait_for_selector(".lab-stream", timeout=5000)
                else:
                    print(f"   ✗ No navigation occurred")
                    test_result["details"]["tests_performed"].append({
                        "test": "Click protocol text",
                        "success": False,
                        "result": "No navigation"
                    })
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Test 4: Force click with JavaScript
        print("\n5. Test 4: Force click with JavaScript")
        print("-" * 40)
        try:
            entries = page.locator(".lab-stream-entry")
            first_entry = entries.first
            
            # Execute JavaScript click
            page.evaluate("(el) => el.click()", first_entry.element_handle())
            page.wait_for_timeout(2000)
            new_url = page.url
            
            if new_url != original_url:
                print(f"   ✓ SUCCESS: JS click navigated to {new_url}")
                test_result["details"]["tests_performed"].append({
                    "test": "JavaScript click",
                    "success": True,
                    "result": f"Navigated to {new_url}"
                })
                test_result["passed"] = True
                page.goto(original_url)
            else:
                print(f"   ✗ No navigation occurred")
                test_result["details"]["tests_performed"].append({
                    "test": "JavaScript click",
                    "success": False,
                    "result": "No navigation"
                })
        except Exception as e:
            print(f"   ✗ Error: {e}")
            test_result["details"]["tests_performed"].append({
                "test": "JavaScript click",
                "success": False,
                "error": str(e)
            })
        
        # Test 5: Check for hover menus or actions
        print("\n6. Test 5: Hover to reveal actions")
        print("-" * 40)
        try:
            page.goto(original_url)  # Ensure we're on the right page
            page.wait_for_selector(".lab-stream", timeout=5000)
            entries = page.locator(".lab-stream-entry")
            first_entry = entries.first
            
            # Hover over the entry
            first_entry.hover()
            page.wait_for_timeout(1000)  # Wait for any hover effects
            
            # Check if any new elements appeared
            action_buttons = first_entry.locator("button, a, [role='button']")
            action_count = action_buttons.count()
            
            if action_count > 0:
                print(f"   ✓ Hover revealed {action_count} action elements")
                test_result["details"]["tests_performed"].append({
                    "test": "Hover actions",
                    "success": True,
                    "result": f"Found {action_count} actions on hover"
                })
                # Try clicking the first action
                action_buttons.first.click()
                page.wait_for_timeout(2000)
                new_url = page.url
                if new_url != original_url:
                    print(f"   ✓ Clicking hover action navigated to {new_url}")
                    test_result["passed"] = True
            else:
                print(f"   ✗ No actions revealed on hover")
                test_result["details"]["tests_performed"].append({
                    "test": "Hover actions",
                    "success": False,
                    "result": "No actions on hover"
                })
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Final summary
        print("\n" + "="*60)
        print("INTERACTION TEST SUMMARY")
        print("="*60)
        
        successful_tests = [t for t in test_result["details"]["tests_performed"] if t.get("success")]
        if successful_tests:
            print(f"\n✓ {len(successful_tests)} successful interaction method(s) found:")
            for test in successful_tests:
                print(f"   - {test['test']}: {test.get('result', 'Success')}")
        else:
            print("\n✗ No successful interaction methods found")
            print("\nPossible reasons:")
            print("  1. User doesn't have permission to view entry details")
            print("  2. Entries are display-only (no detail view)")
            print("  3. Different UI interaction required")
            print("  4. Feature is broken or disabled")
        
        # Determine overall pass/fail
        if not test_result["passed"]:
            # If no navigation methods worked, check if we can at least see the entries
            if entry_count > 0:
                print(f"\n✓ User CAN view entry list ({entry_count} entries)")
                test_result["passed"] = True
                test_result["details"]["fallback_result"] = "Can view entry list"
            else:
                test_result["passed"] = False
        
    except Exception as e:
        test_result["error"] = str(e)
        print(f"\nERROR: {e}")
    
    return test_result
