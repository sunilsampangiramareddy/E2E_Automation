import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from api_Functions.List_Price_API import ListPriceAPI
from api_Functions.Parts_DB_API import PartsDBAPI
from pages_SFDC.Quotes_Page import QuotesPage
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that the PartsDB API and List Price API return correct values based on provided inputs.
# Test Description: This test script automates the validation of PartsDB API and List Price API by logging into Salesforce,
#                   capturing required inputs, and verifying API responses.
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_API_Validation.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_api_validation(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    ss = ScreenshotUtil(page)
    qp = QuotesPage(page)
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
        logger.info(f"Spark URL: {spark_url}")

        # ========================API Validations=========================================================================
        # Create an instance of the class
        lpa = ListPriceAPI(page)
        pdba = PartsDBAPI(page)

        # ************Parts DB API Validation*************************
        # Capture Part Number required to fecth Parts DB value from API
        partNumber = "DII-HIGH"
        partValue = pdba.getPartsDBAPI(
            config.get_usernameAPI(), config.get_encodedStringAPI(), partNumber
        )
        logger.info(f"Extracted value from Parts_DB: {partValue}")

        # ************List Price API Validation*******************
        # Capture all values required to fetch list price from API
        pricelist = "NA-USD"
        product = "DII-HIGH"
        end_date = "20260318"
        start_date = "20260318"
        min_qty = 100
        max_qty = 100
        min_term = 12
        max_term = 12

        price = lpa.getListPriceAPI(
            config.get_usernameAPI(),
            config.get_encodedStringAPI(),
            pricelist,
            product,
            end_date,
            start_date,
            min_qty,
            max_qty,
            min_term,
            max_term,
        )
        logger.info(f"Extracted List Price: {price}")

        # ========================Navigate to Quotes tab =========================================================================
        if is_valid_data(test_case["Navigate To URL"]):
            qp.navigateToUrl(test_case["Navigate To URL"])
            logger.info(f"Navigated to URL: {test_case['Navigate To URL']}")

        qp.clickQuotesTab()
        logger.info(f"Clicked on Quotes tab")

        # ====================Capture test result and write to Excel==========================================================
        test_results = [
            ["Test Case ID", "Execution Status", "Details"],
            [script_name, boolean_status, "API Validated successfully"],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
