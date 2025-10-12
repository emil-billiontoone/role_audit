"""
Test Module: Can Edit Completed Steps
======================================
Checks if a user can edit completed steps correctly.
"""

from playwright.sync_api import Page, expect, TimeoutError
import re

BASE_URL = "https://clarity-dev.btolims.com"

EDIT_CRITERIA = {
    "popup_type": ["modal", "native_dialog"],
    "has_ok_button": True,
    "has_cancel_button": True,
    "required_text": ["Are you sure", "edit", "completed step"],
    "modal_title": "Edit Completed Step"
}


def test_can_edit_completed_steps(page: Page):
    print("\n===== TEST: Can Edit Completed Steps =====")

    home_url = f"{BASE_URL}/clarity/home"
    results = {"passed": False, "reason": None}

    try:
        # Wait for lab-stream section to load
        print(f"Navigating to edit step page")
        page.goto(f"{BASE_URL}/clarity/work-complete/5418879")
        print("Found edit step page")

        # Look for edit button
        edit_button = find_edit_button(page)
        if not edit_button:
            results["reason"] = "No Edit button found"
            print("No Edit button found. Failing test.")
            page.goto(home_url)
            return results

        print("Edit button found — clicking...")
        popup_info = click_and_capture_popup(page, edit_button)

        print("Analyzing popup...")
        match_result = verify_popup(popup_info, EDIT_CRITERIA)

        if not match_result["is_match"]:
            print("Popup does not match expected criteria:")
            for r in match_result["reason"]:
                print(f"   - {r}")
            results["reason"] = "; ".join(match_result["reason"])
            page.goto(home_url)
            return results

        print("Popup matches expected criteria.")
        results["passed"] = True
        results["reason"] = "Edit confirmation popup validated successfully."
        page.goto(home_url)
        return results

    except TimeoutError:
        print("Timeout waiting for lab-stream section")
        results["reason"] = "Timeout waiting for lab-stream section"
    except Exception as e:
        print(f"Unexpected error: {e}")
        results["reason"] = str(e)

    # Always return home
    try:
        page.goto(home_url)
    except:
        pass

    return results


# ---------------- Helper functions ---------------- #

def find_edit_button(page: Page):
    """Try multiple selectors to find an Edit button."""
    selectors = [
        "button:has-text('Edit')",
        "button[aria-label*='edit' i]",
        "button[class*='edit']",
        "a:has-text('Edit')"
    ]
    for s in selectors:
        try:
            locator = page.locator(s).first
            if locator.is_visible(timeout=2000):
                print(f"   Found edit button ({s})")
                return locator
        except:
            continue
    return None


def click_and_capture_popup(page: Page, edit_button):
    """Click edit button and detect modal or native popup."""
    popup_info = {
        "popup_type": None,
        "modal_title": None,
        "captured_text": "",
        "has_ok_button": False,
        "has_cancel_button": False
    }

    dialog_info = {"message": None}

    def handle_dialog(dialog):
        dialog_info["message"] = dialog.message
        dialog.accept()

    page.on("dialog", handle_dialog)

    # Click and wait a bit
    edit_button.click()
    page.wait_for_timeout(1000)
    page.remove_listener("dialog", handle_dialog)

    # Native dialog case
    if dialog_info["message"]:
        popup_info["popup_type"] = "native_dialog"
        popup_info["captured_text"] = dialog_info["message"]
        return popup_info

    # Modal detection
    modal_selector = ".modal, [role='dialog'], .x-window, .popup"
    modals = page.locator(modal_selector)
    if modals.count() > 0:
        popup_info["popup_type"] = "modal"
        modal = modals.first
        try:
            popup_info["captured_text"] = modal.text_content().strip()
        except:
            pass

        # Title check
        for tsel in [".modal-title", ".x-window-header-text", "[role='dialog'] h2"]:
            try:
                title_el = modal.locator(tsel)
                if title_el.count() > 0:
                    popup_info["modal_title"] = title_el.first.text_content().strip()
                    break
            except:
                continue

        # Button checks
        for ok_text in ["OK", "Ok", "Yes", "Confirm"]:
            if page.locator(f"button:has-text('{ok_text}')").count() > 0:
                popup_info["has_ok_button"] = True
                break

        for cancel_text in ["Cancel", "No", "Close"]:
            if page.locator(f"button:has-text('{cancel_text}')").count() > 0:
                popup_info["has_cancel_button"] = True
                break

    return popup_info


def verify_popup(popup, expected):
    """Compare popup properties with expected criteria."""
    result = {"is_match": True, "reason": []}

    # Type
    if popup.get("popup_type") not in expected["popup_type"]:
        result["is_match"] = False
        result["reason"].append(
            f"Unexpected popup type: {popup.get('popup_type')}"
        )

    # Buttons
    if expected["has_ok_button"] and not popup.get("has_ok_button"):
        result["is_match"] = False
        result["reason"].append("Missing OK button")

    if expected["has_cancel_button"] and not popup.get("has_cancel_button"):
        result["is_match"] = False
        result["reason"].append("Missing Cancel button")

    # Text
    text_blob = (
        (popup.get("captured_text") or "") + " " + (popup.get("modal_title") or "")
    ).lower()
    for phrase in expected["required_text"]:
        if phrase.lower() not in text_blob:
            result["is_match"] = False
            result["reason"].append(f"Missing text: '{phrase}'")

    # Modal title
    if expected.get("modal_title") and popup.get("modal_title"):
        if expected["modal_title"].lower() not in popup["modal_title"].lower():
            result["is_match"] = False
            result["reason"].append(
                f"Title mismatch: expected '{expected['modal_title']}', got '{popup['modal_title']}'"
            )

    return result