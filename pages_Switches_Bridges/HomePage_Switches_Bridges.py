from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageSwitchesBridges:
    nw = 3
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.addToQuote = self.page.locator(
            "//span[@class='oj-button-text' and text()='Add to Quote']"
        )

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
        if subProduct == "Switches/Bridges":
            # Dynamically create the XPath using the subProduct argument
            locator = self.page.locator(
                f"(//*[normalize-space(text())='{subProduct}'])[3]"
            )
            # Wait for the element to be visible
            locator.wait_for(state="visible", timeout=60000)
            # Click on the element
            locator.click()
            self.page.locator("(//a[normalize-space(text())='Configure'])[1]").click()
            time.sleep(self.mw)

    def access_SelectAll(self):
        self.page.get_by_role("tab", name="Access").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("tab", name="Access").click()
        self.page.get_by_role("checkbox", name="Select All").check()
        time.sleep(self.nw)
        self.page.get_by_role("tab", name="Switches").click()
        time.sleep(self.nw)

    def selectManufacturer_Switch(self, manufacturer):
        self.page.get_by_role("combobox", name="Manufacturer").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Manufacturer").click()
        self.page.get_by_role("combobox", name="Manufacturer").click()
        self.page.get_by_role("combobox", name="Manufacturer").fill(manufacturer)
        self.page.get_by_text(manufacturer, exact=True).click()
        time.sleep(self.nw)

    def selectType_Switch(self, switch_type):
        self.page.get_by_role("combobox", name="Type").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Type").click()
        self.page.get_by_role("combobox", name="Type").click()
        self.page.get_by_role("combobox", name="Type").fill(switch_type)
        self.page.get_by_text(switch_type, exact=True).click()
        time.sleep(self.nw)

    def selectPorts_Switch(self, ports):
        self.page.get_by_role("combobox", name="Ports").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Ports").click()
        self.page.get_by_role("combobox", name="Ports").click()
        self.page.get_by_role("combobox", name="Ports").fill(str(ports))
        self.page.get_by_text(str(ports), exact=True).click()
        time.sleep(self.nw)

    def selectCountry_Region_PowerAndRackmount(self, country_region):
        self.page.get_by_role("combobox", name="Country / Region").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Country / Region").click()
        self.page.get_by_role("combobox", name="Country / Region").click()
        self.page.get_by_role("combobox", name="Country / Region").fill(country_region)
        self.page.get_by_text(country_region, exact=True).click()
        time.sleep(self.nw)

    def selectResponseTime_Services(self, response_time):
        self.page.get_by_role("combobox", name="Response Time").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Response Time").click()
        self.page.get_by_role("combobox", name="Response Time").click()
        self.page.get_by_role("combobox", name="Response Time").fill(response_time)
        self.page.get_by_text(response_time, exact=True).click()
        time.sleep(self.nw)

    def selectServiceLevel_Services(self, service_level):
        self.page.get_by_role("combobox", name="Service Level").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Service Level").click()
        self.page.get_by_role("combobox", name="Service Level").click()
        self.page.get_by_role("combobox", name="Service Level").fill(service_level)
        self.page.get_by_text(service_level, exact=True).click()
        time.sleep(self.nw)

    def selectTerm_Services(self, term):
        self.page.get_by_role("combobox", name="Term").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Term").click()
        self.page.get_by_role("combobox", name="Term").click()
        self.page.get_by_role("combobox", name="Term").fill(str(term))
        self.page.get_by_text(str(term), exact=True).click()
        self.page.get_by_role("combobox", name="Term").press("Tab")
        time.sleep(self.nw)

    def clickAgree_PopUp(self):
        try:
            # Wait for the "Agree" button to be visible (up to 5 seconds)
            self.page.get_by_role("button", name="Agree").wait_for(
                state="visible", timeout=5000
            )
            self.page.get_by_role("button", name="Agree").click()
            logger.info("Successfully clicked the 'Agree' button.")
        except TimeoutError:
            # If the button does not appear within 5 seconds, log a warning and continue
            logger.warning(
                "The 'Agree' button popup did not appear within the timeout."
            )
        except Exception as e:
            # Log any unexpected errors that might occur
            logger.error(
                f"An unexpected error occurred while handling the 'Agree' popup: {e}"
            )

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
