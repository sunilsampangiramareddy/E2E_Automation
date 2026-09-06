import pytest
import logging
import os
from playwright.sync_api import Page
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from common_Methods.Common_Methods import CommonMethods
 
 
# =========================================================================================================================
# Test Metadata
# =========================================================================================================================

# Test Scenario: 550148 - Verify DDS-related fields and guidance attributes are accessible only to authorized users and visible according to assigned permission sets.

# Test Description:
#                  1. Login to Salesforce with the primary test user and verify the Opportunities page is displayed.
#                  2. Open Setup and log in one by one as the configured Read/Edit and Read-Only user personas.
#                  3. Search for the Multi Quote record using the MQ ID from the test data.
#                  4. For Read/Edit users, verify DDS fields are visible and the Edit Deal Score action is available.
#                  5. For Read-Only users, verify DDS fields are visible and the Edit Deal Score action is not available.
#                  6. Log out each persona, return to the main tab, and record any validation failures.

# Author: Alok Kumar Gupta
# Reviewed by: Sunil Reddy
# =========================================================================================================================
 
 
logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_DDS_Accessibility_Validations.xlsx")
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
def test_DDS_Accessibility_Validations(page: Page, base_url, config, test_case) -> None:
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []
    oppty_name = ""
    oppty_number = ""
  
 
    try:
        # =================================Login to SFDC==========================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(f"***{script_name} - Test Script Execution Started for Iteration - {test_case['Iteration']} and {test_case['Test Case ID']} ***")
            print(f"ℹ️ ***{script_name} - Test Script Execution Started for Iteration - {test_case['Iteration']} and {test_case['Test Case ID']} ***")

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
                print(f"❌ Opportunities label is not visible on the homepage")
                validation_failures.append("Opportunities label is not visible on the homepage")
                ss.capture_screenshot("Captured Homepage details")

            if test_case["User Persona Login"].strip().lower() == "yes":

                User_Personas = [str(test_case["User Persona_Read/Edit"].strip()),                             
                                str(test_case["User Persona_Read-Only"].strip())]                              

                for User_Persona in User_Personas:              

                        cm.clickElement("HomePage", "setup_Icon")
                        cm.clickElement("HomePage", "setup_menu_item")
                        secondTab = cm.switchToTab(page.context, tab_index=1, expected_tab_count=2)
                        cm.waitForPageLoad(secondTab)
                        logger.info("Clicked on Setup icon")    
                        cm = CommonMethods(secondTab, locator_manager)
                        cm.clickElement("GeneralSetup", "search_Setup_Input")
                        cm.enterText(
                            "GeneralSetup", "search_Setup_Input", User_Persona
                        )
                        cm.clickByLinkText(
                            User_Persona, partial_match=True, occurrence=1
                        )
                        logger.info("Searched for user in Setup")

                        frame_locator_setup = locator_manager.get_locator("HomePage", "frame_Locator")
                        cm.switchToFrame(frame_locator_setup)
                        cm.page.get_by_role("button", name="Login", exact=True).nth(1).click()
                        logger.info("Clicked Login button from Setup frame")
                        cm = CommonMethods(secondTab, locator_manager)

                        if test_case["Authorised Users Accessibility Validation"].strip().lower() == "yes":
                            cm.clickElement("MultiQuoteWizard", "multi_Quotes_Link")
                            cm.waitForStable(5)
                            cm.clickElement("MultiQuoteWizard", "search_Searchbox")
                            legacy_mq_id = str(
                                cm.convertDoubleToInt(float(test_case["MultiQuote ID"]))
                            ).strip()
                            cm.enterText("MultiQuoteWizard", "search_Searchbox", legacy_mq_id)
                            cm.pressKey("MultiQuoteWizard", "search_Searchbox", "Enter")
                            cm.waitForStable(3)
                            cm.clickByLinkText(legacy_mq_id, partial_match=True)

                            if User_Persona == str(test_case["User Persona_Read/Edit"]).strip():
                            
                                required_labels = [
                                    "deal_Score_To_2_Net_Label",
                                    "deal_Score_To_3_Net_Label",
                                    "deal_Score_To_4_Net_Label",
                                    "deal_Score_To_5_Net_Label",
                                    "Edit_Deal Score to 2 Net",
                                ]
                                all_labels_visible = cm.isElementVisibleInSequence(
                                    "MultiQuotePage", required_labels, 60000
                                )

                                if all_labels_visible:
                                    logger.info(f"{User_Persona} has the access to view and Edit the MQ.")
                                    print(f"✅ {User_Persona} has the access to view and Edit the MQ.")
                                else:
                                    logger.error(f"Either view access or edit access is missing for {User_Persona} on the MQ.")
                                    print(f"❌ Either view access or edit access is missing for {User_Persona} on the MQ.")
                                    validation_failures.append(
                                        f"Either view access or edit access is missing for {User_Persona} on the MQ."                   
                                    )

                                logout_link_text = f"Log out as {User_Persona}"
                                cm.clickByLinkText(logout_link_text, partial_match=True)
                                cm.waitForStable(10)
                                first_Tab = cm.closeCurrentTabAndSwitchToPreviousTab(page.context)
                                cm = CommonMethods(first_Tab, locator_manager)

                            if User_Persona == str(test_case["User Persona_Read-Only"]).strip():
                                            
                                required_labels = [
                                    "deal_Score_To_2_Net_Label",
                                    "deal_Score_To_3_Net_Label",
                                    "deal_Score_To_4_Net_Label",
                                    "deal_Score_To_5_Net_Label",
                                ]
                                all_labels_visible = cm.isElementVisibleInSequence(
                                    "MultiQuotePage", required_labels, 60000
                                )

                                isElementVisible = cm.isElementVisible("MultiQuotePage", "Edit_Deal Score to 2 Net")
                            
                                if all_labels_visible and not isElementVisible:
                                    logger.info(f"{User_Persona} has the access to only view the MQ and edit is disabled.")
                                    print(f"✅ {User_Persona} has the access to only view the MQ and edit is disabled.")
                                else:
                                    logger.error(f"Either view access is missing or edit is not disabled for {User_Persona} on the MQ.")
                                    print(f"❌ Either view access is missing or edit is not disabled for {User_Persona} on the MQ.")
                                    validation_failures.append(
                                        f"Either view access is missing or edit is not disabled for {User_Persona} on the MQ."                   
                                    )

                                logout_link_text = (
                                    f"{test_case['Log out Partial Label']} {User_Persona}"
                                )
                                cm.clickByLinkText(logout_link_text, partial_match=True)
                                cm.waitForStable(10)
                                first_Tab = cm.closeCurrentTabAndSwitchToPreviousTab(page.context)
                                cm = CommonMethods(first_Tab, locator_manager)
                            

               

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
            logger.info(f"***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}***")
            print(f"✅ ***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']} ***")

        else:
            logger.info(f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}")
            print(f"➡️ Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}")
            pytest.skip(f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}")
 
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
 