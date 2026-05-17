from playwright.sync_api import Page, expect, TimeoutError
import time
import logging
from datetime import datetime, timedelta

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageKeystone:
    nw = 2
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.keystoneStorageAsServiceV3 = self.page.locator(
            "//span[text()='Keystone Storage-as-a-Service v3']"
        )
        self.orderType = self.page.locator("(//input[@role='combobox'])[3]")
        self.targetSiteDate = self.page.locator("(//input[@role='combobox'])[2]")
        self.targetStartDate = self.page.locator(
            "//input[@type='text' and @role='combobox' and @id='targetSiteReadinessDate_KFS|input']"
        )
        self.keystoneServicesTab = self.page.locator(
            "//a[normalize-space()='Keystone Services']"
        )
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")

    def clickProductName(self, productName: str):
        if productName == "Keystone Storage-as-a-Service v3":
            wait_for_element(self.keystoneStorageAsServiceV3)
            self.keystoneStorageAsServiceV3.click()
            time.sleep(self.nw)
            self.page.locator("(//a[text()='Configure'])[2]").click()
            time.sleep(self.mw)
        else:
            raise ValueError(f"Invalid product name: {productName}")

    def selectOrderType(self, orderType: str):
        wait_for_element(self.orderType)
        self.orderType.click()
        time.sleep(self.nw)
        xpath = f"//span[text()='{orderType}']"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def selectTargetSiteDate(self):
        # Get the current date in DD/MM/YYYY format
        current_date = datetime.now().strftime(
            "%d/%m/%Y"
        )  # Format the date as DD/MM/YYYY
        wait_for_element(self.targetSiteDate)
        self.targetSiteDate.click()
        self.targetSiteDate.fill(current_date)
        self.targetSiteDate.press("Tab")
        time.sleep(self.sw)

    def selectTargetStartDate(self):
        # Calculate the current date + 10 days
        future_date = (datetime.now() + timedelta(days=10)).strftime(
            "%d/%m/%Y"
        )  # Format as DD/MM/YYYY
        wait_for_element(self.targetStartDate)
        self.targetStartDate.click()
        self.targetStartDate.fill(future_date)
        self.targetStartDate.press("Tab")
        time.sleep(self.sw)

    def clickKeystoneServicesTab(self):
        wait_for_element(self.keystoneServicesTab)
        self.keystoneServicesTab.click()
        time.sleep(self.sw)

    def selectDataType(self, dataType: str):
        self.page.locator(
            "//div[contains(@class, 'cpq-table-data-cell') and contains(@class, 'col-dataType_KS')]"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//div[contains(@class, 'cpq-table-data-cell') and contains(@class, 'col-dataType_KS')]"
        ).dblclick()
        time.sleep(self.nw)
        self.page.locator(
            "//input[@id='oj-searchselect-filter-dataType_KS|input' and @class='oj-inputtext-input oj-text-field-input oj-component-initnode' and @type='text']"
        ).click()
        self.page.locator(
            "//input[@id='oj-searchselect-filter-dataType_KS|input' and @class='oj-inputtext-input oj-text-field-input oj-component-initnode' and @type='text']"
        ).fill(dataType)
        xpath = f"//span[text()='{dataType}']"
        self.page.locator(xpath).click()
        time.sleep(self.sw)

    def selectServiceLevel(self, serviceLevel: str):
        self.page.get_by_role("gridcell").nth(2).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(2).click()
        time.sleep(self.nw)
        self.page.locator('[id="serviceLevel_KS|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-serviceLevel_KS|input"]').fill(
            serviceLevel
        )
        self.page.get_by_text(serviceLevel, exact=True).click()
        time.sleep(self.sw)

    def enterTotalCapacityCommitted(self, totalCapacity: str):
        self.page.locator(
            "//div[@role='gridcell' and contains(@class, 'col-quantity_KS')]"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//div[@role='gridcell' and contains(@class, 'col-quantity_KS')]"
        ).dblclick()
        time.sleep(self.nw)
        self.page.locator(
            "//input[@id='quantity_KS|input' and @role='spinbutton' and @aria-invalid='true']"
        ).click()
        self.page.locator(
            "//input[@id='quantity_KS|input' and @role='spinbutton' and @aria-invalid='true']"
        ).fill(str(totalCapacity))
        time.sleep(self.sw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
