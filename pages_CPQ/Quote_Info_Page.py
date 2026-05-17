from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class QuoteInfoPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.quoteInfoTab = self.page.get_by_role("tab", name=" Quote Info")
        self.keystone = self.page.locator("(//input[@role='combobox'])[3]")

    def clickQuoteInfoTab(self):
        wait_for_element(self.quoteInfoTab)
        self.quoteInfoTab.click()
        time.sleep(self.sw)

    def enterKeystone(self, option: str):
        wait_for_element(self.keystone)
        self.keystone.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{option}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def check_OverrideInvalidLODPart(self):
        self.page.get_by_role(
            "list", name="List of fields of section Quote Info"
        ).get_by_label("", exact=True).wait_for(state="visible", timeout=60000)
        self.page.get_by_role(
            "list", name="List of fields of section Quote Info"
        ).get_by_label("", exact=True).check()
        time.sleep(self.sw)
