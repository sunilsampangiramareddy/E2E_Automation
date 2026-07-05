import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    # Navigate to the Quotes page via the main navigation link
    page.get_by_role("link", name="Quotes", exact=True).click()

    # Open the search type dropdown and choose Quote Number
    page.locator("#combobox-button-261").click()
    page.get_by_role("option", name="Quote Number").click()

    # Enter the quote number in the search field and execute search
    page.get_by_placeholder("Enter minimum 3 characters to").click()
    page.get_by_placeholder("Enter minimum 3 characters to").fill("344256")
    page.get_by_title("Search").click()

    # Change search criteria to Quote Name
    page.locator("#combobox-button-795").click()
    page.locator("#combobox-button-795-1-795").get_by_text("Quote Name").click()

    # Enter the quote name and search again
    page.get_by_placeholder("Enter minimum 3 characters to").click()
    page.get_by_placeholder("Enter minimum 3 characters to").fill(
        "Quote 344256 for Apple Inc. - T"
    )
    page.get_by_title("Search").click()

    # Open the actions menu for the selected quote and click Copy
    page.get_by_role("button", name="Show actions").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("menuitem", name="Copy").click()

    # Switch to the new popup page created by the Copy action
    page1 = page1_info.value
    page1.goto(
        "https://netappinctest10.bigmachines.com/redwood/vp/cx-cpq/application/container/quotes/quotes-detail?id=636529855&mode=live&processVariableName=ucpqStandardCommerceProcess"
    )

    # Verify or interact with the Quote Info tab on the new page
    page1.get_by_role("tab", name=" Quote Info").click()
