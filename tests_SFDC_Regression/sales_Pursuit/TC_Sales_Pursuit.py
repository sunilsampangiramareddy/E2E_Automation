
from pages_SFDC import Sales_Pursuit_Page
import pytest
import logging
import os
from playwright.sync_api import Page
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.Sales_Pursuit_Page import SalesPursuitPage
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from utils.locator_manager import LocatorManager
from common_Methods.Common_Methods import CommonMethods
# ================================================================================================================================
# Test Metadata
# ================================================================================================================================
# ADO Test ID -  480551,473941,473937
# Test Scenario: End-to-end validation of Sales Pursuit functionality in Salesforce
#                1.Verify Sales Pursuit Access/Visibility on Sales Initiatives for CSA/CSM Manager Profiles
#                2.Verify multi-layered filtering capability is enabled on Sales Pursuit list view
#                3.Verify Opportunity Association for different user profiles on 'Target Value _ ADD-ON & Block Workload' Records
# Test Description: Automates the workflow for creating a new opportunity, navigating to the Sales Pursuit page,
#                   editing Sales Pursuit entries, associating opportunities, and validating success messages and filters.
# Author: Aswathy Sreelekha
# Modified By: Ayushee
# Reviewer: Sunil Reddy
# ================================================================================================================================
logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_Sales_Pursuit.xlsx"
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
def test_Sales_Pursuit(page: Page, base_url, config, test_case) -> None:
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
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
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****\033[0m"
            )
            if is_valid_data(test_case["User Name"]):
                cm.enterText("LoginPage", "username_Input", test_case["User Name"])
                logger.info(f"Username entered: {test_case['User Name']}")
            cm.clickElement("LoginPage", "next_Button")
            logger.info(f"Clicked on next button")
            cm.enterText("LoginPage", "password_Input", config.get_encodedString())
            logger.info(f"Entered password")
            cm.clickElement("LoginPage", "signin_Button")
            logger.info(f"Signin button clicked")
            cm.clickElement("LoginPage", "yes_Button")
            logger.info(f"Yes button clicked")
            is_visible = cm.isElementVisible("HomePage", "opportunities_Label")
            cm.assertTrue(
                is_visible, "Opportunities label is not visible on the homepage"
            )
            logger.info(
                f"Opportunities label has been verified on the homepage: {is_visible}"
            )
            # =========================================Create Opportunity and Navigate to Sales Pursuit========================================================
            if test_case["Create Opportunity"].strip().lower() == "yes":
                cm.clickElementAndWait("HomePage", "opportunities_Tab", 2)
                cm.clickElement("HomePage", "new_Opportunity_Button")
                logger.info(f"Clickecd on new opportunity button")
                if is_valid_data(test_case["Account Name"]):
                    if is_valid_data(test_case["Account Name"]):
                        co.enterAccount(str(test_case["Account CMAT ID"]))
                        logger.info(
                            f"Entered and selected account: {test_case['Account Name']}"
                        )
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
                                    cm.enterText(
                                        "CreateOpportunity",
                                        "Opportunity_Name_Input",
                                        test_case["Opportunity Name"],
                                    )
                                    logger.info(
                                        f"Entered opportunity name: {test_case['Opportunity Name']}"
                                    )
                                if is_valid_data(test_case["Primary Contact"]):
                                    co.select_PrimaryContact(
                                        test_case["Primary Contact"]
                                    )
                                    logger.info(
                                        f"Selected primary contact: {test_case['Primary Contact']}"
                                    )
                                if is_valid_data(test_case["Sales Play"]):
                                    cm.clickElement(
                                        "CreateOpportunity", "sales_Play_Combobox"
                                    )
                                    cm.clickByText(test_case["Sales Play"])
                                    logger.info(
                                        f"Selected sales play: {test_case['Sales Play']}"
                                    )
                                if is_valid_data(test_case["Channel"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "channel",
                                        test_case["Channel"],
                                    )
                                    logger.info(
                                        f"Selected channel: {test_case['Channel']}"
                                    )
                            if test_case["Opportunity Type"] == x1p_Oppty:
                                if is_valid_data(test_case["Opportunity Name"]):
                                    co.enterOpportunityName_1p(
                                        test_case["Opportunity Name"]
                                    )
                                    logger.info(
                                        f"Entered 1P opportunity name: {test_case['Opportunity Name']}"
                                    )
                                if is_valid_data(test_case["Sales Type"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "sales_Type_1p",
                                        test_case["Sales Type"],
                                    )
                                    logger.info(
                                        f"Selected 1P sales type: {test_case['Sales Type']}"
                                    )
                                if is_valid_data(test_case["Primary Contact"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "primary_Contact_1p",
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
                                    logger.info(
                                        f"Selected hyperscaler: {test_case['Hyperscaler']}"
                                    )
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
                                    logger.info(
                                        f"Selected sales type: {test_case['Sales Type']}"
                                    )
                                if is_valid_data(test_case["Installed Base Type"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "installed_Base_Type",
                                        test_case["Installed Base Type"],
                                    )
                                    logger.info(
                                        f"Selected installed base type: {test_case['Installed Base Type']}"
                                    )
                                if is_valid_data(test_case["Currency"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "currency",
                                        test_case["Currency"],
                                    )
                                    ss.capture_screenshot(
                                        "Captured Create Opportunity details"
                                    )
                                    logger.info(
                                        f"Selected currency: {test_case['Currency']}"
                                    )
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
                                    logger.info(
                                        f"Selected pathway: {test_case['Pathway']}"
                                    )
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
                            if cm.isElementVisible(
                                "CreateOpportunity", "end_Customer_Label", 10000
                            ):
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
                                    cm.clickElement("CreateOpportunity", "next_Button")
                                    logger.info(f"Clicked on next button")
                            if test_case["Opportunity Type"] == x1p_Oppty:
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
                                    logger.info(
                                        f"Selected reseller SE: {test_case['Reseller SE']}"
                                    )
                                cm.clickElement("CreateOpportunity", "next_Button")
                                logger.info(f"Clicked on next button")
                            oppty_number = cm.readText(
                                "CreateOpportunity", "opportunity_Number"
                            )
                            logger.info(f"Opportunity Number: {oppty_number}")
                            print(
                                f"\033[94mℹ️ Opportunity Number: {oppty_number}\033[0m"
                            )
                            oppty_name = cm.readText(
                                "CreateOpportunity", "opportunity_Name"
                            )
                            logger.info(f"Opportunity Name: {oppty_name}")
                            print(f"\033[94mℹ️ Opportunity Name: {oppty_name}\033[0m")
                        spark_url = cm.getCurrentURL()
                        logger.info(f"Captured Spark URL: {spark_url}")
                        print(f"\033[94mℹ️ Captured Spark URL: {spark_url}\033[0m")
                        go_To_Sales_Persuit = cm.isElementPresent(
                            "SalesPursuitPage", "sales_Pursuit_Link"
                        )
                        if go_To_Sales_Persuit == True:
                            cm.clickElement("SalesPursuitPage", "sales_Pursuit_Link")
                        else:
                            cm.clickElement(
                                "SalesPursuitPage", "show_More_Navigation_Item"
                            )
                            cm.clickElement(
                                "SalesPursuitPage", "sales_Pursuit_Menuitem"
                            )
                        logger.info("Sucessfully Navigated to sales pursuit Page")
                        sp = SalesPursuitPage(page)
                        if test_case["Filter Validation"].strip().lower() == "yes":
                            print(
                                f"\n\033[94mℹ️ ================Add Filter & Delete Filter Validations===============================================================================\033[0m"
                            )
                            add_Filters_locators = [
                                "add_Filter_Button",
                                "add_Filter_Button",
                                "add_Filter_Button",
                            ]
                            cm.clickElementsInSequence("SalesPursuitPage",add_Filters_locators)

                            delete_Filters_Locators = [
                                "delete_Filter_Button",
                                "delete_Filter_Button",
                                "delete_Filter_Button",
                            ]
                            cm.clickElementsInSequence("SalesPursuitPage",delete_Filters_Locators)
                            logger.info(
                                "Add Filter and Delete Button is validated and validation passed successfully."
                            )
                        cm.clickElement("SalesPursuitPage", "edit_Button")
                        logger.info("Clicked on edit button")
                        cm.clickElement("SalesPursuitPage", "investigating_Pursuit")
                        logger.info("Clicked on investigating pursuit")
                        cm.clickByText(test_case["Investigating Pursuit"])
                        logger.info(
                            f"Clicked by text: {test_case['Investigating Pursuit']}"
                        )
                        cm.clickElement("SalesPursuitPage", "pursuit_Action")
                        logger.info("Clicked on pursuit action")
                        cm.clickByText(test_case["Pursuit Action"])
                        logger.info(f"Clicked by text: {test_case['Pursuit Action']}")
                        cm.clickElement("SalesPursuitPage", "next_Button")
                        logger.info(f"Clicked on next button")
                        sp.selectOpportunity(oppty_number)
                        logger.info(
                            f"Opportunity is sucessfully selected from search box"
                        )
                        logger.info(f"Clicked on Save Button")
                        if test_case["Status Validations"].strip().lower() == "yes":
                            if is_valid_data(test_case["Expected Message"]):
                                record_Updated_Status = cm.readText(
                                    "SalesPursuitPage",
                                    "record_Updated",
                                )
                            logger.info(
                                f"Captured Resource Request Status: {record_Updated_Status}"
                            )
                            expected_status = cm.checkExpectedTextInActual(
                                actual_text=record_Updated_Status,
                                expected_text=test_case["Expected Message"],
                            )
                            if not expected_status:
                                failure_message = (
                                    f"Record Updated status validation failed: "
                                    f"Expected '{test_case['Expected Message']}', "
                                    f"Actual status found '{record_Updated_Status}'"
                                )
                                validation_failures.append(failure_message)
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")
                            else:
                                logger.info(
                                    f"Record Updated status validation passed. "
                                    f"Expected status '{test_case['Expected Message']}' is displayed."
                                )
                                print(
                                    f"\033[92m✅ Record Updated status validation passed: "
                                    f"{test_case['Expected Message']}\033[0m"
                                )
            # ======================================Checking for Validation Failures=========================================================================================
            print(
                f"\n\033[94mℹ️ ================Checking for Validation Failures=========================================================================================================\033[0m"
            )
            logger.info("Checking for validation failures")
            if validation_failures:
                print("\033[91m❌ The following validation(s) failed:\033[0m")
                logger.error("The following validation(s) failed:")
                for failure in validation_failures:
                    logger.error(failure)
                    print(f"\033[91m❌ {failure}\033[0m")
                pytest.fail(
                    "One or more validations failed. Check the logs for details."
                )
            else:
                print("\033[92m✅ All validations passed successfully.\033[0m")
                logger.info("All validations passed successfully.")
            # =========================================Capture Test Result and Write To Excel==============================================
            test_results = [
                ["Test Case ID", "Execution Status", "Details"],
                [script_name, boolean_status, "Logged in successfully"],
            ]
            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)
            logger.info(
                f"*****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\n\033[92m✅ *****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****\033[0m"
            )
        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}"
            )
            print(
                f"\033[93m➡️ Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}\033[0m"
            )
            pytest.skip(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}"
            )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
