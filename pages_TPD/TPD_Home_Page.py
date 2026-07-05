from datetime import datetime

from playwright.sync_api import Page, expect
import time

from utils.utils import wait_for_element


class TPDHomePage:
    nw = 2
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.globalSearch = page.locator("//a[@href='/global-search']")
        self.transactionNumber = page.locator('//*[@id="transactionNumber"]')
        self.poNumber = page.locator('//*[@id="poNumber"]')
        self.goButton = page.locator('//*[@id="go-submit-search"]')
        self.subProcessStatus = page.locator(
            '//*[@id="tpd-table"]/tbody/tr/td[17]/app-tpd-table-field'
        )
        self.orderStatus = page.locator(
            '//*[@id="tpd-table"]/tbody/tr/td[16]/app-tpd-table-field'
        )
        self.transactionReview = page.locator(
            "//div[contains(text(), 'Transaction Review')]"
        )
        self.rpaReview = page.locator("//div[contains(text(), 'RPA Review')]")
        self.actionsDD = page.locator("(//select[@id='transaction-actions'])[1]")
        self.actions_GoButton = page.locator('//*[@id="action-go-btn"]')
        self.yesButton = page.locator("//button[normalize-space(text())='Yes']")

    def navigateToUrl(self, url):
        self.page.goto(url)
        time.sleep(self.sw)

    def clickGlobalSearch(self):
        wait_for_element(self.globalSearch)
        self.globalSearch.click()

    def searchByTransactionNumber(self, transaction_Number):
        wait_for_element(self.transactionNumber)
        self.transactionNumber.click()
        self.transactionNumber.fill(str(transaction_Number))

    def searchByPONumber(self, po_Number):
        wait_for_element(self.poNumber)
        self.poNumber.click()
        self.poNumber.fill(str(po_Number))

    def clickGoButton(self):
        wait_for_element(self.goButton)
        self.goButton.click()

    def getSubProcessStatus(self):
        wait_for_element(self.subProcessStatus)
        subProcess_Status = self.subProcessStatus.inner_text()
        return subProcess_Status

    def getOrderStatus(self):
        wait_for_element(self.orderStatus)
        order_Status = self.orderStatus.inner_text()
        return order_Status

    def clickTransactionReview(self):
        wait_for_element(self.transactionReview)
        self.transactionReview.click()

    def clickRPAReview(self):
        wait_for_element(self.rpaReview)
        self.rpaReview.click()

    def clickSearchQuote(self, quote_number):
        xpath = f"//a[normalize-space(text())='{quote_number}']"
        self.page.locator(xpath).click()

    def select_ActionsDD(self, option_value: str) -> None:
        wait_for_element(self.actionsDD)
        self.actionsDD.select_option(value=option_value)

    def clickActionsGoButton(self):
        wait_for_element(self.actions_GoButton)
        self.actions_GoButton.click()

    def clickYesButton(self):
        wait_for_element(self.yesButton)
        self.yesButton.click()
        time.sleep(self.mw)

    def checkGlobalSearchVisibility_SessionTimeOut(self):
        element = self.globalSearch
        if element.is_visible():
            element.click()
            if element.is_visible():
                print("Global Search is visible on the TPD homepage")
            else:
                print("Global Search is not visible on the TPD homepage")
        else:
            print("Global Search is not visible on the TPD homepage")

    def getCurrentTime(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_time
