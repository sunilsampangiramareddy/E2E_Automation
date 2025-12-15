from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

logger = logging.getLogger('playwright_pytest')

class AccountInformationPage:
    nw=3; sw=5; mw=10; lw=20
            
    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()
       
    def _initialize_locators(self):  
        self.accountInformationTab = self.page.locator('//*[@id="cx-cpq-58ddf3ec-ff14-45d4-8d77-303c703c2c48"]/div/div')
        self.shippingMethod = self.page.get_by_role("combobox", name="Shipping Method") 
        self.shippingInstructions = self.page.get_by_role("textbox", name="Shipping Instructions")      
        
        
    def clickAccountInformationTab(self):
        #expect(self.accountInformationTab).to_be_visible()
        self.accountInformationTab.click()
        time.sleep(self.sw)
        
    
    def enterAccountInformation(self):
        self.page.get_by_title("Sold To").click()
        self.page.locator("(//span[contains(text(),'Edit')])[1]").click()
        time.sleep(self.sw)
        self.page.get_by_label("Search Type :").select_option("Contact")
        self.page.get_by_role("textbox", name="First Name").click()
        self.page.get_by_role("textbox", name="First Name").fill("Aaron")
        self.page.get_by_role("textbox", name="Last Name").click()
        self.page.get_by_role("textbox", name="Last Name").fill("Washington")
        self.page.get_by_role("button", name="Search").click()
        self.page.get_by_role("button", name="Select").click()
        time.sleep(self.sw)
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.mw)
        self.page.get_by_title("Bill To").click()
        self.page.locator("(//span[contains(text(),'Edit')])[2]").click()
        time.sleep(self.sw)
        self.page.get_by_role("button", name="Set").click()
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.mw)
        self.page.get_by_text("End Customer").click()
        self.page.locator("(//span[contains(text(),'Edit')])[3]").click()
        time.sleep(self.sw)
        self.page.get_by_role("textbox", name="First Name").click()
        self.page.get_by_role("textbox", name="First Name").fill("Aaron")
        self.page.get_by_role("textbox", name="Last Name").click()
        self.page.get_by_role("textbox", name="Last Name").fill("Washington")
        self.page.get_by_role("button", name="Search").click()
        self.page.get_by_role("button", name="Select").click()
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.mw)
        self.page.get_by_text("Software Delivery").click()
        self.page.locator("(//span[contains(text(),'Edit')])[4]").click()
        time.sleep(self.sw)
        self.page.get_by_role("button", name="Set").click()
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.mw)
        self.page.get_by_text("Ship To Customer").click()
        self.page.locator("(//span[contains(text(),'Edit')])[5]").click()
        time.sleep(self.sw)
        self.page.get_by_role("button", name="Set").click()
        self.page.get_by_role("button", name="Close").click()
        time.sleep(self.mw)
    
    def selectShippingMethod(self):
        expect(self.shippingMethod).to_be_visible()
        self.shippingMethod.click()
        self.page.get_by_text("1DAY-1DY-1DY").click()
        time.sleep(self.nw)
    
    def enterShippingInstructions(self):
        expect(self.shippingInstructions).to_be_visible()
        self.shippingInstructions.click()
        self.page.get_by_role("textbox", name="Shipping Instructions").fill("Test")
        time.sleep(self.nw)
        