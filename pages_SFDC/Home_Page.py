from playwright.sync_api import Page, expect
import time

class HomePage:
    nw=2; sw=5; mw=10; lw=20
    
    def __init__(self,  page:Page):
        self.page = page
        self.opportunitiesLabel = page.get_by_role("link", name="Opportunities")
        self.newOpportunityButton = page.get_by_role("button", name="New Opportunity")
        self.productsLink = page.get_by_role("link", name="Products (0)")
        self.addProducts = page.get_by_role("button", name="Add Products")
        self.searchProducts =  page.get_by_role("combobox", name="Search <Entity> Search <")
        self.svgButton = page.get_by_role("option", name="Search Products \"All SAN").locator("svg")
        self.serachProduct = page.locator('//tr[1]/td[2]/span/div/span')
        self.nextButton = page.get_by_role("button", name="Next")
        self.editSalesPrice =  page.get_by_role("button", name="Edit Sales Price: Item null")
        self.enterPirce = page.get_by_role("textbox", name="Sales Price")
        self.saveButton = page.get_by_role("button", name="Save")
        self.createQuote_1 = page.locator("//button[normalize-space()='Create Quote']") 
        self.createQuote_2 = page.locator("//button[@class='slds-button slds-button_brand'][normalize-space()='Create Quote']") 
       
               
    def isOpportunitiesLabelVisible(self):
        expect(self.opportunitiesLabel).to_be_visible()
        time.sleep(self.nw)
        
    def clickOpportunitiesTab(self):
        expect(self.opportunitiesLabel).to_be_visible()
        self.opportunitiesLabel.click()
        time.sleep(self.mw) 
        
    def clickNewOpportunityButton(self):
        expect(self.newOpportunityButton).to_be_visible()
        self.newOpportunityButton.click()
        time.sleep(self.mw)
        
    def selectProduct(self, productName):
        self.productsLink.click()
        self.addProducts.click()
        self.searchProducts.click()
        self.searchProducts.fill(productName)
        self.searchProducts.press('Enter')
        time.sleep(self.nw)
        self.svgButton.click()
        self.serachProduct.click()
        self.nextButton.click()
        time.sleep(self.nw)
        
    def enterProductPrice(self, productPrice):
        self.editSalesPrice.click()
        self.enterPirce.fill(str(productPrice))
        self.saveButton.click()
        time.sleep(self.sw)
        self.page.go_back()
        time.sleep(self.mw)
        
    def create_Quote(self):
        self.createQuote_1.click()
        time.sleep(3)
        with self.page.context.expect_page() as new_page_info:
            self.createQuote_2.click()
        new_tab = new_page_info.value
        time.sleep(self.lw)        
        time.sleep(self.mw)    
        return new_tab

        
    
        
        
        
        
        
        
        
        
        
        
        