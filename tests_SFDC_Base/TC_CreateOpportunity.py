import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can successfully create an opportunity in Salesforce.
# Test Description: This test script automates the creation of Direct, Indirect and 1P opportunities in Salesforce
#                   using various data inputs.
# Author: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_CreateOpportunity.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Load locators from JSON
locator_file_path = os.path.join(working_directory, "locators", "locators.json")
locator_manager = LocatorManager(locator_file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_createOpportunity(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    cm = CommonMethods(page, locator_manager)
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

        spark_url = hp.getCurrentURL()
        logger.info(f"Spark URL: {spark_url}")

        # =======================Create Opportunity===========================================================================
        cm.clickElement("HomePage", "opportunities_Tab")
        logger.info(f"Clicked on opportunities tab")

        cm.clickElement("HomePage", "new_Opportunity_Button")
        logger.info(f"Clicked on new opportunity button")

        if is_valid_data(test_case["Account Name"]):
            co.enterAccount(test_case["Account Name"])
            logger.info(f"Entered and selected account: {test_case['Account Name']}")

        cm.clickElement("CreateOpportunity", "next_Button")
        logger.info(f"Clicked on next button")

        if (
            test_case["Channel"] == direct_Oppty
            or test_case["Channel"] == indirect_Oppty
            or test_case["Opportunity Type"] == x1p_Oppty
        ):
            if is_valid_data(test_case["Opportunity Type"]):
                cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "opportunity_Type",
                    test_case["Opportunity Type"],
                )
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
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "primary_Contact",
                        test_case["Primary Contact"],
                    )
                    logger.info(
                        f"Selected primary contact: {test_case['Primary Contact']}"
                    )
                if is_valid_data(test_case["Sales Play"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "sales_Play",
                        test_case["Sales Play"],
                    )
                    logger.info(f"Selected sales play: {test_case['Sales Play']}")
                if is_valid_data(test_case["Channel"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "channel",
                        test_case["Channel"],
                    )
                    logger.info(f"Selected channel: {test_case['Channel']}")

            if test_case["Opportunity Type"] == x1p_Oppty:
                if is_valid_data(test_case["Opportunity Name"]):
                    co.enterOpportunityName_1p(test_case["Opportunity Name"])
                    logger.info(
                        f"Entered 1P opportunity name: {test_case['Opportunity Name']}"
                    )
                if is_valid_data(test_case["Sales Type"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "sales_Type_1P",
                        test_case["Sales Type"],
                    )
                    logger.info(f"Selected 1P sales type: {test_case['Sales Type']}")
                if is_valid_data(test_case["Primary Contact"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "primary_Contact_1P",
                        test_case["Primary Contact"],
                    )
                    logger.info(
                        f"Selected 1P primary contact: {test_case['Primary Contact']}"
                    )
                if is_valid_data(test_case["Hyperscaler"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "hyperscaler",
                        test_case["Hyperscaler"],
                    )
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
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "sales_Type",
                        test_case["Sales Type"],
                    )
                    logger.info(f"Selected sales type: {test_case['Sales Type']}")
                    """
                if is_valid_data(test_case["Installed Base Type"]):
                    co.selectInstalledBaseType(test_case["Installed Base Type"])
                    logger.info(f"Selected installed base type: {test_case['Installed Base Type']}")
                    """
                if is_valid_data(test_case["Currency"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "currency",
                        test_case["Currency"],
                    )
                    ss.capture_screenshot("Captured Create Opportunity details")
                    logger.info(f"Selected currency: {test_case['Currency']}")
                cm.clickElement("CreateOpportunity", "next_Button")
                logger.info(f"Clicked on next button")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["Pathway"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "pathway",
                        test_case["Pathway"],
                    )
                    logger.info(f"Selected pathway: {test_case['Pathway']}")
                if is_valid_data(test_case["Partner Sales Model"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "partner_Sales_Model",
                        test_case["Partner Sales Model"],
                    )
                    logger.info(
                        f"Selected partner sales model: {test_case['Partner Sales Model']}"
                    )
                cm.clickElement("CreateOpportunity", "next_Button")
                logger.info(f"Clicked on next button")

            if (
                test_case["Opportunity Type"] == std_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["End Customer Usage"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "end_Customer_Usage",
                        test_case["End Customer Usage"],
                    )
                    logger.info(
                        f"Selected end customer usage: {test_case['End Customer Usage']}"
                    )

            if (
                test_case["Channel"] == direct_Oppty
                or test_case["Opportunity Type"] == x1p_Oppty
            ):
                cm.clickElement("CreateOpportunity", "next_Button")
                logger.info(f"Clicked on next button")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                cm.clickElement("CreateOpportunity", "next_Button")
                logger.info(f"Clicked on next button")
                if is_valid_data(test_case["Reseller Sales Rep"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "reseller_Sales_Rep",
                        test_case["Reseller Sales Rep"],
                    )
                    logger.info(
                        f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}"
                    )
                if is_valid_data(test_case["Reseller SE"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "reseller_SE",
                        test_case["Reseller SE"],
                    )
                    logger.info(f"Selected reseller SE: {test_case['Reseller SE']}")
                cm.clickElement("CreateOpportunity", "next_Button")
                logger.info(f"Clicked on next button")

            oppty_number = cm.readText("CreateOpportunity", "opportunity_Number")
            logger.info(f"Opportunity Number: {oppty_number}")

            oppty_name = cm.readText("CreateOpportunity", "opportunity_Name")
            logger.info(f"Opportunity Name: {oppty_name}")

        spark_url = cm.getCurrentURL()
        logger.info(f"Captured Spark URL: {spark_url}")

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
                oppty_number,  # type: ignore
                oppty_name,  # type: ignore
                "Opportunity created successfully",
            ],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
