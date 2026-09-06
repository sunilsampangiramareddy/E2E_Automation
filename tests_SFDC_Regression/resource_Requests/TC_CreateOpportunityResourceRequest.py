import pytest
import logging
import os
from playwright.sync_api import Page
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from common_Methods.Common_Methods import CommonMethods

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: 474996 TC01 - 1P opportunity - Resource requests - PCS Solution Architects and Hyperscaler CSM, Adding Assignee to team member.
# Test Description: This test verifies that a resource request can be submitted from an opportunity,
#                   validates the opportunity name and POC details, and confirms the request status
#                   is set to 'Pending Assignment' after submission.
# Author: Ashwathy Sreelekha
# Modified By: Alok kumar Gupta
# Review By: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_CreateOpportunityResourceRequest.xlsx"
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
def test_createOpportunityResourceRequest(
    page: Page, base_url, config, test_case
) -> None:
    cm = CommonMethods(page, locator_manager)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    boolean_status = "Pass"
    validation_failures = []
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"

    try:
        # ==================================Login to SFDC=================================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"ℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****"
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
            if is_visible:
                logger.info(
                    f"Opportunities label has been verified on the homepage: {is_visible}"
                )
                print(f"✅ Opportunities label verified on the homepage")
            else:
                print(f"❌ Opportunities label is not visible on the homepage")
                validation_failures.append(
                    "Opportunities label is not visible on the homepage"
                )

            # ========================Create Opportunity======================================================================================
            if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":
                if test_case["Create Opportunity"].strip().lower() == "yes":

                    cm.clickElement("HomePage", "opportunities_Tab")
                    logger.info(f"Clicked on opportunities tab")

                    cm.clickElement("HomePage", "new_Opportunity_Button")
                    logger.info(f"Clicked on new opportunity button")

                    if is_valid_data(test_case["Account Name"]):
                        co.enterAccount(test_case["Account Name"])
                        logger.info(
                            f"Entered and selected account: {test_case['Account Name']}"
                        )

                    cm.clickElement("CreateOpportunity", "next_Button")
                    logger.info(f"Clicked on next button")

                    if (
                        test_case["Channel"] == direct_Oppty
                        or test_case["Channel"] == indirect_Oppty
                        or test_case["Opportunity Type"] == x1p_Oppty
                    ):
                        if is_valid_data(test_case["Opportunity Type"]):
                            cm.selectOptionInListbox(
                                "CreateOpportunity",
                                "opportunity_Type",
                                test_case["Opportunity Type"],
                            )
                            logger.info(
                                f"Selected opportunity type: {test_case['Opportunity Type']}"
                            )

                        if test_case["Opportunity Type"] == std_Oppty:
                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName(test_case["Opportunity Name"])
                                logger.info(f"Entered opportunity name")
                            if is_valid_data(test_case["Primary Contact"]):
                                co.select_PrimaryContact(test_case["Primary Contact"])
                                logger.info(
                                    f"Selected primary contact: {test_case['Primary Contact']}"
                                )
                            if is_valid_data(test_case["Sales Play"]):
                                cm.clickElement(
                                    "CreateOpportunity", "sales_Play_Combobox"
                                )
                                cm.clickByText(test_case["Sales Play"])
                                logger.info(
                                    f"Selected sales play: {test_case['Sales Play']}"
                                )
                            if is_valid_data(test_case["Channel"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity", "channel", test_case["Channel"]
                                )
                                logger.info(f"Selected channel: {test_case['Channel']}")

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName_1p(
                                    test_case["Opportunity Name"]
                                )
                                logger.info(f"Entered opportunity name")
                            if is_valid_data(test_case["Sales Type"]):
                                cm.clickElement(
                                    "CreateOpportunity", "sales_Type_Combobox"
                                )
                                cm.clickByText(test_case["Sales Type"])
                                logger.info(
                                    f"Selected 1P sales type: {test_case['Sales Type']}"
                                )
                            if is_valid_data(test_case["Primary Contact"]):
                                co.select_PrimaryContact(test_case["Primary Contact"])
                                logger.info(
                                    f"Selected 1P primary contact: {test_case['Primary Contact']}"
                                )
                            if is_valid_data(test_case["Hyperscaler"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "hyperscaler",
                                    test_case["Hyperscaler"],
                                )
                                logger.info(
                                    f"Selected hyperscaler: {test_case['Hyperscaler']}"
                                )
                            if is_valid_data(test_case["Confidential"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "Confidential",
                                    test_case["Confidential"],
                                )
                                logger.info(
                                    f"Confidential type: {test_case['Confidential']}"
                                )

                        if (
                            test_case["Channel"] == indirect_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):
                            if is_valid_data(test_case["Reseller Account"]):
                                co.selectReseller(test_case["Reseller Account"])
                                logger.info(
                                    f"Entered reseller account: {test_case['Reseller Account']}"
                                )

                        if (
                            test_case["Opportunity Type"] == std_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):
                            if is_valid_data(test_case["Sales Type"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Type",
                                    test_case["Sales Type"],
                                )
                                logger.info(
                                    f"Selected sales type: {test_case['Sales Type']}"
                                )
                            if is_valid_data(test_case["Installed Base Type"]):
                                co.selectInstalledBaseType(
                                    test_case["Installed Base Type"]
                                )
                                logger.info(
                                    f"Selected installed base type: {test_case['Installed Base Type']}"
                                )
                            if is_valid_data(test_case["Currency"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "currency",
                                    test_case["Currency"],
                                )
                                logger.info(
                                    f"Selected currency: {test_case['Currency']}"
                                )
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                        if (
                            test_case["Channel"] == indirect_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):
                            if is_valid_data(test_case["Pathway"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity", "pathway", test_case["Pathway"]
                                )
                                logger.info(f"Selected pathway: {test_case['Pathway']}")
                            if is_valid_data(test_case["Partner Sales Model"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "partner_Sales_Model",
                                    test_case["Partner Sales Model"],
                                )
                                logger.info(
                                    f"Selected partner sales model: {test_case['Partner Sales Model']}"
                                )
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                        if cm.isElementVisible(
                            "CreateOpportunity", "end_Customer_Label", 10000
                        ):
                            if (
                                test_case["Opportunity Type"] == std_Oppty
                                and test_case["Opportunity Type"] != x1p_Oppty
                            ):
                                if is_valid_data(test_case["End Customer Usage"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "end_Customer_Usage",
                                        test_case["End Customer Usage"],
                                    )
                                    logger.info(
                                        f"Selected end customer usage: {test_case['End Customer Usage']}"
                                    )

                                cm.clickElement("CreateOpportunity", "next_Button")
                                logger.info(f"Clicked on next button")

                        if (
                            test_case["Channel"] == indirect_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")
                            if is_valid_data(test_case["Reseller Sales Rep"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "reseller_Sales_Rep",
                                    test_case["Reseller Sales Rep"],
                                )
                                logger.info(
                                    f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}"
                                )
                            if is_valid_data(test_case["Reseller SE"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "reseller_SE",
                                    test_case["Reseller SE"],
                                )
                                logger.info(
                                    f"Selected reseller SE: {test_case['Reseller SE']}"
                                )
                            if is_valid_data(test_case["Distrubutor"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "distributor",
                                    test_case["Distrubutor"],
                                )
                                logger.info(
                                    f"Selected distributor: {test_case['Distrubutor']}"
                                )
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                        oppty_number = cm.readText(
                            "CreateOpportunity", "opportunity_Number"
                        )
                        logger.info(f"Opportunity Number: {oppty_number}")
                        print(f"ℹ️ Opportunity Number: {oppty_number}")

                        oppty_name = cm.readText(
                            "CreateOpportunity", "opportunity_Name"
                        )
                        logger.info(f"Opportunity Name: {oppty_name}")
                        print(f"ℹ️ Opportunity Name: {oppty_name}")

                    spark_url = cm.getCurrentURL()
                    logger.info(f"Captured Spark URL: {spark_url}")
                    print(f"ℹ️ Captured Spark URL: {spark_url}")

            if test_case["Opportunity Type"] != x1p_Oppty:
                sales_type_lower = (test_case["Sales Type"] or "").strip().lower()

                if sales_type_lower == test_case["Expected Sales Type"].strip().lower():
                    account_check = cm.assertExpectedInActualText(
                        oppty_name, test_case["Account Name"]
                    )
                    sales_type_check = cm.assertExpectedInActualText(
                        oppty_name, test_case["Sales Type"]
                    )
                    if account_check and sales_type_check:
                        print(f"✅ Opportunity name validated: {oppty_name}")
                    else:
                        print(
                            f"❌ Expected opportunity name to contain account name '{test_case['Account Name']}' and sales type '{test_case['Sales Type']}', but got '{oppty_name}'"
                        )
                        validation_failures.append(
                            f"Expected opportunity name to contain account name '{test_case['Account Name']}' and sales type '{test_case['Sales Type']}', but got '{oppty_name}'"
                        )
                else:
                    if cm.assertExpectedInActualText(
                        oppty_name, test_case["Account Name"]
                    ):
                        print(f"✅ Opportunity name validated: {oppty_name}")
                    else:
                        print(
                            f"❌ Expected opportunity name to contain account name '{test_case['Account Name']}', but got '{oppty_name}'"
                        )
                        validation_failures.append(
                            f"Expected opportunity name to contain account name '{test_case['Account Name']}', but got '{oppty_name}'"
                        )

                cm.clickElement("OpportunityDetailPage", "details_Tab")
                cm.waitForStable(4)

                if test_case["POC Validations"].strip().lower() == "yes":

                    cm.mouseWheelToBottom(800, scrolls=8, wait_time=0)

                    if cm.isElementVisible("OpportunityDetailPage", "poc_Button_Text"):
                        print(f"✅ POC button is visible on the details tab")
                    else:
                        print(f"❌ POC button is not visible on the details tab")
                        validation_failures.append(
                            "POC button is not visible on the details tab"
                        )

                    if cm.isElementVisible(
                        "OpportunityDetailPage", "edit_POC_Status_Button"
                    ):
                        print(
                            f"✅ Edit POC Status button is visible on the details tab"
                        )
                    else:
                        print(
                            f"❌ Edit POC Status button is not visible on the details tab"
                        )
                        validation_failures.append(
                            "Edit POC Status button is not visible on the details tab"
                        )

                    if cm.isElementVisible(
                        "OpportunityDetailPage", "edit_POC_Failed_Reason_Button"
                    ):
                        print(
                            f"✅ Edit POC Failed Reason button is visible on the details tab"
                        )
                    else:
                        print(
                            f"❌ Edit POC Failed Reason button is not visible on the details tab"
                        )
                        validation_failures.append(
                            "Edit POC Failed Reason button is not visible on the details tab"
                        )

                    if cm.isElementVisible(
                        "OpportunityDetailPage", "edit_POC_Comments_Button"
                    ):
                        print(
                            f"✅ Edit POC Comments button is visible on the details tab"
                        )
                    else:
                        print(
                            f"❌ Edit POC Comments button is not visible on the details tab"
                        )
                        validation_failures.append(
                            "Edit POC Comments button is not visible on the details tab"
                        )

                    if cm.isElementVisible(
                        "OpportunityDetailPage", "edit_POC_Start_Date_Button"
                    ):
                        print(
                            f"✅ Edit POC Start Date button is visible on the details tab"
                        )
                    else:
                        print(
                            f"❌ Edit POC Start Date button is not visible on the details tab"
                        )
                        validation_failures.append(
                            "Edit POC Start Date button is not visible on the details tab"
                        )

                    if cm.isElementVisible(
                        "OpportunityDetailPage", "edit_POC_End_Date_Button"
                    ):
                        print(
                            f"✅ Edit POC End Date button is visible on the details tab"
                        )
                    else:
                        print(
                            f"❌ Edit POC End Date button is not visible on the details tab"
                        )
                        validation_failures.append(
                            "Edit POC End Date button is not visible on the details tab"
                        )

                    if cm.isElementVisible(
                        "OpportunityDetailPage", "edit_POC_Original_End_Date_Button"
                    ):
                        print(
                            f"✅ Edit POC Original End Date button is visible on the details tab"
                        )
                    else:
                        print(
                            f"❌ Edit POC Original End Date button is not visible on the details tab"
                        )
                        validation_failures.append(
                            "Edit POC Original End Date button is not visible on the details tab"
                        )

                    print(f"✅ POC details validated on the details tab")

            if test_case["Request Team Validation"].strip().lower() == "yes":

                request_team_options = [
                    test_case["Requested Team Option 1"],
                    test_case["Requested Team Option 2"],
                ]

                cm.clickElement("OpportunityDetailPage", "show_More_Actions_Button")
                cm.clickElement("OpportunityDetailPage", "request_A_Resource_Menuitem")
                cm.clickElement("OpportunityDetailPage", "request_Team_Combobox")

                if cm.isElementVisible(
                    "OpportunityDetailPage", "request_Team_Option_Hyperscaler_CSM"
                ):
                    print(
                        f"✅ Request Team option '{request_team_options[0]}' is visible"
                    )
                else:
                    print(
                        f"❌ Request Team option '{request_team_options[0]}' is not visible"
                    )
                    validation_failures.append(
                        f"Request Team option '{request_team_options[0]}' is not visible"
                    )
                if cm.isElementVisible(
                    "OpportunityDetailPage",
                    "request_Team_Option_PCS_Solution_Architects",
                ):
                    print(
                        f"✅ Request Team option '{request_team_options[1]}' is visible"
                    )
                else:
                    print(
                        f"❌ Request Team option '{request_team_options[1]}' is not visible"
                    )
                    validation_failures.append(
                        f"Request Team option '{request_team_options[1]}' is not visible"
                    )

                cm.clickElement(
                    "OpportunityDetailPage",
                    "request_Team_Option_PCS_Solution_Architects",
                )
                cm.clickElement("OpportunityDetailPage", "requested_Activity_Input")
                cm.enterText(
                    "OpportunityDetailPage",
                    "requested_Activity_Input",
                    "test automation",
                )
                cm.clickElement("OpportunityDetailPage", "submit_Button")
                logger.info("Completed account resource request form")
                print(f"ℹ️ Resource request form submitted")
                cm.waitForStable(2)

                if cm.isElementVisible(
                    "OpportunityDetailPage", "pending_Assignment_Status_1"
                ):
                    print(f"✅ Request status 'Pending Assignment' is visible")
                else:
                    print(f"❌ Request status 'Pending Assignment' is not visible")
                    validation_failures.append(
                        "Request status 'Pending Assignment' is not visible"
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
            logger.info(
                f"***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}***"
            )
            print(
                f"✅ ***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}***"
            )
        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}"
            )
            print(
                f"➡️ Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}"
            )
            pytest.skip(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}"
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
