import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://clarity-dev.btolims.com/clarity/login/auth?unauthenticated=1")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("edeguzman")
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill("912087690kMandolin14$")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="PROJECTS & Samples ").click()
    page.get_by_role("textbox", name="Filter...").fill("Emil")
    page.get_by_role("textbox", name="Filter...").click()
    page.get_by_role("textbox", name="Filter...").click()
    page.get_by_role("textbox", name="Filter...").click()
    page.get_by_role("textbox", name="Filter...").fill("Emil Project Test")
    page.locator("#loadmask-1075").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
