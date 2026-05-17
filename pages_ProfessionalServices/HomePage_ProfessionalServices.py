from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageProfessionalServices:
    nw = 3
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.productName = self.page.locator("(//*[text()='Professional Services'])[1]")
        self.selfServiceUsingFirmFixedPriceOrPackagedTimeMaterials_NoButton = (
            self.page.locator("//*[normalize-space(text())='No']")
        )
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

    def clickSelfServiceUsingFirmFixedPriceOrPackagedTimeMaterials_NoButton(self):
        wait_for_element(
            self.selfServiceUsingFirmFixedPriceOrPackagedTimeMaterials_NoButton
        )
        self.selfServiceUsingFirmFixedPriceOrPackagedTimeMaterials_NoButton.click()
        time.sleep(self.nw)

    def clickSubProductName(self, subProduct):
        # Dynamically create the XPath using the subProduct argument
        locator = self.page.locator(f"//*[normalize-space(text())='{subProduct}']")
        # Wait for the element to be visible
        locator.wait_for(state="visible", timeout=60000)
        # Click on the element
        locator.click()
        time.sleep(self.sw)

    def enterQuantity_PS_TMS_CONSLT_DAY_TE(self, qty):
        self.page.get_by_text("0").nth(5).wait_for(state="visible", timeout=60000)
        self.page.get_by_text("0").nth(5).click()
        self.page.locator('[id="tNMPPBHQty|input"]').click()
        self.page.locator('[id="tNMPPBHQty|input"]').fill(str(qty))
        self.page.locator('[id="tNMPPBHQty|input"]').press("Tab")
        time.sleep(self.nw)

    def selectPercentage_PS_TMS_CONSLT_DAY_TE(self, perentage):
        self.page.locator('[id="tNMPPBHServiceType|input"]').wait_for(
            state="visible", timeout=60000
        )
        self.page.locator('[id="tNMPPBHServiceType|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-tNMPPBHServiceType|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-tNMPPBHServiceType|input"]'
        ).fill(perentage)
        self.page.get_by_text(perentage).click()
        time.sleep(self.nw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
