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

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: 478215_Resource Request from Accounts Tab- Verify Hyperscaler CSM  and PCS Solution Architects is  available
# Test Description:
#   This script validates Resource Request creation from Account page.
#   It validates Request Team picklist values, selects request team from Excel,
#   enters Request Activity, submits the request, and validates Approval History statuses.
#   1. Login to Spark Instace
#   2. Navigate to Account
#   3. Create an Resource Request, Verify Request Team values
#   4. Verify Resource Request Status & Approval History Status values
# Author: Sagar Ch
# Reviewer: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_Account_Resource_Request.xlsx"
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
def test_Account_Resource_Request(page: Page, base_url, config, test_case) -> None:
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []

    try:
        # ================================== Execution Flag Check ======================================================
        if test_case["Execution"].strip().lower() == "yes":

            # ================================== Login to SFDC =========================================================
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for Iteration:{test_case['Iteration']}*****\033[0m"
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

            # ================================== Navigate to Account ===================================================
            cm.clickElement("HomePage", "accounts_Tab")
            logger.info("Clicked on Accounts tab")

            cm.clickElement("AccountList", "account_Search_Input")
            logger.info("Clicked on global search button")

            if is_valid_data(test_case["Account Name"]):
                cm.enterText(
                    "AccountList",
                    "account_Search_Input",
                    test_case["Account Name"],
                )
                logger.info(
                    f"Entered account name in global search box: {test_case['Account Name']}"
                )
                cm.pressEnter("AccountList", "account_Search_Input")
                logger.info("Pressed Enter on global search input")
                cm.clickElement("AccountList", "account_First_Result_Link")
                logger.info(f"Clicked on searched account: {test_case['Account Name']}")

            # ================================== Create Resource Request ===============================================
            if test_case["Create Resource Request"].strip().lower() == "yes":

                cm.clickElement("HomePage", "Account_Show_More_Actions")
                logger.info("Clicked on Account Show More Actions button")

                cm.clickElement("HomePage", "Request_Resource_Button")
                logger.info("Clicked on Request a Resource button")

                # ===================Request Team Picklist Values Validations==========================
                cm.clickElement("HomePage", "request_Team_Combobox")
                logger.info("Clicked on Request Team picklist")

                hyperscaler_csm_visible = cm.isElementVisible(
                    "HomePage",
                    "request_Team_Hyperscaler_CSM_Option",
                )

                if not hyperscaler_csm_visible:
                    failure_message = (
                        "Hyperscaler CSM option is not visible in Request Team picklist"
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Hyperscaler CSM option has been verified: {hyperscaler_csm_visible}"
                    )
                    print(
                        "\033[92m✅ Hyperscaler CSM option is visible in Request Team picklist\033[0m"
                    )

                pcs_solution_architects_visible = cm.isElementVisible(
                    "HomePage",
                    "request_Team_PCS_Solution_Architects_Option",
                )

                if not pcs_solution_architects_visible:
                    failure_message = "PCS Solution Architects option is not visible in Request Team picklist"
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"PCS Solution Architects option has been verified: {pcs_solution_architects_visible}"
                    )
                    print(
                        "\033[92m✅ PCS Solution Architects option is visible in Request Team picklist\033[0m"
                    )

                # ====================Select Request Team based on Excel value===============================
                if is_valid_data(test_case["Request Team To Select"]):
                    cm.clickByText(test_case["Request Team To Select"])

                if is_valid_data(test_case["Request Activity"]):
                    cm.enterText(
                        "HomePage",
                        "requested_Activity_Input",
                        test_case["Request Activity"],
                    )
                    logger.info(
                        f"Entered Request Activity: {test_case['Request Activity']}"
                    )

                cm.clickElement("HomePage", "submit_Button")
                logger.info("Clicked on Submit button")
            else:
                logger.info(
                    "Create Resource Request flag is set to No. Skipping Resource Request creation."
                )
                print(
                    "\033[93mℹ️ Create Resource Request flag is No. Skipping Resource Request creation.\033[0m"
                )

            # ================================== Validate Request Status From Excel ====================================
            if test_case["Status Validations"].strip().lower() == "yes":
                if is_valid_data(test_case["Expected Request Status"]):
                    resource_request_status = cm.readText(
                        "HomePage",
                        "RR_Status",
                    )
                    logger.info(
                        f"Captured Resource Request Status: {resource_request_status}"
                    )

                    expected_status_available = cm.checkExpectedTextInActual(
                        actual_text=resource_request_status,
                        expected_text=test_case["Expected Request Status"],
                    )
                    if not expected_status_available:
                        failure_message = (
                            f"Resource Request status validation failed: "
                            f"Expected '{test_case['Expected Request Status']}', "
                            f"Actual status found '{resource_request_status}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Resource Request status validation passed. "
                            f"Expected status '{test_case['Expected Request Status']}' is displayed."
                        )
                        print(
                            f"\033[92m✅ Resource Request status validation passed: "
                            f"{test_case['Expected Request Status']}\033[0m"
                        )

                # ================================== Approval History Validation From Excel ================================
                if test_case["Approval Page Validations"].strip().lower() == "yes":
                    cm.clickElement("HomePage", "approval_History_Tab")
                    logger.info("Clicked on Approval History tab")
                    print("\033[94mℹ️ Clicked on Approval History tab\033[0m")
                    # ============================== Approval History Status 1 =============================================
                    if is_valid_data(test_case["Approval History Status 1"]):
                        approval_history_status1 = cm.readText(
                            "HomePage",
                            "approval_status_1",
                        )
                        logger.info(
                            f"Captured Approval History Status 1: {approval_history_status1}"
                        )
                        print(
                            f"\033[94mℹ️ Captured Approval History Status 1: {approval_history_status1}\033[0m"
                        )

                        approval_status_1_available = cm.checkExpectedTextInActual(
                            actual_text=approval_history_status1,
                            expected_text=test_case["Approval History Status 1"],
                        )

                        if not approval_status_1_available:
                            failure_message = (
                                f"Approval History Status 1 validation failed: "
                                f"Expected '{test_case['Approval History Status 1']}', "
                                f"Actual status found '{approval_history_status1}'"
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Approval History Status 1 has been verified: "
                                f"{test_case['Approval History Status 1']}"
                            )
                            print(
                                f"\033[92m✅ Approval History Status 1 validation passed: "
                                f"{test_case['Approval History Status 1']}\033[0m"
                            )

                    # ============================== Approval History Status 2 =============================================
                    if is_valid_data(test_case["Approval History Status 2"]):
                        approval_history_status2 = cm.readText(
                            "HomePage",
                            "approval_status_2",
                        )
                        logger.info(
                            f"Captured Approval History Status 2: {approval_history_status2}"
                        )
                        print(
                            f"\033[94mℹ️ Captured Approval History Status 2: {approval_history_status2}\033[0m"
                        )

                        approval_status_2_available = cm.checkExpectedTextInActual(
                            actual_text=approval_history_status2,
                            expected_text=test_case["Approval History Status 2"],
                        )

                        if not approval_status_2_available:
                            failure_message = (
                                f"Approval History Status 2 validation failed: "
                                f"Expected '{test_case['Approval History Status 2']}', "
                                f"Actual status found '{approval_history_status2}'"
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Approval History Status 2 has been verified: "
                                f"{test_case['Approval History Status 2']}"
                            )
                            print(
                                f"\033[92m✅ Approval History Status 2 validation passed: "
                                f"{test_case['Approval History Status 2']}\033[0m"
                            )

                else:
                    logger.info(
                        "Approval Page Validations flag is set to No. Skipping Approval History validation."
                    )
                    print(
                        "\033[93m⚠️ Approval Page Validations flag is No. Skipping Approval History validation.\033[0m"
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
            # ================================== Write Test Result =====================================================
            test_results = [
                [
                    "Test Case ID",
                    "Execution Status",
                    "Account Name",
                    "Request Team",
                    "Request Activity",
                    "Expected Request Status",
                    "Approval History Status 1",
                    "Approval History Status 2",
                    "Details",
                ],
                [
                    test_case["Test Case ID"],
                    boolean_status,
                    test_case["Account Name"],
                    test_case["Request Team To Select"],
                    test_case["Request Activity"],
                    test_case["Expected Request Status"],
                    test_case["Approval History Status 1"],
                    test_case["Approval History Status 2"],
                    "Resource Request created and statuses validated successfully",
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
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
