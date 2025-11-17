import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://netapp2--uat.sandbox.lightning.force.com/")
    page.get_by_role("textbox", name="Email Address").click()
    page.get_by_role("textbox", name="Email Address").fill("apptestmbob4@netapp.com")
    page.get_by_role("button", name="Next").click()
   
    page.get_by_role("textbox", name="Enter the password for").click()
    page.get_by_role("textbox", name="Enter the password for").fill("T7k@X8~{9j=*RYWh")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("button", name="Yes").click()
   
    expect(page.locator("div").filter(has_text=re.compile(r"^Sales$")).nth(1)).to_be_visible()
    expect(page.get_by_label("Global", exact=True).get_by_role("list")).to_contain_text("Opportunities")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
