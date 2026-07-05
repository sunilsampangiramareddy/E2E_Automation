from pages_CPQ.Products_Page import ProductsPage
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
from pages_TPD.TPD_Home_Page import TPDHomePage
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify TPD session
# Test Description: Verify that the TPD session remains active and does not time out after a certain period of
#                   inactivity(2 hours)
# Author: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_TPD_Session.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_TPD_Session(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    boolean_status = "Pass"
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"

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

        # =====================================TPD=========================================================================================
        thp = TPDHomePage(page)
        logger.info(f"TPDHomePage instance created for the new tab")

        if is_valid_data(test_case["TPD URL"]):
            thp.navigateToUrl(test_case["TPD URL"])
            logger.info(f"Navigated to TPD URL: {test_case['TPD URL']}")

        current_time = thp.getCurrentTime()
        logger.info(
            f"Captured current time before starting the iterations: {current_time}"
        )

        for i in range(8):  # Loop to run 8 times
            print(
                f"Iteration {i + 1}: Performing actions to validate TPD session time out"
            )

            thp.clickGlobalSearch()
            logger.info(f"Clicked on global search")

            thp.searchByTransactionNumber("356860")
            logger.info(f"Searched by transaction number: 356860")

            thp.searchByPONumber("356860")
            logger.info(f"Searched by PO number: 356860")

            thp.clickGoButton()
            logger.info(f"Clicked on Go button")

            tpd_subProcessStatus = thp.getSubProcessStatus()
            logger.info(f"Captured subprocess status: {tpd_subProcessStatus}")

            tpd_orderStatus = thp.getOrderStatus()
            logger.info(f"Captured order status: {tpd_orderStatus}")

            time.sleep(900)
            thp.checkGlobalSearchVisibility_SessionTimeOut()
            logger.info(f"Checked global search visibility in iteration {i + 1}")
            current_time = thp.getCurrentTime()
            logger.info(f"Captured current time in iteration {i + 1}: {current_time}")
            ss.capture_screenshot(f"Captured TPD details in iteration {i + 1}")

        current_time = thp.getCurrentTime()
        logger.info(f"Captured current time after all iterations: {current_time}")

        thp.checkGlobalSearchVisibility_SessionTimeOut()
        logger.info(
            f"Checked global search visibility after all iterations to validate session timeout"
        )
        ss.capture_screenshot("Captured TPD details after all iterations")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
