from playwright.sync_api import Page, expect
import time

class HomePage:
    nw=3; sw=5; mw=10; lw=20
    
    def __init__(self,  page:Page):
        self.page = page
        self.opportunitiesLabel = page.get_by_role("link", name="Opportunities")
        self.newOpportunityButton = page.get_by_role("button", name="New Opportunity")
               
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