from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class ApprovalRequestPage:
    nw = 2
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.approvalRequestTab = self.page.locator(
            "//span[normalize-space()='Approval Request']"
        )
        self.selectJustification = self.page.locator("//input[@role='combobox']")
        self.initiateApproval = self.page.locator(
            "//oj-c-button[@class='oj-sm-margin-4x-end cx-cpq-header-action-button oj-complete']//button[@aria-label='Initiate Approval'][normalize-space()='Initiate Approval']"
        )
        self.competitionTab = self.page.locator("//span[text()='Competition']")
        self.competitor = self.page.locator("(//input[@role='combobox'])[1]")
        self.competitorModel = self.page.locator("(//input[@role='combobox'])[3]")
        self.netPriceOfferedByVendor = self.page.locator(
            "(//input[@role='combobox'])[5]"
        )
        self.competitorProduct = self.page.locator("(//input[@role='combobox'])[2]")
        self.rawFullStackVendor = self.page.locator("(//input[@role='combobox'])[4]")
        self.competitiveAdvantage = self.page.locator("//textarea[@autocomplete='on']")
        self.addCompetitionButton = self.page.locator(
            "//button[text()='Add Competition']"
        )
        self.incumbentVendorTab = self.page.locator("//span[text()='Incumbent Vendor']")
        self.incumbentVendor = self.page.locator("(//input[@role='combobox'])[1]")
        self.addIncumbentButton = self.page.locator("//button[text()='Add Incumbent']")

    def clickApprovalRequestTab(self):
        wait_for_element(self.approvalRequestTab)
        self.approvalRequestTab.click()
        time.sleep(self.mw)

    def select_Justification(self, option_value: str) -> None:
        wait_for_element(self.selectJustification)
        self.selectJustification.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{option_value}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def clickCompetitionTab(self):
        wait_for_element(self.competitionTab)
        self.competitionTab.click()
        time.sleep(self.nw)

    def enterCompetitor(self, competitor_name: str):
        wait_for_element(self.competitor)
        self.competitor.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{competitor_name}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def enterCompetitorModel(self, model_name: str):
        wait_for_element(self.competitorModel)
        self.competitorModel.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{model_name}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def enterNetPriceOfferedByVendor(self, option_value: str):
        wait_for_element(self.netPriceOfferedByVendor)
        self.netPriceOfferedByVendor.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{option_value}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def enterCompetitorProduct(self, product_name: str):
        wait_for_element(self.competitorProduct)
        self.competitorProduct.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{product_name}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def enterRawFullStackVendor(self, vendor_name: str):
        wait_for_element(self.rawFullStackVendor)
        self.rawFullStackVendor.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{vendor_name}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def enterCompetitiveAdvantage(self, advantage: str):
        wait_for_element(self.competitiveAdvantage)
        self.competitiveAdvantage.click()
        self.competitiveAdvantage.clear()
        self.competitiveAdvantage.fill(advantage)
        time.sleep(self.nw)

    def clickAddCompetitionButton(self):
        wait_for_element(self.addCompetitionButton)
        self.addCompetitionButton.click()
        time.sleep(self.mw)

    def clickIncumbentVendorTab(self):
        wait_for_element(self.incumbentVendorTab)
        self.incumbentVendorTab.click()
        time.sleep(self.nw)

    def enterIncumbentVendor(self, vendor_name: str):
        wait_for_element(self.incumbentVendor)
        self.incumbentVendor.click()
        time.sleep(self.nw)
        xpath = f"//span[span[text()='{vendor_name}']]"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def clickAddIncumbentButton(self):
        wait_for_element(self.addIncumbentButton)
        self.addIncumbentButton.click()
        time.sleep(self.mw)

    def addComments(self, comments: str):
        self.page.locator("//span[text()='Comments']").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("//span[text()='Comments']").click()
        time.sleep(self.nw)
        self.page.locator("(//input[@autocomplete='on'])[1]").click()
        self.page.locator("(//input[@autocomplete='on'])[1]").fill(comments)
        self.page.locator("(//button[@role='button'])[5]").click()
        time.sleep(self.nw)
        self.page.locator("//oj-option/a/div/span[text()='Add Comment']").click()
        time.sleep(self.mw)

    def clickInitiateApproval(self):
        wait_for_element(self.initiateApproval)
        self.initiateApproval.click()
        time.sleep(self.lw)
