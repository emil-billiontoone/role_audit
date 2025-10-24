"""
Shared utilities for permission tests
======================================
Common helper functions for all permission test modules.
"""

import os
from datetime import datetime

SCREENSHOT_DIR = "test_results/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def capture_screenshot(page, test_name, status=""):
    """
    Helper function to capture screenshot with readable timestamp.
    
    Args:
        page: Playwright page object
        test_name: Name of the test (e.g., "create_sample")
        status: Optional status suffix (e.g., "pass", "fail")
    
    Returns:
        tuple: (screenshot_path, success_boolean)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    status_suffix = f"_{status}" if status else ""
    screenshot_file = os.path.join(SCREENSHOT_DIR, f"{test_name}{status_suffix}_{timestamp}.png")
    
    try:
        page.screenshot(path=screenshot_file, full_page=False)
        print(f"Screenshot captured: {screenshot_file}")
        return screenshot_file, True
    except Exception as e:
        error_msg = f"Failed to capture screenshot: {e}"
        print(error_msg)
        return error_msg, False


def clean_error_message(error):
    """
    Clean up verbose error messages for cleaner reporting.
    
    Playwright errors often include verbose "Call log:" sections that are
    useful for debugging but clutter reports. This extracts just the main error.
    
    Args:
        error: Exception object or string
    
    Returns:
        str: Cleaned error message
    
    Examples:
        >>> error = "Timeout 30000ms exceeded.\\nCall log:\\n  - waiting for..."
        >>> clean_error_message(error)
        'Timeout 30000ms exceeded.'
    """
    error_str = str(error)
    
    # Remove verbose Playwright call logs
    if "Call log:" in error_str:
        error_str = error_str.split("Call log:")[0].strip()
    
    # Remove excessive whitespace/newlines
    error_str = " ".join(error_str.split())
    
    # Truncate very long error messages (keep first 200 chars)
    if len(error_str) > 200:
        error_str = error_str[:197] + "..."
    
    return error_str

