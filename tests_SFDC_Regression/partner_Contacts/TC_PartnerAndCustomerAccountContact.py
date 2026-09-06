import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Account_Detail import AccountDetail
from utils.data_validation import is_valid_data
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# ADO Test ID - 481855 and 482414
# Test Scenario: 1) Verify users are not able to create 'Customer' contact for 'Partner' account
#                2) Verify users are not able to create 'Partner' contact for 'Customer' account
# Test Description: This test verifies that users cannot add a customer and partner contact to a partner and customer account respectively in Salesforce.
#                   The test attempts to add a new contact to a partner and customer account and validates that an appropriate error
#                   message is displayed, indicating that the action is not permitted. The test covers the following steps:
#                   1. Login to Salesforce using valid credentials.
#                   2. Navigate to the Accounts tab and search for a specific partner account.
#                   3. Attempt to add a new customer and partner contact to the partner and customer account.
#                   4. Validate that the correct error message is displayed, indicating the restriction.
#                   5. Capture the test results and write them to an Excel file.
# Author & Modifier: Aswathy S and Ayushee
# Reviewer : Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_PartnerAndCustomerAccountContact.xlsx"
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
def test_Partner_And_Customer_Account_Contact(page: Page, base_url, config, test_case) -> None:
    ad = AccountDetail(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []

    try:
        # ==================================Login to SFDC=================================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']} and for the test case id {test_case['Test Case ID']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']} and for the test case id {test_case['Test Case ID']}*****\033[0m"
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
#==========================================Account Tab Navigation===============================#
            cm.clickElement("HomePage", "accounts_Tab")
            logger.info("Clicked on Account tab")

            cm.clickElement("HomePage", "search_Bar")
            logger.info("Clicked on search bar")

            if is_valid_data(test_case["Account Name"]):
                cm.enterText(
                    "HomePage", "search_Bar", test_case["Account Name"]
                )
                logger.info(f"Entered search term: {test_case['Account Name']}")

                cm.pressKey("HomePage", "search_Bar", "Enter")
                logger.info(
                    f"Pressed Enter key to search for: {test_case['Account Name']}"
                )

                cm.clickByText(test_case["Account Name"])
                logger.info(
                    f"Clicked on searched account: {test_case['Account Name']}"
                )
            if test_case["Contact Type"].strip().lower() == "customer":          
                cm.scrollToElement("HomePage", "show_All_Details_Button")
                logger.info("Scrolled to Show All Details button")

                cm.clickElement("HomePage", "show_All_Details_Button")
                logger.info("Clicked on Show All Details button")

                cm.clickElementByPosition("HomePage", "contacts_Link", "nth", 1)
                logger.info("Clicked on New button to add new contact")

            if test_case["Contact Type"].strip().lower() == "partner":
                cm.scrollToElement("ContactPage", "view_All_Link")
                logger.info("Scrolled to View All Details button")
                
                cm.clickElement("ContactPage", "view_All_Link")
                logger.info("Clicked on View All Details button")

            if test_case["Add Contact"].strip().lower() == "yes":
                cm.clickElement("HomePage", "new_Button")
                logger.info("Clicked on New button to add new contact")

            if test_case["Contact Type"].strip().lower() == "partner":
                cm.clickElement("ContactPage","partner_Radio_Button")
                logger.info("Clicked on radio button to select Partner Contact")

            cm.clickElement("HomePage", "next_Button")
            logger.info("Clicked on Next button to proceed with adding new contact")

            if is_valid_data(test_case["Salutation"]):
                ad.selectSalutation(test_case["Salutation"])
                logger.info(f"Selected salutation: {test_case['Salutation']}")

            if is_valid_data(test_case["First Name"]):
                cm.enterText(
                    "HomePage", "first_Name_Textbox", test_case["First Name"]
                )
                logger.info(f"Entered first name: {test_case['First Name']}")

            if is_valid_data(test_case["Last Name"]):
                cm.enterText(
                    "HomePage", "last_Name_Textbox", test_case["Last Name"]
                )
                logger.info(f"Entered last name: {test_case['Last Name']}")

            if test_case["Contact Type"].strip().lower() == "customer":

                if is_valid_data(test_case["Account Name"]):
                    ad.selectAccountName(test_case["Account Name"])
                    logger.info(
                        f"Selected account name: {test_case['Account Name']}"
                )
                if is_valid_data(test_case["Email"]):
                    cm.enterText("HomePage", "email_Textbox", test_case["Email"])
                    logger.info(f"Entered email: {test_case['Email']}")

                if is_valid_data(str(test_case["Phone"])):
                    cm.enterText("HomePage", "phone_Textbox", str(test_case["Phone"]))
                    logger.info(f"Entered phone: {test_case['Phone']}")

            if test_case["Contact Type"].strip().lower() == "partner":
                cm.enterText("ContactPage", "email_TextBox", test_case["Email"])
                logger.info(f"Entered email: {test_case['Email']}")

            cm.clickElementByPosition("HomePage", "save_Button", "nth", 0)
            logger.info("Clicked on Save button to save the new contact")

            if test_case["Contact Type"].strip().lower() == "customer":
                if test_case["Validate Error Message"].strip().lower() == "yes":

                    if is_valid_data(test_case["Error Message"]):

                        error_message = cm.readText("HomePage", "error_Label_2")
                        logger.info(f"Read error message: {error_message}")

                        comparison_result = cm.checkExpectedTextInActual(
                            error_message, test_case["Error Message"]
                        )

                        if not comparison_result:
                            failure_message = f"Error message validation failed: Expected '{test_case['Error Message']}' but got different message"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual error message with expected error message: {test_case['Error Message']}"
                            )
                            print(
                                f"\033[92m✅ Compared actual error message with expected error message: {test_case['Error Message']}\033[0m\n"
                                f"\033[92m✅ User is not able to add customer contact for partner account\033[0m"
                            )

            if test_case["Contact Type"].strip().lower() == "partner":
                if test_case["Validate Error Message"].strip().lower() == "yes":

                    if is_valid_data(test_case["Error Message"]):

                        error_message = cm.readText("HomePage", "error_Label")
                        logger.info(f"Read error message: {error_message}")

                        comparison_result = cm.checkExpectedTextInActual(
                            error_message, test_case["Error Message"]
                        )

                        if not comparison_result:
                            failure_message = f"Error message validation failed: Expected '{test_case['Error Message']}' but got different message"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual error message with expected error message: {test_case['Error Message']}"
                            )
                            print(
                                f"\033[92m✅ Compared actual error message with expected error message: {test_case['Error Message']}\033[0m\n"
                                f"\033[92m✅ User is not able to add partner contact for customer account\033[0m"
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

            # =========================================Capture Test Result and Write To Excel================================================
            test_results = [
                [
                    "Test Case ID",
                    "Execution Status",
                    "Details",
                ],
                [
                    script_name,
                    boolean_status,
                    f"{script_name} Test Script Execution Completed Successfully",
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
            # If execution flag is not 'yes', explicitly skip the test
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
