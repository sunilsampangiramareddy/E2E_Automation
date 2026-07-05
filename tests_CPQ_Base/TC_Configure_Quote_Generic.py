from pages_CPQ.Products_Page import ProductsPage
import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_GTC.HomePage_GTC import HomePageGTC
from common_Methods.Common_Methods import CommonMethods
from common_Validations.Common_Validations import CommonValidations
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_FAS_AFF_ASA_AFX.HomePage_FAS_AFF_ASA_AFX import HomePageFAS_AFF_ASA_AFX
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
# Test Scenario: Verify that a user can configure FAS/AFF/ASA/AFX clusters product(AFF-A20), submit a quote and approve
#                the quote in TPD using Generic Methods.
# Test Description: This test script automates the process of logging into Salesforce, creating an Diret opportunity,
#                   configuring FAS/AFF/ASA/AFX clusters product(AFF-A20), updating its details in the Account Information
#                   ,GTC Risks, Approval Request, Attachments, and Purchase Order tabs and validating the quote status
#                   by approving the quote in TPD.
# Author: Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_Configure_Quote_Generic.xlsx")
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
def test_Configure_Quote_Generic(page: Page, base_url, config, test_case) -> None:
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
        # =================================Login to SFDC==========================================================================
        page.goto(base_url)
        logger.info(f"Launching application URL: {base_url}")
        logger.info(f"***{script_name} Test Script Execution Started***")

        if is_valid_data(test_case["User Name"]):
            cm.enterText("LoginPage", "username_Input", test_case["User Name"])
            logger.info(f"Username entered: {test_case['User Name']}")

        cm.clickElement("LoginPage", "next_Button")
        logger.info(f"Clicked on next button")

        # lp.enterPassword(os.getenv("PASSWORD"))
        cm.enterText("LoginPage", "password_Input", config.get_encodedString())
        logger.info(f"Entered password")

        cm.clickElement("LoginPage", "signin_Button")
        logger.info(f"Signin button clicked")

        cm.clickElement("LoginPage", "yes_Button")
        logger.info(f"Yes button clicked")

        is_visible = cm.isElementVisible("HomePage", "opportunities_Label")
        cm.assertTrue(is_visible, "Opportunities label is not visible on the homepage")
        logger.info(
            f"Opportunities label has been verified on the homepage: {is_visible}"
        )
        ss.capture_screenshot("Captured Homepage details")

        # =======================Create Opportunity===========================================================================
        cm.clickElement("HomePage", "opportunities_Tab")
        logger.info(f"Clicked on opportunities tab")

        cm.clickElement("HomePage", "new_Opportunity_Button")
        logger.info(f"Clicked on new opportunity button")

        if is_valid_data(test_case["Account Name"]):
            co.enterAccount(test_case["Account Name"])
            logger.info(f"Entered and selected account: {test_case['Account Name']}")

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
                    logger.info(f"Selected sales play: {test_case['Sales Play']}")
                if is_valid_data(test_case["Channel"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "channel",
                        test_case["Channel"],
                    )
                    logger.info(f"Selected channel: {test_case['Channel']}")

            if test_case["Opportunity Type"] == x1p_Oppty:
                if is_valid_data(test_case["Opportunity Name"]):
                    co.enterOpportunityName_1p(test_case["Opportunity Name"])
                    logger.info(f"Entered opportunity name")
                if is_valid_data(test_case["Sales Type"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "sales_Type_1P",
                        test_case["Sales Type"],
                    )
                    logger.info(f"Selected 1P sales type: {test_case['Sales Type']}")
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
                    logger.info(f"Selected hyperscaler: {test_case['Hyperscaler']}")

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
                    logger.info(f"Selected sales type: {test_case['Sales Type']}")
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
                    ss.capture_screenshot("Captured Create Opportunity details")
                    logger.info(f"Selected currency: {test_case['Currency']}")
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
                    logger.info(f"Selected reseller SE: {test_case['Reseller SE']}")
                cm.clickElement("CreateOpportunity", "next_Button")
                logger.info(f"Clicked on next button")

            oppty_number = cm.readText("CreateOpportunity", "opportunity_Number")
            logger.info(f"Opportunity Number: {oppty_number}")

            oppty_name = cm.readText("CreateOpportunity", "opportunity_Name")
            logger.info(f"Opportunity Name: {oppty_name}")

        spark_url = cm.getCurrentURL()
        logger.info(f"Captured Spark URL: {spark_url}")

        # =======================Add Product in SFDC=================================================================================
        if is_valid_data(test_case["Product Name"]):
            hp.selectProduct(test_case["Product Name"])
            logger.info(f"Selected product: {test_case['Product Name']}")

        if is_valid_data(test_case["Product Price"]):
            hp.enterProductPrice(test_case["Product Price"])
            ss.capture_screenshot("Captured Product in SFDC Details")
            logger.info(f"Entered product price: {test_case['Product Price']}")

        cm.navigateToUrl(spark_url)
        logger.info(f"Navigated back to Spark URL: {spark_url}")

        # ========================Create Quote=======================================================================================
        hp.createQuote()
        logger.info(f"Clicked on create quote")

        new_tab = cm.switchToTab(page.context, tab_index=1, expected_tab_count=2)
        logger.info("Switched to the new tab after clicking on Create Quote option")

        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(new_tab)
        logger.info(f"HomePageCPQ instance created for the new tab")
        ss = ScreenshotUtil(new_tab)
        logger.info(f"ScreenshotUtil instance created for the new tab")
        hp = HomePage(new_tab)
        logger.info(f"HomePage instance created for the new tab")
        cm = CommonMethods(new_tab, locator_manager)
        logger.info(f"CommonMethods instance created for the new tab")

        cm.clickElementAndWait(
            page_name="QuoteInfoPage",
            element_name="save_Button",
            wait_time=5,
        )
        logger.info(f"Clicked on save button")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=20000)
        ss.capture_screenshot("Captured Quote details")

        # ============================Capture Quote Details==========================================================================
        # Perform actions on the new tab
        quote_number = cm.readText("HomePage_CPQ", "quote_Number")
        logger.info(f"Quote Number: {quote_number}")

        quote_name = cm.readText("HomePage_CPQ", "quote_Name")
        logger.info(f"Quote Name: {quote_name}")

        cpq_url = cm.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        quote_status = cm.readText("HomePage_CPQ", "quote_Status")
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")

        quote_status = cm.verifyElementStatus("HomePage_CPQ", "quote_Status", "Draft")
        cm.assertTrue(
            quote_status,
            f"Quote status is not in expected state: Expected 'Draft', but found something else: {quote_status}",
        )
        logger.info(f"Verified quote status is in expected state Draft: {quote_status}")

        # =============================Configure FAS/AFF/ASA/AFX Product================================================================
        pp = ProductsPage(new_tab)
        logger.info(f"ProductsPage instance created for the new tab")

        cm.clickElement("ProductsPage", "products_Tab")
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

        cm.clickElement("ProductsPage", "configure_Button")
        logger.info(f"Clicked on Configure button")

        hpFAS = HomePageFAS_AFF_ASA_AFX(new_tab)
        logger.info(f"HomePageFAS_AFF_ASA_AFX instance created for the new tab")

        if is_valid_data(test_case["Product"]):
            hpFAS.clickProductName(test_case["Product"])
            logger.info(f"Clicked on product: {test_case['Product']}")

        if is_valid_data(test_case["Sub Product"]):
            hpFAS.selectSubProduct(test_case["Sub Product"])
            logger.info(f"Clicked on sub-product: {test_case['Sub Product']}")

        if is_valid_data(test_case["Cluster"]):
            hpFAS.configureCluster(test_case["Cluster"])
            logger.info(f"Clicked on cluster: {test_case['Cluster']}")

        hpFAS.access_SelectAll()
        logger.info(f"Accessed select all option under access tab")

        if is_valid_data(test_case["Model"]):
            hpFAS.selectSystemModel(test_case["Model"])
            logger.info(f"Selected Model: {test_case['Model']}")

        hpFAS.clickAddHaPair()
        logger.info(f"Clicked on Add HA Pair button")

        hpFAS.clickConfigureButton()
        logger.info(f"Clicked on configure button")

        hpFAS.clickStorageTab()
        logger.info(f"Clicked on storage tab")

        if is_valid_data(test_case["Drive Type_Base Storage"]):
            hpFAS.selectDriveType_BaseStorage(test_case["Drive Type_Base Storage"])
            logger.info(f"Selected drive type: {test_case['Drive Type_Base Storage']}")

        if is_valid_data(test_case["Drive Pack Qty_Base Storage"]):
            hpFAS.enterDrivePackQty_BaseStorage(
                test_case["Drive Pack Qty_Base Storage"]
            )
            logger.info(
                f"Selected drive pack qty: {test_case['Drive Pack Qty_Base Storage']}"
            )

        hpFAS.clickTabNICsandAdapters()
        logger.info(f"Clicked on Nics and Adapters tab")

        if is_valid_data(test_case["Cable Type_Adapters"]):
            hpFAS.selectCableType_Adapters(test_case["Cable Type_Adapters"])
            logger.info(f"Selected cable type: {test_case['Cable Type_Adapters']}")

        if is_valid_data(test_case["Cable Length_Adapters"]):
            hpFAS.selectCableLength_Adapters(test_case["Cable Length_Adapters"])
            logger.info(f"Selected cable length: {test_case['Cable Length_Adapters']}")

        hpFAS.clickBackToClusterManager()
        logger.info(f"Clicked on Back to Cluster manager button")

        hpFAS.clickServicesTab()
        logger.info(f"Clicked on Services tab")

        hpFAS.clickIsThisATechRefresh()
        logger.info(f"Clicked No button for Is this a tech refresh")

        hpFAS.clickDoesYourCustomerRequireBlueXP()
        logger.info(
            f"Clicked No button for Does your Customer require BlueXP to be deployed by the Professional Services Team"
        )

        hpFAS.clickDoesYourCustomerNeedPSONTAP()
        logger.info(
            f"Clicked No button for Does your Customer need PS to fully design and configure their ONTAP system"
        )

        hpFAS.clickDoYouWantToAddRansomwareRecoveryAssurance()
        logger.info(
            f"Clicked No button for Do you want to add the Ransomware Recovery Assurance Service"
        )

        hpFAS.clickAddToQuote()
        logger.info(f"Clicked on Add to Quote button")
        ss.capture_screenshot("Captured Product configuration details")

        # =============================Read LIG Product Table=========================================================================
        cm.clickElement("ProductsPage", "products_Tab")
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

        pp.expandAllProducts()
        logger.info(f"Expanded all products in the LIG product table")

        hpc.readProductTable(new_tab, "Product")
        logger.info(f"Completed reading Product column values from LIG table")

        hpc.readProductTable(new_tab, "Part Description")
        logger.info(f"Completed reading Part Description column values from LIG table")

        hpc.readProductTable(new_tab, "Qty")
        logger.info(f"Completed reading Qty column values from LIG table")

        hpc.readProductTable(new_tab, "Ext Qty")
        logger.info(f"Completed reading Ext Qty column values from LIG table")

        hpc.readProductTable(new_tab, "List Price")
        logger.info(f"Completed reading List Price column values from LIG table")

        hpc.readProductTable(new_tab, "Extended List Price")
        logger.info(
            f"Completed reading Extended List Price column values from LIG table"
        )

        hpc.readProductTable(new_tab, "Treshold Group")
        logger.info(f"Completed reading Treshold Group column values from LIG table")

        hpc.readProductTable(new_tab, "Eligible Discount Source")
        logger.info(
            f"Completed reading Eligible Discount Source column values from LIG table"
        )

        hpc.readProductTable(new_tab, "Eligible Discount")
        logger.info(f"Completed reading Eligible Discount column values from LIG table")

        hpc.readProductTable(new_tab, "Current Discount")
        logger.info(f"Completed reading Current Discount column values from LIG table")

        hpc.readProductTable(new_tab, "Net Price")
        logger.info(f"Completed reading Net Price column values from LIG table")

        hpc.readProductTable(new_tab, "Extended Net Price")
        logger.info(
            f"Completed reading Extended Net Price column values from LIG table"
        )

        hpc.readProductTable(new_tab, "Serial Number")
        logger.info(f"Completed reading Serial Number column values from LIG table")

        hpc.readProductTable(new_tab, "Service Start Date")
        logger.info(
            f"Completed reading Service Start Date column values from LIG table"
        )

        hpc.readProductTable(new_tab, "Service End Date")
        logger.info(f"Completed reading Service End Date column values from LIG table")

        hpc.readProductTable(new_tab, "Service Duration")
        logger.info(f"Completed reading Service Duration column values from LIG table")

        pp.collapseAllProducts()
        logger.info(f"Collapsed all products in the LIG product table")

        quote_status = cm.verifyElementStatus(
            "HomePage_CPQ", "quote_Status", "Configured"
        )
        cm.assertTrue(
            quote_status,
            f"Quote status is not in expected state: Expected 'Configured', but found something else: {quote_status}",
        )
        logger.info(
            f"Verified quote status is in expected state Configured: {quote_status}"
        )

        cm.clickElementAndWait(
            page_name="HomePage_CPQ",
            element_name="save_Icon",
            wait_time=10,
        )
        logger.info(f"Clicked on Save button")
        ss.capture_screenshot("Captured LIG Product table details")

        # ==============================Account Information Tab=================================================================================
        aip = AccountInformationPage(new_tab)
        logger.info(f"AccountInformationPage instance created for the new tab")

        cm.clickElement("AccountInformationPage", "account_Information_Tab")
        logger.info(f"Clicked on Account Information Tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

        if is_valid_data(test_case["First Name_Sold To"]):
            aip.enterSoldTo(
                test_case["First Name_Sold To"], test_case["Last Name_Sold To"]
            )
            logger.info(
                f"Entered Sold To details: {test_case['First Name_Sold To']}, {test_case['Last Name_Sold To']}"
            )

        aip.enterBillTo()
        logger.info(f"Entered Bill To details")

        if is_valid_data(test_case["First Name_End Customer"]):
            aip.enterEndCustomer(
                test_case["First Name_End Customer"],
                test_case["Last Name_End Customer"],
            )
            logger.info(
                f"Entered End Customer details: {test_case['First Name_End Customer']}, {test_case['Last Name_End Customer']}"
            )

        aip.enterSoftwareDelivery()
        logger.info(f"Entered Software Delivery details")

        aip.enterShipToCustomer()
        logger.info(f"Entered Ship To Customer details")

        if is_valid_data(test_case["Shipping Method"]):
            aip.selectShippingMethod(test_case["Shipping Method"])
            logger.info(f"Selected shipping method: {test_case['Shipping Method']}")

        if is_valid_data(test_case["Shipping Instructions"]):
            cm.enterText(
                "AccountInformationPage",
                "shipping_Instructions",
                test_case["Shipping Instructions"],
            )
            logger.info(
                f"Entered shipping instructions: {test_case['Shipping Instructions']}"
            )

        cm.clickElementAndWait(
            page_name="HomePage_CPQ",
            element_name="save_Icon",
            wait_time=10,
        )
        logger.info(f"Clicked on Save button")
        ss.capture_screenshot("Captured Account Information details")
        """
        # ======================================GTC Tab=======================================================================
        hpgtc = HomePageGTC(new_tab)
        logger.info(f"HomePageGTC instance created for the new tab")

        hpgtc.clickGTCTab()
        logger.info(f"Clicked on GTC tab")

        hpgtc.selectEndCustomerDRCheckbox()
        logger.info(f"Selected End Customer DR checkbox")

        if is_valid_data(test_case["DR Override Justification"]):
            hpgtc.enterDROverrideJustification(test_case["DR Override Justification"])
            logger.info(
                f"Entered DR Override Justification: {test_case['DR Override Justification']}"
            )

        hpgtc.selectOverrideImportControlCheckbox()
        logger.info(f"Selected Override Import Control checkbox")

        hpgtc.selectEndCustomerENACheckbox()
        logger.info(f"Selected End Customer ENA checkbox")

        hpgtc.clickOverrideGTCButton()
        logger.info(f"Clicked on Override GTC button")

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured Account Information details")
        logger.info(f"Clicked on Save button")
        """
        # ============================Capture Quote Details==========================================================================
        # Perform actions on the new tab
        # quote_number = cm.readText("HomePage_CPQ", "quote_Number")
        # logger.info(f"Quote Number: {quote_number}")

        quote_name = cm.readText("HomePage_CPQ", "quote_Name")
        logger.info(f"Quote Name: {quote_name}")

        cpq_url = cm.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        quote_status = cm.readText("HomePage_CPQ", "quote_Status")
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")
        # ======================================Approval Request Tab=================================================================================
        ar = ApprovalRequestPage(new_tab)
        logger.info(f"ApprovalRequestPage instance created for the new tab")

        cm.clickElement("ApprovalRequestPage", "approval_Request_Tab")
        logger.info(f"Clicked on Approval request tab")
        """
        if is_valid_data(test_case["Justification"]):
            ar.select_Justification(test_case["Justification"])
            logger.info(f"Selected justification: {test_case['Justification']}")

        ar.clickCompetitionTab()
        logger.info(f"Clicked on Competition tab")

        if is_valid_data(test_case["Competitor"]):
            ar.enterCompetitor(test_case["Competitor"])
            logger.info(f"Entered competitor: {test_case['Competitor']}")

        if is_valid_data(test_case["Competitor Model"]):
            ar.enterCompetitorModel(test_case["Competitor Model"])
            logger.info(f"Entered competitor model: {test_case['Competitor Model']}")

        if is_valid_data(test_case["Net Price Offered By Vendor"]):
            ar.enterNetPriceOfferedByVendor(test_case["Net Price Offered By Vendor"])
            logger.info(
            f"Entered net price offered by vendor: {test_case['Net Price Offered By Vendor']}"
        )

        if is_valid_data(test_case["Competitor Product"]):
            ar.enterCompetitorProduct(test_case["Competitor Product"])
            logger.info(f"Entered competitor product: {test_case['Competitor Product']}")

        if is_valid_data(test_case["Raw Full Stack Vendor"]):
            ar.enterRawFullStackVendor(test_case["Raw Full Stack Vendor"])
            logger.info(
            f"Entered raw/full stack vendor: {test_case['Raw Full Stack Vendor']}"
        )

        if is_valid_data(test_case["Competitive Advantage"]):
            ar.enterCompetitiveAdvantage(test_case["Competitive Advantage"])
            logger.info(
            f"Entered competitive advantage: {test_case['Competitive Advantage']}"
        )

        ar.clickAddCompetitionButton()
        logger.info(f"Clicked on Add Competition button")

        ar.clickIncumbentVendorTab()
        logger.info(f"Clicked on Incumbent Vendor tab")

        if is_valid_data(test_case["Incumbent Vendor"]):
            ar.enterIncumbentVendor(test_case["Incumbent Vendor"])
            logger.info(f"Entered incumbent vendor: {test_case['Incumbent Vendor']}")

        ar.clickAddIncumbentButton()
        logger.info(f"Clicked on Add Incumbent button")

        if is_valid_data(test_case["Approval Comments"]):
            ar.addComments(test_case["Approval Comments"])
            logger.info(
            f"Added comments in approval request: {test_case['Approval Comments']}"
        )
        """

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

        # =====================================Attachments Tab=================================================================================
        ap = AttachmentsPage(new_tab)
        logger.info(f"AttachmentsPage instance created for the new tab")

        cm.clickElement("AttachmentsPage", "attachments_Tab")
        logger.info(f"Clicked on Attachments tab")

        ap.selectDragAndDrop()
        logger.info(f"Selected file to upload")

        if is_valid_data(test_case["Attachment Type"]):
            ap.selectAttachmentType(test_case["Attachment Type"])
            logger.info(f"Selected attachment type: {test_case['Attachment Type']}")

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

        # =============================Purchase Order Tab=================================================================================
        po = PurchaseOrderPage(new_tab)
        logger.info(f"PurchaseOrderPage instance created for the new tab")

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
            cm.enterText("PurchaseOrderPage", "po_Comments", test_case["PO Comments"])
            logger.info(f"Entered PO comments: {test_case['PO Comments']}")

        cm.clickElementAndWait(
            page_name="PurchaseOrderPage", element_name="submit_PO_Button", wait_time=20
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

        # =====================================TPD=========================================================================================
        thp = TPDHomePage(new_tab)
        logger.info(f"TPDHomePage instance created for the new tab")

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
        logger.info(f"Clicked on quote link in {tpd_subProcessStatus}: {quote_number}")

        cm.selectOptionInListbox("HomePage_TPD", "actions_DD", "Accepted")
        logger.info(f"Selected Accepted from Actions dropdown")

        cm.clickElement("HomePage_TPD", "actions_Go_Button")
        logger.info(f"Clicked on Actions Go button")

        cm.clickElement("HomePage_TPD", "yes_Button")
        logger.info(f"Clicked on Yes button in confirmation pop-up")
        ss.capture_screenshot("Captured TPD details")

        # ========================================Capture Test Result and Write To Excel==============================================
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
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
