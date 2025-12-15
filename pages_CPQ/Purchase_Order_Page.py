from playwright.sync_api import Page, expect, TimeoutError
import time
import logging
import os

logger = logging.getLogger('playwright_pytest')

class PurchaseOrderPage:
    nw=3; sw=5; mw=10; lw=20
            
    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()
        
    def _initialize_locators(self):  
        self.purchaseOrderTab = self.page.get_by_role("tab", name=" Purchase Order")
        self.purchaseOrderNumber = self.page.get_by_role("textbox", name="PO Number")
        self.poDate = self.page.get_by_role("list", name="List of fields of section").locator("input[type=\"text\"]")
        self.poEmail = self.page.get_by_role("textbox", name="Order Acknowledgement Contact")
        self.comments = self.page.get_by_role("textbox", name="Order Review Comments")
        self.submitPO =  self.page.get_by_role("button", name="Submit PO")
    
    def clickPurchaseOrderTab(self):
        expect(self.purchaseOrderTab).to_be_visible()
        self.purchaseOrderTab.click()
        time.sleep(self.sw)
        
    def enterPONumber(self):
        expect(self.purchaseOrderNumber).to_be_visible()
        self.purchaseOrderNumber.click()
        self.purchaseOrderNumber.fill("12345")
        time.sleep(self.nw)
        
    def enterPODate(self):
        expect(self.poDate).to_be_visible()
        self.poDate.click()
        self.poDate.fill("12-12-2025")
        time.sleep(self.nw)
        
    def enterPOEmail(self):
        expect(self.poEmail).to_be_visible()
        self.poEmail.click()
        self.poEmail.fill("test@mail.com")
        time.sleep(self.nw)
        
    def enterPOComments(self):
        expect(self.comments).to_be_visible()
        self.comments.click()
        self.comments.fill("test")
        time.sleep(self.nw)
        
    def clickSubmitPO(self):
        expect(self.submitPO).to_be_visible()
        self.submitPO.click()
        time.sleep(self.lw)
        
        
        
        