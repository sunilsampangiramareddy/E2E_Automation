from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageEAndEFSeries:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.productName = self.page.locator("(//*[text()='E/EF-Series'])[1]")
        self.SelfServiceUsingFirmFixedPriceOrPackagedTimeMaterials_NoButton = (
            self.page.locator("")
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

    def selectSubProduct(self, sub_Product):
        if sub_Product == "EF-SERIES (New Systems and Add On Storage) (Legacy)":
            self.page.locator(
                "//*[text()='EF-SERIES (New Systems and Add On Storage) (Legacy)']"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator(
                "//*[text()='EF-SERIES (New Systems and Add On Storage) (Legacy)']"
            ).click()
            self.page.locator("(//a[text()='Configure'])[2]").click()
            time.sleep(self.sw)
        elif sub_Product == "E-SERIES (New Systems and Add On Storage) (Legacy)":
            self.page.locator(
                "//*[text()='E-SERIES (New Systems and Add On Storage) (Legacy)']"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator(
                "//*[text()='E-SERIES (New Systems and Add On Storage) (Legacy)']"
            ).click()
            self.page.locator("(//a[text()='Configure'])[1]").click()
            time.sleep(self.sw)
        else:
            raise ValueError(f"Invalid sub product name: {sub_Product}")

    def select_SubProduct(self, sub_Product):
        try:
            # Construct the XPath with the parameterized sub_Product
            xpath = f"//a[contains(@href, 'templateName={sub_Product}')]"
            # Wait for the element to be visible
            self.page.locator(xpath).wait_for(state="visible", timeout=60000)
            # Click the element
            self.page.locator(xpath).click()
            time.sleep(self.sw)
        except Exception as e:
            print(f"Error selecting sub product {sub_Product}: {e}")

    def access_SelectAll(self):
        self.page.get_by_role("tab", name="Access").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("tab", name="Access").click()
        self.page.get_by_role("checkbox", name="Select All").check()
        time.sleep(self.nw)
        self.page.get_by_role("tab", name="System").click()
        time.sleep(self.nw)

    def selectModel_System(self, model):
        self.page.get_by_role("combobox", name="Model").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Model").click()
        self.page.get_by_role("combobox", name="Model").click()
        self.page.get_by_role("combobox", name="Model").fill(model)
        self.page.get_by_text(model).first.click()
        time.sleep(self.nw)

    def selectControllerMemory_System(self, controllerMemory):
        self.page.get_by_role("combobox", name="Controller Memory").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Controller Memory").click()
        self.page.get_by_role("combobox", name="Controller Memory").click()
        self.page.get_by_role("combobox", name="Controller Memory").fill(
            controllerMemory
        )
        self.page.get_by_text(controllerMemory).first.click()
        time.sleep(self.nw)

    def selectEnclosure_BaseStorageOptions(self, enclosure):
        self.page.get_by_role("combobox", name="4RU-60Drive (DE6600 and").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="4RU-60Drive (DE6600 and").click()
        self.page.get_by_role("combobox", name="Enclosure").click()
        self.page.get_by_role("combobox", name="Enclosure").click()
        self.page.get_by_role("combobox", name="Enclosure").fill(enclosure)
        self.page.get_by_text(enclosure).click()
        time.sleep(self.nw)

    def selectCapacityStorage(self, capacity):
        self.page.get_by_role("gridcell").nth(2).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(2).click()
        self.page.locator('[id="capacity_eSeriesBaseStorage|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-capacity_eSeriesBaseStorage|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-capacity_eSeriesBaseStorage|input"]'
        ).fill(capacity)
        self.page.get_by_text(capacity).click()
        time.sleep(self.nw)

    def enterQtyPerEnclosure_Storage(self, qty):
        self.page.get_by_role("gridcell", name="0").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell", name="0").click()
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').click()
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').click()
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').fill(str(qty))
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').press("Tab")
        time.sleep(self.nw)

    def enterQtyPerEnclosure_Storage_2(self, qty):
        self.page.get_by_role("gridcell", name="0").last.wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell", name="0").last.click()
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').click()
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').click()
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').fill(str(qty))
        self.page.locator('[id="qty_eSeriesBaseStorage|input"]').press("Tab")
        time.sleep(self.nw)

    def selectEncryption_Storage(self, encryption):
        self.page.get_by_role("gridcell").nth(1).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(1).click()
        self.page.locator('[id="encryption_eSeriesBaseStorage|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-encryption_eSeriesBaseStorage|input"]'
        ).fill(encryption)
        self.page.get_by_text(encryption).click()
        time.sleep(self.nw)

    def selectCard_HIC(self, card):
        self.page.get_by_role("combobox", name="Card").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Card").click()
        self.page.get_by_role("combobox", name="Card").click()
        self.page.get_by_role("combobox", name="Card").fill(card)
        self.page.get_by_text(card).click()
        time.sleep(self.nw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
