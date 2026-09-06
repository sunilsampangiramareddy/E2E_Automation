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
# Test Scenario: 482268, 481505
#   Private Offer Request creation, validation, approval, manual offer update, and Opportunity validation.
#
# Test Description:
#   This script performs the below Salesforce automation flow:
#   1. Login to Salesforce.
#   2. Create Opportunity based on Excel test data.
#   3. Capture Opportunity URL for later navigation.
#   4. Attempt Private Offer Request creation before Hyperscaler update and validate expected error message.
#   5. Update Opportunity Hyperscaler and Purchase Type.
#   6. Create Private Offer Request from Opportunity Show More Actions.
#   7. Enter Private Offer Request Required fields.
#   8. Save Private Offer Request and validate initial status.
#   9. Add Dimension.
#   10. Submit Private Offer Request for approval and validate Pending Review status.
#   11. Validate Final Unit Price mandatory error.
#   12. Update Final Unit Price on Dimension.
#   13. Update Manual Offer Details section.
#   14. Approve Marketplace Operations Status and validate approved locked message.
#   15. Navigate back to Opportunity and validate closed status/product details.
#   16. Capture result and write execution details to Excel.
#
# Author : Sagar Ch
# Reviewer: Sunil Reddy
# ======================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression",
    "TC_PrivateOfferRequest_And_OpptyAutoClosure.xlsx",
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
def test_PrivateOfferRequest_And_OpptyAutoClosure(page: Page, base_url, config, test_case) -> None:
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
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "primary_Contact_1P",
                                    test_case["Primary Contact"],
                                )
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
            # ============================== Private Offer Request Creation ============================================
            if test_case["Private Offer Request Creation"].strip().lower() == "yes":

                # ========================== Click Private Offer Request before selecting Hyperscaler ====================================
                if is_valid_data(test_case["Error Message_Hyperscaler Selection"]):
                    cm.clickElement("OpportunityDetailPage", "show_More_Actions_Button")
                    logger.info("Clicked on Show More Actions button on Opportunity")

                    cm.clickElement("OpportunityDetailPage", "privateoffer_Request_Menuitem")
                    logger.info("Clicked on Private Offer Request before Hyperscaler update")

                    expected_error_message = str(
                        test_case["Error Message_Hyperscaler Selection"]
                    ).strip()

                    actual_error_message = cm.readText(
                        "OpportunityDetailPage",
                        "hyperscaler_Error_Message",
                    )

                    logger.info(
                        f"Captured Hyperscaler Selection Error Message: {actual_error_message}"
                    )

                    hyperscaler_error_validation = cm.checkExpectedTextInActual(
                    actual_text=actual_error_message,
                    expected_text=expected_error_message,
                    )

                    if not hyperscaler_error_validation:
                        failure_message = (
                            f"Hyperscaler Selection Error Message Validation Failed: "
                            f"Expected '{expected_error_message}' but got '{actual_error_message}'"
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual Hyperscaler Selection Error Message: "
                            f"{actual_error_message} with expected Hyperscaler Selection Error Message: "
                            f"{expected_error_message}"
                        )
                        print(
                            f"\033[92m✅ Compared actual Hyperscaler Selection Error Message: "
                            f"{actual_error_message} with expected Hyperscaler Selection Error Message: "
                            f"{expected_error_message}\033[0m"
                        )

                    cm.clickElement("OpportunityDetailPage", "finish_Button")
                    logger.info("Clicked on Finish button after Hyperscaler error validation")

                # ========================== Update Hyperscaler and Purchase Type ======================================
                if test_case["Hyperscaler Selection"].strip().lower() == "yes":
                    if is_valid_data(test_case["Hyperscaler"]):
                        cm.clickElement(
                            "OpportunityDetailPage",
                            "opportunity_Hyperscaler_Edit_Icon",
                        )
                        logger.info("Clicked on Opportunity Hyperscaler edit icon")

                        cm.clickElement(
                        "OpportunityDetailPage",
                        "hyperscaler_Dropdown_Button",
                    )
                        logger.info("Clicked Hyperscaler dropdown")

                        cm.clickByText(test_case["Hyperscaler"])
                        logger.info(f"Selected Hyperscaler: {test_case["Hyperscaler"]}")

                    if is_valid_data(test_case["Purchase Type"]):
                        purchase_type_value = str(test_case["Purchase Type"]).strip()

                        cm.clickElement(
                            "OpportunityDetailPage",
                            "purchaseType_Dropdown_Button",
                        )
                        logger.info("Clicked Purchase Type dropdown")

                        cm.clickByText(purchase_type_value)
                        logger.info(f"Selected Purchase Type: {purchase_type_value}")

                    cm.clickElement(
                        "OpportunityDetailPage",
                        "save_Button",
                    )
                    logger.info("Clicked Save button after Hyperscaler and Purchase Type update")
                # ========================== Open Private Offer Request ================================================
                cm.clickElement("OpportunityDetailPage", "show_More_Actions_Button")
                logger.info("Clicked on Show More Actions button on Opportunity")

                cm.clickElement("OpportunityDetailPage", "privateoffer_Request_Menuitem")
                logger.info("Clicked on Private Offer Request menu item after Hyperscaler update")

                # ========================== Fill Private Offer Request fields =========================================
                if is_valid_data(test_case["Annual Revenue Before Discount"]):
                    annual_revenue_before_discount = (
                        str(test_case["Annual Revenue Before Discount"]).strip()
                    )

                    cm.clickElement("PrivateOfferRequest", "annual_Revenue_Before_Discount")
                    logger.info("Clicked Annual Revenue Before Discount Field")
                    cm.enterText(
                        "PrivateOfferRequest",
                        "annual_Revenue_Before_Discount",
                        annual_revenue_before_discount,
                    )
                    logger.info(
                        f"Entered Annual Revenue Before Discount: {annual_revenue_before_discount}"
                    )

                if is_valid_data(test_case["Cloud Marketplace Listing Name"]):
                    cloud_marketplace_listing_name = str(
                        test_case["Cloud Marketplace Listing Name"]
                    ).strip()

                    cm.clickElement("PrivateOfferRequest", "cloud_Marketplace_Listing_Dropdown")
                    logger.info("Clicked Cloud Marketplace Listing Name Field")
                    cm.clickByText(cloud_marketplace_listing_name)
                    logger.info(
                        f"Selected Cloud Marketplace Listing Name: {cloud_marketplace_listing_name}"
                    )

                if is_valid_data(test_case["Term Type"]):
                    term_type = (test_case["Term Type"]).strip()

                    cm.clickElement("PrivateOfferRequest", "term_Type_Dropdown")
                    logger.info("Clicked on Term Type Drop Down")

                    cm.clickByText(term_type)
                    logger.info(f"Selected Term Type: {term_type}")

                if is_valid_data(str(test_case["Term Length Months"])):
                    
                    cm.clickElement("PrivateOfferRequest", "term_Length_Months_Select")
                    logger.info("Clicked on Term Length Months Selection Picklist")

                    cm.selectDropdownByValueAndWait(
                    "PrivateOfferRequest",
                    "term_Length_Months_Select",
                    str(test_case["Term Length Months"]),3,)

                    logger.info(f"Selected Term Length Months: {(test_case["Term Length Months"])}")

                if is_valid_data(test_case["Discount Justification Category"]):

                    cm.clickElement(
                        "PrivateOfferRequest",
                        "discount_Justification_Category_Select",
                    )
                    logger.info("Clicked on Discount Justification Category Picklist")

                    cm.selectDropdownByValueAndWait(
                    "PrivateOfferRequest",
                    "discount_Justification_Category_Select",
                    str(test_case["Discount Justification Category"]),3,)

                    logger.info(
                        f"Selected Discount Justification Category: "
                        f"{test_case["Discount Justification Category"]}"
                    )

                if is_valid_data(test_case["Justification for Discount"]):
                    justification_for_discount = str(
                        test_case["Justification for Discount"]
                    ).strip()

                    cm.clickElement("PrivateOfferRequest", "justification_For_Discount")
                    logger.info("Clicked on Justification for Discount")
                    cm.enterText(
                        "PrivateOfferRequest",
                        "justification_For_Discount",
                        justification_for_discount,
                    )
                    logger.info(
                        f"Entered Justification for Discount: {justification_for_discount}"
                    )
                # ========================== Save Private Offer Request ================================================
                cm.clickElement("PrivateOfferRequest", "private_Offer_Save_Button")
                logger.info("Clicked Save button on Private Offer Request page")
                cm.waitForStable(3)
                # ========================== Validate Initial Status ===================================================
                if is_valid_data(test_case["Private Offer Request Status"]):
                    expected_private_offer_status = str(
                        test_case["Private Offer Request Status"]
                    ).strip()

                    actual_private_offer_status = cm.readText(
                        "PrivateOfferRequest",
                        "private_Offer_Request_Status_Value",
                    )
                    logger.info(
                        f"Captured Private Offer Request Status: {actual_private_offer_status}"
                    )

                private_offer_status_validation = cm.checkExpectedTextInActual(
                actual_text=actual_private_offer_status,
                expected_text=expected_private_offer_status,
                )
                    
                if not private_offer_status_validation:
                    failure_message = (
                        f"Private Offer Request Status Validation Failed: "
                        f"Expected '{expected_private_offer_status}' but got "
                        f"'{actual_private_offer_status}'"
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual Private Offer Request Status: "
                        f"{actual_private_offer_status} with expected Private Offer Request Status: "
                        f"{expected_private_offer_status}"
                    )
                    print(
                        f"\033[92m✅ Compared actual Private Offer Request Status: "
                        f"{actual_private_offer_status} with expected Private Offer Request Status: "
                        f"{expected_private_offer_status}\033[0m"
                    )
                # ======================= Private Offer Requets Page URL =====================================
                    private_offer_request_url = cm.getCurrentURL()
                    logger.info(
                        f"Captured Private Offer Request URL: {private_offer_request_url}"
                    )
                # ========================== Add Dimension ============================================================
                if test_case["Add Dimension"].strip().lower() == "yes":
                    cm.clickElement("PrivateOfferRequest", "add_Dimension_Button")
                    logger.info("Clicked Add Dimension button")

                    if is_valid_data(test_case["Dimension"]):
                        dimension_value = (test_case["Dimension"]).strip()

                        cm.clickElement("PrivateOfferRequest", "dimension_Dropdown")
                        logger.info("Clicked on Dimension Selection Drop Down")

                        cm.clickByText(dimension_value)
                        logger.info(f"Selected Dimension: {dimension_value}")

                    if is_valid_data(test_case["Quantity"]):
                        quantity_value = (str(test_case["Quantity"]).strip())

                        cm.clickElement("PrivateOfferRequest", "quantity_Input")
                        logger.info("Clicked on Quantity Field")

                        cm.enterText("PrivateOfferRequest", "quantity_Input", quantity_value)
                        logger.info(f"Entered Quantity: {quantity_value}")

                    if is_valid_data(test_case["Discount Percentage Amount"]):
                        discount_percentage_value = (
                            (str(test_case["Discount Percentage Amount"]).strip().replace(".0", "")
                        ))

                        cm.clickElement(
                            "PrivateOfferRequest",
                            "discount_Percentage_Amount_Input",
                        )
                        logger.info("Clicked on Discount Percentage Amount Field")
                        cm.enterText(
                            "PrivateOfferRequest",
                            "discount_Percentage_Amount_Input",
                            discount_percentage_value,
                        )
                        logger.info(
                            f"Entered Discount Percentage Amount: {discount_percentage_value}"
                        )

                    if is_valid_data(test_case["Total Discounted Price"]):
                        total_discounted_price_value = (
                            (str(test_case["Total Discounted Price"]).strip().replace(".0", "")
                        ))

                        cm.clickElement(
                            "PrivateOfferRequest",
                            "total_Discounted_Price_Input",
                        )
                        logger.info("Clicked on Total Discounted Price Field")
                        cm.enterText(
                            "PrivateOfferRequest",
                            "total_Discounted_Price_Input",
                            total_discounted_price_value,
                        )
                        logger.info(
                            f"Entered Total Discounted Price: {total_discounted_price_value}"
                        )

                    if is_valid_data(test_case["UoM"]):
                        uom_value = (test_case["UoM"]).strip()

                        cm.clickElement("PrivateOfferRequest", "uom_Dropdown")
                        logger.info("Clicked on UOM Selection Field")
                        cm.clickByText(uom_value)
                        logger.info(f"Selected UoM: {uom_value}")

                    cm.clickElement("PrivateOfferRequest", "dimension_Save_Button")
                    logger.info("Dimension saved successfully")

                # ========================== Approval Flow =============================================================
                if test_case["Approval"].strip().lower() == "yes":
    
                    cm.clickElement("PrivateOfferRequest", "submit_For_Approval_Button")
                    logger.info("Clicked Submit for Approval button")

                    cm.waitForStable(5)
                    cm.clickElement("PrivateOfferRequest", "submit_Button")
                    logger.info("Clicked Submit button on confirmation popup")
                    cm.waitForStable(3)
                    if is_valid_data(test_case["Private Offer Status After Submit"]):
                        expected_status_after_submit = str(
                            test_case["Private Offer Status After Submit"]
                        ).strip()

                        actual_status_after_submit = cm.readText(
                            "PrivateOfferRequest",
                            "private_Offer_Request_Status_Value",
                        )

                        logger.info(
                            f"Captured Private Offer Request Status after submit: "
                            f"{actual_status_after_submit}"
                        )

                        status_after_submit_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_status_after_submit,
                        expected_text=expected_status_after_submit,
                        )

                        if not status_after_submit_validation:
                            failure_message = (
                                f"Private Offer Request Status After Submit Validation Failed: "
                                f"Expected '{expected_status_after_submit}' but got "
                                f"'{actual_status_after_submit}'"
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual Private Offer Request Status after submit: "
                                f"{actual_status_after_submit} with expected Private Offer Request Status "
                                f"after submit: {expected_status_after_submit}"
                            )
                            print(
                                f"\033[92m✅ Compared actual Private Offer Request Status after submit: "
                                f"{actual_status_after_submit} with expected Private Offer Request Status "
                                f"after submit: {expected_status_after_submit}\033[0m"
                            )

                    cm.mouseWheelToBottom(800, scrolls=8, wait_time=0)
                    # ====================== Try Approval Before Final Unit Price ======================================
                    if is_valid_data(test_case["Marketplace Operations Status"]):
                        marketplace_operations_status = (
                            test_case["Marketplace Operations Status"]
                        ).strip()

                        cm.clickElement(
                            "PrivateOfferRequest",
                            "marketplace_Operations_Status_Edit_Icon",
                        )
                        logger.info("Clicked Marketplace Operations Status edit icon")

                        cm.clickElement("PrivateOfferRequest",
                                        "marketplace_Operations_Status_Dropdown",)
                        logger.info("Clicked Marketplace Operations Status Drop Down icon")

                        cm.clickByText(marketplace_operations_status)
                        logger.info(
                            f"Selected Marketplace Operations Status: "
                            f"{marketplace_operations_status}"
                        )

                        cm.clickElement("PrivateOfferRequest", "save_Button")
                        logger.info(
                            "Clicked Save button after selecting Marketplace Operations Status"
                        )

                    # ====================== Verify Final Unit Price Error Message =====================================
                    if is_valid_data(test_case["Final Unit Price Error Message"]):
                        expected_marketplace_error = (
                            test_case["Final Unit Price Error Message"]
                        ).strip()

                        actual_marketplace_error = cm.readText(
                            "PrivateOfferRequest",
                            "final_Unit_Price_Error_Message",
                        )

                        logger.info(
                            f"Captured Final Unit Price Error Message: "
                            f"{actual_marketplace_error}"
                        )

                        final_unit_price_error_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_marketplace_error,
                        expected_text=expected_marketplace_error,
                        )

                        if not final_unit_price_error_validation:
                            failure_message = (
                                f"Final Unit Price Error Message Validation Failed: "
                                f"Expected '{expected_marketplace_error}' but got "
                                f"'{actual_marketplace_error}'"
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual Final Unit Price Error Message: "
                                f"{actual_marketplace_error} with expected Final Unit Price Error Message: "
                                f"{expected_marketplace_error}"
                            )
                            print(
                                f"\033[92m✅ Compared actual Final Unit Price Error Message: "
                                f"{actual_marketplace_error} with expected Final Unit Price Error Message: "
                                f"{expected_marketplace_error}\033[0m"
                            )

                        cm.clickElement("PrivateOfferRequest", "cancel_Button")
                        logger.info("Clicked Cancel button after validation error")
                    # ====================== Navigate to Dimension =====================================================
                    cm.clickElement("PrivateOfferRequest", "dimension_Record_Link")
                    logger.info("Clicked Dimension record link from related list")

                    # ====================== Update Final Unit Price ===================================================
                    if is_valid_data(test_case["Final Unit Price"]):
                        final_unit_price = (
                            str(test_case["Final Unit Price"]).strip().replace(".0", "")
                        )

                        cm.clickElement("PrivateOfferRequest", "final_Unit_Price_Edit_Icon")
                        logger.info("Clicked Final Unit Price edit icon")

                        cm.clickElement("PrivateOfferRequest", "final_Unit_Price_Input")
                        logger.info("Clicked Final Unit Price input field")

                        cm.enterText(
                            "PrivateOfferRequest",
                            "final_Unit_Price_Input",
                            final_unit_price,
                        )
                        logger.info(f"Entered Final Unit Price: {final_unit_price}")

                        cm.clickElement("PrivateOfferRequest", "save_Button")
                        logger.info("Clicked Save button after updating Final Unit Price")

                    # ====================== Navigate Back to Private Offer Request ====================================
                    cm.navigateToUrl(private_offer_request_url)
                    logger.info(
                        f"Navigated back to Private Offer Request URL: "
                        f"{private_offer_request_url}"
                    )
                    cm.waitForStable(3)
                    cm.mouseWheelToBottom(800, scrolls=8, wait_time=0)
                     # ====================== Try Approval AFter Final Unit Price ======================================
                    if is_valid_data(test_case["Marketplace Operations Status"]):
                        marketplace_operations_status = (
                            test_case["Marketplace Operations Status"]
                        ).strip()

                        cm.clickElement(
                            "PrivateOfferRequest",
                            "marketplace_Operations_Status_Edit_Icon",
                        )
                        logger.info("Clicked Marketplace Operations Status edit icon")

                        cm.clickElement("PrivateOfferRequest",
                                        "marketplace_Operations_Status_Dropdown",)
                        logger.info("Clicked Marketplace Operations Status Drop Down icon")

                        cm.clickByText(marketplace_operations_status)
                        logger.info(
                            f"Selected Marketplace Operations Status: "
                            f"{marketplace_operations_status}"
                        )

                        cm.clickElement("PrivateOfferRequest", "save_Button")
                        logger.info(
                            "Clicked Save button after selecting Marketplace Operations Status"
                        )
                        cm.waitForStable(3)
                    # ====================== Manual Offer Details Section Update =======================================
                    if test_case["Manual Offer section Update"].strip().lower() == "yes":

                        cm.clickElement("PrivateOfferRequest", "manual_Offer_Name_Edit_Icon")
                        logger.info("Clicked Manual Offer Details edit icon")

                        if is_valid_data(test_case["Offer Name"]):
                            offer_name = (test_case["Offer Name"]).strip()

                            cm.clickElement("PrivateOfferRequest", "offer_Name_Input")
                            logger.info("Clicked Manual Offer Name Field")
                            cm.enterText("PrivateOfferRequest", "offer_Name_Input", offer_name)
                            logger.info(f"Entered Offer Name: {offer_name}")

                        if is_valid_data(test_case["Offer ID"]):
                            offer_id = str(
                            cm.generateRandomNumber(
                                min_value=10000,
                                max_value=99999))
                            logger.info(f"Generated random 5-digit Offer ID: {offer_id}")

                            cm.clickElement(
                                "PrivateOfferRequest",
                                "offer_ID_Input")
                            logger.info("Clicked Manual Offer ID Field")

                            cm.enterText(
                                "PrivateOfferRequest",
                                "offer_ID_Input",
                                offer_id)
                            logger.info(f"Entered Offer ID: {offer_id}")

                            print(f"\033[92m✅ Entered random Offer ID: {offer_id}\033[0m")
                        if is_valid_data(test_case["Offer URL"]):
                            offer_url = str(test_case["Offer URL"]).strip()

                            cm.clickElement("PrivateOfferRequest", "offer_URL_Input")
                            logger.info("Clicked Manual Offer URL Field")
                            cm.enterText("PrivateOfferRequest", "offer_URL_Input", offer_url)
                            logger.info(f"Entered Offer URL: {offer_url}")

                            offer_accepted_date = cm.generateDate(format="mm/dd/yyyy")
                            logger.info(f"Using generated Offer Accepted Date: {offer_accepted_date}")

                            cm.clickElement(
                                "PrivateOfferRequest",
                                "offer_Accepted_Date_Input",
                            )

                            cm.enterText(
                                "PrivateOfferRequest",
                                "offer_Accepted_Date_Input",
                                offer_accepted_date,
                            )

                            logger.info(f"Entered Offer Accepted Date: {offer_accepted_date}")
                            print(
                                f"\033[92m✅ Entered Offer Accepted Date: {offer_accepted_date}\033[0m"
                            )
                       
                        cm.waitForStable(2)
                        cm.clickElement("PrivateOfferRequest", "save_Button")
                        logger.info("Clicked Save button after updating Manual Offer Details")

                    # ====================== Verify Approved Locked Message ============================================
                    if is_valid_data(test_case["Approved Locked Message"]):
                        expected_approved_locked_message = str(
                            test_case["Approved Locked Message"]
                        ).strip()

                        actual_approved_locked_message = cm.readText(
                            "PrivateOfferRequest",
                            "approved_Locked_Message",
                        )

                        logger.info(
                            f"Captured Approved Locked Message: "
                            f"{actual_approved_locked_message}"
                        )

                        approved_locked_message_validation = cm.checkExpectedTextInActual(
                        actual_text=actual_approved_locked_message,
                        expected_text=expected_approved_locked_message,
                        )

                        if not approved_locked_message_validation:
                            failure_message = (
                                f"Approved Locked Message Validation Failed: "
                                f"Expected '{expected_approved_locked_message}' but got "
                                f"'{actual_approved_locked_message}'"
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual Approved Locked Message: "
                                f"{actual_approved_locked_message} with expected Approved Locked Message: "
                                f"{expected_approved_locked_message}"
                            )
                            print(
                                f"\033[92m✅ Compared actual Approved Locked Message: "
                                f"{actual_approved_locked_message} with expected Approved Locked Message: "
                                f"{expected_approved_locked_message}\033[0m"
                            )

            # ============================== Navigate Back to Opportunity ==============================================
                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Opportunity URL: {spark_url}")
                cm.waitForStable(5)
                cm.refreshPage()
                logger.info("Opportunity Page Refresh")
                cm.waitForStable(2)
            # ============================== Validate Opportunity Closed Message =======================================
            if is_valid_data(test_case["Expected Opportunity Closed Message"]):
                expected_closed_message = str(
                    test_case["Expected Opportunity Closed Message"]
                ).strip()

                actual_closed_message = cm.readText(
                    "OpportunityDetailPage",
                    "opportunity_Closed_Message",
                )

                logger.info(f"Captured Opportunity Closed Message: {actual_closed_message}")

                opportunity_closed_message_validation = cm.checkExpectedTextInActual(
                    actual_text=actual_closed_message,
                    expected_text=expected_closed_message,
                    )

                if not opportunity_closed_message_validation:
                    failure_message = (
                        f"Opportunity Closed Message Validation Failed: "
                        f"Expected '{expected_closed_message}' but got "
                        f"'{actual_closed_message}'"
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual Opportunity Closed Message: "
                        f"{actual_closed_message} with expected Opportunity Closed Message: "
                        f"{expected_closed_message}"
                    )
                    print(
                        f"\033[92m✅ Compared actual Opportunity Closed Message: "
                        f"{actual_closed_message} with expected Opportunity Closed Message: "
                        f"{expected_closed_message}\033[0m"
                    )
            # ============================== Validate Opportunity Stage ================================================
            if is_valid_data(test_case["Expected Opportunity Stage"]):
                expected_opportunity_stage = str(
                    test_case["Expected Opportunity Stage"]
                ).strip()

                actual_stage_visible = cm.isElementVisible(
                    "OpportunityDetailPage",
                    "opportunity_Stage_Closed_Won",
                )

                logger.info(
                    f"Opportunity Closed Won stage visible status: {actual_stage_visible}"
                )

                opportunity_stage_validation = cm.checkExpectedTextInActual(
                actual_text="Closed Won" if actual_stage_visible else "Not Visible",
                expected_text=expected_opportunity_stage,
                )

                if not opportunity_stage_validation:
                    failure_message = (
                        f"Opportunity Stage Validation Failed: "
                        f"Expected '{expected_opportunity_stage}' but got "
                        f"'{'Closed Won' if actual_stage_visible else 'Not Visible'}'. "
                        f"Closed Won Visible: '{actual_stage_visible}'"
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual Opportunity Stage: "
                        f"{'Closed Won' if actual_stage_visible else 'Not Visible'} "
                        f"with expected Opportunity Stage: {expected_opportunity_stage}"
                    )
                    print(
                        f"\033[92m✅ Compared actual Opportunity Stage: "
                        f"{'Closed Won' if actual_stage_visible else 'Not Visible'} "
                        f"with expected Opportunity Stage: {expected_opportunity_stage}\033[0m"
                    )

            # ============================== Click Opportunity Product ================================================
            if is_valid_data(test_case["Opportunity Product Name"]):
                opportunity_product_name = str(
                    test_case["Opportunity Product Name"]
                ).strip()

                cm.clickByText(opportunity_product_name)
                logger.info(f"Clicked Opportunity Product: {opportunity_product_name}")

            # ============================== Validate Sales Price ======================================================
            if is_valid_data(test_case["Expected Sales Price"]):

                expected_sales_price_raw = str(test_case["Expected Sales Price"]).strip()

                actual_sales_price_text = cm.readText(
                    "OpportunityDetailPage",
                    "opportunity_Product_Sales_Price",
                )
                logger.info(
                    f"Captured Opportunity Product Sales Price: {actual_sales_price_text}"
                )

                sales_price_validation = cm.checkExpectedTextInActual(
                actual_text=actual_sales_price_text,
                expected_text=expected_sales_price_raw,
                )

                if not sales_price_validation:
                    failure_message = (
                        f"Sales Price Validation Failed: "
                        f"Expected '{expected_sales_price_raw}' but got "
                        f"'{actual_sales_price_text}'"
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual Sales Price: {actual_sales_price_text} "
                        f"with expected Sales Price: {expected_sales_price_raw}"
                    )
                    print(
                        f"\033[92m✅ Compared actual Sales Price: "
                        f"{actual_sales_price_text} with expected Sales Price: "
                        f"{expected_sales_price_raw}\033[0m"
                    )
            # ============================== Validate Quantity / Capacity =============================================
            if is_valid_data(test_case["Expected Quantity"]):

                expected_quantity_raw = str(test_case["Expected Quantity"]).strip()

                actual_quantity_text = cm.readText(
                    "OpportunityDetailPage",
                    "opportunity_Product_Quantity",
                )

                logger.info(
                    f"Captured Opportunity Product Quantity/Capacity: {actual_quantity_text}"
                )
                quantity_validation = cm.checkExpectedTextInActual(
                actual_text=actual_quantity_text,
                expected_text=expected_quantity_raw,
                )

                if not quantity_validation:
                    failure_message = (
                        f"Quantity/Capacity Validation Failed: "
                        f"Expected '{expected_quantity_raw}' but got "
                        f"'{actual_quantity_text}'"
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual Quantity/Capacity: {actual_quantity_text} "
                        f"with expected Quantity/Capacity: {expected_quantity_raw}"
                    )
                    print(
                        f"\033[92m✅ Compared actual Quantity/Capacity: "
                        f"{actual_quantity_text} with expected Quantity/Capacity: "
                        f"{expected_quantity_raw}\033[0m"
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
