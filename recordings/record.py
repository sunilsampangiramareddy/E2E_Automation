import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/?gws_rd=ssl&zx=1763403449032&no_sw_cr=1")
    page.get_by_role("combobox", name="Search").click()
    page.get_by_role("combobox", name="Search").fill("selenium tutorial guru99")
    page.goto("https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dselenium%2Btutorial%2Bguru99%26sca_esv%3D63c7fd65582f6674%26source%3Dhp%26ei%3Dt2YbaeitH96b4-EPvK6gkQE%26iflsig%3DAOw8s4IAAAAAaRt0x9xNge6K2z4SxSE4N1XZNR3x5kjG%26ved%3D0ahUKEwio5dbg5fmQAxXezTgGHTwXKBIQ4dUDCBA%26uact%3D5%26oq%3Dselenium%2Btutorial%2Bguru99%26gs_lp%3DEgdnd3Mtd2l6IhhzZWxlbml1bSB0dXRvcmlhbCBndXJ1OTkyBRAAGIAEMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSM1YUO0JWNNWcAN4AJABAJgBaKABuw-qAQQyNS4xuAEDyAEA-AEBmAIdoAL6EKgCCsICChAAGAMYjwEY6gLCAgoQLhgDGI8BGOoCwgILEAAYgAQYsQMYgwHCAgUQLhiABMICDhAuGMcBGLEDGNEDGIAEwgIIEAAYgAQYsQPCAgsQLhiABBjHARjRA8ICDhAuGIAEGIoFGLEDGIMBwgIOEC4YgAQYsQMYxwEY0QPCAggQLhiABBixA8ICCxAuGIAEGLEDGIMBwgILEC4YsQMYgAQYigXCAgkQABiABBgKGAuYAw-SBwQyNi4zoAfGpwGyBwQyMy4zuAfiEMIHCDAuOC4xOS4yyAeEAQ%26sclient%3Dgws-wiz%26sei%3DxmYbaZf5H-GP4-EPx6DtmA8&q=EgTKA3kFGMbN7cgGIjBiM4kZZO5rDExD2LTNtHO8i0G-8gc66mZABMXeVYNyo5kXYIIONHp8qFeJYqoAqQsyAVJaAUM")
    #page.locator("iframe[name=\"a-8n69xztd6x0r\"]").content_frame.get_by_role("checkbox", name="I'm not a robot").click()
    page.get_by_role("link", name="Selenium", exact=True).click()
    page.get_by_role("link", name="Read More").click()
    page.get_by_label("Primary Navigation").get_by_role("link", name="SAP").click()
    page.get_by_role("link", name="CRM").click()
    page.get_by_label("Primary Navigation").get_by_role("link", name="Testing").click()
    page.get_by_role("link", name="JUnit").click()
    page.get_by_role("link", name="AI", exact=True).click()
    page.get_by_role("link", name="Data Science").click()
    page.get_by_role("link", name="What is Data Science?", exact=True).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
