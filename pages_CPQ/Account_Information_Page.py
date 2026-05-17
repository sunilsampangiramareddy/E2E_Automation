from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class AccountInformationPage:
    nw = 4
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.accountInformationTab = self.page.locator(
            '//*[@id="cx-cpq-58ddf3ec-ff14-45d4-8d77-303c703c2c48"]/div/div'
        )
        self.shippingMethod = self.page.get_by_role("combobox", name="Shipping Method")
        self.shippingInstructions = self.page.get_by_role(
            "textbox", name="Shipping Instructions"
        )

    def clickAccountInformationTab(self):
        wait_for_element(self.accountInformationTab)
        self.accountInformationTab.click()
        time.sleep(self.sw)

    def enterSoldTo(self, first_name, last_name):
        self.page.get_by_title("Sold To").wait_for(state="visible", timeout=60000)
        self.page.get_by_title("Sold To").click()
        self.page.wait_for_selector(
            "(//span[contains(text(),'Edit')])[1]",
            state="visible",
            timeout=60000,
        )
        self.page.locator("(//span[contains(text(),'Edit')])[1]").click()
        time.sleep(self.nw)
        self.page.get_by_label("Search Type :").wait_for(state="visible", timeout=60000)
        self.page.get_by_label("Search Type :").select_option("Contact")
        time.sleep(self.nw)
        self.page.get_by_role("textbox", name="First Name").click()
        self.page.get_by_role("textbox", name="First Name").fill(first_name)
        self.page.get_by_role("textbox", name="Last Name").click()
        self.page.get_by_role("textbox", name="Last Name").fill(last_name)
        self.page.get_by_role("button", name="Search").click()
        self.page.get_by_role("button", name="Select").first.click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    def enterBillTo(self):
        self.page.get_by_title("Bill To").wait_for(state="visible", timeout=60000)
        self.page.get_by_title("Bill To").click()
        self.page.locator("(//span[contains(text(),'Edit')])[2]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//span[contains(text(),'Edit')])[2]").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Set").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Set").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    def enterEndCustomer(self, first_name, last_name):
        self.page.get_by_text("End Customer").wait_for(state="visible", timeout=60000)
        self.page.get_by_text("End Customer").click()
        self.page.locator("(//span[contains(text(),'Edit')])[3]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//span[contains(text(),'Edit')])[3]").click()
        time.sleep(self.nw)
        self.page.get_by_role("textbox", name="First Name").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("textbox", name="First Name").click()
        self.page.get_by_role("textbox", name="First Name").fill(first_name)
        self.page.get_by_role("textbox", name="Last Name").click()
        self.page.get_by_role("textbox", name="Last Name").fill(last_name)
        self.page.get_by_role("button", name="Search").click()
        self.page.get_by_role("button", name="Select").first.click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    def enterSoftwareDelivery(self):
        self.page.get_by_text("Software Delivery").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_text("Software Delivery").click()
        self.page.wait_for_selector(
            "(//span[contains(text(),'Edit')])[4]",  # XPath selector for the element
            state="visible",
            timeout=60000,
        )
        self.page.locator("(//span[contains(text(),'Edit')])[4]").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Set").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Set").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    # This method is for Service customer 4th place holder
    def enterServiceCustomer(self):
        self.page.locator("(//div[@title='Service Customer'])[1]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//div[@title='Service Customer'])[1]").click()
        self.page.locator("(//span[contains(text(),'Edit')])[4]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//span[contains(text(),'Edit')])[4]").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Set").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Set").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    # This method is for Service customer 6th place holder
    def enterServiceCustomer_2(self):
        self.page.locator("(//div[@title='Service Customer'])[1]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//div[@title='Service Customer'])[1]").click()
        self.page.locator("(//span[contains(text(),'Edit')])[6]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//span[contains(text(),'Edit')])[6]").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Set").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Set").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    # This method is for the scenario where ShipTo Customer is same as SoldTo Customer
    def enterShipToCustomer(self):
        self.page.get_by_text("Ship To Customer").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_text("Ship To Customer").click()
        self.page.locator("(//span[contains(text(),'Edit')])[5]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//span[contains(text(),'Edit')])[5]").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Set").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Set").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    # This method is for the scenario where ShipTo Customer is same as End Customer
    def enterShipToCustomer_2(self):
        self.page.get_by_text("Ship To Customer").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_text("Ship To Customer").click()
        self.page.locator("(//span[contains(text(),'Edit')])[5]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//span[contains(text(),'Edit')])[5]").click()
        time.sleep(self.nw)
        self.page.get_by_label("Same As :").wait_for(state="visible", timeout=60000)
        self.page.get_by_label("Same As :").select_option("End Customer")
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Set").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Set").click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Close").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.nw)

    def selectShippingMethod(self, shipping_method):
        wait_for_element(self.shippingMethod)
        self.shippingMethod.click()
        self.page.get_by_text(shipping_method).click()
        time.sleep(self.nw)

    def enterShippingInstructions(self, shipping_instructions):
        wait_for_element(self.shippingInstructions)
        self.shippingInstructions.click()
        self.page.get_by_role("textbox", name="Shipping Instructions").fill(
            shipping_instructions
        )
        time.sleep(self.nw)
