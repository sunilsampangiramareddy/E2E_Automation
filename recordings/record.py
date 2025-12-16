import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.guru99.com/")
    page.get_by_role("link", name="Home").click()
    page.get_by_label("Primary Navigation").get_by_role("link", name="Testing").click()
    page.get_by_label("Primary Navigation").get_by_role("link", name="SAP", exact=True).click()
    page.get_by_role("link", name="Web").click()
    page.get_by_label("Primary Navigation").get_by_role("link", name="Big Data").click()
    page.get_by_role("link", name="AI", exact=True).click()
    page.get_by_role("button", name="Testing", exact=True).click()
    page.get_by_role("button", name="SAP", exact=True).click()
    page.get_by_role("button", name="Web", exact=True).click()
    page.get_by_role("button", name="Must Learn!").click()
    page.get_by_role("link", name="➤ Java", exact=True).click()
    page.get_by_role("link", name="What is Java?").click()
    page.get_by_role("button", name="Expand Table of Contents").click()
    page.get_by_role("link", name="What is Java?").click()
    page.get_by_role("link", name="What is Java Platform?").click()
    page.get_by_role("link", name="Java Definition and Meaning").click()
    page.get_by_role("link", name="MySQL").click()
    page.get_by_role("link", name="What is a Database?").click()
    page.get_by_role("button", name="Expand Table of Contents").click()
    page.get_by_role("link", name="Types of Databases").click()
    page.get_by_role("link", name="Data Warehouse").click()
