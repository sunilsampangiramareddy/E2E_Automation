import pytest
import logging
import os
from playwright.sync_api import Page

from pages_SFDC.Create_Lead import CreateLead
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from utils.locator_manager import LocatorManager
from common_Methods.Common_Methods import CommonMethods

# =============================================================================
# Test Scenario  : 491228 TC04 –Sales Type for Standard Oppty from Lead Conversion – Land, Expand and Protect Customer Types
# Test Description: Validates that the Sales Type is correctly assigned on an
#                   opportunity created from lead conversion, and that invalid
#                   Sales Type edits produce appropriate error messages.
# Modified By    : Alok
# Author         : Ashwathy Sreelekha
# =============================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_Sales_Type_Lead_Conversion.xlsx"
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
def test_sales_type_lead_conversion_test(
    page: Page, base_url, config, test_case
) -> None:
    cl = CreateLead(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []

    try:
        # =================================Login to SFDC==========================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"***{script_name} - Test Script Execution Started for TestCase IDs - {test_case['Iteration']}***"
            )
            print(
                f"ℹ️ ***{script_name} - Test Script Execution Started for TestCase IDs - {test_case['Iteration']}***"
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
            if is_visible:
                logger.info(f"Opportunities label has been verified on the homepage")
                print(f"✅ Opportunities label verified on the homepage")
            else:
                print("❌ Opportunities label not visible on the homepage")
                validation_failures.append(
                    "Opportunities label not visible on the homepage"
                )

            spark_url_home = cm.getCurrentURL()
            logger.info(f"Spark URL: {spark_url_home}")
            print(f"ℹ️ Spark URL: {spark_url_home}")

            # =======================Create Lead===========================================================================
            if test_case["Create Lead"].strip().lower() == "yes":

                cm.clickElement("HomePage", "leads_Link")
                logger.info("Leads link clicked")

                cl.createNewLead(
                    test_case["Salutation"],
                    test_case["Primary Contact"],
                    test_case["Lead Account Name"],
                    test_case["Company Name"],
                    test_case["Mobile"],
                    test_case["Address"],
                    test_case["Street"],
                    test_case["City"],
                    test_case["Zip"],
                    test_case["Meeting Type"],
                    test_case["Qualification criteria"],
                    test_case["Meeting link"],
                    test_case["Product"],
                    test_case["Meeting Category"],
                )
                logger.info("Lead created")

            cm.clickElement("LeadDetail", "converted_status_button")
            cm.clickElement("LeadDetail", "select_converted_status_button")
            cm.selectDropdownByText("LeadDetail", "status_dropdown", "Qualified")
            cm.clickElement("LeadDetail", "save_button")
            logger.info("Lead qualified")
            cm.assertContainsText(
                "LeadDetail", "lead_heading", test_case["Primary Contact"]
            )

            cm.waitForStable(30)
            logger.info("Waiting for lead conversion to complete")
            cm.refreshPage()
            logger.info("Page refreshed after lead conversion")
            cm.waitForStable(3)
            logger.info("Waiting for lead conversion to complete")

            # cm.scrollToElement("LeadDetail", "opportunity_name_label")
            # cm.scrollToBottom

            page.mouse.wheel(0, 3800)
            cm.clickElement("LeadDetail", "opportunity_name_link")
            logger.info("Opportunity name clicked")

            spark_url = cm.getCurrentURL()
            logger.info(f"Opportunity URL: {spark_url}")
            print(f"ℹ️ Opportunity URL: {spark_url}")

            oppty_sales_type = cm.readText(
                "CreateOpportunity", "opportunity_Sales_Type"
            )
            logger.info(f"Opportunity Sales Type: {oppty_sales_type}")
            print(f"ℹ️ Opportunity Sales Type: {oppty_sales_type}")

            if cm.assertExpectedActualText(oppty_sales_type, test_case["Sales Type"]):
                print(f"✅ Sales Type validated: {oppty_sales_type}")
            else:
                print(
                    f"❌ Sales Type mismatch: Expected '{test_case['Sales Type']}' but got '{oppty_sales_type}'"
                )
                validation_failures.append(
                    f"Sales Type mismatch: Expected '{test_case['Sales Type']}' but got '{oppty_sales_type}'"
                )

            cm.clickElement("CreateOpportunity", "edit_Sales_Play_Button")
            cm.clickElement("CreateOpportunity", "sales_Play_Combobox")
            cm.clickByText(test_case["Sales Play"])
            cm.clickElement("HomePage", "save_Button")
            logger.info(f"Edited opportunity sales play to {test_case['Sales Play']}")

            if test_case["Sales Type Error"].strip().lower() == "yes":

                cm.clickElement("CreateOpportunity", "edit_Sales_Type_Button")
                cm.clickElement("CreateOpportunity", "sales_Type_Combobox")
                cm.clickByText(test_case["Sales Type Invalid"])
                cm.clickElement("HomePage", "save_Button")
                logger.info(f"Edited opportunity sales type")

                result = cm.assertContainsText(
                    "HomePage", "error_Label", test_case["Error Message"]
                )
                if result:
                    logger.info("Validated error message")
                    print(f"✅ Error message validated: {test_case['Error Message']}")
                else:
                    print(
                        f"❌ Expected error message to contain '{test_case['Error Message']}'"
                    )
                    validation_failures.append(
                        f"Expected error message to contain '{test_case['Error Message']}'"
                    )

                cm.clickElement("HomePage", "cancel_Button")

            cm.clickElementByPosition("HomePage", "show_more_actions", "nth", 0)

            cm.waitForElementState(
                "CreateOpportunity",
                "copy_Opportunity_MenuItem",
                "visible",
                timeout=5000,
            )
            cm.clickElement("CreateOpportunity", "copy_Opportunity_MenuItem")
            logger.info(f"Clicked on copy opportunity button")

            cm.clickElement("CreateOpportunity", "continue_Button")
            logger.info(f"Clicked on continue button")

            cm.waitForStable(2)

            oppty_sales_type = cm.readText(
                "CreateOpportunity", "opportunity_Sales_Type"
            )
            if cm.assertExpectedActualText(oppty_sales_type, test_case["Sales Type"]):
                logger.info(
                    f"Validated opportunity sales type is {test_case['Sales Type']}"
                )
                print(
                    f"✅ Sales Type validated on copied opportunity: {oppty_sales_type}"
                )
            else:
                print(
                    f"❌ Sales Type mismatch: Expected '{test_case['Sales Type']}' but got '{oppty_sales_type}'"
                )
                validation_failures.append(
                    f"Sales Type mismatch: Expected '{test_case['Sales Type']}' but got '{oppty_sales_type}'"
                )

            if test_case["Customer Type"].strip() == "Expand":

                cm.waitForStable(5)

                cm.clickElement("CreateOpportunity", "edit_Sales_Type_Button")
                cm.clickElement("CreateOpportunity", "sales_Type_Combobox")
                cm.clickByText(test_case["Sales Type 2"])
                cm.clickElement("HomePage", "save_Button")
                logger.info(
                    f"Edited opportunity sales type to {test_case['Sales Type 2']}"
                )

                result = cm.assertContainsText(
                    "HomePage",
                    "error_Label",
                    (test_case["Installed Base Type Error Message"]),
                )
                if result:
                    logger.info("Validated error message")
                    print(
                        f"✅ Error message validated: {test_case['Installed Base Type Error Message']}"
                    )
                else:
                    print(
                        f"❌ Expected error message to contain '{test_case['Installed Base Type Error Message']}'"
                    )
                    validation_failures.append(
                        f"Expected error message to contain '{test_case['Installed Base Type Error Message']}'"
                    )

                cm.clickElement("HomePage", "cancel_Button")

                cm.clickElement("CreateOpportunity", "edit_Sales_Type_Button")
                cm.clickElement("CreateOpportunity", "sales_Type_Combobox")
                cm.clickByText(test_case["Sales Type 3"])
                cm.clickElement("CreateOpportunity", "installed_Base_Type_Combobox")
                cm.clickByText(test_case["Installed Base Type"])
                cm.clickElement("CreateOpportunity", "sales_Play_Combobox")
                cm.clickByText(test_case["Sales Play 2"])
                cm.clickElement("HomePage", "save_Button")
                logger.info(
                    f"Edited opportunity sales type to {test_case['Sales Type 3']}"
                )

                cm.clickElement("CreateOpportunity", "edit_Sales_Type_Button")
                cm.clickElement("CreateOpportunity", "sales_Type_Combobox")
                cm.clickByText(test_case["Sales Type 2"])
                cm.clickElement("CreateOpportunity", "installed_Base_Type_Combobox")
                cm.clickByTextByPosition(test_case["Installed Base Type 2"], "nth", 0)
                cm.clickElement("CreateOpportunity", "sales_Play_Combobox")
                cm.clickByText(test_case["Sales Play 3"])
                cm.clickElement("HomePage", "save_Button")
                logger.info(
                    f"Edited opportunity sales type to {test_case['Sales Type 2']}"
                )

                result = cm.assertContainsText(
                    "HomePage", "error_Label", (test_case["Sales Type Error Message"])
                )
                if result:
                    logger.info(
                        f"Validated error message for sales type change when sales type is renewal"
                    )
                    print(
                        f"✅ Error message validated: {test_case['Sales Type Error Message']}"
                    )
                else:
                    print(
                        f"❌ Expected error message to contain '{test_case['Sales Type Error Message']}'"
                    )
                    validation_failures.append(
                        f"Expected error message to contain '{test_case['Sales Type Error Message']}'"
                    )

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
                    "Details",
                ],
                [
                    script_name,
                    boolean_status,
                    "Opportunity created successfully",
                ],
            ]
            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)
            logger.info(
                f"***{script_name} Test Script Execution Completed Successfully***"
            )
            print(
                f"✅ ***{script_name} Test Script Execution Completed Successfully***"
            )
        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
            )
            print(
                f"➡️ Execution flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
            )
            pytest.skip(
                f"Execution flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
