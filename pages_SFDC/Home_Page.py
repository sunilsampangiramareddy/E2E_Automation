from playwright.sync_api import Page, expect
import time

from utils.utils import wait_for_element


class HomePage:
    nw = 2
    sw = 5
    bw = 30

    def __init__(self, page: Page):
        self.page = page
        self.opportunitiesLabel = page.get_by_role("link", name="Opportunities")
        self.newOpportunityButton = page.get_by_role("button", name="New Opportunity")
        self.productsLink = page.get_by_role("link", name="Products (0)")
        self.addProducts = page.get_by_role("button", name="Add Products")
        self.searchProducts = page.locator("//input[@title='Search Products']")
        self.svgButton = page.get_by_role(
            "option", name='Search Products "All SAN'
        ).locator("svg")
        self.serachProduct = page.locator("//tr[1]/td[2]/span/div/span")
        self.nextButton = page.get_by_role("button", name="Next")
        self.editSalesPrice = page.get_by_role(
            "button", name="Edit Sales Price: Item null"
        )
        self.enterPirce = page.get_by_role("textbox", name="Sales Price")
        self.saveButton = page.get_by_role("button", name="Save")
        self.createQuote_1 = page.locator("//button[normalize-space()='Create Quote']")
        self.createQuote_2 = page.locator(
            "//button[@class='slds-button slds-button_brand'][normalize-space()='Create Quote']"
        )

    def isOpportunitiesLabelVisible(self):
        wait_for_element(self.opportunitiesLabel)
        return self.opportunitiesLabel.is_visible()

    def clickOpportunitiesTab(self):
        wait_for_element(self.opportunitiesLabel)
        self.opportunitiesLabel.click()

    def clickNewOpportunityButton(self):
        wait_for_element(self.newOpportunityButton)
        self.newOpportunityButton.click()

    def selectProduct(self, productName):
        wait_for_element(self.productsLink)
        self.productsLink.click()
        self.addProducts.click()
        self.searchProducts.click()
        self.searchProducts.fill(productName)
        time.sleep(self.nw)
        self.searchProducts.press("Enter")
        # self.svgButton.wait_for(state="visible", timeout=60000)
        # self.svgButton.click()
        wait_for_element(self.serachProduct)
        self.serachProduct.click()
        self.nextButton.click()

    def enterProductPrice(self, productPrice):
        wait_for_element(self.editSalesPrice)
        self.editSalesPrice.click()
        self.enterPirce.fill(str(productPrice))
        self.saveButton.click()
        time.sleep(self.sw)
        # self.page.go_back()

    def create_Quote(self):
        wait_for_element(self.createQuote_1)
        self.createQuote_1.click()
        wait_for_element(self.createQuote_2)
        with self.page.context.expect_page() as new_page_info:
            self.createQuote_2.click()
        new_tab = new_page_info.value
        return new_tab

    def getCurrentURL(self):
        current_url = self.page.url
        return current_url

    def navigateToUrl(self, url):
        self.page.goto(url)

    def refreshPage(self):
        self.page.reload(timeout=60000)
