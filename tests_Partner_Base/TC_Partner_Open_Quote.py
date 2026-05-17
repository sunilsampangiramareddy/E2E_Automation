from pages_CPQ.Products_Page import ProductsPage
import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from conftest import base_url, page
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_Partner.PartnerHome_Page import PartnerHomePage
from pages_Partner.PartnerLogin_Page import PartnerLoginPage
from pages_Partner.PartnerQuote_Page import PartnerQuotePage
from pages_Partner.Read_OTP import ReadOTP
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can log in to the Partner Portal and open a quote successfully.
# Test Description: This test script automates the process of logging into the Partner Portal, navigating
#                   to the Quote Console, searching for a specific quote, and capturing its details, including product
#                   and pricing information from the LIG product table.
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_Partner_Open_Quote.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.smoke
@pytest.mark.master
def test_Partner_Open_Quote(page: Page, base_url, config, test_case) -> None:
    plp = PartnerLoginPage(page)
    ss = ScreenshotUtil(page)
    php = PartnerHomePage(page)
    pqp = PartnerQuotePage(page)
    boolean_status = "Pass"

    try:
        # =================================Login to Partner Portal==========================================================================
        page.goto(base_url)
        logger.info(f"Launching application URL: {base_url}")
        logger.info(f"***{script_name} Test Script Execution Started***")

        if is_valid_data(test_case["Partner Url"]):
            plp.navigateToUrl(test_case["Partner Url"])
            logger.info(f"Navigated to URL: {test_case['Partner Url']}")

        if is_valid_data(test_case["User Name"]):
            plp.enterUserName(test_case["User Name"])
            logger.info(f"Username entered: {test_case['User Name']}")

        plp.clickNextButton()
        logger.info("Clicked on next button")

        otp = ReadOTP.get_otp_from_imap()
        assert otp is not None, "OTP was not received in time"
        logger.info(f"OTP: {otp}")

        plp.enterOTP(otp)
        logger.info(f"Entered OTP: {otp}")

        plp.clickContinueButton()
        logger.info("Clicked on continue button")

        plp.isHomeLabelDisplayed()
        logger.info("Home label is displayed, login successful")
        ss.capture_screenshot("Captured Homepage details")

        partner_url = plp.getCurrentURL()
        logger.info(f"Partner URL: {partner_url}")

        # ========================Navigate to Quotes console page and click on the searched quote=========================================================================
        php.handle_popup_1(30)
        logger.info("Handled popup_1")

        php.handle_popup_2(30)
        logger.info("Handled popup_2")

        php.navigateToQuoteConsole()
        logger.info("Navigated to Quote Console")

        ## ---Either use QuoteName or QuoteNumber, but dont use both---------------------
        if is_valid_data(test_case["Quote Name"]):
            pqp.selectByQuoteName(test_case["Quote Name"])
            logger.info(f"Searched for Quote Name: {test_case['Quote Name']}")
            """
        if is_valid_data(test_case["Quote Number"]):
            pqp.searchByQuoteNumber(test_case["Quote Number"])
            logger.info(f"Searched for Quote Number: {test_case['Quote Number']}")
            """

        new_tab = pqp.clickSearchedQuote(test_case["Quote Number"])
        logger.info("Clicked on Searched Quote")
        ss.capture_screenshot("Captured Quote console page details")

        # ============================Capture Quote Details==========================================================================
        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(new_tab)
        logger.info(f"HomePageCPQ instance created for the new tab")
        ss = ScreenshotUtil(new_tab)
        logger.info(f"ScreenshotUtil instance created for the new tab")

        # Perform actions on the new tab
        quote_number = hpc.getQuoteNumber()
        logger.info(f"Quote Number: {quote_number}")

        quote_name = hpc.getQuoteName()
        logger.info(f"Quote Name: {quote_name}")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")

        cpq_url = plp.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp()
        ss.capture_screenshot("Captured Quote details")

        # =============================Read LIG Product Table=========================================================================
        pp = ProductsPage(new_tab)
        logger.info(f"ProductsPage instance created for the new tab")

        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp_2()

        pp.expandAllProducts()
        logger.info(f"Expanded all products in the LIG product table")

        hpc.readProductTable(new_tab, "Product")
        logger.info(f"Reading Product column values from product LIG table")

        hpc.readProductTable(new_tab, "List Price")
        logger.info(f"Reading List Price column values from product LIG table")

        pp.collapseAllProducts()
        logger.info(f"Collapsed all products in the LIG product table")
        ss.capture_screenshot("Captured LIG Product table details")

        # =========================================Capture Test Result and Write To Excel==============================================
        test_results = [
            ["Test Case ID", "Execution Status", "Details"],
            [script_name, boolean_status, "Quote opened successfully"],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
