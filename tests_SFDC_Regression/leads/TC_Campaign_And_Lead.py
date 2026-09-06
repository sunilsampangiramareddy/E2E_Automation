import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.campaign import Campaign
from pages_SFDC.Lead_Detail import LeadDetail
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from utils.locator_manager import LocatorManager

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# ADO Test IDs - 473788,393076
# Test Scenario: 
# 1.Lead to Campaign linking - Verifying that user can create or edit campaign members & add or opt-in a Lead to an existing active Campaign
# 2.TC-391567 Associate Lead to a Campaign and verify the Campaign Members.
# Test Description: Navigate to the Campaigns object in Salesforce, associate a lead with a campaign, verify the association,
#                   and remove the association. This involves logging into Salesforce, navigating to the Campaigns and Leads
#                   screens, performing association tasks, and validating the results.
# Author: Aswathy/ Jhansi
# Reviewed By: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_Campaign_And_Lead.xlsx"
)
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]

# Load locators from JSON
locator_file_path = os.path.join(working_directory, "locators", "locators.json")
locator_manager = LocatorManager(locator_file_path)


@pytest.mark.parametrize(
    "test_case",
    test_data.to_dict(orient="records"),
    ids=lambda test_case, index=iter(
        range(1, len(test_data) + 1)
    ): f"test_case{next(index)}",
)
@pytest.mark.master
@pytest.mark.regression
def test_Campaign_And_Lead(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    cp = Campaign(page)
    lp = LeadDetail(page)
    ss = ScreenshotUtil(page)
    boolean_status = "Pass"
    cm = CommonMethods(page, locator_manager)
    validation_failures = []

    try:
        # =================================Login to SFDC=========================================================================
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

            # ================= Navigate to Campaigns object ===============
            if test_case["Navigate To Campaigns Screen"].strip().lower() == "yes":

                cm.clickElement("HomePage", "app_Launcher")
                logger.info(f"Clicked on App Launcher")

                if is_valid_data(test_case["Campaigns Menu Item"]):
                    cm.clickElement("HomePage", "app_Launcher_Search")
                    logger.info(f"Clicked on App Launcher Search")

                    cm.enterText(
                        "HomePage",
                        "app_Launcher_Search",
                        test_case["Campaigns Menu Item"],
                    )
                    logger.info(
                        f"Searched for {test_case['Campaigns Menu Item']} in App Launcher"
                    )

                    cm.clickElement("HomePage", "campaigns")
                    logger.info(f"Selected Campaigns from search results")

                    existing_campaign_name = cp.capture_Existing_Campaign_Name()
                    logger.info(
                        f"Existing campaign name captured: {existing_campaign_name}"
                    )

                    cm.clickElement("HomePage", "leads")
                    logger.info("Leads link clicked")

                    existing_lead_name = lp.capture_Existing_Lead_Name()
                    logger.info(f"Existing lead name captured: {existing_lead_name}")

                    cm.clickElement("HomePage", "leads")
                    cm.clickByTextByPosition(existing_lead_name, "nth", 0)
                    logger.info(
                        f"Navigated to lead listing page for lead: {existing_lead_name}"
                    )

                    cm.clickElement("HomePage", "show_Actions_For_Campaign")
                    logger.info("Clicked on Show actions for Campaign button")

                    cm.clickElement("HomePage", "add_To_Campaign_MenuItem")
                    logger.info("Clicked on Add to Campaign menu item")

                    cm.clickElement("HomePage", "campaign")
                    logger.info("Clicked on Campaign combobox")

                    cm.enterTextAndWait("HomePage", "campaign", existing_campaign_name,1)
                    logger.info(
                        f"Entered campaign name {existing_campaign_name} in Campaign combobox"
                    )

                    cm.clickByTextByPosition(existing_campaign_name, "nth", 2)
                    logger.info(
                        f"Selected campaign {existing_campaign_name} from the dropdown"
                    )

                    cm.clickElement("HomePage", "next_Button")
                    logger.info(f"Clicked on Next button")
                    
                    cm.clickElement("HomePage", "save_Button")
                    logger.info(
                        f"Clicked on Save button to associate lead with campaign"
                    )

                    cm.clickElement("HomePage", "app_Launcher")
                    logger.info(f"Clicked on App Launcher")

                    cm.clickElement("HomePage", "app_Launcher_Search")
                    if is_valid_data(test_case["Campaigns Menu Item"]):
                        cm.enterText(
                            "HomePage",
                            "app_Launcher_Search",
                            test_case["Campaigns Menu Item"],
                        )
                        logger.info(
                            f"Searched for {test_case['Campaigns Menu Item']} in App Launcher"
                        )

                        cm.clickElement("HomePage", "campaigns")
                        logger.info(
                            f"Selected {test_case['Campaigns Menu Item']} from search results"
                        )

                        cm.clickByLinkText(
                            link_text=existing_campaign_name, partial_match=True
                        )
                        logger.info(
                            f"Opened campaign detail page for campaign: {existing_campaign_name}"
                        )

                        cm.clickElementAndWait("HomePage", "related_Tab", 2)
                        cp.verify_Lead_Association_With_Campaign(existing_lead_name)
                        logger.info(
                            f"Verified that lead {existing_lead_name} is associated with campaign {existing_campaign_name}"
                        )

                        cp.remove_Association()
                        logger.info(
                            f"Removed association of lead {existing_lead_name} from campaign {existing_campaign_name}"
                        )

                        cm.clickElement("HomePage", "leads")
                        logger.info("Leads link clicked")

                        cm.clickByLinkText(
                            link_text=existing_lead_name, partial_match=True
                        )
                        logger.info(
                            f"Navigated to lead detail page for lead: {existing_lead_name}"
                        )

                        if (
                            test_case["Verify Campaign Associations"].strip().lower()
                            == "yes"
                        ):
                            campaign_Association_Removed = (
                                lp.verify_Campaign_Association_Removed(
                                    existing_campaign_name
                                )
                            )
                            if campaign_Association_Removed:
                                logger.info(
                                    f"Verified that campaign {existing_campaign_name} is no longer associated with lead {existing_lead_name}"
                                )
                                print(
                                    f"\033[92m✅ Verified that campaign {existing_campaign_name} is no longer associated with lead {existing_lead_name}\033[0m"
                                )
                            else:
                                failure_message = f"Campaign {existing_campaign_name} is still associated with the lead"
                                validation_failures.append(
                                    failure_message
                                )  # Add failure to the list
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

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
                    "NA",
                    "NA",
                    "Validations done successfully",
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
