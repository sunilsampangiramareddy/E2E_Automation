from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_CPQ.Quote_Info_Page import QuoteInfoPage
import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Home_Page import HomePage
from pages_StorageGrid.HomePage_StorageGrid import HomePageStorageGrid
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from reusable_Components.Reusable_Components import ReusableComponents
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from pages_SFDC.Developer_Console import DeveloperConsole

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Base", "TC_SFDC_ReusableComponent.xlsx"
)
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Load locators from JSON
locator_file_path = os.path.join(working_directory, "locators", "locators.json")
locator_manager = LocatorManager(locator_file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize(
    "test_case",
    test_data.to_dict(orient="records"),
    ids=lambda test_case, index=iter(
        range(1, len(test_data) + 1)
    ): f"test_case{next(index)}",
)
@pytest.mark.master
@pytest.mark.regression
def test_ReusableComponent(page: Page, base_url, config, test_case) -> None:
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    rc = ReusableComponents(page, locator_manager)
    boolean_status = "Pass"
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"
    validation_failures = []

    try:
        # ==================================Login to SFDC=================================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****"
            )

            sfdc_homepage_url = rc.loginToSFDC(config, test_case=test_case)
            logger.info(
                f"Login to SFDC is successful and captured the homepage URL: {sfdc_homepage_url}"
            )

            # ========================Create Direct Opportunity======================================================================================
            if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":
                if test_case["Create Opportunity"].strip().lower() == "yes":
                    if test_case["Channel"].strip().lower() == "direct":
                        direct_oppty_details = rc.createDirectOpportunity(
                            test_case=test_case
                        )
                        logger.info(
                            f"Direct opportunity created successfully with details: {direct_oppty_details}"
                        )

            # ========================Create Indirect Opportunity======================================================================================
            if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":
                if test_case["Create Opportunity"].strip().lower() == "yes":
                    if test_case["Channel"].strip().lower() == "indirect":
                        indirect_oppty_details = rc.createIndirectOpportunity(
                            test_case=test_case
                        )
                        logger.info(
                            f"Indirect opportunity created successfully with details: {indirect_oppty_details}"
                        )

            # ========================Create 1P Opportunity======================================================================================
            if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":
                if test_case["Create Opportunity"].strip().lower() == "yes":
                    if test_case["Opportunity Type"].strip().lower() == "1p":
                        x1p_oppty_details = rc.create1POpportunity(test_case=test_case)
                        logger.info(
                            f"1P opportunity created successfully with details: {x1p_oppty_details}"
                        )

            # ========================Add Product in SFDC=====================================================================================
            if test_case["Add Products"].strip().lower() == "yes":
                rc.addProductsInSFDC(test_case=test_case)
                logger.info(f"Products added successfully in SFDC for the opportunity")

            # ========================Capture Oppotunity Details=====================================================================================
            opportunityDetails = rc.captureOpportunityDetails()
            logger.info(
                f"Opportunity details captured successfully for the opportunity: {opportunityDetails}"
            )

            # ========================Capture Quote Details=====================================================================================
            quoteDetails = rc.captureQuoteDetails()
            logger.info(
                f"Quote details captured successfully for the opportunity: {quoteDetails}"
            )

            # ========================Persona Login========================================================================================
            rc.personaLogin(test_case=test_case)
            logger.info(
                f"Persona login successful for the user: {test_case['Persona']}"
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
