from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

logger = logging.getLogger('playwright_pytest')

class ApprovalRequestPage:
    nw=3; sw=5; mw=10; lw=20
            
    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()
       
    def _initialize_locators(self):  
        self.approvalRequestTab = self.page.locator("//span[normalize-space()='Approval Request']")
        self.initiateApproval =  self.page.locator("//oj-c-button[@class='oj-sm-margin-4x-end cx-cpq-header-action-button oj-complete']//button[@aria-label='Initiate Approval'][normalize-space()='Initiate Approval']")
        
            
    def clickApprovalRequestTab(self):
        expect(self.approvalRequestTab).to_be_visible()
        self.approvalRequestTab.click()
        time.sleep(self.sw)
    
    def clickInitiateApproval(self):
        expect(self.initiateApproval).to_be_visible()
        self.initiateApproval.click()
        time.sleep(self.lw)
        
        