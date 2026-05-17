from datetime import datetime, timedelta

from playwright.sync_api import Page, expect, TimeoutError
import time
import logging
import os

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class PurchaseOrderPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.purchaseOrderTab = self.page.get_by_role("tab", name=" Purchase Order")
        self.purchaseOrderNumber = self.page.get_by_role("textbox", name="PO Number")
        self.poDate = self.page.locator("//input[@placeholder='dd/MM/yyyy']")
        self.poEmail = self.page.get_by_role(
            "textbox", name="Order Acknowledgement Contact"
        )
        self.comments = self.page.get_by_role("textbox", name="Order Review Comments")
        self.submitPO = self.page.get_by_role("button", name="Submit PO")
        self.fulfillmentMethod = self.page.get_by_role(
            "combobox", name="Fulfillment Method"
        )
        self.fulfillmentJustification = self.page.get_by_role(
            "combobox", name="Fulfillment Justification"
        )
        self.fulfillmentRequestedBy = self.page.get_by_role(
            "combobox", name="Fulfillment Requested By"
        )

    def clickPurchaseOrderTab(self):
        wait_for_element(self.purchaseOrderTab)
        self.purchaseOrderTab.click()
        time.sleep(self.sw)

    def enterPONumber(self, po_number):
        wait_for_element(self.purchaseOrderNumber)
        self.purchaseOrderNumber.click()
        self.purchaseOrderNumber.fill(po_number)
        time.sleep(self.nw)

    def enterPODate(self):
        # Calculate the date for today minus one day
        current_date_minus_one = (datetime.now() - timedelta(days=1)).strftime(
            "%d/%m/%Y"
        )
        wait_for_element(self.poDate)
        self.poDate.click()
        self.poDate.fill(current_date_minus_one)
        time.sleep(self.nw)

    def enterPOEmail(self, po_email):
        wait_for_element(self.poEmail)
        self.poEmail.click()
        self.poEmail.fill(po_email)
        time.sleep(self.nw)

    def enterPOComments(self, po_comments):
        wait_for_element(self.comments)
        self.comments.click()
        self.comments.fill(po_comments)
        time.sleep(self.nw)

    def selectFulfillmentMethod(self, fulfilment_Method):
        wait_for_element(self.fulfillmentMethod)
        self.fulfillmentMethod.click()
        self.fulfillmentMethod.click()
        self.fulfillmentMethod.fill(fulfilment_Method)
        self.page.get_by_text(fulfilment_Method).click()
        time.sleep(self.nw)

    def selectFulfillmentJustification(self, fulfilment_Justification):
        wait_for_element(self.fulfillmentJustification)
        self.fulfillmentJustification.click()
        self.fulfillmentJustification.click()
        self.fulfillmentJustification.fill(fulfilment_Justification)
        self.page.get_by_text(fulfilment_Justification).click()
        time.sleep(self.nw)

    def selfFulfillmentRequestedBy(self, fulfilment_RequestedBy):
        wait_for_element(self.fulfillmentRequestedBy)
        self.fulfillmentRequestedBy.click()
        self.fulfillmentRequestedBy.click()
        self.fulfillmentRequestedBy.fill(fulfilment_RequestedBy)
        self.page.get_by_text(fulfilment_RequestedBy).first.click()
        time.sleep(self.nw)

    def clickSubmitPO(self):
        wait_for_element(self.submitPO)
        self.submitPO.click()
        time.sleep(self.lw)
        time.sleep(self.mw)
