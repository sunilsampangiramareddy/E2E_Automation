from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Account_Detail import AccountDetail
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
# Test Case#: 479903
# Title: Test Script for Creating a New Partner Account in SFDC
# Description: This script automates the process of logging into Salesforce (SFDC), navigating to the Accounts tab, and 
#              creating a new partner account. The test data is loaded from an Excel file, and locators are loaded from a 
#              JSON file
# Author: Jhansi GR
# Review: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_New_Partner_Account_Creation_SFDC.xlsx")
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
def test_New_Partner_Account_Creation_SFDC(page: Page, base_url, config, test_case) -> None:
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

            # ================================== Partner Account Creation ====================================
            if test_case["Create Partner Account"].strip().lower() == "yes":
                cm.clickElement("HomePage", "accounts_Tab")
                logger.info("Clicked on Accounts tab")

                cm.clickElement("CreatePartnerAccount", "new_Button")
                logger.info("Clicked on New button to create a new partner account")

                if cm.isElementPresent("CreatePartnerAccount", "select_Account_Type", 5000):
                    cm.clickElement("CreatePartnerAccount", "account_Partner_Type")
                    logger.info("Selected Partner as Account Type")

                if is_valid_data(test_case["Account Name"]):
                    partner_account_name = f" {test_case['Account Name']}_{cm.generateRandomString(4)}_{cm.generateRandomNumber()}"
                    cm.enterText("CreatePartnerAccount", "partner_Acccount_Name_Input", partner_account_name)
                    logger.info(f"Entered Account Name: {partner_account_name}")

                cm.clickElementByPosition("CreatePartnerAccount", "search_Button", "nth", 1)
                logger.info("Clicked on Search button")

                #================ Handling if duplicate account found ============
                if cm.isElementPresent("CreatePartnerAccount", "no_Duplicate_Account_Info", 5000):
                    logger.info("No duplicate accounts found, proceeding to create a new partner account creation")
                    cm.clickElement("CreatePartnerAccount", "continue_to_Create_New_Partner_Button")
                    logger.info("Clicked on Continue to Create New Partner button")                    
                else:
                    logger.info("Duplicate account found")
                    cm.clickElement("CreatePartnerAccount", "continue_New_Partner_Request_Button")
                    logger.info("Clicked on Continue New Partner Request button")
                    

                #================= Address entry ===================

                if is_valid_data(test_case["Main Phone Number"]):
                    cm.enterText("CreatePartnerAccount", "main_Phone_Number", f"{test_case['Main Phone Number']}")
                    logger.info(f"Entered Main Phone Number: {test_case['Main Phone Number']}")

                if is_valid_data(test_case["Web Site Address"]):
                    cm.enterText("CreatePartnerAccount", "web_Site_Address", test_case["Web Site Address"])
                    logger.info(f"Entered Website Address: {test_case['Web Site Address']}")

                if is_valid_data(test_case["Country"]):
                    cm.clickElement("CreatePartnerAccount", "country")
                    cm.clickByText(test_case["Country"])
                    logger.info(f"Selected Country: {test_case['Country']}")

                if is_valid_data(test_case["Street"]):
                    cm.enterText("CreatePartnerAccount", "street", test_case["Street"])
                    logger.info(f"Entered Street: {test_case['Street']}")

                if is_valid_data(test_case["City"]):
                    cm.enterText("CreatePartnerAccount", "city", test_case["City"])
                    logger.info(f"Entered City: {test_case['City']}")

                if is_valid_data(test_case["State_Province"]):
                    cm.clickElement("CreatePartnerAccount", "state_Province")
                    cm.clickByText(test_case["State_Province"])
                    logger.info(f"Selected State/Province: {test_case['State_Province']}")

                if is_valid_data(test_case["Zip Code"]):
                    cm.enterText("CreatePartnerAccount", "zip_Postal_Code", f"{test_case['Zip Code']}")
                    logger.info(f"Entered Zip/Postal Code: {test_case['Zip Code']}")   

                cm.clickElementAndWait("CreatePartnerAccount", "save_Partner_And_Continue_Button", 2)
                logger.info("Clicked on Save Partner and Continue button to proceed with Partner Account creation")

                #================= Domain entry ===================
                if is_valid_data(test_case["Domain"]):
                    cm.enterText("CreatePartnerAccount", "domain", test_case["Domain"])
                    logger.info(f"Entered Domain: {test_case['Domain']}")

                cm.clickElementAndWait("CreatePartnerAccount", "save_Domain_And_Continue_Button", 2)
                logger.info("Clicked on Save Domain and Continue button")

                #================ Program Details - Main Program =======================
                if is_valid_data(test_case["Main Program"]):
                    cm.clickElement("CreatePartnerAccount", "main_Program")
                    cm.clickByText(test_case["Main Program"])
                    logger.info(f"Selected Main Program: {test_case['Main Program']}")

                cm.clickByText(test_case["Business Right"])
                logger.info(f"Selected Service Provider: {test_case['Business Right']}")
                cm.clickElement("CreatePartnerAccount", "available_To_Selected_Button")
                logger.info("Clicked on Available to Selected button")

                cm.clickElement("CreatePartnerAccount", "partner_Level")
                cm.clickByText(test_case["Partner Level"])
                logger.info(f"Selected Partner Level: {test_case['Partner Level']}")

                cm.clickByText(test_case["Partner Type"])
                logger.info(f"Selected Partner Type: {test_case['Partner Type']}")

                cm.clickElement("CreatePartnerAccount", "save_And_Continue_Button")
                logger.info("Clicked on Save and Continue button")

                #================ Contact Details ===================
                if is_valid_data(test_case["First Name1"]):
                    cm.enterText("CreatePartnerAccount", "first_Name_Input", test_case["First Name1"])
                    logger.info(f"Entered First Name: {test_case['First Name1']}")

                if is_valid_data(test_case["Last Name1"]):
                    cm.enterText("CreatePartnerAccount", "last_Name_Input", test_case["Last Name1"])
                    logger.info(f"Entered Last Name: {test_case['Last Name1']}")

                if is_valid_data(test_case["Email1"]):
                    email1 = f"{cm.generateRandomAlphanumeric()}@{test_case["Domain"]}"
                    cm.enterText("CreatePartnerAccount", "email_Input", email1)
                    logger.info(f"Entered Email: {email1}")

                if is_valid_data(test_case["Phone1"]):
                    cm.enterText("CreatePartnerAccount", "phone_Number_Input", f"{test_case['Phone1']}")
                    logger.info(f"Entered Phone Number: {test_case['Phone1']}")

                cm.clickByText(test_case["Contact Type"])
                logger.info(f"Selected Contact Type: {test_case['Contact Type']}")
                cm.clickElement("CreatePartnerAccount", "available_To_Selected_Button")
                logger.info("Clicked on Available to Selected button")

                cm.clickElement("CreatePartnerAccount", "save_Contacts_And_Continue_Button")
                logger.info("Clicked on Save Contacts and Continue button")

                #================ Primary Partner Manager ===================
                if is_valid_data(test_case["Primary Partner Manager"]):
                    cm.selectComboboxOption("CreatePartnerAccount", "primary_Partner_Manager", test_case["Primary Partner Manager"])
                    logger.info(f"Selected Primary Partner Manager: {test_case['Primary Partner Manager']}")

                #================ Save and Complete ========================
                cm.clickElement("CreatePartnerAccount", "save_And_Complete_Button")
                logger.info("Clicked on Save and Complete button")        

                #================= open the created account =================
                cm.enterText("HomePage", "search_Bar", partner_account_name)
                logger.info(f"Entered search term: {partner_account_name}")

                cm.pressKey("HomePage", "search_Bar", "Enter")
                logger.info(f"Pressed Enter key to search for: {partner_account_name}")

                cm.clickByText(partner_account_name)
                logger.info(f"Clicked on searched account: {partner_account_name}")

                #==================== validate account status====================
                if test_case["Validate Partner Status"].strip().lower() == "yes":
                    actual_Partner_Status = cm.readText("CreatePartnerAccount", "partner_Status_Value")    
                    partner_status_Validation =cm.checkExpectedTextInActual(actual_Partner_Status, test_case["Partner Status"])                

                    if partner_status_Validation:
                        logger.info(f"Partner account status validation is successful for account: {partner_account_name}, expected Partner Status: {test_case['Partner Status']}, actual Partner Status: {actual_Partner_Status}")
                        print(f"✅ Partner account status validation is successful for account: {partner_account_name}, expected Partner Status: {test_case['Partner Status']}, actual Partner Status: {actual_Partner_Status}")

                        #================== click on Sync To CMAT button ======================
                        cm.clickElement("CreatePartnerAccount", "sync_To_CMAT_Button")
                        logger.info(f"Clicked on 'Sync To CMAT' button for account: {partner_account_name}")
                    else:
                        validation_failures.append(f"Partner account status validation is failed for account: {partner_account_name}, expected Partner Status: {test_case['Partner Status']}, but actual Partner Status: {actual_Partner_Status}")
                        logger.error(f"Partner account status validation is failed for account: {partner_account_name}, expected Partner Status: {test_case['Partner Status']}, but actual Partner Status: {actual_Partner_Status}")
                        print(f"❌ Partner account status validation is failed for account: {partner_account_name}, expected Partner Status: {test_case['Partner Status']}, but actual Partner Status: {actual_Partner_Status}")


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
                    "Partner Account created successfully",
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