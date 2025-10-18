import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://clarity-dev.btolims.com/clarity/login/auth?unauthenticated=1")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("emilusertest")
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill("912087690kMandolin14$")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="Configuration").click()
    page.get_by_text("CONSUMABLES").click()
    page.get_by_text("Controls").click()
    page.get_by_role("button", name="NEW CONTROL").click()
    page.get_by_role("textbox", name="Enter Control Sample Name").click()
    page.get_by_role("textbox", name="Enter Control Sample Name").fill("Emil Control Test")
    page.get_by_role("button", name="Save").click()
    page.locator("#controltypelistview-1092").press("ControlOrMeta+f")
    page.get_by_role("button", name="Delete").click()
    page.get_by_role("button", name="Delete Item").click()
    page.locator("#config-view").press("ControlOrMeta+f")
    page.locator(".right-col").click()
    page.locator("#config-view").press("ControlOrMeta+f")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
