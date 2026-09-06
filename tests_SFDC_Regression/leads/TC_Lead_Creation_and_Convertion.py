import pytest
import logging
import os
from datetime import datetime
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
# ADO Test IDs :  473707,473789,474716
# Test Scenario: 
# 1. Verify that DSR can create a lead and Lead can be converted to Opportunity
# 2. Verify that for Opportunities that are created by Lead Conversion, the Meeting Outcome field is mandatory to close lost the opportunity.
# 3. Verify the person who is the Meeting feedback assignee will be added to the Opportunity Team, with a role of Secondary Client Executive with Edit Access if the person is different than the Opportunity Owner.
# Test Description: This test script validates the creation of a lead by a DSR and its subsequent conversion to an opportunity. It checks for proper error messages, field validations, and successful lead conversion.
# Author & Modifier: Aswathy S
# Reviewer: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_Lead_Creation_and_Conversion.xlsx")
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
def test_Lead_Creation_and_Conversion(page: Page, base_url, config, test_case) -> None:
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

            if test_case["Navigate to Account"].strip().lower() == "yes":

                cm.clickElement("HomePage", "accounts_Tab")
                logger.info("Clicked on Account tab")

                cm.clickElement("HomePage", "search_Bar")
                logger.info("Clicked on search bar")

                if is_valid_data(test_case["Account Name"] and str(test_case["Account CMAT"])):              

                    cm.enterText("HomePage", "search_Bar", str(test_case["Account CMAT"]))
                    logger.info(f"Entered search term: {test_case['Account CMAT']}")

                    cm.pressKey("HomePage", "search_Bar", "Enter")
                    logger.info(f"Pressed Enter key to search for: {test_case['Account Name']}")

                    cm.clickByTextAndWait(test_case["Account Name"],8)
                    logger.info(f"Clicked on searched account: {test_case['Account Name']}")
                    
                    account_url = cm.getCurrentURL()
                    logger.info(f"{account_url}")

                    cm.mouseWheel("HomePage", 800, scrolls=2, wait_time=1)

                    cm.clickElement("HomePage","account_leads_Link")
                    logger.info("Leads link clicked")

            # ==================================Add new lead=================================================================================
            elif test_case["Navigate to Account"].strip().lower() == "no":
                cm.clickElementByPosition("HomePage","leads_Link","nth",0)
                logger.info("Leads link clicked")

            if test_case["Create Lead"].strip().lower() == "yes":

                cm.clickElement("HomePage", "new_Button")
                logger.info("Clicked on New button to create a new Lead")

                cm.clickElement("HomePage", "salutation_Dropdown")
                logger.info("Clicked on Salutation dropdown")

                if(is_valid_data(test_case["Salutation"])):
                    cm.clickByText(test_case["Salutation"])
                    logger.info("Selected Salutation dropdown")

                cm.clickElement("HomePage", "first_Name_Input")
                logger.info("Clicked on First Name field")

                if(is_valid_data(test_case["First Name"])):
                    cm.enterText("HomePage", "first_Name_Input", test_case["First Name"])
                    logger.info("Entered First Name field")

                cm.clickElement("HomePage", "last_Name_Input")
                logger.info("Clicked on Last Name field")

                if(is_valid_data(test_case["Last Name"])):
                    cm.enterText("HomePage", "last_Name_Input", test_case["Last Name"])
                    logger.info("Entered Last Name field")

                cm.clickElement("HomePage", "company_Input")
                logger.info("Clicked on Company field")

                if(is_valid_data(test_case["Account Name"])):
                    cm.enterText("HomePage", "company_Input", test_case["Account Name"])
                    logger.info("Entered name in Company field")

                if(test_case["Validate Error Message"].strip().lower() == "yes"):

                    if is_valid_data(test_case["Error Message"]):
                        cm.clickElementByPositionAndWait("HomePage","save_Button","nth",1,5)
                        logger.info("Saved changes")
                        error_message = cm.readText("HomePage", "error_Label")
                        logger.info(f"Read error message: {error_message}")
    
                        comparison_result = cm.checkExpectedTextInActual(error_message, test_case["Error Message"])
    
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
                            )
                        cm.clickElement("HomePage", "close_Error_Button")
                        logger.info("Clicked on Close button")

                if test_case["Navigate to Account"].strip().lower() == "no":
                    cm.clickElement("HomePage", "lead_Account")
                    cm.enterText("HomePage", "lead_Account", test_case["Account Name"])
                    cm.clickByTextByPosition(test_case["Account CMAT"], "nth", 0)
                    logger.info(f"Selected account: {test_case['Account Name']}")

                email=cm.generateRandomEmail()

                cm.clickElement("HomePage","email_Input")
                logger.info("Clicked email field")

                cm.enterTextAndWait("HomePage", "email_Input", email,5)
                logger.info("Entered email")

                cm.clickElementByPositionAndWait("HomePage","save_Button","nth",1,5)
                logger.info("Saved changes")

                lead_Name = f"{test_case['Salutation']} {test_case['First Name']} {test_case['Last Name']}"
                logger.info(f"Captured lead name: {lead_Name}")
                print(f"\033[92m✅ Captured lead name: {lead_Name}\033[0m\n")

            if test_case["Navigate to Account"].strip().lower() == "yes":
                cm.clickByTextByPosition(lead_Name, "nth", 0)

            cm.waitForStable(8)
            lead_url = cm.getCurrentURL()
            logger.info(f"Captured lead URL: {lead_url}")

            if test_case["Qualify Lead"].strip().lower() == "yes":

                if test_case["Navigate to Account"].strip().lower() == "yes":
                    cm.mouseWheel("HomePage", 800, scrolls=4, wait_time=3)
                else:
                    cm.mouseWheel("HomePage", 800, scrolls=6, wait_time=3)
                logger.info("Scrolled down the page")

                cm.clickElement("HomePage", "edit_meeting_set_date_Button")
                logger.info("Clicked on Edit Meeting Set Date button")

                cm.clickElement("HomePage", "grp_meeting_set_date")

                meeting_date = cm.generateDate("mm/dd/yyyy")
                cm.enterText("HomePage", "grp_meeting_set_date", meeting_date)
                logger.info(f"Entered Meeting Set Date: {meeting_date}")

                if is_valid_data(test_case["Meeting Type"]):
                    cm.clickElement("HomePage", "cmb_meeting_type")
                    cm.pressEnter("HomePage", "cmb_meeting_type")
                    logger.info("Clicked on Meeting Type dropdown")
                    cm.clickByText(test_case["Meeting Type"])
                    logger.info(f"Selected Meeting Type: {test_case['Meeting Type']}")

                if is_valid_data(test_case["Qualification Criteria"]):
                    cm.enterText(
                        "HomePage", "txt_qualification_criteria", test_case["Qualification Criteria"]
                    )

                if is_valid_data(test_case["Meeting Link"]):
                    cm.enterText("HomePage", "txt_meeting_link", test_case["Meeting Link"])

                if is_valid_data(test_case["Product"]):
                    cm.clickElement("HomePage", "cmb_product")
                    cm.enterText("HomePage", "cmb_product", test_case["Product"])
                    cm.pressEnter("HomePage", "cmb_product")
                    cm.clickByTextByPosition(test_case["Product"],"nth",1)
                    logger.info(f"Selected Product: {test_case['Product']}")

                if is_valid_data(test_case["Meeting Category"]):
                    cm.clickElement("HomePage", "cmb_meeting_category")
                    cm.pressEnter("HomePage", "cmb_meeting_category")
                    cm.pressKey("HomePage", "cmb_meeting_category", "ArrowDown")
                    cm.pressKey("HomePage", "cmb_meeting_category", "ArrowDown")
                    cm.pressEnter("HomePage", "cmb_meeting_category")

                cm.clickElementByPositionAndWait("HomePage", "save_Button", "nth", 0, 5)
                logger.info("Clicked on Save button")

                if test_case["Change Meeting assignee"].strip().lower() == "yes":
                                    
                    cm.clickElement("HomePage", "edit_Meeting_Assignee_Button")
                    logger.info("Clicked on Change Meeting Assignee button")

                    cm.clickElement("HomePage", "clear_Assignee_Button")
                    logger.info("Clicked on Clear Meeting Assignee button")

                    if is_valid_data(test_case["Meeting Assignee"]):
                        cm.enterText("HomePage", "meeting_Assignee", test_case["Meeting Assignee"])
                        cm.clickByTextByPosition(test_case["Meeting Assignee"], "nth", 1)
                        logger.info(f"Selected Meeting Assignee: {test_case['Meeting Assignee']}")

                    cm.clickElementByPositionAndWait("HomePage", "save_Button", "nth", 0, 5)
                    logger.info("Clicked on Save button")

                cm.clickByText("Converted")
                logger.info("Clicked converted")

                cm.clickByText("Select Converted Status")
                logger.info("Clicked select converted status")      

                cm.clickElement("HomePage","converted_Status_Dropdown")
                logger.info("Clicked select converted status")     

                if is_valid_data(test_case["Converted Status"]):
                    cm.pressKey("HomePage","converted_Status_Dropdown","ArrowDown")
                    cm.pressEnter("HomePage","converted_Status_Dropdown")
                    logger.info(f"Selected converted status: {test_case['Converted Status']}")

                cm.clickElementAndWait("HomePage","save_Button",30)
                logger.info("Clicked save button")

                lead_url = cm.getCurrentURL()
                logger.info(f"Captured lead URL after conversion: {lead_url}")

                cm.refreshPage()
                logger.info("Refreshed the page")

                if test_case["Navigate to Account"].strip().lower() == "yes":
                    cm.mouseWheel("HomePage", 800, scrolls=5, wait_time=3)
                else:
                    cm.mouseWheel("HomePage", 800, scrolls=6, wait_time=3)
                logger.info("Scrolled down the page")

                oppty_Name = cm.readText("HomePage","oppty_Label_Lead")
                logger.info(f"Captured opportunity name: {oppty_Name}")
                print(f"\033[92m✅ Captured opportunity name: {oppty_Name}\033[0m\n")

                cm.clickElementAndWait("HomePage","oppty_Label_Lead",5)
                logger.info(f"Clicked on opportunity name: {oppty_Name}")

                oppty_url = cm.getCurrentURL()
                logger.info(f"Captured opportunity URL: {oppty_url}")

                if test_case["Validate Meeting assignee"].strip().lower() == "yes":
                    cm.mouseWheel("HomePage", 800, scrolls=1, wait_time=2)
                    
                    cm.clickElement("HomePage","opportunity_Teams_Link")
                    logger.info("Clicked on opportunity teams link")

                    oppty_teams_grid = cm.readText("HomePage","grid")

                    comparison_result1 = cm.checkExpectedTextInActual(oppty_teams_grid, test_case["Meeting Assignee"])
                    comparison_result2 = cm.checkExpectedTextInActual(oppty_teams_grid, test_case["Role"])
                        
                    if not comparison_result1 or not comparison_result2:
                        failure_message = f"Error message validation failed: Expected '{test_case['Meeting Assignee']}' and '{test_case['Role']}' but got different message"
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual opportunity teams grid with expected Meeting Assignee: {test_case['Meeting Assignee']} and Role: {test_case['Role']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual opportunity teams grid with expected Meeting Assignee: {test_case['Meeting Assignee']} and Role: {test_case['Role']}\033[0m\n"                                                            
                        )
                    

                if test_case["Close Opportunity"].strip().lower() == "yes":

                    cm.clickElement("HomePage","mark_As_Closed_Lost")
                    logger.info("Clicked on Mark as Closed Lost button")

                    if is_valid_data(test_case["Closed Reason"]):
                        cm.selectDropdownByText("HomePage","reason_Dropdown",test_case["Closed Reason"])
                        logger.info(f"Selected Close Lost Reason: {test_case['Closed Reason']}")

                    if is_valid_data(test_case["Primary Reason"]):
                        cm.selectDropdownByIndex("HomePage","primary_reason_Dropdown",2)
                        logger.info(f"Selected Close Lost Primary Reason: {test_case['Primary Reason']}")

                    if is_valid_data(test_case["Additional Insights"]):
                        cm.enterText("HomePage","additional_Insights",test_case["Additional Insights"])
                        logger.info(f"Entered Additional Insights: {test_case['Additional Insights']}")

                    if is_valid_data(test_case["Competitor"]):
                        cm.selectDropdownByIndex("HomePage","competitor",14)
                        logger.info(f"Selected Competitor: {test_case['Competitor']}")

                    cm.clickElementAndWait("HomePage","save_Button",5)

                    if test_case["Validate Close Lost Error Message"].strip().lower() == "yes":
                        if is_valid_data(test_case["Close Lost Error Message"]):
                            error_message = cm.readText("HomePage", "exception_Error_Label")
                            logger.info(f"Read error message: {error_message}")
    
                            comparison_result = cm.checkExpectedTextInActual(error_message, test_case["Close Lost Error Message"])
    
                            if not comparison_result:
                                failure_message = f"Error message validation failed: Expected '{test_case['Close Lost Error Message']}' but got different message"
                                validation_failures.append(failure_message)
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")
                            else:
                                logger.info(
                                    f"Compared actual error message with expected error message: {test_case['Close Lost Error Message']}"
                                )
                                print(
                                    f"\033[92m✅ Compared actual error message with expected error message: {test_case['Close Lost Error Message']}\033[0m\n"                                                            
                                )

                    cm.clickElement("HomePage", "finish_Button")
                    logger.info("Clicked on Finish button")

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
