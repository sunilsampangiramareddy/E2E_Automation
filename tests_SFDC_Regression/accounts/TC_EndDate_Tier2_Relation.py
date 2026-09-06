from common_Methods.Common_Methods import CommonMethods
import pytest
import logging
import os
from playwright.sync_api import Page
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.data_validation import is_valid_data
from utils.write_excel_results import WriteExcelResults

# ===================================================================================================================================
# Test Metadata
# ===================================================================================================================================
# Test Case#: 469175
# Title: Verify if Business Right is Reseller and Status changes to Terminated, then user can edit end-date Tier 2 relations manually
# Description: This script automates the process of verifying that when a business entity has the Business Right of "Reseller"
#              and its Status changes to "Terminated," the system allows the user to manually end-date the associated Tier 2
#              relations. The test includes validation of the UI behavior and database updates.
# Author: Ayushee
# Review: Sunil Reddy
# ===================================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_EndDate_Tier2_Relation.xlsx"
)
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
def test_EndDate_Tier2_Relation(page: Page, base_url, config, test_case) -> None:
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
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}*****\033[0m"
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

                if cm.isElementPresent(
                    "CreatePartnerAccount", "select_Account_Type", 5000
                ):
                    cm.clickElement("CreatePartnerAccount", "account_Partner_Type")
                    logger.info("Selected Partner as Account Type")

                if is_valid_data(test_case["Account Name"]):
                    partner_account_name = f" {test_case['Account Name']}_{cm.generateRandomString(4)}_{cm.generateRandomNumber()}"
                    cm.enterText(
                        "CreatePartnerAccount",
                        "partner_Acccount_Name_Input",
                        partner_account_name,
                    )
                    logger.info(f"Entered Account Name: {partner_account_name}")

                cm.clickElementByPosition(
                    "CreatePartnerAccount", "search_Button", "nth", 1
                )
                logger.info("Clicked on Search button")

                # ================ Handling if duplicate account found ============
                if cm.isElementPresent(
                    "CreatePartnerAccount", "no_Duplicate_Account_Info", 5000
                ):
                    logger.info(
                        "No duplicate accounts found, proceeding to create a new partner account creation"
                    )
                    cm.clickElement(
                        "CreatePartnerAccount", "continue_to_Create_New_Partner_Button"
                    )
                    logger.info("Clicked on Continue to Create New Partner button")
                else:
                    logger.info("Duplicate account found")
                    cm.clickElement(
                        "CreatePartnerAccount", "continue_New_Partner_Request_Button"
                    )
                    logger.info("Clicked on Continue New Partner Request button")

                # ================= Address entry ===================

                if is_valid_data(test_case["Main Phone Number"]):
                    cm.enterText(
                        "CreatePartnerAccount",
                        "main_Phone_Number",
                        f"{test_case['Main Phone Number']}",
                    )
                    logger.info(
                        f"Entered Main Phone Number: {test_case['Main Phone Number']}"
                    )

                if is_valid_data(test_case["Web Site Address"]):
                    cm.enterText(
                        "CreatePartnerAccount",
                        "web_Site_Address",
                        test_case["Web Site Address"],
                    )
                    logger.info(
                        f"Entered Website Address: {test_case['Web Site Address']}"
                    )

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
                    logger.info(
                        f"Selected State/Province: {test_case['State_Province']}"
                    )

                if is_valid_data(test_case["Zip Code"]):
                    cm.enterText(
                        "CreatePartnerAccount",
                        "zip_Postal_Code",
                        f"{test_case['Zip Code']}",
                    )
                    logger.info(f"Entered Zip/Postal Code: {test_case['Zip Code']}")

                cm.clickElementAndWait(
                    "CreatePartnerAccount", "save_Partner_And_Continue_Button", 2
                )
                logger.info(
                    "Clicked on Save Partner and Continue button to proceed with Partner Account creation"
                )

                # ================= Domain entry ===================
                if is_valid_data(test_case["Domain"]):
                    cm.enterText("CreatePartnerAccount", "domain", test_case["Domain"])
                    logger.info(f"Entered Domain: {test_case['Domain']}")

                cm.clickElementAndWait(
                    "CreatePartnerAccount", "save_Domain_And_Continue_Button", 2
                )
                logger.info("Clicked on Save Domain and Continue button")

                # ================ Program Details - Main Program =======================
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

                # ================ Contact Details ===================
                if is_valid_data(test_case["First Name1"]):
                    cm.enterText(
                        "CreatePartnerAccount",
                        "first_Name_Input",
                        test_case["First Name1"],
                    )
                    logger.info(f"Entered First Name: {test_case['First Name1']}")

                if is_valid_data(test_case["Last Name1"]):
                    cm.enterText(
                        "CreatePartnerAccount",
                        "last_Name_Input",
                        test_case["Last Name1"],
                    )
                    logger.info(f"Entered Last Name: {test_case['Last Name1']}")

                if is_valid_data(test_case["Email1"]):
                    email1 = f"{cm.generateRandomAlphanumeric()}@{test_case["Domain"]}"
                    cm.enterText("CreatePartnerAccount", "email_Input", email1)
                    logger.info(f"Entered Email: {email1}")

                if is_valid_data(test_case["Phone1"]):
                    cm.enterText(
                        "CreatePartnerAccount",
                        "phone_Number_Input",
                        f"{test_case['Phone1']}",
                    )
                    logger.info(f"Entered Phone Number: {test_case['Phone1']}")

                cm.clickByText(test_case["Contact Type"])
                logger.info(f"Selected Contact Type: {test_case['Contact Type']}")
                cm.clickElement("CreatePartnerAccount", "available_To_Selected_Button")
                logger.info("Clicked on Available to Selected button")

                cm.clickElement(
                    "CreatePartnerAccount", "save_Contacts_And_Continue_Button"
                )
                logger.info("Clicked on Save Contacts and Continue button")

                # ================ Primary Partner Manager ===================
                if is_valid_data(test_case["Primary Partner Manager"]):
                    cm.selectComboboxOption(
                        "CreatePartnerAccount",
                        "primary_Partner_Manager",
                        test_case["Primary Partner Manager"],
                    )
                    logger.info(
                        f"Selected Primary Partner Manager: {test_case['Primary Partner Manager']}"
                    )

                # ================ Save and Complete ========================
                cm.clickElement("CreatePartnerAccount", "save_And_Complete_Button")
                logger.info("Clicked on Save and Complete button")

                # ================= open the created account =================
                cm.enterText("HomePage", "search_Bar", partner_account_name)
                logger.info(f"Entered search term: {partner_account_name}")

                cm.pressKey("HomePage", "search_Bar", "Enter")
                logger.info(f"Pressed Enter key to search for: {partner_account_name}")

                cm.clickByText(partner_account_name)
                logger.info(f"Clicked on searched account: {partner_account_name}")

                partner_account_url = cm.getCurrentURL()
                logger.info(f"Captured Spark URL: {partner_account_url}")

                # =============================Creating Tier 2 Partner Relation ==========================#

                cm.mouseWheel("HomePage", 800, scrolls=1, wait_time=2)
                cm.scrollAndClick("HomePage", "show_All_Details_Button")
                logger.info("Clicked show all")
                cm.clickElement("CreatePartnerAccount", "partner_Relation")
                logger.info(f"Clicked on Partner Relation Related quick link")

                cm.clickElement("CreatePartnerAccount", "new_Button")
                logger.info(f"Clicked on New Button to create 2 tier partner relation")

                cm.clickElement("CreatePartnerAccount", "distributor")
                cm.enterText(
                    "CreatePartnerAccount",
                    "distributor",
                    test_case["Distributor Account Name"],
                )
                cm.clickByText(test_case["Distributor Account Name"])
                cm.clickElement("CreatePartnerAccount", "partner_Tier")
                partner_Tier = str(test_case["Partner Tier"]).strip().replace(".0", "")
                cm.enterText("CreatePartnerAccount", "partner_Tier", partner_Tier)
                cm.clickElement("CreatePartnerAccount", "save_Button")
                logger.info(f"Clicked on Save Button")

                cm.navigateToUrl(partner_account_url)
                logger.info(f"Navigated back to Spark URL: {partner_account_url}")

                # =============================Creating Partner Attribute ==========================#

                cm.mouseWheel("HomePage", 800, scrolls=1, wait_time=2)
                cm.scrollAndClick("HomePage", "show_All_Details_Button")
                logger.info("Clicked show all")
                cm.clickElement("CreatePartnerAccount", "partner_Attributes")
                logger.info(f"Clicked on Partner Attributes Related quick link")

                cm.clickElement("CreatePartnerAccount", "new_Button")
                logger.info(
                    f"Clicked on New Button to Partner Atrribute partner relation"
                )

                cm.clickElement("CreatePartnerAccount", "business_Right_Listbox")
                logger.info(f"Clicked on Business Right combobox")
                cm.clickByText(test_case["Business Right New"])
                logger.info(f"Selected option from Business right combobox")

                cm.clickElement("CreatePartnerAccount", "partner_Level")
                logger.info(f"Clicked on Parter level combobox")
                cm.clickElement("CreatePartnerAccount", "approved_Business_Right")
                logger.info(f"Selected option from Partner Level combobox")

                cm.clickElement("CreatePartnerAccount", "business_Right_Status")
                logger.info(f"Clicked on Business Right Status combobox")
                cm.clickElement("CreatePartnerAccount", "pending_Approval_Status")
                logger.info(f"Selected option from Business Right Status comobox")

                cm.clickElement("CreatePartnerAccount", "main_Program")
                logger.info(f"Clicked on Main Program")

                cm.enterTextAndWait(
                    "CreatePartnerAccount",
                    "main_Program",
                    test_case["Main Program Value"],
                    2,
                )
                cm.clickElement("CreatePartnerAccount", "show_More_Results")
                cm.clickElement("CreatePartnerAccount", "main_Program_Radio_Button")
                cm.clickElement("CreatePartnerAccount", "select_Button")
                logger.info(f"Main program selected")

                cm.clickElement("CreatePartnerAccount", "is_Primary_Checkbox")
                logger.info(f"checked IsPrimary checkbox")

                cm.clickElement("CreatePartnerAccount", "save_Button")
                logger.info(f"Clicked on Save Button")

                # =============================Termination Of Partner Attribute ==========================#

                cm.clickElement("CreatePartnerAccount", "show_Action_Button")
                cm.clickElement("CreatePartnerAccount", "edit_Button")

                cm.clickElement("CreatePartnerAccount", "business_Right_Status")
                logger.info(f"Clicked on Business Right Status combobox")
                cm.clickByText(test_case["Business Right Status New"])
                logger.info(f"Selected option from Business Right Status comobox")
                cm.clickElement("CreatePartnerAccount", "save_Button")
                logger.info(f"Clicked on Save Button")

                cm.navigateToUrl(partner_account_url)
                logger.info(f"Navigated back to Spark URL: {partner_account_url}")

                cm.mouseWheel("HomePage", 800, scrolls=1, wait_time=2)
                cm.scrollAndClick("HomePage", "show_All_Details_Button")
                logger.info("Clicked show all")
                cm.clickElement("CreatePartnerAccount", "partner_Relation")
                logger.info(f"Clicked on Partner Relation Related quick link")

                cm.clickElement("CreatePartnerAccount", "partner_Relation_Value")
                logger.info(f"Opened Partner Relation Record having Partner Tier 2")

                # ============================= Validation of Partner Relation End Date ==========================#
                if test_case["Purchasing Channel End date"].strip().lower() == "yes":
                    is_visible = cm.isElementVisible(
                        "CreatePartnerAccount", "purchasing_Channel_End_Date"
                    )
                    if is_visible:
                        logger.info(
                            f"Purchasing Channel End date Edit Option is visible"
                        )
                        print(f"✅ Purchasing Channel End date Edit Option is visible")
                    else:
                        print(
                            f"❌ Purchasing Channel End date Edit Option is NOT visible"
                        )
                        validation_failures.append(
                            "Purchasing Channel End date Edit Option is NOT visible"
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
                    "Partner Account created successfully",
                ],
            ]
            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)
            logger.info(
                f"*****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}*****"
            )
            print(
                f"\n\033[92m✅ *****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}*****\033[0m"
            )
        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}"
            )
            print(
                f"\033[93m➡️ Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}\033[0m"
            )
            pytest.skip(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and {test_case['Test Case ID']}"
            )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
