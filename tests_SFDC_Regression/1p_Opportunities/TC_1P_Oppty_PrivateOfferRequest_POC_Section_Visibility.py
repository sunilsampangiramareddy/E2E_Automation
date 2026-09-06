import pytest
import logging
import os
from datetime import datetime
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from pages_SFDC.Wwss_Forecasting_Request import WWSSForecastingRequest
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# Test Metadata
# ======================================================================================================================
# Test Scenario: 485906
#   1P Opportunity Private Offer Request creation & POC Fields Validations
#
# Test Description:
#   This script performs the below Salesforce automation flow:
#   1. Login to Salesforce.
#   2. Create 1P Opportunity based on Excel test data.
#   3. Capture Opportunity URL for later navigation.
#   4. Attempt Private Offer Request creation, Option should not be displayed restricted for 1P Opportunity Creation
#   5. Now Navigate to Details Tab
#   6. Verify POC Related Fields under Validation Event Section
#   7. Capture result and write execution details to Excel.
#
# Author : Sagar Ch
# Reviewer: Sunil Reddy
# ======================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression",
    "TC_1P_Oppty_PrivateOfferRequest_POC_Section_Visibility.xlsx",
)
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Load locators from JSON
locator_file_path = os.path.join(working_directory, "locators", "locators.json")
locator_manager = LocatorManager(locator_file_path)

# Get the test script name without extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize(
    "test_case",
    test_data.to_dict(orient="records"),
    ids=lambda test_case, index=iter(range(1, len(test_data) + 1)): f"test_case{next(index)}",
)
@pytest.mark.master
@pytest.mark.regression
def test_1P_Oppty_PrivateOfferRequest_POC_Section_Visibility(page: Page, base_url, config, test_case) -> None:
    cm = CommonMethods(page, locator_manager)
    ss = ScreenshotUtil(page)
    co = CreateOpportunity(page)

    boolean_status = "Pass"
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"

    validation_failures = []
    spark_url = ""
    oppty_name = ""
    oppty_number = ""

    try:
        # ================================== Login to SFDC =============================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")

            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:"
                f"{test_case['Iteration']} and for the test case id {test_case['Test Case ID']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for the Iteration:"
                f"{test_case['Iteration']} and for the test case id {test_case['Test Case ID']}*****\033[0m"
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
            cm.assertTrue(is_visible, "Opportunities label is not visible on the homepage")
            logger.info(f"Opportunities label has been verified on the homepage: {is_visible}")

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
                                    "CreateOpportunity",
                                    "channel",
                                    test_case["Channel"],
                                )
                                logger.info(f"Selected channel: {test_case['Channel']}")

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName_1p(
                                    test_case["Opportunity Name"]
                                )
                                logger.info(f"Entered opportunity name")
                            if is_valid_data(test_case["Sales Type"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Type_1P",
                                    test_case["Sales Type"],
                                )
                                logger.info(
                                    f"Selected 1P sales type: {test_case['Sales Type']}"
                                )
                            if is_valid_data(test_case["Primary Contact"]):
                                cm.clickElement("CreateOpportunity",
                                                                    "primary_Contact_1P",)
                                logger.info("Clicked on Contact Selection Field")
                                cm.clickByText(test_case["Primary Contact"])
                                logger.info(
                                    f"Selected sales play: {test_case['Primary Contact']}"
                                )
                            if is_valid_data(test_case["Confidential"]):
                                cm.clickElement("CreateOpportunity",
                                                                    "Confidential",)
                                logger.info("Clicked on Confidential Field")
                                cm.selectDropdownByValue("CreateOpportunity",
                                "Confidential",test_case["Confidential"],)
                                logger.info(
                                    f"Selected confidential value: {test_case['Confidential']}"
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
                                """
                            if is_valid_data(test_case["Installed Base Type"]):
                                co.selectInstalledBaseType(test_case["Installed Base Type"])
                                logger.info(f"Selected installed base type: {test_case['Installed Base Type']}")
                                """
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
                                    "CreateOpportunity",
                                    "pathway",
                                    test_case["Pathway"],
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
                        print(f"\033[94mℹ️ Opportunity Number: {oppty_number}\033[0m")

                        oppty_name = cm.readText(
                            "CreateOpportunity", "opportunity_Name"
                        )
                        logger.info(f"Opportunity Name: {oppty_name}")
                        print(f"\033[94mℹ️ Opportunity Name: {oppty_name}\033[0m")

                    spark_url = cm.getCurrentURL()
                    logger.info(f"Captured Spark URL: {spark_url}")
                    print(f"\033[94mℹ️ Captured Spark URL: {spark_url}\033[0m")

# ============================== 1P Opportunity Validation Event & Private Offer Request Validation ==============================

        # ========================== Validate Private Offer Request Option Not Available ====================================
            if test_case["Private Offer Request Validation"].strip().lower() == "yes":

                if is_valid_data(test_case["Private Offer Request Menu Item"]):
                    private_offer_request_menu_item = str(
                        test_case["Private Offer Request Menu Item"]
                    ).strip()

                    cm.clickElement(
                        "OpportunityDetailPage",
                        "show_More_Actions_Button",
                    )
                    logger.info("Clicked on Show More Actions button on Opportunity")

                    private_offer_request_visible = cm.isElementVisible(
                        "OpportunityDetailPage",
                        "privateoffer_Request_Menuitem",
                    )

                    logger.info(
                        f"Private Offer Request menu item visible status: "
                        f"{private_offer_request_visible}"
                    )

                    if private_offer_request_visible:
                        actual_private_offer_request_menu_item = cm.readText(
                            "OpportunityDetailPage",
                            "privateoffer_Request_Menuitem",
                        )

                        logger.info(
                            f"Captured Private Offer Request Menu Item: "
                            f"{actual_private_offer_request_menu_item}"
                        )

                        private_offer_request_menu_validation = cm.checkExpectedTextInActual(
                            actual_text=actual_private_offer_request_menu_item,
                            expected_text=private_offer_request_menu_item,
                        )

                        if private_offer_request_menu_validation:
                            failure_message = (
                                f"Private Offer Request Menu Item Validation Failed: "
                                f"Expected '{private_offer_request_menu_item}' "
                                f"should not be available, but got "
                                f"'{actual_private_offer_request_menu_item}'"
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Private Offer Request Menu Item "
                                f"'{private_offer_request_menu_item}' "
                                f"is not available as expected"
                            )
                            print(
                                f"\033[92m✅ Private Offer Request Menu Item "
                                f"'{private_offer_request_menu_item}' "
                                f"is not available as expected\033[0m"
                            )
                    else:
                        logger.info(
                            f"Private Offer Request Menu Item "
                            f"'{private_offer_request_menu_item}' "
                            f"is not available as expected"
                        )
                        print(
                            f"\033[92m✅ Private Offer Request Menu Item "
                            f"'{private_offer_request_menu_item}' "
                            f"is not available as expected\033[0m"
                        )
            # ========================== Validate Validation Event Section & POC Fields ====================================
            if test_case["POC Fields Validation"].strip().lower() == "yes":

                cm.clickElement(
                    "OpportunityDetailPage",
                    "details_Tab",
                )
                logger.info("Clicked on Details Tab")
                cm.mouseWheelToBottom(800, scrolls=8, wait_time=0)
                # ========================== Validate Validation Event Section ====================================
                if is_valid_data(test_case["Validation Event Section"]):
                    expected_validation_event_section = str(
                        test_case["Validation Event Section"]
                    ).strip()

                    actual_validation_event_section = cm.readText(
                        "OpportunityDetailPage",
                        "validation_Event_Section",
                    )

                    logger.info(
                        f"Captured Validation Event Section: {actual_validation_event_section}"
                    )

                    validation_event_section_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_validation_event_section,
                        expected_text=expected_validation_event_section,
                    )

                    if not validation_event_section_validation:
                        failure_message = (
                            f"Validation Event Section Validation Failed: "
                            f"Expected '{expected_validation_event_section}' but got "
                            f"'{actual_validation_event_section}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual Validation Event Section: "
                            f"{actual_validation_event_section} with expected Validation Event Section: "
                            f"{expected_validation_event_section}"
                        )
                        print(
                            f"\033[92m✅ Compared actual Validation Event Section: "
                            f"{actual_validation_event_section} with expected Validation Event Section: "
                            f"{expected_validation_event_section}\033[0m"
                        )

                # ========================== Validate POC Start Date Field ====================================
                if is_valid_data(test_case["POC Start Date Field"]):
                    expected_poc_start_date_field = str(
                        test_case["POC Start Date Field"]
                    ).strip()

                    actual_poc_start_date_field = cm.readText(
                        "OpportunityDetailPage",
                        "poc_Start_Date_Label",
                    )

                    logger.info(
                        f"Captured POC Start Date Field: {actual_poc_start_date_field}"
                    )

                    poc_start_date_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_poc_start_date_field,
                        expected_text=expected_poc_start_date_field,
                    )

                    if not poc_start_date_validation:
                        failure_message = (
                            f"POC Start Date Field Validation Failed: "
                            f"Expected '{expected_poc_start_date_field}' but got "
                            f"'{actual_poc_start_date_field}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual POC Start Date Field: "
                            f"{actual_poc_start_date_field} with expected POC Start Date Field: "
                            f"{expected_poc_start_date_field}"
                        )
                        print(
                            f"\033[92m✅ Compared actual POC Start Date Field: "
                            f"{actual_poc_start_date_field} with expected POC Start Date Field: "
                            f"{expected_poc_start_date_field}\033[0m"
                        )

                # ========================== Validate POC End Date Field ====================================
                if is_valid_data(test_case["POC End Date Field"]):
                    expected_poc_end_date_field = str(
                        test_case["POC End Date Field"]
                    ).strip()

                    actual_poc_end_date_field = cm.readText(
                        "OpportunityDetailPage",
                        "poc_End_Date_Label",
                    )

                    logger.info(
                        f"Captured POC End Date Field: {actual_poc_end_date_field}"
                    )

                    poc_end_date_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_poc_end_date_field,
                        expected_text=expected_poc_end_date_field,
                    )

                    if not poc_end_date_validation:
                        failure_message = (
                            f"POC End Date Field Validation Failed: "
                            f"Expected '{expected_poc_end_date_field}' but got "
                            f"'{actual_poc_end_date_field}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual POC End Date Field: "
                            f"{actual_poc_end_date_field} with expected POC End Date Field: "
                            f"{expected_poc_end_date_field}"
                        )
                        print(
                            f"\033[92m✅ Compared actual POC End Date Field: "
                            f"{actual_poc_end_date_field} with expected POC End Date Field: "
                            f"{expected_poc_end_date_field}\033[0m"
                        )

                # ========================== Validate POC Status Field ====================================
                if is_valid_data(test_case["POC Status Field"]):
                    expected_poc_status_field = str(
                        test_case["POC Status Field"]
                    ).strip()

                    actual_poc_status_field = cm.readText(
                        "OpportunityDetailPage",
                        "poc_Status_Label",
                    )

                    logger.info(
                        f"Captured POC Status Field: {actual_poc_status_field}"
                    )

                    poc_status_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_poc_status_field,
                        expected_text=expected_poc_status_field,
                    )

                    if not poc_status_validation:
                        failure_message = (
                            f"POC Status Field Validation Failed: "
                            f"Expected '{expected_poc_status_field}' but got "
                            f"'{actual_poc_status_field}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual POC Status Field: "
                            f"{actual_poc_status_field} with expected POC Status Field: "
                            f"{expected_poc_status_field}"
                        )
                        print(
                            f"\033[92m✅ Compared actual POC Status Field: "
                            f"{actual_poc_status_field} with expected POC Status Field: "
                            f"{expected_poc_status_field}\033[0m"
                        )

                # ========================== Validate POC Size (TB) Field ====================================
                if is_valid_data(test_case["POC Size (TB) Field"]):
                    expected_poc_size_tb_field = str(
                        test_case["POC Size (TB) Field"]
                    ).strip()

                    actual_poc_size_tb_field = cm.readText(
                        "OpportunityDetailPage",
                        "poc_Size_TB_Label",
                    )

                    logger.info(
                        f"Captured POC Size (TB) Field: {actual_poc_size_tb_field}"
                    )

                    poc_size_tb_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_poc_size_tb_field,
                        expected_text=expected_poc_size_tb_field,
                    )

                    if not poc_size_tb_validation:
                        failure_message = (
                            f"POC Size (TB) Field Validation Failed: "
                            f"Expected '{expected_poc_size_tb_field}' but got "
                            f"'{actual_poc_size_tb_field}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual POC Size (TB) Field: "
                            f"{actual_poc_size_tb_field} with expected POC Size (TB) Field: "
                            f"{expected_poc_size_tb_field}"
                        )
                        print(
                            f"\033[92m✅ Compared actual POC Size (TB) Field: "
                            f"{actual_poc_size_tb_field} with expected POC Size (TB) Field: "
                            f"{expected_poc_size_tb_field}\033[0m"
                        )

                # ========================== Validate POC Data Source Field ====================================
                if is_valid_data(test_case["POC Data Source Field"]):
                    expected_poc_data_source_field = str(
                        test_case["POC Data Source Field"]
                    ).strip()

                    actual_poc_data_source_field = cm.readText(
                        "OpportunityDetailPage",
                        "poc_Data_Source_Label",
                    )

                    logger.info(
                        f"Captured POC Data Source Field: {actual_poc_data_source_field}"
                    )

                    poc_data_source_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_poc_data_source_field,
                        expected_text=expected_poc_data_source_field,
                    )

                    if not poc_data_source_validation:
                        failure_message = (
                            f"POC Data Source Field Validation Failed: "
                            f"Expected '{expected_poc_data_source_field}' but got "
                            f"'{actual_poc_data_source_field}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual POC Data Source Field: "
                            f"{actual_poc_data_source_field} with expected POC Data Source Field: "
                            f"{expected_poc_data_source_field}"
                        )
                        print(
                            f"\033[92m✅ Compared actual POC Data Source Field: "
                            f"{actual_poc_data_source_field} with expected POC Data Source Field: "
                            f"{expected_poc_data_source_field}\033[0m"
                        )

                # ========================== Validate POC Lead Field ====================================
                if is_valid_data(test_case["POC Lead Field"]):
                    expected_poc_lead_field = str(
                        test_case["POC Lead Field"]
                    ).strip()

                    actual_poc_lead_field = cm.readText(
                        "OpportunityDetailPage",
                        "poc_Lead_Label",
                    )

                    logger.info(
                        f"Captured POC Lead Field: {actual_poc_lead_field}"
                    )

                    poc_lead_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_poc_lead_field,
                        expected_text=expected_poc_lead_field,
                    )

                    if not poc_lead_validation:
                        failure_message = (
                            f"POC Lead Field Validation Failed: "
                            f"Expected '{expected_poc_lead_field}' but got "
                            f"'{actual_poc_lead_field}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual POC Lead Field: "
                            f"{actual_poc_lead_field} with expected POC Lead Field: "
                            f"{expected_poc_lead_field}"
                        )
                        print(
                            f"\033[92m✅ Compared actual POC Lead Field: "
                            f"{actual_poc_lead_field} with expected POC Lead Field: "
                            f"{expected_poc_lead_field}\033[0m"
                        )

               
                # ============================== Checking for Validation Failures ==========================================
            print(
                "\n\033[94mℹ️ ================Checking for Validation Failures============================\033[0m"
            )
            logger.info("Checking for validation failures")

            if validation_failures:
                boolean_status = "Fail"
                print("\033[91m❌ The following validation(s) failed:\033[0m")
                logger.error("The following validation(s) failed:")

                for failure in validation_failures:
                    logger.error(failure)
                    print(f"\033[91m❌ {failure}\033[0m")

                pytest.fail("One or more validations failed. Check the logs for details.")
            else:
                print("\033[92m✅ All validations passed successfully.\033[0m")
                logger.info("All validations passed successfully.")

            # ============================== Capture Test Result and Write To Excel ====================================
            test_results = [
                [
                    "Test Case ID",
                    "Opportunity Name",
                    "Opportunity Number",
                    "Execution Status",
                    "Details",
                ],
                [
                    script_name,
                    oppty_name,
                    oppty_number,
                    boolean_status,
                    f"{script_name} Test Script Execution Completed Successfully",
                ],
            ]

            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)

            logger.info(
                f"*****{script_name} Test Script Execution Completed Successfully "
                f"for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\n\033[92m✅ *****{script_name} Test Script Execution Completed Successfully "
                f"for the Iteration:{test_case['Iteration']}*****\033[0m"
            )

        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case "
                f"for the Iteration:{test_case['Iteration']}"
            )
            print(
                f"\033[93m➡️ Execution flag is set to 'No'. Skipping the test case "
                f"for the Iteration:{test_case['Iteration']}\033[0m"
            )
            pytest.skip(
                f"Execution flag is set to 'No'. Skipping the test case "
                f"for the Iteration:{test_case['Iteration']}"
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
