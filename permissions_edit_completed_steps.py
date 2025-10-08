"""
Test Module: Can Edit Completed Steps
======================================
Self-contained test for checking if a role can edit completed steps.
"""

from playwright.sync_api import Page, TimeoutError
import time
import re

def test_can_edit_completed_steps(page: Page) -> dict:
    """
    Test if the current user can edit completed steps.
    
    Args:
        page: Playwright page object (already logged in)
    
    Returns:
        dict: Test results with pass/fail status and details
    """
    
    # Define what we're looking for
    EDIT_COMPLETED_CRITERIA = {
        "popup_type": ["modal", "native_dialog"],
        "has_ok_button": True,
        "has_cancel_button": True,
        "minimum_fields": 0,
        "required_text": [
            "Are you sure",
            "edit", 
            "completed step"
        ],
        "modal_title": "Edit Completed Step"
    }
    
    # Run the audit
    print("\n" + "="*60)
    print("TEST: Can Edit Completed Steps")
    print("="*60)
    print("Looking for confirmation dialog when editing completed steps...")
    
    results = audit_edit_permission(page, EDIT_COMPLETED_CRITERIA)
    
    # Prepare test summary
    test_summary = {
        "test_name": "Can Edit Completed Steps",
        "passed": results["passed"],
        "description": "Checks if user gets confirmation when editing completed steps",
        "details": {
            "total_entries": results["total_entries"],
            "entries_checked": results["entries_checked"],
            "entries_with_permission": len(results["entries_with_matching_popup"]),
            "entries_without_permission": len(results["entries_with_non_matching_popup"])
        },
        "raw_results": results
    }
    
    # Print summary
    if test_summary["passed"]:
        print(f"\nRESULT: PASSED - User CAN edit completed steps")
        print(f"Found confirmation dialog in {test_summary['details']['entries_with_permission']} entries")
    else:
        print(f"\nRESULT: FAILED - User CANNOT edit completed steps")
        print(f"No confirmation dialogs found in {test_summary['details']['entries_checked']} entries")
    
    return test_summary


def audit_edit_permission(page: Page, expected_popup_elements: dict = None) -> dict:
    """
    Complete audit of edit permissions by checking all lab-stream-entries.
    Balanced timing: waits for elements to load, but closes popups quickly.
    """
    
    print("="*60)
    print("BALANCED EDIT CONFIRMATION TEST")
    print("="*60)
    print("\nThis version:")
    print("   - Waits for pages to fully load")
    print("   - Ensures Edit button is ready before clicking")
    print("   - Analyzes popups thoroughly")
    print("   - Closes popups quickly after analysis\n")
    print("Expected popup:")
    print("  Title: 'Edit Completed Step?'")
    print("  Text: 'Are you sure you want to edit a completed step?'")
    print("  Buttons: OK and Cancel")
    print("="*60)

    # Default expected elements if none provided
    if expected_popup_elements is None:
        expected_popup_elements = {
            "has_save_button": True,
            "has_cancel_button": True,
            "minimum_fields": 1,
            "popup_type": ["modal", "form", "inline_edit"]
        }
    
    audit_result = {
        "passed": False,
        "total_entries": 0,
        "entries_checked": 0,
        "entries_with_edit_button": 0,
        "entries_without_edit_button": [],
        "entries_with_matching_popup": [],
        "entries_with_non_matching_popup": [],
        "details": [],
        "final_result": ""
    }
    
    try:
        # Wait for lab-stream section
        print("\n" + "="*60)
        print("STARTING COMPLETE EDIT PERMISSION AUDIT (BALANCED)")
        print("="*60)
        
        print("\n1. Looking for lab-stream section...")
        page.wait_for_selector(".lab-stream", timeout=10000)
        print("   Found lab-stream")
        
        # Find all lab-stream-entry elements
        entries = page.locator(".lab-stream-entry")
        entry_count = entries.count()
        audit_result["total_entries"] = entry_count
        
        print(f"\n2. Found {entry_count} lab-stream-entry elements")
        
        if entry_count == 0:
            audit_result["final_result"] = "FAILED: No entries found to test"
            print("   No entries found - Test FAILED")
            return audit_result
        
        # Store the original URL to return to it after each test
        original_url = page.url
        
        # Loop through each entry
        print("\n3. Testing each entry...")
        print("-"*40)
        
        for i in range(entry_count):
            print(f"\nENTRY {i + 1} of {entry_count}:")
            
            # Make sure we're on the original page
            if page.url != original_url:
                print(f"   Returning to original page...")
                page.goto(original_url)
                page.wait_for_selector(".lab-stream", timeout=10000)
                # Re-get entries after navigation
                entries = page.locator(".lab-stream-entry")
            
            entry = entries.nth(i)
            audit_result["entries_checked"] += 1
            
            # Click on this entry to navigate to its page
            print(f"   Clicking on entry {i + 1}...")
            try:
                entry.click()
                # Wait for navigation and page to fully load
                page.wait_for_load_state("networkidle", timeout=5000)
                
                # Additional wait to ensure JavaScript rendering completes
                page.wait_for_timeout(1000)
                
                # Check current URL to confirm navigation
                entry_url = page.url
                if entry_url != original_url:
                    print(f"   Navigated to entry page")
                else:
                    print(f"   WARNING: Still on same page")
                
            except Exception as e:
                print(f"   Failed to navigate to entry: {e}")
                continue
            
            # Look for Edit button on this entry's page
            print(f"   Waiting for Edit button to load...")
            edit_button = wait_for_edit_button(page)
            
            if not edit_button:
                print(f"   No Edit button found after waiting")
                audit_result["entries_without_edit_button"].append(i + 1)
                continue
            
            print(f"   Edit button found and ready")
            audit_result["entries_with_edit_button"] += 1
            
            # Click Edit button and check popup
            print(f"   Clicking Edit button...")
            popup_info = click_and_analyze_popup_balanced(page, edit_button)
            
            # Print debug info
            if popup_info.get('popup_type'):
                print(f"   Detected: {popup_info.get('popup_type')}")
                if popup_info.get('modal_title'):
                    print(f"   Title: {popup_info['modal_title']}")
                if popup_info.get('captured_text'):
                    text_preview = popup_info['captured_text'][:80]
                    if len(popup_info['captured_text']) > 80:
                        text_preview += "..."
                    print(f"   Text: {text_preview}")
            
            # Check if popup matches expected criteria
            matches = check_popup_matches_expected(popup_info, expected_popup_elements)
            
            if matches["is_match"]:
                print(f"   MATCH FOUND!")
                audit_result["entries_with_matching_popup"].append({
                    "entry": i + 1,
                    "popup_info": popup_info,
                    "match_details": matches["details"]
                })
                audit_result["passed"] = True
            else:
                print(f"   No match")
                audit_result["entries_with_non_matching_popup"].append({
                    "entry": i + 1,
                    "popup_info": popup_info,
                    "mismatch_reason": matches["reason"]
                })
            
            # Close the popup quickly after analysis
            print(f"   Closing popup...")
            close_popup_efficiently(page, popup_info.get('popup_type'))
        
        # Determine final verdict
        print("\n" + "="*60)
        print("AUDIT SUMMARY")
        print("="*60)
        
        print(f"\nEntries tested: {audit_result['entries_checked']}/{audit_result['total_entries']}")
        print(f"Entries with Edit button: {audit_result['entries_with_edit_button']}")
        print(f"Entries with matching popup: {len(audit_result['entries_with_matching_popup'])}")
        
        if audit_result["passed"]:
            audit_result["final_result"] = f"PASSED: Found {len(audit_result['entries_with_matching_popup'])} matching popup(s)"
            print(f"\nAUDIT PASSED")
            entries_list = [e['entry'] for e in audit_result['entries_with_matching_popup']]
            print(f"   Matching entries: {entries_list}")
        else:
            if audit_result["entries_with_edit_button"] == 0:
                audit_result["final_result"] = "FAILED: No Edit buttons found"
                print(f"\nAUDIT FAILED: No Edit buttons found")
            else:
                audit_result["final_result"] = "FAILED: No matching popups found"
                print(f"\nAUDIT FAILED: Popups don't match expected criteria")
        
        print("="*60)
        
    except TimeoutError:
        audit_result["final_result"] = "FAILED: Could not find lab-stream section"
        print("FAILED: Timeout finding lab-stream section")
    except Exception as e:
        audit_result["final_result"] = f"FAILED: Error during audit - {str(e)}"
        print(f"FAILED: {e}")
    
    return audit_result


def wait_for_edit_button(page: Page):
    """
    Wait for Edit button to load and be ready to click.
    Tries multiple strategies with proper waiting.
    """
    strategies = [
        ("button:has-text('Edit')", "Button with text 'Edit'"),
        ("button[aria-label*='edit' i]", "Button with edit aria-label"),
        ("button[class*='edit']", "Button with edit class"),
        ("a:has-text('Edit')", "Link with text 'Edit'"),
    ]
    
    # Try each strategy with a reasonable timeout
    for selector, description in strategies:
        try:
            # Wait for the element to be present and visible
            locator = page.locator(selector).first
            if locator.is_visible(timeout=2000):
                # Ensure button is enabled and ready
                page.wait_for_function(
                    f"document.querySelector('{selector}') && !document.querySelector('{selector}').disabled",
                    timeout=1000
                )
                print(f"      Found: {description}")
                return locator
        except:
            continue
    
    # Fallback: try role-based selector
    try:
        locator = page.get_by_role("button", name=re.compile("Edit", re.I)).first
        if locator.is_visible(timeout=2000):
            return locator
    except:
        pass
    
    return None


def click_and_analyze_popup_balanced(page: Page, edit_button) -> dict:
    """
    Click Edit button, wait for popup to appear, then analyze it.
    Balanced timing: proper wait for popup, quick analysis.
    """
    
    # Modal selectors for ExtJS/ISIS and standard modals
    modal_selectors = [
        ".modal",
        "[role='dialog']",
        ".dialog",
        ".popup",
        ".x-window",
        ".isis-message-box",
        "[id*='messagebox']",
        ".x-message-box",
        ".ext-mb-content"
    ]
    
    # Capture state before clicking
    modals_before = page.locator(", ".join(modal_selectors)).count()
    forms_before = page.locator("form").count()
    url_before = page.url
    
    # Set up listener for native dialogs
    dialog_detected = {"type": None, "message": None}
    
    def handle_dialog(dialog):
        dialog_detected["type"] = dialog.type
        dialog_detected["message"] = dialog.message
        # Accept for now to continue testing
        dialog.accept()
    
    page.on("dialog", handle_dialog)
    
    # Click the Edit button
    try:
        # Ensure button is still visible before clicking
        edit_button.scroll_into_view_if_needed()
        edit_button.click()
        
        # Wait for popup/modal to appear
        page.wait_for_timeout(1000)
        
    except Exception as e:
        page.remove_listener("dialog", handle_dialog)
        return {"error": f"Failed to click: {str(e)[:200]}"}
    
    # Remove dialog listener
    page.remove_listener("dialog", handle_dialog)
    
    # Initialize popup info
    popup_info = {
        "popup_type": None,
        "has_save_button": False,
        "has_ok_button": False,
        "has_cancel_button": False,
        "editable_fields": 0,
        "modal_title": None,
        "visible_text": [],
        "captured_text": "",
        "form_labels": []
    }
    
    # Check for native dialog
    if dialog_detected["message"]:
        popup_info["popup_type"] = "native_dialog"
        popup_info["captured_text"] = dialog_detected["message"]
        popup_info["visible_text"] = dialog_detected["message"].split()
        return popup_info
    
    # Check for modal/dialog
    modals_after = page.locator(", ".join(modal_selectors)).count()
    if modals_after > modals_before:
        popup_info["popup_type"] = "modal"
        
        # Wait a moment for modal content to render
        page.wait_for_timeout(300)
        
        # Get modal title - try multiple selectors
        title_selectors = [
            ".x-window-header-text",
            "[id*='_header_hd-textEl']",
            ".modal-title",
            ".dialog-title",
            ".isis-message-box-title",
            "[role='dialog'] h1",
            "[role='dialog'] h2",
            ".modal-header h2",
            ".modal-header h3"
        ]
        
        for selector in title_selectors:
            try:
                titles = page.locator(selector)
                if titles.count() > 0:
                    title_text = titles.first.text_content()
                    if title_text:
                        popup_info["modal_title"] = title_text.strip()
                        break
            except:
                continue
        
        # Get modal content
        content_selectors = [
            ".isis-message-box-text",
            ".x-window-body",
            ".modal-body",
            ".dialog-content",
            "[id*='messagebox'] .x-window-body",
            ".ext-mb-text",
            "[role='dialog'] .content",
            "[role='dialog'] .body"
        ]
        
        for selector in content_selectors:
            try:
                contents = page.locator(selector)
                if contents.count() > 0:
                    text = contents.first.text_content()
                    if text:
                        popup_info["captured_text"] = text.strip()
                        popup_info["visible_text"] = [w.strip() for w in text.split() if w.strip()]
                        break
            except:
                continue
        
        # If still no text, get all text from modal
        if not popup_info["captured_text"]:
            try:
                modal = page.locator(", ".join(modal_selectors)).first
                all_text = modal.text_content()
                if all_text:
                    popup_info["captured_text"] = all_text.strip()
                    popup_info["visible_text"] = [w.strip() for w in all_text.split() if w.strip()]
            except:
                pass
    
    # Check for form/inline edit
    forms_after = page.locator("form").count()
    if forms_after > forms_before and not popup_info["popup_type"]:
        popup_info["popup_type"] = "form"
    
    # Check if URL changed
    if page.url != url_before:
        popup_info["popup_type"] = "page_navigation"
        popup_info["new_url"] = page.url
    
    # Check for buttons
    button_checks = [
        ("save", ["Save", "Update", "Submit"]),
        ("ok", ["OK", "Ok", "Okay", "Confirm", "Yes"]),
        ("cancel", ["Cancel", "Close", "Discard", "No"])
    ]
    
    for button_type, patterns in button_checks:
        for pattern in patterns:
            try:
                button_count = page.locator(f"button:text-is('{pattern}')").count()
                button_count += page.locator(f"button:has-text('{pattern}')").count()
                
                if button_count > 0:
                    if button_type == "save":
                        popup_info["has_save_button"] = True
                    elif button_type == "ok":
                        popup_info["has_ok_button"] = True
                    elif button_type == "cancel":
                        popup_info["has_cancel_button"] = True
                    break
            except:
                continue
    
    # Count editable fields
    try:
        editable = page.locator("input:not([readonly]):not([disabled]):visible, textarea:not([readonly]):not([disabled]):visible, select:not([disabled]):visible")
        popup_info["editable_fields"] = editable.count()
    except:
        pass
    
    # Get form labels
    try:
        labels = page.locator("label:visible")
        if labels.count() > 0:
            popup_info["form_labels"] = [labels.nth(i).text_content().strip() for i in range(min(labels.count(), 10))]
    except:
        pass
    
    # Determine popup type if still unknown
    if not popup_info["popup_type"] and (popup_info["has_save_button"] or popup_info["editable_fields"] > 0):
        popup_info["popup_type"] = "inline_edit"
    
    return popup_info


def close_popup_efficiently(page: Page, popup_type: str = None):
    """
    Close popup quickly but ensure it's actually closed.
    For confirmation dialogs, click Cancel to avoid changes.
    """
    try:
        # For confirmation modals, click Cancel
        if popup_type == "modal":
            cancel_selectors = [
                "button:text-is('Cancel')",
                "button:text-is('No')",
                "button:has-text('Cancel')",
                "button:has-text('Close')"
            ]
            
            for selector in cancel_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible(timeout=500):
                        btn.click()
                        # Wait briefly for modal to close
                        page.wait_for_timeout(300)
                        return
                except:
                    continue
        
        # For inline edits
        if popup_type == "inline_edit":
            try:
                cancel = page.locator("button:has-text('Cancel'), button:has-text('Discard')").first
                if cancel.is_visible(timeout=500):
                    cancel.click()
                    page.wait_for_timeout(300)
                    return
            except:
                pass
        
        # Fallback: Press Escape
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        
    except:
        pass


def check_popup_matches_expected(popup_info: dict, expected: dict) -> dict:
    """Check if popup matches expected criteria."""
    result = {
        "is_match": True,
        "details": [],
        "reason": []
    }
    
    # Check popup type
    if "popup_type" in expected:
        expected_types = expected["popup_type"] if isinstance(expected["popup_type"], list) else [expected["popup_type"]]
        if popup_info.get("popup_type") not in expected_types:
            result["is_match"] = False
            result["reason"].append(f"Popup type '{popup_info.get('popup_type')}' not in expected {expected_types}")
        else:
            result["details"].append(f"Popup type matches: {popup_info.get('popup_type')}")
    
    # Check for buttons
    if expected.get("has_save_button", False) and not popup_info.get("has_save_button"):
        result["is_match"] = False
        result["reason"].append("Expected Save button not found")
    elif expected.get("has_save_button", False):
        result["details"].append("Save button found")
    
    if expected.get("has_ok_button", False) and not popup_info.get("has_ok_button"):
        result["is_match"] = False
        result["reason"].append("Expected OK button not found")
    elif expected.get("has_ok_button", False):
        result["details"].append("OK button found")
    
    if expected.get("has_cancel_button", False) and not popup_info.get("has_cancel_button"):
        result["is_match"] = False
        result["reason"].append("Expected Cancel button not found")
    elif expected.get("has_cancel_button", False):
        result["details"].append("Cancel button found")
    
    # Check minimum fields
    if "minimum_fields" in expected:
        if popup_info.get("editable_fields", 0) < expected["minimum_fields"]:
            result["is_match"] = False
            result["reason"].append(f"Only {popup_info.get('editable_fields', 0)} fields, expected at least {expected['minimum_fields']}")
        else:
            result["details"].append(f"Has {popup_info.get('editable_fields', 0)} editable fields")
    
    # Check for required text
    if "required_text" in expected:
        # Combine all text sources
        all_text_parts = []
        if popup_info.get("visible_text"):
            all_text_parts.append(" ".join(popup_info["visible_text"]))
        if popup_info.get("captured_text"):
            all_text_parts.append(popup_info["captured_text"])
        if popup_info.get("form_labels"):
            all_text_parts.append(" ".join(popup_info["form_labels"]))
        if popup_info.get("modal_title"):
            all_text_parts.append(popup_info["modal_title"])
        
        all_text = " ".join(all_text_parts).lower()
        
        for required in expected["required_text"]:
            if required.lower() not in all_text:
                result["is_match"] = False
                result["reason"].append(f"Required text '{required}' not found")
            else:
                result["details"].append(f"Found required text: '{required}'")
    
    # Check modal title
    if "modal_title" in expected:
        if expected["modal_title"].lower() not in str(popup_info.get("modal_title", "")).lower():
            result["is_match"] = False
            result["reason"].append(f"Modal title '{popup_info.get('modal_title')}' doesn't match expected '{expected['modal_title']}'")
        else:
            result["details"].append(f"Modal title matches: {popup_info.get('modal_title')}")
    
    return result


