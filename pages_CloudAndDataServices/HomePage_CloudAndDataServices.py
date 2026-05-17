from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageCloudAndDataServices:
    nw = 3
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.productName = self.page.locator(
            "(//*[text()='Cloud and Data Services'])[1]"
        )
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")

    def clickProductName(self, product_name):
        if product_name == "Cloud and Data Services":
            wait_for_element(self.productName)
            self.productName.click()
            time.sleep(self.nw)
        else:
            raise ValueError(f"Invalid product name: {product_name}")

    def selectSubProduct(self, sub_Product):
        if sub_Product == "Data Infrastructure Insights - Capacity":
            self.page.locator(
                "//*[text()='Data Infrastructure Insights - Capacity']"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator(
                "//*[text()='Data Infrastructure Insights - Capacity']"
            ).click()
            self.page.locator("(//a[text()='Configure'])[4]").click()
            time.sleep(self.sw)
        else:
            raise ValueError(f"Invalid sub product name: {sub_Product}")

    def enterTenantSN(self):
        # Generate a random 20-digit number starting with 950
        tenantSN = "950" + "".join([str(random.randint(0, 9)) for _ in range(17)])
        self.page.get_by_role("textbox", name="Tenant SN").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("textbox", name="Tenant SN").click()
        self.page.get_by_role("textbox", name="Tenant SN").click()
        self.page.get_by_role("textbox", name="Tenant SN").fill(tenantSN)
        self.page.get_by_role("textbox", name="Tenant SN").press("Tab")
        # Log the generated tenantSN
        logger.info(f"Entered Tenant SN: {tenantSN}")
        time.sleep(self.nw)

    def enterNewQty_HighPerformance(self, qty):
        self.page.get_by_role("gridcell").nth(3).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(3).click()
        self.page.locator('[id="quantity|input"]').click()
        self.page.locator('[id="quantity|input"]').click()
        self.page.locator('[id="quantity|input"]').fill(str(qty))
        self.page.locator('[id="quantity|input"]').press("Tab")
        time.sleep(self.nw)

    def selectBillingFrequency(self, billingFrequency):
        self.page.get_by_role("combobox", name="Required Billing Frequency").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Required Billing Frequency").click()
        self.page.get_by_role("combobox", name="Billing Frequency").fill(
            billingFrequency
        )
        self.page.get_by_text(billingFrequency).click()
        time.sleep(self.nw)

    def enterTermMonths(self, term):
        self.page.get_by_role("spinbutton", name="Term (Months)").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("spinbutton", name="Term (Months)").click()
        self.page.get_by_role("spinbutton", name="Term (Months)").click()
        self.page.get_by_role("spinbutton", name="Term (Months)").fill(str(term))
        self.page.get_by_role("spinbutton", name="Term (Months)").press("Tab")
        time.sleep(self.nw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)
