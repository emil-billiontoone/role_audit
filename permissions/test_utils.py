"""
Shared utilities for permission tests
======================================
Common helper functions for all permission test modules.
"""

import os
from datetime import datetime

SCREENSHOT_DIR = "screenshots"
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

