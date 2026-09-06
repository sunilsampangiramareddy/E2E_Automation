import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
#Test Case#: 481524
#  Test Scenario: Indirect Opportunity Reseller Change
# Test Description: Create an indirect opportunity in Salesforce, then update the reseller account through account parties.
#                   This involves logging into Salesforce, creating an opportunity, possibly adding products, and changing the reseller.
# Author: Aswathy/Jhansi
# Reviewer: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_IndirectOpportunity_ResellerChange.xlsx"
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
def test_IndirectOpportunity_ResellerChange(
    page: Page, base_url, config, test_case
) -> None:
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
        # =================================Login to SFDC==========================================================================
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

            spark_url = hp.getCurrentURL()
            logger.info(f"Spark URL: {spark_url}")

            # =======================Create Opportunity===========================================================================
            if test_case["Create Opportunity"].strip().lower() == "yes":

                cm.clickElement("HomePage", "opportunities_Tab")
                logger.info(f"Clicked on opportunities tab")

                cm.clickElement("HomePage", "new_Opportunity_Button")
                logger.info(f"Clicked on new opportunity button")

                if is_valid_data(test_case["Account Name"]):
                    co.enterAccount(test_case["Account Name"])
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
                            co.enterOpportunityName(test_case["Opportunity Name"])
                            logger.info(f"Entered opportunity name")
                        if is_valid_data(test_case["Primary Contact"]):
                            co.select_PrimaryContact(test_case["Primary Contact"])
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
                            logger.info(f"Selected channel: {test_case['Channel']}")

                    if test_case["Opportunity Type"] == x1p_Oppty:
                        if is_valid_data(test_case["Opportunity Name"]):
                            co.enterOpportunityName_1p(test_case["Opportunity Name"])
                            logger.info(f"Entered opportunity name")
                        if is_valid_data(test_case["Sales Type"]):
                            cm.selectOptionInListbox(
                                "CreateOpportunity",
                                "sales_Type_1P",
                                test_case["Sales Type"],
                            )
                            logger.info(
                                f"Selected 1P sales type: {test_case['Sales Type']}"
                            )
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
                        if is_valid_data(test_case["Distrubutor"]):
                            cm.selectOptionInListbox(
                                "CreateOpportunity",
                                "distributor",
                                test_case["Distrubutor"],
                            )
                            logger.info(
                                f"Selected distributor: {test_case['Distrubutor']}"
                            )
                        cm.clickElement("CreateOpportunity", "next_Button")
                        logger.info(f"Clicked on next button")

                    oppty_number = cm.readText(
                        "CreateOpportunity", "opportunity_Number"
                    )
                    logger.info(f"Opportunity Number: {oppty_number}")
                    print(f"\033[94mℹ️ Opportunity Number: {oppty_number}\033[0m")

                    oppty_name = cm.readText("CreateOpportunity", "opportunity_Name")
                    logger.info(f"Opportunity Name: {oppty_name}")
                    print(f"\033[94mℹ️ Opportunity Name: {oppty_name}\033[0m")

                spark_url = cm.getCurrentURL()
                logger.info(f"Captured Spark URL: {spark_url}")
                print(f"\033[94mℹ️ Captured Spark URL: {spark_url}\033[0m")

            #  ==============================Update Reseller Account in Indirect Opportunity through Account Parties========================
            if test_case["Change Reseller"].strip().lower() == "yes":

                cm.mouseWheel("down", 300, 2)
                cm.scrollToElement("HomePage", "account_Parties_link")
                
                cm.clickElement("HomePage", "account_Parties_link")
                logger.info(f"Opened account party related list")

                cm.clickElement("HomePage", "show_Actions")
                logger.info(f"Clicked on show actions button")
                cm.clickElementAndWait("HomePage", "delete_MenuItem", 2)
                logger.info(f"Selected delete menu item")
                cm.clickElementAndWait("HomePage", "delete", 2)
                logger.info(
                    f"Clicked on delete button and deleted existing account parties"
                )

                cm.clickElement("HomePage", "new_Button")
                logger.info(f"Clicked on new button in account parties page")
                cm.clickElement("HomePage", "account_Combobox")
                logger.info(f"Clicked on account combobox")
                # cm.selectComboboxOption(
                #     "HomePage", "account_Combobox", test_case["Partner Account"]
                # )
                cm.enterText("HomePage", "account_Combobox", test_case["Partner Account"])
                cm.clickByTextByPosition(test_case["Partner Account"], "last", 1)
                logger.info(
                    f"Selected account: {test_case['Partner Account']} in account combobox"
                )
                cm.clickElement("HomePage", "role_Combobox")
                logger.info(f"Clicked on role combobox")
                cm.clickByText("Reseller")
                logger.info(f"Selected role as Reseller in role combobox")
                cm.clickElementByPosition("HomePage", "save_Button", "last", 1)
                logger.info(f"Clicked on save button in account parties page")
                logger.info(f"Added account party: {test_case['Partner Account']}")

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to opportunity details page")

                cm.clickElementAndWait("HomePage", "partner_Tab", 2)
                logger.info(f"Navigated to Partner tab")

                cm.mouseWheel("down", 200, 2)
                cm.clickElementByPosition(
                    "HomePage", "edit_Reseller_Partner_Tab", "first", 0
                )
                cm.clickElementAndWait("HomePage", "reseller", 2)
                logger.info(f"Clicked on reseller combobox")
                cm.pressKey("HomePage", "reseller", "Delete")
                logger.info(f"Cleared existing reseller value")
                co.selectReseller(
                    test_case["Partner Account"]
                )  # utilized same as in create opportunity code
                logger.info(
                    f"Selected new reseller value: {test_case['Partner Account']}"
                )
                cm.clickElementAndWait("HomePage", "save_Button", 2)
                logger.info(f"Updated reseller: {test_case['Partner Account']}")

                # Validation of updated reseller value in the opportunity details page
                if test_case["Reseller Validation"].strip().lower() == "yes":
                    cm.refreshPage()
                    logger.info(f"Refreshed the page")

                    cm.clickElementAndWait("HomePage", "partner_Tab", 2)
                    logger.info(f"Navigated to Partner tab")

                    if is_valid_data(test_case["Partner Account_1"]):
                        actual_reseller = cm.readTextAndWait(
                            "HomePage", "reseller_Value", wait_time=2
                        )
                        logger.info(
                            f"Captured actual reseller value: {actual_reseller}"
                        )
                        reseller_validation = cm.assertText(
                            "HomePage", "reseller_Value", test_case["Partner Account_1"]
                        )
                        if reseller_validation:
                            logger.info(
                                f"Compared actual Reseller account: {actual_reseller} with expected Reseller account: {test_case['Partner Account_1']}"
                            )
                            print(
                                f"✅ Compared actual Reseller account: {actual_reseller} with expected Reseller account: {test_case['Partner Account_1']}"
                            )
                        else:
                            failure_message = f"Reseller change Validation Failed: Expected '{test_case['Partner Account_1']}' but got '{actual_reseller}'"
                            validation_failures.append(
                                failure_message
                            )  # Add failure to the list
                            logger.warning(failure_message)
                            print(f"❌ {failure_message}")

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
                    oppty_number,
                    oppty_name,
                    "Opportunity created successfully",
                ],
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
