from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageStorageGrid:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")

    def clickProductName(self, product_name):
        # Dynamically create the XPath using the product_name argument
        locator = self.page.locator(
            f"(//*[normalize-space(text())='{product_name}'])[1]"
        )
        # Wait for the element to be visible
        locator.wait_for(state="visible", timeout=60000)
        # Click on the element
        locator.click()
        time.sleep(self.nw)

    def selectSubProduct(self, sub_Product):
        if sub_Product == "StorageGRID Appliance and Software":
            self.page.locator(
                "//*[text()='StorageGRID Appliance and Software']"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator(
                "//*[text()='StorageGRID Appliance and Software']"
            ).click()
            self.page.locator("(//a[text()='Configure'])[1]").click()
            time.sleep(self.sw)
        else:
            raise ValueError(f"Invalid sub product name: {sub_Product}")

    def access_SelectAll(self):
        self.page.get_by_role("tab", name="Access").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("tab", name="Access").click()
        self.page.get_by_role("checkbox", name="Select All").check()
        time.sleep(self.nw)
        self.page.get_by_role("tab", name="Configuration").click()
        time.sleep(self.nw)

    def selectModel_StorageNodes(self, model):
        self.page.locator('[id="SG_Model|input"]').wait_for(
            state="visible", timeout=60000
        )
        self.page.locator('[id="SG_Model|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-SG_Model|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-SG_Model|input"]').fill(model)
        self.page.get_by_text(model).click()
        time.sleep(self.nw)

    def selectDriveType_StorageNodes(self, drive_type):
        self.page.get_by_role("combobox", name="Drive Type", exact=True).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Drive Type", exact=True).click()
        self.page.get_by_role("combobox", name="Drive Type", exact=True).click()
        self.page.get_by_role("combobox", name="Drive Type", exact=True).fill(
            drive_type
        )
        self.page.get_by_text(drive_type).first.click()
        time.sleep(self.nw)

    def enterQty_StorageNodes(self, qty):
        self.page.locator('[id="SG_qty|input"]').wait_for(
            state="visible", timeout=60000
        )
        self.page.locator('[id="SG_qty|input"]').click()
        self.page.locator('[id="SG_qty|input"]').fill(str(qty))
        self.page.locator('[id="SG_qty|input"]').press("Tab")
        time.sleep(self.nw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
