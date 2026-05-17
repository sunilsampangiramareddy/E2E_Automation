import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.get_by_role("link", name="Quotes", exact=True).click()
    page.locator("#combobox-button-261").click()
    page.get_by_role("option", name="Quote Number").click()
    page.get_by_placeholder("Enter minimum 3 characters to").click()
    page.get_by_placeholder("Enter minimum 3 characters to").fill("344256")
    page.get_by_title("Search").click()
    page.locator("#combobox-button-795").click()
    page.locator("#combobox-button-795-1-795").get_by_text("Quote Name").click()
    page.get_by_placeholder("Enter minimum 3 characters to").click()
    page.get_by_placeholder("Enter minimum 3 characters to").fill(
        "Quote 344256 for Apple Inc. - T"
    )
    page.get_by_title("Search").click()
    page.get_by_role("button", name="Show actions").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("menuitem", name="Copy").click()
    page1 = page1_info.value
    page1.goto(
        "https://netappinctest10.bigmachines.com/redwood/vp/cx-cpq/application/container/quotes/quotes-detail?id=636529855&mode=live&processVariableName=ucpqStandardCommerceProcess"
    )
    page1.get_by_role("tab", name=" Quote Info").click()
