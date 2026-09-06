from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Login_Page import LoginPage
import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.data_validation import is_valid_data
from utils.write_excel_results import WriteExcelResults

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Case#: 541793
# Title: Test Script for Verifying Partner Connect Fields in SFDC
# Description: This script automates the process of logging into Salesforce (SFDC), searching for a partner account, and 
#              validating various fields in the Partner Connect section. The test data is loaded from an Excel file, and 
#              locators are loaded from a JSON file
# Author: Jhansi GR
# Reviewer: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_Verify_Partner_Connect_Fields.xlsx")
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
def test_Verify_Partner_Connect_Fields(page: Page, base_url, config, test_case) -> None:
    cm = CommonMethods(page, locator_manager)
    ss = ScreenshotUtil(page)
    validation_failures = []
    boolean_status = "Pass"

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

            # ================================== Search for Partner Account ====================================
            cm.clickElement("HomePage", "accounts_Tab")
            logger.info("Clicked on Account tab")

            cm.clickElement("HomePage", "search_Bar")
            logger.info("Clicked on search bar")

            if is_valid_data(test_case["Partner Account Name"]):              

                cm.enterText("HomePage", "search_Bar", test_case["Partner Account Name"])
                logger.info(f"Entered search term: {test_case['Partner Account Name']}")

                cm.pressKey("HomePage", "search_Bar", "Enter")
                logger.info(f"Pressed Enter key to search for: {test_case['Partner Account Name']}")

                cm.clickByText(test_case["Partner Account Name"])
                logger.info(f"Clicked on searched account: {test_case['Partner Account Name']}")

            # ================================== Verify Partner Connect Fields ====================================
            if test_case["Validate Partner Connect Fields"].strip().lower() == "yes":
                cm.clickElementAndWait("Partner_Connect", "details_tab", 3)
                logger.info(f"Navigated to Account details tab")

                if test_case["Partner Connect Section"].strip().lower() == "yes":
                    if cm.isElementVisible("Partner_Connect", "partner_Connect_Section"):
                        cm.scrollToElement("Partner_Connect", "partner_Connect_Section")
                        logger.info(f"Verified Partner Connect section is present")
                        print(f"✅ Verified that Partner Connect section is present")

                        if test_case["Primary Language"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "primary_Language_Field"):
                                logger.info(f"Verified Primary Language field is present")
                                print(f"✅ Verified that Primary Language field is present")
                            else:
                                failure_message = f"Primary Language field validation failed: Primary Language field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Primary Description"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "primary_Description_Field"):
                                logger.info(f"Verified Primary Description field is present")
                                print(f"✅ Verified that Primary Description field is present")
                            else:
                                failure_message = f"Primary Description field validation failed: Primary Description field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Secondary Language"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "secondary_Language_Field"):
                                logger.info(f"Verified Secondary Language field is present")
                                print(f"✅ Verified that Secondary Language field is present")
                            else:
                                failure_message = f"Secondary Language field validation failed: Secondary Language field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Secondary Description"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "secondary_Description_Field"):
                                logger.info(f"Verified Secondary Description field is present")
                                print(f"✅ Verified that Secondary Description field is present")
                            else:
                                failure_message = f"Secondary Description field validation failed: Secondary Description field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Short Description"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "short_Description_Field"):
                                logger.info(f"Verified Short Description field is present")
                                print(f"✅ Verified that Short Description field is present")
                            else:
                                failure_message = f"Short Description field validation failed: Short Description field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Opt In"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "opt_in_Field"):
                                logger.info(f"Verified Opt-in field is present")
                                print(f"✅ Verified that Opt-in field is present")
                            else:
                                failure_message = f"Opt-in field validation failed: Opt-in field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Technology Alliance Solutions"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "technology_Alliance_Solutions_Field"):
                                logger.info(f"Verified Technology Alliance Solutions field is present")
                                print(f"✅ Verified that Technology Alliance Solutions field is present")
                            else:
                                failure_message = f"Technology Alliance Solutions field validation failed: Technology Alliance Solutions field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Partner Logo"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "partner_Logo_Field"):
                                logger.info(f"Verified Partner Logo field is present")
                                print(f"✅ Verified that Partner Logo field is present")
                            else:
                                failure_message = f"Partner Logo field validation failed: Partner Logo field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Demo Lab Availability"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "demo_Lab_Availability_Field"):
                                logger.info(f"Verified Demo Lab Availability field is present")
                                print(f"✅ Verified that Demo Lab Availability field is present")
                            else:
                                failure_message = f"Demo Lab Availability field validation failed: Demo Lab Availability field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")

                        if test_case["Serial Number"].strip().lower() == "yes":
                            if cm.isElementVisible("Partner_Connect", "serial_Number_Field"):
                                logger.info(f"Verified Serial Number field is present")
                                print(f"✅ Verified that Serial Number field is present")
                            else:
                                failure_message = f"Serial Number field validation failed: Serial Number field is not visible"
                                validation_failures.append(
                                    failure_message
                                ) 
                                logger.warning(failure_message)
                                print(f"\033[91m❌ {failure_message}\033[0m")


                    else:                        
                        failure_message = f"Partner Connect Section validation failed: Partner Connect Section is not visible"
                        validation_failures.append(
                            failure_message
                        ) 
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
                    "Partner Connect fields on Account objectverified successfully",
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