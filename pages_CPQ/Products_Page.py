from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class ProductsPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.addParts = self.page.locator("//button[text()='Add Parts']")
        self.productsTab = self.page.get_by_role("tab", name=" Products")
        self.configureButton = self.page.get_by_role("button", name="Configure Product")

    def clickProductsTab(self):
        wait_for_element(self.productsTab)
        self.productsTab.click()

    def clickConfigureButton(self):
        wait_for_element(self.configureButton)
        self.configureButton.click()

    def expandAllProducts(self):
        self.page.wait_for_selector(
            '//*[@id="cx_cpq_products_and_pricing_lig_section"]/div[1]/div/div[1]/oj-c-menu-button/button/span',
            state="visible",
            timeout=60000,
        )
        self.page.locator(
            '//*[@id="cx_cpq_products_and_pricing_lig_section"]/div[1]/div/div[1]/oj-c-menu-button/button/span'
        ).click()
        time.sleep(self.nw)
        self.page.locator("//span[normalize-space(text())='Expand All']").click()
        time.sleep(self.mw)
        self.productsTab.click()
        time.sleep(self.nw)

    def collapseAllProducts(self):
        self.page.wait_for_selector(
            '//*[@id="cx_cpq_products_and_pricing_lig_section"]/div[1]/div/div[1]/oj-c-menu-button/button/span',
            state="visible",
            timeout=60000,
        )
        self.page.locator(
            '//*[@id="cx_cpq_products_and_pricing_lig_section"]/div[1]/div/div[1]/oj-c-menu-button/button/span'
        ).click()
        time.sleep(self.nw)
        self.page.locator("//span[normalize-space(text())='Collapse All']").click()
        time.sleep(self.mw)

    def clickAddParts(self):
        wait_for_element(self.addParts)
        self.addParts.click()
        time.sleep(self.mw)

    def searchProductNamePartNumberOrModelNumber(self, search_item):
        self.page.locator(
            "//input[@aria-label='Search product name, part number or model']"
        ).wait_for(state="visible", timeout=60000)
        search_input = self.page.locator(
            "//input[@aria-label='Search product name, part number or model']"
        )
        search_input.click()
        search_input.fill(search_item)
        time.sleep(self.nw)
        search_input.press("Enter")
        time.sleep(self.nw)
        xpath = f"//span[@title='{search_item}']"
        self.page.locator(xpath).click()
        self.page.locator("(//button[text()='Add'])[1]").click()
        time.sleep(self.lw)
