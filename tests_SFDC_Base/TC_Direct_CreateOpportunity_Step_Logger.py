import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from utils.step_logger import StepLogger


# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can successfully create an Direct opportunity in Salesforce and Add products.
# Test Description: This test script automates the creation of Direct opportunity and Add products in Salesforce
#                   using various data inputs.
# Author: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData", "TC_Direct_CreateOpportunity_Step_Logger.xlsx"
)
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_createDirectOpportunityStepLogger(
    page: Page, base_url, config, test_case
) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    boolean_status = "Pass"
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"
    step_logger = StepLogger(report_dir="reports")  # StepLogger instance

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
            step_logger.log_step(step_name="Username entered", page=page)

        lp.clickNextButton()
        logger.info(f"Clicked on next button")

        # lp.enterPassword(os.getenv("PASSWORD"))
        lp.enterPassword(config.get_encodedString())
        logger.info(f"Entered password")
        step_logger.log_step(step_name="Entered password", page=page)

        step_logger.log_step(step_name="Click on Signin button", page=page)
        lp.clickSigninButton()
        logger.info(f"Signin button clicked")

        step_logger.log_step(step_name="Click on Yes button", page=page)
        lp.clickYesButton()
        logger.info(f"Yes button clicked")

        hp.isOpportunitiesLabelVisible()
        logger.info(f"Opportunities label has been verified on the homepage")
        ss.capture_screenshot("Captured Homepage details")
        step_logger.log_step(
            step_name="Opportunities label has been verified on the homepage", page=page
        )

        spark_url = hp.getCurrentURL()
        logger.info(f"Spark URL: {spark_url}")

        # =======================Create Opportunity===========================================================================
        hp.clickOpportunitiesTab()
        logger.info(f"Clicked on opportunities tab")

        hp.clickNewOpportunityButton()
        logger.info(f"Clickecd on New Opportunity button")
        step_logger.log_step(step_name="Clicked on New Opportunity button", page=page)

        if is_valid_data(test_case["Account Name"]):
            co.enterAccount(test_case["Account Name"])
            logger.info(f"Entered and selected account: {test_case['Account Name']}")
            step_logger.log_step(step_name="Entered and selected account", page=page)

        step_logger.log_step(step_name="Clicked on Next button", page=page)
        co.clickNextButton()
        logger.info(f"Clicked on Next button")

        if (
            test_case["Channel"] == direct_Oppty
            or test_case["Channel"] == indirect_Oppty
            or test_case["Opportunity Type"] == x1p_Oppty
        ):
            if is_valid_data(test_case["Opportunity Type"]):
                co.selectOpportunityType(test_case["Opportunity Type"])
                logger.info(
                    f"Selected opportunity type: {test_case['Opportunity Type']}"
                )

            if test_case["Opportunity Type"] == std_Oppty:
                if is_valid_data(test_case["Opportunity Name"]):
                    co.enterOpportunityName(test_case["Opportunity Name"])
                    logger.info(
                        f"Entered opportunity name: {test_case['Opportunity Name']}"
                    )
                if is_valid_data(test_case["Primary Contact"]):
                    co.selectPrimaryContact(test_case["Primary Contact"])
                    logger.info(
                        f"Selected primary contact: {test_case['Primary Contact']}"
                    )
                if is_valid_data(test_case["Sales Play"]):
                    co.selectSalesPlay(test_case["Sales Play"])
                    logger.info(f"Selected sales play: {test_case['Sales Play']}")
                if is_valid_data(test_case["Channel"]):
                    co.selectChannel(test_case["Channel"])
                    logger.info(f"Selected channel: {test_case['Channel']}")

            if test_case["Opportunity Type"] == x1p_Oppty:
                if is_valid_data(test_case["Opportunity Name"]):
                    co.enterOpportunityName_1p(test_case["Opportunity Name"])
                    logger.info(
                        f"Entered 1P opportunity name: {test_case['Opportunity Name']}"
                    )
                if is_valid_data(test_case["Sales Type"]):
                    co.selectSalesType_1p(test_case["Sales Type"])
                    logger.info(f"Selected 1P sales type: {test_case['Sales Type']}")
                if is_valid_data(test_case["Primary Contact"]):
                    co.selectPrimaryContact_1p(test_case["Primary Contact"])
                    logger.info(
                        f"Selected 1P primary contact: {test_case['Primary Contact']}"
                    )
                if is_valid_data(test_case["Hyperscaler"]):
                    co.selectHyperscaler(test_case["Hyperscaler"])
                    logger.info(f"Selected hyperscaler: {test_case['Hyperscaler']}")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["Reseller Account"]):
                    co.selectReseller(test_case["Reseller Account"])
                    logger.info(
                        f"Entered reseller account: {test_case['Reseller Account']}"
                    )

            if (
                test_case["Opportunity Type"] == std_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["Sales Type"]):
                    co.selectSalesType(test_case["Sales Type"])
                    logger.info(f"Selected sales type: {test_case['Sales Type']}")
                    """
                if is_valid_data(test_case["Installed Base Type"]):
                    co.selectInstalledBaseType(test_case["Installed Base Type"])
                    logger.info(f"Selected installed base type: {test_case['Installed Base Type']}")
                    """
                if is_valid_data(test_case["Currency"]):
                    co.selectCurrency(test_case["Currency"])
                    ss.capture_screenshot("Captured Create Opportunity details")
                    logger.info(f"Selected currency: {test_case['Currency']}")
                    step_logger.log_step(
                        step_name="Entered create oppotunity details", page=page
                    )
                co.clickNextButton()
                logger.info(f"Clicked on next button")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["Pathway"]):
                    co.selectPathway(test_case["Pathway"])
                    logger.info(f"Selected pathway: {test_case['Pathway']}")
                if is_valid_data(test_case["Partner Sales Model"]):
                    co.selectPartnerSalesModel(test_case["Partner Sales Model"])
                    logger.info(
                        f"Selected partner sales model: {test_case['Partner Sales Model']}"
                    )
                co.clickNextButton()
                logger.info(f"Clicked on next button")

            if (
                test_case["Opportunity Type"] == std_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["End Customer Usage"]):
                    co.selectEndCustomerUsage_option(test_case["End Customer Usage"])
                    logger.info(
                        f"Selected end customer usage: {test_case['End Customer Usage']}"
                    )

            if (
                test_case["Channel"] == direct_Oppty
                or test_case["Opportunity Type"] == x1p_Oppty
            ):
                co.clickNextButton_2()
                logger.info(f"Clicked on next button")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                co.clickNextButton()
                logger.info(f"Clicked on next button")
                if is_valid_data(test_case["Reseller Sales Rep"]):
                    co.selectResellerSalesRep(test_case["Reseller Sales Rep"])
                    logger.info(
                        f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}"
                    )
                if is_valid_data(test_case["Reseller SE"]):
                    co.selectResellerSE(test_case["Reseller SE"])
                    logger.info(f"Selected reseller SE: {test_case['Reseller SE']}")
                co.clickNextButton_2()
                logger.info(f"Clicked on next button")

            oppty_number = co.captureOpportunityNumber()
            logger.info(f"Opportunity Number: {oppty_number}")

            oppty_name = co.captureOpportunityName()
            logger.info(f"Opportunity Name: {oppty_name}")
            step_logger.log_step(
                step_name="Opportunity created and captured details", page=page
            )

        spark_url = hp.getCurrentURL()
        logger.info(f"Captured Spark URL: {spark_url}")

        # =======================Add Product in SFDC=================================================================================
        if is_valid_data(test_case["Product Name"]):
            hp.selectProduct(test_case["Product Name"])
            logger.info(f"Selected product: {test_case['Product Name']}")
            step_logger.log_step(step_name="Selected product", page=page)

        if is_valid_data(test_case["Product Price"]):
            hp.enterProductPrice(test_case["Product Price"])
            ss.capture_screenshot("Captured Product in SFDC Details")
            logger.info(f"Entered product price: {test_case['Product Price']}")
            step_logger.log_step(step_name="Entered product price", page=page)

        hp.navigateToUrl(spark_url)
        logger.info(f"Navigated back to Spark URL: {spark_url}")

        # =========================================Capture Test Result and Write To Excel==============================================
        test_results = [
            [
                "Test Case ID",
                "Execution Status",
                "Opportunity Number",
                "Opportunity Name",
                "Details",
            ],
            [
                script_name,
                boolean_status,
                oppty_number, # type: ignore
                oppty_name, # type: ignore
                "Opportunity created successfully",
            ],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

        # Generate the HTML report using step logger
        step_logger.generate_html_report(output_file=script_name)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
