from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class ProductsAdditionPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.grid = self.page.get_by_role("gridcell")
        self.add_to_quote = self.page.get_by_role("button", name="Add to Quote").first

    def addProductListing(self, product_listing: str, term: str, cycle: str, product_name: str, quantity: str):
        wait_for_element(self.grid.nth(1))
        self.grid.nth(1).click()
        self.page.get_by_text(product_listing, exact=True).click()
        time.sleep(self.nw)
        self.grid.nth(2).click()
        normalized_term = str(int(float(term))) if str(term).replace(".", "", 1).isdigit() and float(term).is_integer() else str(term)
        self.page.get_by_text(normalized_term).click()
        time.sleep(self.nw)
        self.grid.nth(3).click()
        self.page.get_by_text(cycle).click()
        row = self.page.locator(
            "cpq-table .cpq-table-body-row",
            has_text=product_name
        )
        row.wait_for(state="visible", timeout=60000)
        row.click()
        qty_cell = row.locator(".col-qty_mp")
        qty_cell.dblclick()
        qty_input = row.locator(".col-qty_mp input")
        qty_input.wait_for(state="visible", timeout=60000)
        normalized_quantity = str(int(float(quantity))) if str(quantity).replace(".", "", 1).isdigit() and float(quantity).is_integer() else str(quantity)
        qty_input.fill(normalized_quantity)
        qty_input.press("Enter")
        self.add_to_quote.click()
        time.sleep(self.nw)
        self.add_to_quote.click()



