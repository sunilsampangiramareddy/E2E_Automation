from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageSoftware:
    nw = 3
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")

    def selectProductName(self, product_name):
        # Dynamically create the XPath using the product_name argument
        locator = self.page.locator(
            f"(//*[normalize-space(text())='{product_name}'])[1]"
        )
        # Wait for the element to be visible
        locator.wait_for(state="visible", timeout=60000)
        # Click on the element
        locator.click()
        time.sleep(self.nw)

    def selectSubProductName(self, subProduct):
        if subProduct == "ONTAP Select":
            # Dynamically create the XPath using the subProduct argument
            locator = self.page.locator(f"//*[normalize-space(text())='{subProduct}']")
            # Wait for the element to be visible
            locator.wait_for(state="visible", timeout=60000)
            # Click on the element
            locator.click()
            self.page.locator("(//a[normalize-space(text())='Configure'])[5]").click()
            time.sleep(self.mw)

    def access_SelectAll(self):
        self.page.get_by_role("tab", name="Access").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("tab", name="Access").click()
        self.page.get_by_role("checkbox", name="Select All").check()
        time.sleep(self.nw)
        self.page.get_by_role("tab", name="Configuration").click()
        time.sleep(self.nw)

    def selectBuy_Configuration(self, buy_option):
        self.page.get_by_role("tab", name="Configuration").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("tab", name="Configuration").click()
        self.page.get_by_role("combobox", name="Buy").click()
        self.page.get_by_role("combobox", name="Buy").fill(buy_option)
        self.page.get_by_text(buy_option, exact=True).first.click()
        time.sleep(self.nw)

    def enterStandard_Licenses(self, standard_licenses):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-tB_ontapSelect"
        ).first.wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-tB_ontapSelect"
        ).first.click()
        self.page.locator('[id="tB_ontapSelect|input"]').click()
        self.page.locator('[id="tB_ontapSelect|input"]').click()
        self.page.locator('[id="tB_ontapSelect|input"]').fill(str(standard_licenses))
        self.page.locator('[id="tB_ontapSelect|input"]').press("Tab")
        time.sleep(self.sw)

    def enterSoftwareSupportTermMonths_Services(self, support_term_months):
        self.page.get_by_role(
            "spinbutton", name="Software Support Term (Months)"
        ).wait_for(state="visible", timeout=60000)
        self.page.get_by_role(
            "spinbutton", name="Software Support Term (Months)"
        ).click()
        self.page.get_by_role(
            "spinbutton", name="Software Support Term (Months)"
        ).click()
        self.page.get_by_role("spinbutton", name="Software Support Term (Months)").fill(
            str(support_term_months)
        )
        self.page.get_by_role(
            "spinbutton", name="Software Support Term (Months)"
        ).press("Tab")
        time.sleep(self.sw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
