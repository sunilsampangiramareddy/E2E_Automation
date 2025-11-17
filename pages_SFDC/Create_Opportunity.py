from playwright.sync_api import Page, expect
import time

class CreateOpportunity:
    nw = 2
    sw = 5
    mw = 10
    lw = 20
    
    def __init__(self, page: Page):
        self.page = page
        self.searchAccount = page.get_by_role("combobox", name="Account")
        self.nextButton = page.get_by_role("button", name="Next")
        self.opportunityName = page.locator('//flowruntime-input-wrapper2/div/lightning-input/lightning-primitive-input-simple/div[1]/div/input')
        self.primaryContact = page.locator('//flowruntime-screen-field[4]/flowruntime-lwc-field/div/flowruntime-picklist-input-lwc/div/lightning-select/div/div/select')
               
    def enterAccount(self, account: str):
        expect(self.searchAccount).to_be_visible()
        self.searchAccount.click()
        self.searchAccount.click()
        time.sleep(self.nw) 
        self.searchAccount.fill(account)
        time.sleep(self.nw) 
        self.page.get_by_role("option", name="Search Show more results for").locator("svg").click()
        self.page.locator('//tr[1]/td[1]/lightning-primitive-cell-checkbox/span/label/span[1]').click()
        self.page.get_by_role("button", name="Select").click()
        time.sleep(self.nw) 
        
    def clickNextButton(self):
        expect(self.nextButton).to_be_visible()
        self.nextButton.click()
        time.sleep(self.sw) 
        
    def enterOpportunityName(self, opportunity_Name: str):
        expect(self.opportunityName).to_be_visible()
        self.opportunityName.click()
        self.opportunityName.fill(opportunity_Name)
        time.sleep(self.nw) 
        
    def selectPrimaryContact_option(self, option_value):
        # Wait for the primaryContact dropdown to be visible
        self.primaryContact.wait_for(state="visible")
        # Select the option by value
        self.primaryContact.select_option(option_value)
        time.sleep(self.nw)
         
        
        