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
# Test Case #1: 473814: Creating a New Site Account in SFDC
# Description: This test case automates the process of logging into Salesforce (SFDC), navigating to the Accounts tab, and 
#              creating a new site/customer account using data from an Excel file. It includes validations for account details 
#              such as Account Level, Security Code, CreatedBy, and Account Name, as well as the creation and validation of 
#              a new contact.
# Test Case #2: 556509: Validate Base Sales User Editability on Site Account
# Description: This test case validates the access restrictions for a base sales user on a Site account in Salesforce, 
#              specifically focusing on the inability to edit fields like Account Currency and Account Team members, along 
#              with verifying the appropriate error messages displayed during these actions
# Author: Jhansi GR
# Review: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_New_Site_Account_Creation_SFDC.xlsx")
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
def test_New_Site_Account_Creation_SFDC(page: Page, base_url, config, test_case) -> None:
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

            # ====================================== Impersonate to Base sales user persona ========================
            if test_case["Login as Base Sales User"].strip().lower() == "yes":
                cm.clickElement("HomePage", "setup_Icon")
                cm.clickElement("HomePage", "setup_menu_item")
                secondTab = cm.switchToTab(page.context, tab_index=1, expected_tab_count=2)
                cm.waitForPageLoad(secondTab)
                logger.info("Clicked on Setup icon")
    
                cm = CommonMethods(secondTab, locator_manager)
                cm.clickElement("GeneralSetup", "search_Setup_Input")
                logger.info(f"Base Sales User Persona: {test_case['Base Sales User Persona']}")
                cm.enterText(
                    "GeneralSetup", "search_Setup_Input", test_case["Base Sales User Persona"]
                )
                cm.clickByLinkText(
                    test_case["Base Sales User Persona"], partial_match=True, occurrence=1
                )
                logger.info("Searched for user in Setup")
    
                frame_locator_setup = locator_manager.get_locator("HomePage", "frame_Locator")
                cm.switchToFrame(frame_locator_setup)
                cm.page.get_by_role("button", name="Login", exact=True).nth(1).click()
                logger.info("Clicked Login button from Setup frame")
    
                cm = CommonMethods(secondTab, locator_manager)
                logger.info(f"created instance of CommonMethods class with secondTab")

            # ======================================Site/Customer Account Creation=====================================
            if test_case["Create Site Account"].strip().lower() == "yes":
                cm.clickElement("HomePage", "accounts_Tab")
                logger.info("Clicked on Accounts tab")

                cm.clickElement("CreatePartnerAccount", "new_Button")
                logger.info("Clicked on New button to create a new Site/Customer account")

                if is_valid_data(test_case["Account Name"]):
                    site_account_name = f" {test_case['Account Name']}_{cm.generateRandomString(4)}_{cm.generateRandomNumber()}"
                    cm.enterText("CreateSiteAccount", "site_Account_Name", site_account_name)
                    logger.info(f"Entered Account Name: {site_account_name}")

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

                cm.clickElement("CreateSiteAccount", "search_Button")
                logger.info("Clicked on Search button to proceed with Site Account creation")

                if is_valid_data(test_case["Website"]):
                    cm.enterText("CreateSiteAccount", "website", test_case["Website"])
                    logger.info(f"Entered Website: {test_case['Website']}")

                if is_valid_data(test_case["Phone"]):
                    cm.enterText("CreateSiteAccount", "phone", f"{test_case['Phone']}")
                    logger.info(f"Entered Phone: {test_case['Phone']}")

                cm.clickElementAndWait("CreateSiteAccount", "save", 5)
                spark_url = cm.getCurrentURL()
                logger.info(f"Current URL after creating Site Account: {spark_url}")
                logger.info(f"Site Account creation completed. Current URL: {spark_url}")
                print(f"✅ Site Account creation is successful. Site Account name: {site_account_name}")

                #================== Validate Account details ============================                
                if test_case["Validate Account level"].strip().lower() == "yes":
                    if is_valid_data(test_case["Expected Account Level"]):
                        logger.info(f"Actual Account Level: {cm.readText('CreatePartnerAccount', 'account_Level_Value')}")
                        validate_Account_Level = cm.assertText("CreatePartnerAccount", "account_Level_Value", test_case["Expected Account Level"])
                        if validate_Account_Level:
                            logger.info(f"Account Level validation passed: {cm.readText('CreatePartnerAccount', 'account_Level_Value')}")
                            print(f"✅ Account Level validation passed: {cm.readText('CreatePartnerAccount', 'account_Level_Value')}")
                        else:
                            validation_failures.append(f"Account Level validation failed. Expected: {test_case['Expected Account Level']}, Actual: {validate_Account_Level}")
                            logger.error(f"Account Level validation failed. Expected: {test_case['Expected Account Level']}, Actual: {validate_Account_Level}")
                            print(f" ❌ Account Level validation failed. Expected: {test_case['Expected Account Level']}, Actual: {validate_Account_Level}")

                if test_case["Validate Security Code"].strip().lower() == "yes":
                    if is_valid_data(test_case["Expected Security Code"]):
                        validate_Security_Code = cm.assertText("CreateSiteAccount", "security_Code_Value", test_case["Expected Security Code"])
                        logger.info(f"Actual Security Code value: {cm.readText('CreateSiteAccount', 'security_Code_Value')}")    
                        if validate_Security_Code:
                            logger.info(f"Security Code validation passed: {cm.readText('CreateSiteAccount', 'security_Code_Value')}")
                            print(f"✅ Security Code validation passed: {cm.readText('CreateSiteAccount', 'security_Code_Value')}")
                        else:
                            validation_failures.append(f"Security Code validation failed. Expected: {test_case['Expected Security Code']}, Actual: {validate_Security_Code}")
                            logger.error(f"Security Code validation failed. Expected: {test_case['Expected Security Code']}, Actual: {validate_Security_Code}")
                            print(f"❌ Security Code validation failed. Expected: {test_case['Expected Security Code']}, Actual: {validate_Security_Code}")

                if test_case["Validate CreatedBy"].strip().lower() == "yes":  
                    cm.clickElementAndWait("Partner_Connect", "details_tab", 2)  
                    logger.info("Navigated to Details tab for CreatedBy validation")
                    if is_valid_data(test_case["Base Sales User Persona"]):
                        validate_CreatedBy = cm.assertText("CreateSiteAccount", "created_By_Value", test_case["Base Sales User Persona"])
                        logger.info(f"Actual CreatedBy value: {cm.readText('CreateSiteAccount', 'created_By_Value')}")
                        if validate_CreatedBy:
                            logger.info(f"CreatedBy validation passed: {cm.readText('CreateSiteAccount', 'created_By_Value')}")
                            print(f"✅ CreatedBy validation passed: {cm.readText('CreateSiteAccount', 'created_By_Value')}")
                        else:
                            validation_failures.append(f"CreatedBy validation failed. Expected: {test_case['Base Sales User Persona']}, Actual: {validate_CreatedBy}")
                            logger.error(f"CreatedBy validation failed. Expected: {test_case['Base Sales User Persona']}, Actual: {validate_CreatedBy}")
                            print(f"❌ CreatedBy validation failed. Expected: {test_case['Base Sales User Persona']}, Actual: {validate_CreatedBy}")

                if test_case["Validate Account Name"].strip().lower() == "yes":
                    validate_Account_Name = cm.assertText("CreateSiteAccount", "site_Account_Name_Value", f"{site_account_name}")
                    logger.info(f"Actual Account Name value: {cm.readText('CreateSiteAccount', 'site_Account_Name_Value')}")
                    if validate_Account_Name:
                        logger.info(f"Account created successfully, Account Name validation passed: {cm.readText('CreateSiteAccount', 'site_Account_Name_Value')}")
                        print(f"✅ Account created successfully, Account Name validation passed: {cm.readText('CreateSiteAccount', 'site_Account_Name_Value')}")
                    else:
                        validation_failures.append(f"Account Name validation failed. Expected: {site_account_name}, Actual: {validate_Account_Name}")
                        logger.error(f"Account Name validation failed. Expected: {site_account_name}, Actual: {validate_Account_Name}")
                        print(f" ❌ Account Name validation failed. Expected: {site_account_name}, Actual: {validate_Account_Name}")

                #==================== new contact creation ===============================
                if test_case["Create New Contact"].strip().lower() == "yes":
                    cm.clickElement("CreateSiteAccount", "contacts_Section")
                    logger.info("Clicked on Contacts section")

                    cm.clickElement("HomePage", "new_Button")
                    logger.info("Clicked on New Contact button")

                    cm.clickElement("CreateSiteAccount", "customer_Record_Type")
                    logger.info("Clicked on Customer Record Type")

                    cm.clickElement("HomePage","next_Button")               
                    logger.info("Clicked on Next button")

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

                    email=cm.generateRandomEmail()
                    
                    cm.clickElement("HomePage","email_Input")
                    logger.info("Clicked email field")
    
                    cm.enterTextAndWait("HomePage", "email_Input", email,5)
                    logger.info("Entered email")

                    cm.clickElementAndWait("CreateSiteAccount", "save", 2)
                    logger.info("Clicked on Save button")
                    logger.info("Contact has been created Successfully")

                    if test_case["Validate Contact Name"].strip().lower() == "yes":
                        actual_Contact_Name = cm.readText("CreateSiteAccount", "actual_Contact_Name")
                        logger.info(f"Actual Contact Name: {actual_Contact_Name}")

                        contact_Name_Validation = cm.assertText("CreateSiteAccount", "actual_Contact_Name", f"{test_case['First Name']} {test_case['Last Name']}")
                        if contact_Name_Validation:
                            logger.info(f"Contact Name validation passed, actual contact name: {actual_Contact_Name}, expected contact name: {test_case['First Name']} {test_case['Last Name']}")
                            print(f"✅ Contact Name validation passed, actual contact name: {actual_Contact_Name}, expected contact name: {test_case['First Name']} {test_case['Last Name']}")
                        else:
                            logger.error(f"Contact Name validation failed, actual contact name: {actual_Contact_Name}, expected contact name: {test_case['First Name']} {test_case['Last Name']}")
                            print(f"❌ Contact Name validation failed, actual contact name: {actual_Contact_Name}, expected contact name: {test_case['First Name']} {test_case['Last Name']}")
                            validation_failures.append(f"Contact Name validation failed, actual contact name: {actual_Contact_Name}, expected contact name: {test_case['First Name']} {test_case['Last Name']}")

            # ========================== Validate account editability (fields, account team) =====================
            if test_case["Validate Account Editability"].strip().lower() == "yes":                
    
                if is_valid_data(test_case["Account CMAT"]):             

                    # ================================== Search for Site Account ====================================
                    cm.clickElement("HomePage", "accounts_Tab")
                    logger.info("Clicked on Account tab")        
                    cm.clickElement("HomePage", "search_Bar")
                    logger.info("Clicked on search bar")    
                    cm.enterText("HomePage", "search_Bar", str(int(test_case["Account CMAT"])))
                    logger.info(f"Entered Account CMAT ID: {test_case['Account CMAT']} in search bar")
                    cm.pressEnter("HomePage", "search_Bar")
                    cm.clickByLinkText(test_case["Account CMAT Name"], partial_match=True)
                    logger.info(f"Navigated to Account: {test_case['Account CMAT']} - {test_case['Account CMAT Name']}")
                    cm.waitForStable(2)

                    # =============== currency editability vaildations ====================================

                    cm.clickElement("CreateSiteAccount", "edit_Account_Currency")
                    logger.info("Clicked on Edit Account Currency button")

                    cm.clickElement("CreateSiteAccount", "account_Currency")
                    logger.info("Clicked on Account Currency dropdown")

                    cm.clickByText(test_case["Currency"])
                    logger.info(f"Selected currency: {test_case['Currency']}")

                    cm.clickElement("CreateSiteAccount", "save")
                    logger.info("Clicked on Save button")

                    currency_Error_Message = cm.readText("HomePage", "error_Label")
                    logger.info(f"Error occurred as expected, and the actual error message displayed: {currency_Error_Message}")
                    print(f"✅ Error occurred as expected, and the actual error message displayed: {currency_Error_Message}")

                    if test_case["Validate Currency Error"].strip().lower() == "yes":
                        if is_valid_data(test_case["Currency Error Message"]):
                            currency_Error_Message_Validation = cm.assertText("HomePage", "error_Label", test_case["Currency Error Message"])
                            if currency_Error_Message_Validation:
                                logger.info(f"Currency error message validation passed, Expected and actual error message is same.")
                                print(f"\033[92m✅ Currency error message validation passed, Base sales user is not able to edit and update the fields like Currency on Account.\033[0m")
                            else:
                                logger.error("Currency error message validation failed, Expected and actual error message do not match.")
                                validation_failures.append("Currency error message validation failed, Expected and actual error message do not match.")
                                print(f"❌ Currency error message validation failed, Expected and actual error message do not match.")                      

                    cm.clickElementAndWait("HomePage","cancel_Button", 2)
                    logger.info("Clicked on cancel button after currency error.")

                    # ====================== Account Team editability validations ==============================
                    cm.mouseWheelToBottom(1000, scrolls=10, wait_time=0)
                    cm.scrollToElement("HomePage", "show_All_Details_Button")
                    logger.info("Scrolled to Show All Details button")
    
                    cm.clickElement("HomePage", "show_All_Details_Button")
                    logger.info("Clicked on Show All Details button")

                    cm.clickElement("CreateSiteAccount", "account_Team_Link")
                    logger.info("Clicked on Account Team link")

                    cm.clickElement("CreateSiteAccount", "add_Team_Members")
                    logger.info("Clicked on Add Team Members button")

                    cm.clickElement("CreateSiteAccount", "add_Team_Member_User")
                    logger.info("Clicked on Add Team Member User button")

                    cm.clickByText(test_case["Base Sales User Persona"])
                    logger.info(f"Clicked on Base Sales User Persona: {test_case['Base Sales User Persona']}")

                    cm.clickElement("CreateSiteAccount", "add_Team_Member_Role")
                    logger.info("Clicked on Add Team Member Role button")

                    cm.clickElement("CreateSiteAccount", "add_team_Member_Role_Select")
                    logger.info("Clicked on Add Team Member Role Select button")

                    cm.clickByText(test_case["Account Team role"])
                    logger.info(f"Clicked on Account Team role: {test_case['Account Team role']}")

                    cm.clickElement("HomePage", "save_Button")
                    logger.info("Clicked on Save button")

                    actual_Account_Team_Error_Msg = cm.readText("CreateSiteAccount", "error_Message_Label")
                    logger.info(f"Actual Account Team Error Message captured: '{actual_Account_Team_Error_Msg}'")
                    
                    account_Team_Error_Msg_Validation = cm.assertExpectedInActualText(actual_Account_Team_Error_Msg, test_case["Account Parties Error Message"])
                    if account_Team_Error_Msg_Validation:
                        logger.info("Account Team Error Message validation passed")
                        print(f"✅ Account Team Error Message validation passed, Base sales user is not able to edit the Account team members as expected.")
                    else:
                        validation_failures.append("Account Team Error Message validation failed")
                        logger.error("Account Team Error Message validation failed")
                        print(f"❌ Account Team Error Message validation failed")

            # ======================================Checking for Validation Failures===============================
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
                    "Customer Account and contact created successfully",
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