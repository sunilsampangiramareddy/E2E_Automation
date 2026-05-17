import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from conftest import base_url, page
from pages_Partner.PartnerLogin_Page import PartnerLoginPage
from pages_Partner.Read_OTP import ReadOTP
from pages_SFDC.Quotes_Page import QuotesPage
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can successfully log in to the Partner Portal.
# Test Description: This test script automates the login functionality for the Partner Portal by navigating to the
#                   Partner URL, entering credentials and verifying the successful login.
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_PartnerLogin.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.smoke
@pytest.mark.master
def test_login(page: Page, base_url, config, test_case) -> None:
    plp = PartnerLoginPage(page)
    ss = ScreenshotUtil(page)
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

        # =========================================Capture Test Result and Write To Excel==============================================
        test_results = [
            ["Test Case ID", "Execution Status", "Details"],
            [script_name, boolean_status, "Logged into Partner Portal successfully"],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
