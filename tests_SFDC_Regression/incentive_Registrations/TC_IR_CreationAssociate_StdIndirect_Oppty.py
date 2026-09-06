import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# ========================================================================================================================================================
# Test Metadata
# ========================================================================================================================================================
# Test Scenario: 1.481503_Create Incentive Registration and Associate to Existing Opportunity for NetApp Quoted Deal Quote Source and validation of source
#                2.489885_Create Incentive Registration for HyperScaler Quote Source and validation of source
# Test Description:
#   This script validates Incentive Registration creation from Salesforce App Launcher.
#   1. Login to Spark Instance
#   2. Navigate to Incentive Registration from App Launcher
#   3. Create New IR
#   4. Search CMAT Address and select Account
#   5. Select Partner Account
#   6. Select/Create Customer Contact
#   7. Select Quote Source and Product
#   8. Enter Project Description and Estimated Booking
#   9. Create Incentive Registration
#   10. Capture and validate Incentive Registration Number
# Author: Sagar Ch And Ayushee
# Reviewer: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression",
    "TC_IR_CreationAssociate_StdIndirect_Oppty.xlsx",
)
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Load locators from JSON
locator_file_path = os.path.join(working_directory, "locators", "locators.json")
locator_manager = LocatorManager(locator_file_path)

# Get script name
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
def test_IR_CreationAssociate_StdIndirect_Oppty(
    page: Page, base_url, config, test_case
) -> None:
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []

    try:
        # ================================== Execution Flag Check ======================================================
        if test_case["Execution"].strip().lower() == "yes":

            # ================================== Login to SFDC =============================================================
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")

            logger.info(
                f"*****{script_name} Test Script Execution Started for "
                f"Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for "
                f"Iteration:{test_case['Iteration']}*****\033[0m"
            )

            if is_valid_data(test_case["User Name"]):
                cm.enterText("LoginPage", "username_Input", test_case["User Name"])
                logger.info(f"Username entered: {test_case['User Name']}")

            cm.clickElement("LoginPage", "next_Button")
            logger.info("Clicked on next button")

            cm.enterText("LoginPage", "password_Input", config.get_encodedString())
            logger.info("Entered password")

            cm.clickElement("LoginPage", "signin_Button")
            logger.info("Signin button clicked")

            cm.clickElement("LoginPage", "yes_Button")
            logger.info("Yes button clicked")

            is_visible = cm.isElementVisible("HomePage", "opportunities_Label")
            cm.assertTrue(
                is_visible,
                "Opportunities label is not visible on the homepage",
            )
            logger.info(
                f"Opportunities label has been verified on homepage: {is_visible}"
            )

            # ================================== Navigate to Incentive Registration ========================================
            cm.clickElement("HomePage", "app_Launcher_Button")
            logger.info("Clicked on App Launcher button")

            if is_valid_data(test_case["App Launcher Search Value"]):
                cm.enterText(
                    "HomePage",
                    "app_Launcher_Search_Input",
                    test_case["App Launcher Search Value"],
                )
                logger.info(
                    f"Entered App Launcher search value: "
                    f"{test_case['App Launcher Search Value']}"
                )

                cm.clickElement(
                    "HomePage",
                    "app_Launcher_Incentive_Registration_Link",
                )
                logger.info(
                    f"Clicked on App Launcher search result: "
                    f"{test_case['App Launcher Search Value']}"
                )

            # ================================== Create Incentive Registration =============================================
            create_ir_flag = (
                str(test_case.get("Create Incentive Registration", "")).strip().lower()
            )

            if create_ir_flag == "yes":
                cm.clickElement("IncentiveRegistrationPage", "new_IR_Button")
                logger.info("Clicked on New IR button")

                # ====================== Search Account by CMAT ID in IR iframe ===========================================
                if is_valid_data(test_case["CMAT Address ID"]):
                    cmat_address_id = (
                        str(test_case["CMAT Address ID"]).strip().replace(".0", "")
                    )

                    frame_locator_setup = locator_manager.get_locator(
                        "HomePage", "frame_Locator"
                    )
                    cm.switchToFrame(frame_locator_setup)
                    logger.info("Switched to Incentive Registration iframe")

                    cm.clickElement("IncentiveRegistrationPage", "cmat_Address")
                    logger.info("Clicked on CMAT Address input")

                    cm.clearText("IncentiveRegistrationPage", "cmat_Address")
                    logger.info("Cleared CMAT Address input")

                    cm.enterText(
                        "IncentiveRegistrationPage",
                        "cmat_Address",
                        cmat_address_id,
                    )
                    logger.info(f"Entered CMAT Address ID: {cmat_address_id}")

                    cm.clickElement(
                        "IncentiveRegistrationPage",
                        "cmat_Search_Button",
                    )
                    logger.info("Clicked on CMAT Search button")

                    cm.clickElement("IncentiveRegistrationPage", "next_Button")
                    logger.info("Clicked on Next button after CMAT Account selection")

                # ====================== Partner Account Selection =========================================================
                if is_valid_data(test_case["Partner Account Name"]):
                    cm.enterText(
                        "IncentiveRegistrationPage",
                        "partner_Account_Search",
                        test_case["Partner Account Name"],
                    )
                    logger.info(
                        f"Entered Partner Name: {test_case['Partner Account Name']}"
                    )
                    cm.pressEnter(
                        "IncentiveRegistrationPage",
                        "partner_Account_Search",
                    )
                    cm.clickElement(
                        "IncentiveRegistrationPage",
                        "partner_Radio_Button",
                    )
                    logger.info("Selected first Partner Account radio button")

                    cm.clickElement(
                        "IncentiveRegistrationPage",
                        "select_Button",
                    )
                    logger.info("Clicked Select button after Partner Account selection")

                    cm.clickElement(
                        "IncentiveRegistrationPage",
                        "next_Button",
                    )
                    logger.info(
                        "Clicked on Next button after Partner Account selection"
                    )

                # ======================= IR Creation Page Contact Selection ==============================================
                if is_valid_data(test_case["Customer Contact Search Text"]):
                    cm.clickElement(
                        "IncentiveRegistrationPage",
                        "customer_Contact_Search",
                    )
                    logger.info("Customer Contact Search Click")

                    cm.enterText(
                        "IncentiveRegistrationPage",
                        "customer_Contact_Search",
                        test_case["Customer Contact Search Text"],
                    )
                    logger.info(
                        f"Entered Contact Name: "
                        f"{test_case['Customer Contact Search Text']}"
                    )
                    cm.clickByText(test_case["Customer Contact Search Text"])
                    logger.info("Customer Contact Selected")

                # ================== Quote Source Selection ===============================================================
                if is_valid_data(test_case["Quote Source"]):

                    cm.clickElement("IncentiveRegistrationPage", "quote_Source_Click")

                    cm.clickByText(test_case["Quote Source"])
                    logger.info("Quote Source Selected")

                # ================== Product Multi Select Selection =======================================================
                if is_valid_data(test_case["Product Name"]):
                    cm.clickByText(test_case["Product Name"])

                    cm.clickElement(
                        "IncentiveRegistrationPage",
                        "product_Right_Arrow",
                    )
                    logger.info(
                        f"Clicked right arrow to move product: "
                        f"{test_case["Product Name"]}"
                    )

                if test_case["Quote Source"].strip().lower() == "hyperscaler":

                    cm.clickElement("IncentiveRegistrationPage", "purchase_Type")
                    logger.info(f"Clicked on Purchase Type Listbox")
                    cm.selectOptionInListbox(
                        "IncentiveRegistrationPage",
                        "purchase_Type",
                        test_case["Purchase Type"],
                    )
                    logger.info(f"Selected the value for Purchase Type Listbox")
                    cm.clickElement("IncentiveRegistrationPage", "hyperscaler_Value")
                    logger.info(f"Clicked on Hyperscaler Listbox")
                    cm.selectOptionInListbox(
                        "IncentiveRegistrationPage",
                        "hyperscaler_Value",
                        test_case["Hyperscaler Value"],
                    )
                    logger.info(f"Selected the value for Hyperscaler Listbox")
                    cm.clickElement("IncentiveRegistrationPage", "hyperscaler_Checkbox")
                    logger.info(f"Checked Will provide when known for payment checkbox")

                # ================== Project Description ==================================================================
                if is_valid_data(test_case["Project Description"]):
                    project_description = str(test_case["Project Description"]).strip()

                    cm.enterText(
                        "IncentiveRegistrationPage",
                        "project_Description",
                        project_description,
                    )

                    logger.info(f"Entered Project Description: {project_description}")
                # ================== Save & Continue ======================================================================
                cm.clickElement(
                    "IncentiveRegistrationPage",
                    "save_Continue_Button",
                )
                logger.info("Clicked on Save & Continue button")
                print("\033[92m✅ Clicked on Save & Continue button\033[0m")

                # ================== Estimated Booking ====================================================================
                if test_case["Quote Source"].strip().lower() != "hyperscaler":
                    if is_valid_data(test_case["Estimated Booking"]):
                        estimated_booking = (
                            str(test_case["CMAT Address ID"]).strip().replace(".0", "")
                        )
                        cm.enterText(
                            "IncentiveRegistrationPage",
                            "estimated_Booking",
                            estimated_booking,
                        )
                        logger.info(
                            f"Entered Estimated Booking value: {estimated_booking}"
                        )

                if test_case["Quote Source"].strip().lower() == "hyperscaler":
                    if is_valid_data(test_case["Estimated Revenue"]):
                        estimated_revenue = (
                            str(test_case["CMAT Address ID"]).strip().replace(".0", "")
                        )
                        cm.enterText(
                            "IncentiveRegistrationPage",
                            "estimated_Revenue",
                            estimated_revenue,
                        )
                        logger.info(
                            f"Entered Estimated Booking value: {estimated_revenue}"
                        )
                # ================== Create Incentive Registration ========================================================
                cm.clickElement(
                    "IncentiveRegistrationPage",
                    "create_Incentive_Registration_Button",
                )
                logger.info("Clicked on Create Incentive Registration button")

                cm.waitForStable(5)
                logger.info("Waiting for IR to be Created")

                cm.switchToParentFrame()
                logger.info("Switch to Parent Frame")
                # ================== Verify Incentive Registration Status ================================================
                if is_valid_data(test_case["Expected IR Status"]):
                    expected_ir_status = str(test_case["Expected IR Status"]).strip()

                    actual_ir_status = cm.readText(
                        "IncentiveRegistrationPage",
                        "ir_Status_Value",
                    )

                    logger.info(
                        f"Captured Incentive Registration Status: {actual_ir_status}"
                    )

                    if actual_ir_status and expected_ir_status in actual_ir_status:
                        logger.info(
                            f"IR created successfully and status verified. "
                            f"Expected: {expected_ir_status}, Actual: {actual_ir_status}"
                        )
                        print(
                            f"\033[92m✅ IR created successfully and status verified: "
                            f"{actual_ir_status}\033[0m"
                        )
                    else:
                        failure_message = (
                            f"IR Status verification failed. "
                            f"Expected: '{expected_ir_status}', "
                            f"Actual: '{actual_ir_status}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")

                # ================== Associate Opportunity ===============================================================
                if test_case["Quote Source"].strip().lower() != "hyperscaler":
                    if test_case["Associate Opportunity"].strip().lower() == "yes":

                        if cm.clickElement(
                            "IncentiveRegistrationPage",
                            "associated_Opportunity_Edit_Icon",
                        ):
                            logger.info("Clicked on Associated Opportunity edit icon")
                            cm.waitForStable(3)
                            logger.info("Waiting for Opportunity Search Results")

                        if is_valid_data(test_case["Opportunity Number"]):

                            if cm.enterText(
                                "IncentiveRegistrationPage",
                                "associated_Opportunity_Input",
                                test_case["Opportunity Number"],
                            ):
                                logger.info(
                                    f"Entered Opportunity Number: {test_case['Opportunity Number']}"
                                )

                            cm.clickByText(test_case["Opportunity Number"])
                            logger.info("Opportunity Selected Based on Number")

                            cm.clickElement(
                                "IncentiveRegistrationPage",
                                "associated_Opportunity_Save_Button",
                            )
                            logger.info("Opportunity Associated Successfully")
                            print(
                                "\033[93mℹ️ Opportunity Associated Successfully\033[0m"
                            )

                    else:
                        logger.info(
                            "Associate Opportunity flag is not Yes. "
                            "Skipping Opportunity association."
                        )

                else:
                    logger.info(
                        "Create Incentive Registration flag is set to No. Skipping IR creation."
                    )
                    print(
                        "\033[93mℹ️ Create Incentive Registration flag is No. "
                        "Skipping IR creation.\033[0m"
                    )
                # =======================================Validation of Quote Source Status========================================================================================

                if test_case["Quote Source Validation"].strip().lower() == "yes":
                    if is_valid_data(test_case["Quote Source"]):
                        quote_source_value = cm.readTextAndWait(
                            "IncentiveRegistrationPage",
                            "quote_Source_value",
                            wait_time=3,
                        )
                        logger.info(
                            f"Captured Quote Source value: {quote_source_value}"
                        )
                        quote_source_validation = cm.checkExpectedTextInActual(
                            actual_text=quote_source_value,
                            expected_text=test_case["Quote Source"],
                        )
                        if not quote_source_validation:
                            failure_message = f"Quote Source Validation Failed: Expected '{test_case['Quote Source"']}' but got '{quote_source_value}'"
                            validation_failures.append(
                                failure_message
                            )  # Add failure to the list
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual Quote Source: {quote_source_value} with expected Quote Source: {test_case['Quote Source']}"
                            )
                            print(
                                f"\033[92m✅ Compared actual Quote Source: {quote_source_value} with expected Quote Source: {test_case['Quote Source']}"
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
            # ================================== Write Test Result =========================================================
            test_results = [
                [
                    "Test Case ID",
                    "Execution Status",
                    "User Persona",
                    "CMAT Address ID",
                    "Partner Account",
                    "Customer Contact",
                    "Quote Source",
                    "Product Name",
                    "Estimated Booking",
                    "Associate Opportunity",
                    "Opportunity Number",
                    "IR Number",
                    "Details",
                ],
                [
                    test_case["Test Case ID"],
                    boolean_status,
                    test_case["User Persona"],
                    test_case["CMAT Address ID"],
                    test_case["Partner Account Name"],
                    test_case["Customer Contact Search Text"],
                    test_case["Quote Source"],
                    test_case["Product Name"],
                    test_case["Estimated Booking"],
                    test_case.get("Associate Opportunity", ""),
                    test_case.get("Opportunity Number", ""),
                ],
            ]

            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)

            logger.info(
                f"*****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\033[92m✅ *****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****\033[0m"
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
        logger.exception(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed_Screenshot")
        raise
