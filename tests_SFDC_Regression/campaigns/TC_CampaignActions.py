import pytest
import logging
import os
from common_Methods.Common_Methods import CommonMethods
from playwright.sync_api import Page
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.campaign import Campaign
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# ADO Test ID - 482738
# Test Scenario: Regression test for Campaign Show Actions
# Test Description: This test script automates the validation of the Campaign Show Actions dropdown.
#                   It navigates to the Campaign app through the App Launcher, opens the Campaign page,
#                   verifies that the 'Create and Edit' option is not available in the Show Actions dropdown.
# Author: Aswathy Sreelekha
# Modified By: Ayushee
# Reviewer: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_CampaignActions.xlsx"
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
def test_CampaignsActions(page: Page, base_url, config, test_case) -> None:
    hp = HomePage(page)
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

            # =========== Navigate to Campaigns and verify Show Actions ============#

            if test_case["Click On Setup Icon"].strip().lower() == "yes":
                cm.clickElement("HomePage", "setup_Icon")
                cm.clickElement("HomePage", "click_On_Setup_Icon", 5)
                logger.info(f"Clicked on Setup icon")

                second_Tab = cm.switchToTab(
                    page.context, tab_index=1, expected_tab_count=2
                )
                logger.info("Switched to the new tab after clicking on SetUp Icon")

                if is_valid_data(test_case["User Persona"]):
                    cm = CommonMethods(second_Tab, locator_manager)
                    cm.clickElement("CampaignPage", "search_SetupBox")
                    cm.enterTextAndWait(
                        "CampaignPage", "search_SetupBox", test_case["User Persona"], 5
                    )
                    cp = Campaign(second_Tab)
                    cp.select_User_Persona(test_case["User Persona"])
                    logger.info(f"Searched for {test_case['User Persona']}  in Setup")

                frame_locator_setup = locator_manager.get_locator(
                    "HomePage", "frame_Locator"
                )
                cm.switchToFrame(frame_locator_setup)
                cm.clickElementByPosition("CampaignPage", "click_Login", "first", 1)

                hp = HomePage(second_Tab)

                cm = CommonMethods(second_Tab, locator_manager)
                cm.clickElement("HomePage", "app_Launcher")
                logger.info(f"Clicked on App Launcher")

                if test_case["Search App Name"].strip().lower() == "yes":
                    if is_valid_data(test_case["App Name"]):
                        cm.clickElement("HomePage", "search_box")
                        cm.enterTextAndWait(
                            "HomePage", "search_box", test_case["App Name"], 5
                        )
                        logger.info(
                            f"Searched for {test_case['App Name']} in App Launcher"
                        )
                        hp.selectFromSearchResults(test_case["App Name"])
                        logger.info(
                            f"Selected {test_case['App Name']} from search results"
                        )

            if (
                test_case["Show More Actions Button Validation"].strip().lower()
                == "yes"
            ):
                print(
                    f"\n\033[94mℹ️ ================Show More Actions Dropdown Button Validations===============================================================================\033[0m"
                )

                cp = Campaign(second_Tab)
                cm.clickElement("CampaignPage", "show_more")

                if test_case["Create Button Validation"].strip().lower() == "yes":
                    create_Option_Result = cm.isElementNotVisible(
                        "CampaignPage", "create_Option"
                    )

                    if create_Option_Result:
                        failure_message = (
                            f"Create Option Button is Visible And Validation Failed'."
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")

                    else:
                        logger.info(
                            "Create Option button is not visible and validation passed successfully."
                        )
                        print(
                            "\033[92m✅ Create Option button is not visible and validation passed successfully.\033[0m"
                        )

                if test_case["Edit Button Validation"].strip().lower() == "yes":
                    edit_Option_Result = cm.isElementNotVisible(
                        "CampaignPage", "edit_Option"
                    )

                    if edit_Option_Result:
                        failure_message = (
                            f"Edit Option Button is Visible And Validation Failed'."
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")

                    else:
                        logger.info(
                            "Edit Option button is not visible and validation passed successfully."
                        )
                        print(
                            "\033[92m✅ Edit Option button is not visible and validation passed successfully.\033[0m"
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
