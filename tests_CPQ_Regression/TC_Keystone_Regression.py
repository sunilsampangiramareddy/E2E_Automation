from common_Methods.Common_Methods import CommonMethods
from common_Validations.Common_Validations import CommonValidations
from pages_CPQ.Products_Page import ProductsPage
from pages_Keystone.HomePage_Keystone import HomePageKeystone
import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_GTC.HomePage_GTC import HomePageGTC
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_FAS_AFF_ASA_AFX.HomePage_FAS_AFF_ASA_AFX import HomePageFAS_AFF_ASA_AFX
from pages_EAndEF_Series.HomePage_EAndEF_Series import HomePageEAndEFSeries
from pages_CPQ.Quote_Info_Page import QuoteInfoPage
from pages_CPQ.Account_Information_Page import AccountInformationPage
from pages_CPQ.Approval_Request_Page import ApprovalRequestPage
from pages_CPQ.Attachments_Page import AttachmentsPage
from pages_CPQ.Purchase_Order_Page import PurchaseOrderPage
from pages_TPD.TPD_Home_Page import TPDHomePage
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Regression test for Keystone product
# Test Description:
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_Keystone_Regression.xlsx")
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
def test_Keystone_Regression(page: Page, base_url, config, test_case) -> None:  # type: ignore
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
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
                f"***{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}***"
            )

            if is_valid_data(test_case["User Name"]):
                cm.enterText("LoginPage", "username_Input", test_case["User Name"])
                logger.info(f"Username entered: {test_case['User Name']}")
                # lp.enterUserName(config.get_username())
                # logger.info("Username entered")

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
            ss.capture_screenshot("Captured Homepage details")

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
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "primary_Contact",
                                    test_case["Primary Contact"],
                                )
                                logger.info(
                                    f"Selected primary contact: {test_case['Primary Contact']}"
                                )
                            if is_valid_data(test_case["Sales Play"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Play",
                                    test_case["Sales Play"],
                                )
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
                                ss.capture_screenshot(
                                    "Captured Create Opportunity details"
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
                        """
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

                        if (
                            test_case["Channel"] == direct_Oppty
                            or test_case["Opportunity Type"] == x1p_Oppty
                        ):
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")
                        """
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

                        oppty_name = cm.readText(
                            "CreateOpportunity", "opportunity_Name"
                        )
                        logger.info(f"Opportunity Name: {oppty_name}")

                    spark_url = cm.getCurrentURL()
                    logger.info(f"Captured Spark URL: {spark_url}")

            # ========================Add Product in SFDC=====================================================================================
            if test_case["Add Products"].strip().lower() == "yes":
                if is_valid_data(test_case["Product Name"]):
                    hp.selectProduct(test_case["Product Name"])
                    logger.info(f"Selected product: {test_case['Product Name']}")

                if is_valid_data(test_case["Product Price"]):
                    hp.enterProductPrice(test_case["Product Price"])
                    ss.capture_screenshot("Captured Product in SFDC Details")
                    logger.info(f"Entered product price: {test_case['Product Price']}")

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")

            # =========================Create Quote============================================================================================
            if test_case["Create Quote"].strip().lower() == "yes":

                hp.createQuote()
                logger.info(f"Clicked on create quote")

                new_tab = cm.switchToTab(
                    page.context, tab_index=1, expected_tab_count=2
                )
                logger.info(
                    "Switched to the new tab after clicking on Create Quote option"
                )

                # Create an instance of HomePageCPQ for the new tab
                hpc = HomePageCPQ(new_tab)
                logger.info(f"HomePageCPQ instance created for the new tab")
                ss = ScreenshotUtil(new_tab)
                logger.info(f"ScreenshotUtil instance created for the new tab")
                hp = HomePage(new_tab)
                logger.info(f"HomePage instance created for the new tab")
                cm = CommonMethods(new_tab, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")
                qip = QuoteInfoPage(new_tab)
                logger.info(f"QuoteInfoPage instance created for the new tab")

                if is_valid_data(test_case["Keystone"]):
                    qip.enterKeystone(test_case["Keystone"])
                    logger.info(f"Entered keystone: {test_case['Keystone']}")

                cm.clickElementAndWait(
                    page_name="QuoteInfoPage",
                    element_name="save_Button",
                    wait_time=5,
                )
                logger.info(f"Clicked on save button")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=20000)
                ss.capture_screenshot("Captured Quote details")

            # =============================Capture Quote Details==============================================================================
            # Perform actions on the new tab
            if test_case["Capture Quote Details"].strip().lower() == "yes":
                quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                logger.info(f"Quote Number: {quote_number}")

                quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                logger.info(f"Quote Name: {quote_name}")

                cpq_url = cm.getCurrentURL()
                logger.info(f"CPQ URL: {cpq_url}")

                quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                ss.capture_screenshot("Captured Quote details")
                logger.info(f"Quote Status: {quote_status}")

                quote_status = cm.verifyElementStatus(
                    "HomePage_CPQ", "quote_Status", "Draft"
                )
                cm.assertTrue(
                    quote_status,
                    f"Quote status is not in expected state: Expected 'Draft', but found something else: {quote_status}",
                )
                logger.info(
                    f"Verified quote status is in expected state Draft: {quote_status}"
                )

            # ====================Configure Keystone Product =================================================================================
            pp = ProductsPage(new_tab)
            logger.info(f"ProductsPage instance created for the new tab")
            kp = HomePageKeystone(new_tab)
            logger.info(f"Keystone Page instance created for the new tab")
            cv = CommonValidations(new_tab)
            logger.info(f"CommonValidations instance created for the new tab")

            if test_case["Configure Product"].strip().lower() == "yes":

                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                cm.clickElement("ProductsPage", "configure_Button")
                logger.info(f"Clicked on Configure button")

                if is_valid_data(test_case["Product"]):
                    kp.click_ProductName(test_case["Product"])
                    logger.info(f"Clicked on product: {test_case['Product']}")

                if is_valid_data(test_case["Sub Product"]):
                    kp.select_SubProduct(test_case["Sub Product"])
                    logger.info(f"Clicked on sub product: {test_case['Sub Product']}")

                if test_case["Keystone Services"].strip().lower() == "yes":
                    kp.clickKeystoneServicesTab()
                    logger.info(f"Clicked on Keystone Services tab")

                    if is_valid_data(test_case["Data Type"]):
                        kp.selectDataType(test_case["Data Type"])
                        logger.info(f"Selected data type: {test_case['Data Type']}")

                    if is_valid_data(test_case["Service Level"]):
                        kp.selectServiceLevel(test_case["Service Level"])
                        logger.info(
                            f"Selected service level: {test_case['Service Level']}"
                        )

                    if is_valid_data(test_case["Total Capacity Committed"]):
                        kp.enterTotalCapacityCommitted(
                            test_case["Total Capacity Committed"]
                        )
                        logger.info(
                            f"Entered total capacity committed: {test_case['Total Capacity Committed']}"
                        )
                    # =============Reading BOM table details and saving to list=================================================================================
                    if test_case["BOM Validation"].strip().lower() == "yes":
                        cm.clickElementAndWait(
                            page_name="ConfigurePage",
                            element_name="bill_Of_Materials",
                            wait_time=5,
                        )
                        logger.info(f"Clicked on Bill of Materials tab")

                        bom_list_part_number = cv.readBOMTable_SaveToList("Part Number")
                        logger.info(f"Read the BOM table details for Part Number")

                        bom_list_quantity = cv.readBOMTable_SaveToList("Quantity")
                        logger.info(f"Read the BOM table details for Quantity")

                        bom_list_description = cv.readBOMTable_SaveToList("Description")
                        logger.info(f"Read the BOM table details for Description")

                        cm.clickElement("ConfigurePage", "close_Button")
                        logger.info(f"Clicked on Close button in BOM table")
                    # =========================================================================================================================

                cm.clickElement("ConfigurePage", "add_To_Quote")
                ss.capture_screenshot("Captured Product configuration details")
                logger.info(f"Clicked on Add to Quote button")

                kp.selectTargetReadinessDate()
                logger.info(f"Selected target readiness date")

                kp.selectTarget_StartDate()
                logger.info(f"Selected target start date")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

            # =============================Read LIG Product Table===============================================================================
            if test_case["Capture LIG Table Details"].strip().lower() == "yes":
                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                pp.expandAllProducts()
                logger.info(f"Expanded all products in the LIG product table")

                hpc.readProductTable(new_tab, "Product")
                logger.info(f"Reading Product column values from product LIG table")

                hpc.readProductTable(new_tab, "List Price")
                logger.info(f"Reading List Price column values from product LIG table")

                hpc.readProductTable(new_tab, "Net Price")
                logger.info(f"Reading Net Price column values from product LIG table")

                # ==================Reading Product table details and saving to list=================================================================================
                if test_case["BOM Validation"].strip().lower() == "yes":
                    product_list_product = cv.readProductTable_SaveToList("Product")
                    logger.info(f"Read Product column values from product LIG table")

                    product_list_qty = cv.readProductTable_SaveToList("Qty")
                    logger.info(f"Read Quantity column values from product LIG table")

                    product_list_part_description = cv.readProductTable_SaveToList(
                        "Part Description"
                    )
                    logger.info(
                        f"Read Part Description column values from product LIG table"
                    )
                # ==========================================================================================================================

                pp.collapseAllProducts()
                logger.info(f"Collapsed all products in the LIG product table")

                hpc.verifyQuoteStatus("Configured")
                logger.info(f"Verified quote status is in expected state: Configured")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                ss.capture_screenshot("Captured LIG Product table details")
                logger.info(f"Clicked on Save button")

            # ========================================Compare BOM and Product Table Details=======================================================================
            if test_case["BOM Validation"].strip().lower() == "yes":
                # Compare BOM Part Numbers with Product Part Numbers
                errors = cv.compare_lists(bom_list_part_number, product_list_product)
                if errors:
                    logger.warning(
                        "Mismatch found during Part Number comparison:\n"
                        + "\n".join(errors)
                    )
                else:
                    logger.info("Part Number comparison passed successfully!")

                # Compare BOM Quantities with Product Quantities
                errors += cv.compare_lists(bom_list_quantity, product_list_qty)
                if errors:
                    logger.warning(
                        "Mismatch found during Quantity comparison:\n"
                        + "\n".join(errors)
                    )
                else:
                    logger.info("Quantity comparison passed successfully!")

                # Compare BOM Descriptions with Product Descriptions
                errors += cv.compare_lists(
                    bom_list_description, product_list_part_description
                )
                if errors:
                    logger.warning(
                        "Mismatch found during Description comparison:\n"
                        + "\n".join(errors)
                    )
                else:
                    logger.info("Description comparison passed successfully!")

                # Final result logging
                if errors:
                    logger.warning(
                        "The following mismatches were found:\n" + "\n".join(errors)
                    )
                    boolean_status = "Fail"
                else:
                    print(
                        "BOM table and Product table values have been verified successfully!"
                    )
                    logger.info(
                        "BOM table and Product table values have been verified successfully!"
                    )

                # ==================Checking value presence in BOM Part Number list==========================================
                if test_case["BOM Validation"].strip().lower() == "yes":
                    if is_valid_data(test_case["BOM Part Number"]):
                        # Check if the text is present in the BOM Part Number list
                        is_present = cv.is_value_present_in_list(
                            test_case["BOM Part Number"],
                            bom_list_part_number,
                            "Part Number",
                        )
                        if is_present:
                            print(
                                f"'{test_case['BOM Part Number']}' is present in the BOM Part Number list."
                            )
                            logger.info(
                                f"'{test_case['BOM Part Number']}' is present in the BOM Part Number list."
                            )
                        else:
                            print(
                                f"'{test_case['BOM Part Number']}' is NOT present in the BOM Part Number list."
                            )
                            logger.warning(
                                f"'{test_case['BOM Part Number']}' is NOT present in the BOM Part Number list."
                            )
                # =============================================================================================================

            # ==================Keystone Internal Hardware Quotes Error Message Validation========================================================
            ar = ApprovalRequestPage(new_tab)
            logger.info(f"ApprovalRequestPage instance created for the new tab")

            if test_case["Error Validation"].strip().lower() == "yes":
                if test_case["Initiate Approval"].strip().lower() == "yes":
                    cm.clickElementAndWait(
                        page_name="ApprovalRequestPage",
                        element_name="initiate_Approval",
                        wait_time=10,
                    )
                    ss.capture_screenshot("Captured Approval Tab details")
                    logger.info(f"Clicked on Initiate Approval button")

                cm.clickElement("HomePage_CPQ", "view_More_Link")
                logger.info(f"Clicked on View more link in Quote info section")

                actual_error_message = cm.readText("HomePage_CPQ", "error_Message")
                logger.info(f"Captured error message: {actual_error_message}")

                if is_valid_data(
                    test_case["Keystone Internal Hardware Quotes Error Message"]
                ):
                    cm.compareExpectedActualText(
                        actual_text=actual_error_message,
                        expected_text=test_case[
                            "Keystone Internal Hardware Quotes Error Message"
                        ],
                    )
                    logger.info(
                        f"Compared actual error message: {actual_error_message} with expected error message: {test_case['Keystone Internal Hardware Quotes Error Message']}"
                    )

                cm.clickElement("HomePage_CPQ", "close_Button")
                logger.info(f"Clicked on Close button in Home Page CPQ")

            # ==================Products Tab-Enter Keystone Internal Hardware Quotes========================================================
            if test_case["Add Internal Hardware Quote"].strip().lower() == "yes":

                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                cm.enterText(
                    "ProductsPage", "keystone_Internal_HardwareQuotes", quote_number
                )
                logger.info(
                    f"Entered Keystone Internal Hardware Quotes: {quote_number}"
                )

                cm.clickElementAndWait(
                    page_name="ProductsPage",
                    element_name="link_Hardware_Quote",
                    wait_time=5,
                )

            # ===============================Account Information Tab=================================================================================
            aip = AccountInformationPage(new_tab)
            logger.info(f"AccountInformationPage instance created for the new tab")

            if test_case["Add Account Information"].strip().lower() == "yes":
                cm.clickElement("AccountInformationPage", "account_Information_Tab")
                logger.info(f"Clicked on Account Information Tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                # Optionally closing the error message pop-up if it appears after saving the quote info details
                cm.clickElement("HomePage_CPQ", "close_Button")
                logger.info(f"Clicked on Close button in Home Page CPQ")

                if test_case["Sold To"].strip().lower() == "yes":
                    if is_valid_data(test_case["First Name_Sold To"]):
                        aip.enterSoldTo(
                            test_case["First Name_Sold To"],
                            test_case["Last Name_Sold To"],
                        )
                        logger.info(
                            f"Entered Sold To details: {test_case['First Name_Sold To']}, {test_case['Last Name_Sold To']}"
                        )

                if test_case["Bill To"].strip().lower() == "yes":
                    aip.enterBillTo()
                    logger.info(f"Entered Bill To details")

                if test_case["End Customer"].strip().lower() == "yes":
                    if is_valid_data(test_case["First Name_End Customer"]):
                        aip.enterEndCustomer(
                            test_case["First Name_End Customer"],
                            test_case["Last Name_End Customer"],
                        )
                        logger.info(
                            f"Entered End Customer details: {test_case['First Name_End Customer']}, {test_case['Last Name_End Customer']}"
                        )

                if test_case["Service Customer"].strip().lower() == "yes":
                    aip.enterServiceCustomer()
                    logger.info(f"Entered Service Customer details")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                ss.capture_screenshot("Captured Account Information details")
                logger.info(f"Clicked on Save button")

            # =======================================Approval Request Tab=================================================================================
            ar = ApprovalRequestPage(new_tab)
            logger.info(f"ApprovalRequestPage instance created for the new tab")

            if test_case["Initiate Approval"].strip().lower() == "yes":
                cm.clickElement("ApprovalRequestPage", "approval_Request_Tab")
                logger.info(f"Clicked on Approval request tab")

                cm.clickElementAndWait(
                    page_name="ApprovalRequestPage",
                    element_name="initiate_Approval",
                    wait_time=10,
                )
                logger.info(f"Clicked on Initiate Approval button")
                ss.capture_screenshot("Captured Approval Tab details")

                quote_status = cm.verifyElementStatus(
                    "HomePage_CPQ", "quote_Status", "Orderable"
                )
                cm.assertTrue(
                    quote_status,
                    f"Quote status is not in expected state: Expected 'Orderable', but found something else: {quote_status}",
                )
                logger.info(
                    f"Verified quote status is in expected state Orderable: {quote_status}"
                )

            # ======================================Attachments Tab=================================================================================
            ap = AttachmentsPage(new_tab)
            logger.info(f"AttachmentsPage instance created for the new tab")

            if test_case["Add Attachment"].strip().lower() == "yes":
                cm.clickElement("AttachmentsPage", "attachments_Tab")
                logger.info(f"Clicked on Attachments tab")

                ap.selectDragAndDrop()
                logger.info(f"Selected file to upload")

                if is_valid_data(test_case["Attachment Type"]):
                    ap.selectAttachmentType(test_case["Attachment Type"])
                    logger.info(
                        f"Selected attachment type: {test_case['Attachment Type']}"
                    )

                if is_valid_data(test_case["Attachment Description"]):
                    ap.enterAttachmentDescription(test_case["Attachment Description"])
                    logger.info(
                        f"Entered attachment description: {test_case['Attachment Description']}"
                    )

                cm.clickElement("AttachmentsPage", "upload_Button")
                logger.info(f"Clicked on upload button")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")
                ss.capture_screenshot("Captured Attachment Tab details")

            # ==============================Purchase Order Tab=================================================================================
            po = PurchaseOrderPage(new_tab)
            logger.info(f"PurchaseOrderPage instance created for the new tab")

            if test_case["Submit PO"].strip().lower() == "yes":
                cm.clickElement("PurchaseOrderPage", "purchase_Order_Tab")
                logger.info(f"Clicked on Purchase order tab")

                cm.enterTextAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="purchase_Order_Number",
                    text=quote_number,
                    wait_time=3,
                )
                logger.info(f"Entered PO number: {quote_number}")

                po.enterPODate()
                logger.info(f"Entered PO date")

                if is_valid_data(test_case["PO Email"]):
                    cm.enterText("PurchaseOrderPage", "po_Email", test_case["PO Email"])
                    logger.info(f"Entered PO email: {test_case['PO Email']}")

                if is_valid_data(test_case["PO Comments"]):
                    cm.enterText(
                        "PurchaseOrderPage", "po_Comments", test_case["PO Comments"]
                    )
                    logger.info(f"Entered PO comments: {test_case['PO Comments']}")

                cm.clickElementAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="submit_PO_Button",
                    wait_time=20,
                )
                logger.info(f"Clicked on Submit PO button")

                quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                logger.info(f"Quote Status: {quote_status}")
                ss.capture_screenshot("Captured PO submission quote status")

                quote_status = cm.verifyElementStatus(
                    "HomePage_CPQ", "quote_Status", "PO Submitted"
                )
                cm.assertTrue(
                    quote_status,
                    f"Quote status is not in expected state: Expected 'PO Submitted', but found something else: {quote_status}",
                )
                logger.info(
                    f"Verified quote status is in expected state PO Submitted: {quote_status}"
                )

            # ======================================TPD=========================================================================================
            thp = TPDHomePage(new_tab)
            logger.info(f"TPDHomePage instance created for the new tab")

            if test_case["Accept in TPD"].strip().lower() == "yes":
                if is_valid_data(test_case["TPD URL"]):
                    cm.navigateToUrl(test_case["TPD URL"])
                    logger.info(f"Navigated to TPD URL: {test_case['TPD URL']}")

                cm.clickElement("HomePage_TPD", "global_Search")
                logger.info(f"Clicked on global search")

                cm.enterText("HomePage_TPD", "transaction_Number", quote_number)
                logger.info(f"Searched by transaction number: {quote_number}")

                cm.enterText("HomePage_TPD", "po_Number", quote_number)
                logger.info(f"Searched by PO number: {quote_number}")

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button")

                tpd_orderStatus = cm.readText("HomePage_TPD", "order_Status")
                logger.info(f"Captured order status: {tpd_orderStatus}")

                tpd_subProcessStatus = cm.readText("HomePage_TPD", "sub_Process_Status")
                logger.info(f"Captured subprocess status: {tpd_subProcessStatus}")

                if tpd_subProcessStatus.strip().lower() == "transaction review pending":
                    cm.clickElement("HomePage_TPD", "transaction_Review")
                    logger.info(f"Clicked on Transaction Review")

                if tpd_subProcessStatus.strip().lower() == "rpa review pending":
                    cm.clickElement("HomePage_TPD", "rpa_Review")
                    logger.info(f"Clicked on RPA Review")

                cm.enterText("HomePage_TPD", "transaction_Number", quote_number)
                logger.info(
                    f"Searched by transaction number in {tpd_subProcessStatus}: {quote_number}"
                )

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button in {tpd_subProcessStatus}")

                thp.clickSearchQuote(quote_number)
                logger.info(
                    f"Clicked on quote link in {tpd_subProcessStatus}: {quote_number}"
                )

                cm.selectOptionInListbox("HomePage_TPD", "actions_DD", "Accepted")
                logger.info(f"Selected Accepted from Actions dropdown")

                cm.clickElement("HomePage_TPD", "actions_Go_Button")
                logger.info(f"Clicked on Actions Go button")

                cm.clickElement("HomePage_TPD", "yes_Button")
                logger.info(f"Clicked on Yes button in confirmation pop-up")
                ss.capture_screenshot("Captured TPD details")

            # =========================================Capture Test Result and Write To Excel================================================
            test_results = [
                [
                    "Test Case ID",
                    "Quote Number",
                    "Quote Name",
                    "Quote Status",
                    "Execution Status",
                    "Details",
                ],
                [
                    script_name,
                    quote_number,
                    quote_name,
                    quote_status,
                    boolean_status,
                    "PO Submitted Quote Successfully",
                ],
            ]
            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)
            logger.info(
                f"***{script_name} Test Script Execution Completed Successfully***"
            )
        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']}"
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
