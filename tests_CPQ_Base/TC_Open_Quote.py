import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_FAS_AFF_ASA_AFX.HomePage_FAS_AFF_ASA_AFX import HomePageFAS_AFF_ASA_AFX
from pages_CPQ.Account_Information_Page import AccountInformationPage
from pages_CPQ.Approval_Request_Page import ApprovalRequestPage
from pages_CPQ.Attachments_Page import AttachmentsPage
from pages_CPQ.Purchase_Order_Page import PurchaseOrderPage
from pages_SFDC.Quotes_Page import QuotesPage
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can search and open a quote successfully in Salesforce.
# Test Description: This test script automates the process of logging into Salesforce, navigating to the Quotes tab,
#                   searching for a quote using its name or number, opening the quote, and validating its details.
# Author: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_Open_Quote.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_Open_Quote(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    qp = QuotesPage(page)
    hp = HomePage(page)
    ss = ScreenshotUtil(page)
    boolean_status = "Pass"

    try:
        # =================================Login to SFDC==========================================================================
        page.goto(base_url)
        logger.info(f"Launching application URL: {base_url}")
        logger.info(f"***{script_name} Test Script Execution Started***")

        if is_valid_data(test_case["User Name"]):
            lp.enterUserName(test_case["User Name"])
            logger.info(f"Username entered: {test_case['User Name']}")
            # lp.enterUserName(config.get_username())
            # logger.info("Username entered")

        lp.clickNextButton()
        logger.info(f"Clicked on next button")

        # lp.enterPassword(os.getenv("PASSWORD"))
        lp.enterPassword(config.get_encodedString())
        logger.info(f"Entered password")

        lp.clickSigninButton()
        logger.info(f"Signin button clicked")

        lp.clickYesButton()
        logger.info(f"Yes button clicked")

        hp.isOpportunitiesLabelVisible()
        logger.info(f"Opportunities label has been verified on the homepage")
        ss.capture_screenshot("Captured Homepage details")

        spark_url = hp.getCurrentURL()
        logger.info(f"Captured Spark URL: {spark_url}")

        # ========================Navigate to Quotes tab and click on the searched quote=========================================================================
        if is_valid_data(test_case["Navigate To URL"]):
            qp.navigateToUrl(test_case["Navigate To URL"])
            logger.info(f"Navigated to URL: {test_case['Navigate To URL']}")

        qp.clickQuotesTab()
        logger.info(f"Clicked on Quotes tab")

        # ---Either use QuoteName or QuoteNumber, but dont use both---------------------
        if is_valid_data(test_case["Quote Name"]):
            qp.searchByQuoteName(test_case["Quote Name"])
            logger.info(f"Searched quote with quote name: {test_case['Quote Name']}")
            """
        if is_valid_data(test_case["Quote Number"]):
            qp.searchByQuoteNumber(test_case["Quote Number"])
            logger.info(
                f"Searched quote with quote number: {test_case['Quote Number']}"
            )
            """

        new_tab = qp.clickSearchedQuote(test_case["Quote Number"])
        logger.info(f"Clicked on Searched Quote")

        # ============================Capture Quote Details==========================================================================
        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(new_tab)
        logger.info(f"HomePageCPQ instance created for the new tab")
        ss = ScreenshotUtil(new_tab)
        logger.info(f"ScreenshotUtil instance created for the new tab")
        hp = HomePage(new_tab)
        logger.info(f"HomePage instance created for the new tab")

        # Perform actions on the new tab
        quote_number = hpc.getQuoteNumber()
        logger.info(f"Quote Number: {quote_number}")

        quote_name = hpc.getQuoteName()
        logger.info(f"Quote Name: {quote_name}")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")

        cpq_url = hp.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp()

        # ====================Capture test result and write to Excel==========================================================
        test_results = [
            ["Test Case ID", "Execution Status", "Details"],
            [script_name, boolean_status, "Quote Opened successfully"],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
