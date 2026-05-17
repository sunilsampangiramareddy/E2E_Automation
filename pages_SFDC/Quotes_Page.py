from playwright.sync_api import Page, expect
import time

from utils.utils import wait_for_element


class QuotesPage:
    nw = 2
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.quotes_Tab = page.locator(
            "//span[@class='slds-truncate' and normalize-space(text())='Quotes']"
        )

    def clickQuotesTab(self):
        wait_for_element(self.quotes_Tab)
        self.quotes_Tab.click()
        time.sleep(self.mw)

    def navigateToUrl(self, url):
        self.page.goto(url)
        time.sleep(self.lw)

    def searchByQuoteName(self, quoteName):
        self.page.locator(
            "//span[@class='slds-truncate' and @part='input-button-value' and text()='-Select field to Search-']"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//span[@class='slds-truncate' and @part='input-button-value' and text()='-Select field to Search-']"
        ).click()
        self.page.locator(
            "(//span[@title='Quote Name' and text()='Quote Name'])[1]"
        ).click()
        time.sleep(self.nw)
        self.page.locator(
            "//input[@class='slds-input' and @placeholder='Enter minimum 3 characters to search' and @part='input']"
        ).click()
        self.page.locator(
            "//input[@class='slds-input' and @placeholder='Enter minimum 3 characters to search' and @part='input']"
        ).fill(quoteName)
        time.sleep(self.nw)
        self.page.locator(
            "//button[@title='Search']//lightning-primitive-icon[@exportparts='icon']"
        ).click()
        time.sleep(self.sw)

    def searchByQuoteNumber(self, quoteNumber):
        self.page.locator(
            "//span[@class='slds-truncate' and @part='input-button-value' and text()='-Select field to Search-']"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//span[@class='slds-truncate' and @part='input-button-value' and text()='-Select field to Search-']"
        ).click()
        self.page.locator(
            "(//span[@title='Quote Number' and text()='Quote Number'])[1]"
        ).click()
        time.sleep(self.nw)
        self.page.locator(
            "//input[@class='slds-input' and @placeholder='Enter minimum 3 characters to search' and @part='input']"
        ).click()
        self.page.locator(
            "//input[@class='slds-input' and @placeholder='Enter minimum 3 characters to search' and @part='input']"
        ).fill(str(quoteNumber))
        time.sleep(self.nw)
        self.page.locator(
            "//button[@title='Search']//lightning-primitive-icon[@exportparts='icon']"
        ).click()
        time.sleep(self.sw)

    def copyQuote(self):
        self.page.locator(
            "//lightning-datatable//tbody//tr//th//lightning-primitive-cell-actions//lightning-button-menu//button//lightning-primitive-icon"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//lightning-datatable//tbody//tr//th//lightning-primitive-cell-actions//lightning-button-menu//button//lightning-primitive-icon"
        ).click()
        time.sleep(self.nw)
        with self.page.context.expect_page() as new_page_info:
            self.page.locator("//lightning-menu-item[1]//div[1]//a[1]").click()
        new_tab = new_page_info.value
        return new_tab

    def clickSearchedQuote(self, quoteNumber):
        with self.page.context.expect_page() as new_page_info:
            xpath = f"//a[text()='{quoteNumber}']"
            self.page.locator(xpath).click()
        new_tab = new_page_info.value
        return new_tab
