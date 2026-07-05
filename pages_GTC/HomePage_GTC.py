from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageGTC:
    nw = 2
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.gtcTab = self.page.locator(
            "//span[normalize-space()='Global Trade Compliance']"
        )
        self.endCustomerDRCheckbox = self.page.locator(
            "(//*[contains(@class, 'IconStyle_currentColor__sdo2n67')])[1]"
        )
        self.endCustomerENACheckbox = self.page.locator(
            "(//*[contains(@class, 'IconStyle_currentColor__sdo2n67')])[2]"
        )
        self.endCustomerENACheckbox_2 = self.page.locator(
            "(//*[contains(@class, 'IconStyle_currentColor__sdo2n67')])[1]"
        )
        self.shipToCustomerENACheckbox = self.page.locator(
            "(//*[contains(@class, 'IconStyle_currentColor__sdo2n67')])[2]"
        )
        self.shipToCustomerENACheckbox_2 = self.page.locator(
            "(//*[contains(@class, 'IconStyle_currentColor__sdo2n67')])[2]"
        )
        self.shipToCustomerDRCheckbox = self.page.locator(
            "(//*[contains(@class, 'IconStyle_currentColor__sdo2n67')])[1]"
        )

    def clickGTCTab(self): 
        wait_for_element(self.gtcTab)
        self.gtcTab.click()
        time.sleep(self.sw)

    def isGTCriskTextVisible(self) -> bool:
        try:
            # Locate the element using the XPath
            element = self.page.locator(
                "//div[@id='txn-header-msgs' and contains(text(), 'This quote has an identified GTC risk.')]"
            )
            # Check if the element exists and is visible
            if element.count() > 0 and element.is_visible():
                # Get the text content of the element
                element_text = element.text_content()
                # Check if the text contains 'GTC risk' and return True/False
                return "GTC risk" in element_text
            else:
                # Element does not exist or is not visible, return False
                logger.info("GTC risk text not found or not visible.")
                return False
        except Exception as e:
            # Handle exceptions (e.g., locator issues)
            logger.error(f"Error occurred while checking GTC risk text: {e}")
            return False

    def selectEndCustomerDRCheckbox(self):
        wait_for_element(self.endCustomerDRCheckbox)
        self.endCustomerDRCheckbox.click()
        self.endCustomerDRCheckbox.press("Tab")
        time.sleep(self.nw)

    def selectEndCustomerENACheckbox(self):
        wait_for_element(self.endCustomerENACheckbox)
        self.endCustomerENACheckbox.click()
        self.endCustomerENACheckbox.press("Tab")
        time.sleep(self.nw)

    def selectEndCustomerENACheckbox_2(self):
        wait_for_element(self.endCustomerENACheckbox_2)
        self.endCustomerENACheckbox_2.click()
        self.endCustomerENACheckbox_2.press("Tab")
        time.sleep(self.nw)

    def selectShipToCustomerENACheckbox(self):
        wait_for_element(self.shipToCustomerENACheckbox)
        self.shipToCustomerENACheckbox.click()
        self.shipToCustomerENACheckbox.press("Tab")
        time.sleep(self.nw)

    def selectShipToCustomerENACheckbox_2(self):
        wait_for_element(self.shipToCustomerENACheckbox_2)
        self.shipToCustomerENACheckbox_2.click()
        self.shipToCustomerENACheckbox_2.press("Tab")
        time.sleep(self.nw)

    def selectShipToCustomerDRCheckbox(self):
        wait_for_element(self.shipToCustomerDRCheckbox)
        self.shipToCustomerDRCheckbox.click()
        self.shipToCustomerDRCheckbox.press("Tab")
        time.sleep(self.nw)

    def enterDROverrideJustification(self, justification):
        self.page.get_by_role("textbox", name="DR Override Justification (").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("textbox", name="DR Override Justification (").click()
        self.page.get_by_role("textbox", name="DR Override Justification (").click()
        self.page.get_by_role("textbox", name="DR Override Justification (").fill(
            justification
        )
        self.page.get_by_role("textbox", name="DR Override Justification (").press(
            "Tab"
        )
        time.sleep(self.nw)

    def enterDROverrideJustification_2(self, justification):
        self.page.locator("//textarea[@id='_rczp59qajxs-input']").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("//textarea[@id='_rczp59qajxs-input']").click()
        self.page.locator("//textarea[@id='_rczp59qajxs-input']").click()
        self.page.locator("//textarea[@id='_rczp59qajxs-input']").fill(justification)
        self.page.locator("//textarea[@id='_rczp59qajxs-input']").press("Tab")
        time.sleep(self.nw)

    def selectOverrideImportControlCheckbox(self):
        self.page.get_by_role(
            "list", name="List of fields of section Import Control"
        ).get_by_label("", exact=True).wait_for(state="visible", timeout=60000)
        self.page.get_by_role(
            "list", name="List of fields of section Import Control"
        ).get_by_label("", exact=True).check()
        time.sleep(self.nw)

    def clickOverrideGTCButton(self):
        self.page.get_by_role("button", name="Override GTC").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Override GTC").click()
        time.sleep(self.mw)
