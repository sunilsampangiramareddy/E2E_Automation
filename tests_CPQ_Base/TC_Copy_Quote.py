from common_Methods.Common_Methods import CommonMethods
from pages_CPQ.Products_Page import ProductsPage
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
from pages_CPQ.Account_Information_Page import AccountInformationPage
from pages_CPQ.Approval_Request_Page import ApprovalRequestPage
from pages_CPQ.Attachments_Page import AttachmentsPage
from pages_CPQ.Purchase_Order_Page import PurchaseOrderPage
from pages_SFDC.Quotes_Page import QuotesPage
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can log in to the Salesforce and copy a quote successfully.
# Test Description: This test script automates the process of logging into Salesforce, copying a quote, updating
#                   its details in the Account Information, Approval Request, Attachments, and Purchase Order tabs,
#                   and validating the quote status after submission.
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_Copy_Quote.xlsx")
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
def test_Copy_Quote(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    qp = QuotesPage(page)
    hp = HomePage(page)
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
            lp.enterUserName(test_case["User Name"])
            logger.info(f"Username entered: {test_case['User Name']}")
            # lp.enterUserName(config.get_username())
            # logger.info("Username entered")

        lp.clickNextButton()
        logger.info(f"Clicked on next button")

        # lp.enterPassword(os.getenv("PASSWORD"))
        lp.enterPassword(config.get_encodedString())
        logger.info(f"Entered password")

        lp.clickSigninButton()
        logger.info(f"Signin button clicked")

        lp.clickYesButton()
        logger.info(f"Yes button clicked")

        hp.isOpportunitiesLabelVisible()
        logger.info(f"Opportunities label has been verified on the homepage")
        ss.capture_screenshot("Captured Homepage details")

        spark_url = hp.getCurrentURL()
        logger.info(f"Captured Spark URL: {spark_url}")

        # ========================Navigate to Quotes tab and click on the Copy quote=========================================================================
        if is_valid_data(test_case["Navigate To URL"]):
            qp.navigateToUrl(test_case["Navigate To URL"])
            logger.info(f"Navigated to URL: {test_case['Navigate To URL']}")

        qp.clickQuotesTab()
        logger.info(f"Clicked on Quotes tab")

        # ---Either use QuoteName or QuoteNumber, but dont use both---------------------
        if is_valid_data(test_case["Quote Name"]):
            qp.searchByQuoteName(test_case["Quote Name"])
            logger.info(f"Searched quote with quote name: {test_case['Quote Name']}")
            """
        if is_valid_data(test_case["Quote Number"]):
            qp.searchByQuoteNumber(test_case["Quote Number"])
            logger.info(
                f"Searched quote with quote number: {test_case['Quote Number']}"
            )
            """

        qp.copy_Quote()
        logger.info(f"Clicked on Copy Quote option for the searched quote")

        secondTab = cm.switchToTab(page.context, tab_index=1, expected_tab_count=2)
        logger.info("Switched to the new tab after clicking on Copy Quote option")

        # ============================Capture Quote Details==========================================================================
        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(secondTab)
        logger.info(f"HomePageCPQ instance created for the new tab")
        ss = ScreenshotUtil(secondTab)
        logger.info(f"ScreenshotUtil instance created for the new tab")
        hp = HomePage(secondTab)
        logger.info(f"HomePage instance created for the new tab")

        # Perform actions on the new tab
        quote_number = hpc.getQuoteNumber()
        logger.info(f"Quote Number: {quote_number}")

        quote_name = hpc.getQuoteName()
        logger.info(f"Quote Name: {quote_name}")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")

        cpq_url = hp.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp()
        ss.capture_screenshot("Captured Quote details")

        # =============================Read LIG Product Table=========================================================================
        pp = ProductsPage(secondTab)
        logger.info(f"ProductsPage instance created for the new tab")

        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp_2()

        hpc.readProductTable(secondTab, "Product")
        logger.info(f"Reading Product column values from product LIG table")

        hpc.readProductTable(secondTab, "List Price")
        logger.info(f"Reading List Price column values from product LIG table")

        hpc.readProductTable(secondTab, "Net Price")
        logger.info(f"Reading Net Price column values from product LIG table")

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured LIG Product table details")
        logger.info(f"Clicked on Save button")

        # =====================Copy quote second time from SFDC Quotes tab and switch to new tab=========================================================
        firstTab = cm.switchToTab(page.context, tab_index=0, expected_tab_count=2)
        logger.info("Switched back to the first tab to copy the quote again")

        qp = QuotesPage(firstTab)
        logger.info(f"QuotesPage instance created for the first tab")

        qp.copy_Quote()
        logger.info(f"Clicked on Copy Quote option for the searched quote")

        thirdTab = cm.switchToTab(page.context, tab_index=2, expected_tab_count=3)
        logger.info("Switched to the new tab after clicking on Copy Quote option")

        # ============================Capture Quote Details==========================================================================
        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(thirdTab)
        logger.info(f"HomePageCPQ instance created for the new tab")
        ss = ScreenshotUtil(thirdTab)
        logger.info(f"ScreenshotUtil instance created for the new tab")
        hp = HomePage(thirdTab)
        logger.info(f"HomePage instance created for the new tab")

        # Perform actions on the new tab
        quote_number = hpc.getQuoteNumber()
        logger.info(f"Quote Number: {quote_number}")

        quote_name = hpc.getQuoteName()
        logger.info(f"Quote Name: {quote_name}")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")

        cpq_url = hp.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp()
        ss.capture_screenshot("Captured Quote details")

        # =============================Read LIG Product Table=========================================================================
        pp = ProductsPage(thirdTab)
        logger.info(f"ProductsPage instance created for the new tab")

        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp_2()

        hpc.readProductTable(thirdTab, "Product")
        logger.info(f"Reading Product column values from product LIG table")

        hpc.readProductTable(thirdTab, "List Price")
        logger.info(f"Reading List Price column values from product LIG table")

        hpc.readProductTable(thirdTab, "Net Price")
        logger.info(f"Reading Net Price column values from product LIG table")

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured LIG Product table details")
        logger.info(f"Clicked on Save button")

        # =========================Close Second tab===================================================================================
        cm.closeTab(page.context, 1)
        logger.info(f"Closed the second tab")

        # ==============================Account Information Tab=================================================================================
        aip = AccountInformationPage(thirdTab)
        logger.info(f"AccountInformationPage instance created for the new tab")

        aip.clickAccountInformationTab()
        logger.info(f"Clicked on Account Information Tab")

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
            aip.enterShippingInstructions(test_case["Shipping Instructions"])
            logger.info(
                f"Entered shipping instructions: {test_case['Shipping Instructions']}"
            )

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured Account Information details")
        logger.info(f"Clicked on Save button")

        # ======================================GTC Tab=======================================================================
        hpgtc = HomePageGTC(thirdTab)
        logger.info(f"HomePageGTC instance created for the new tab")

        logger.info(f"Checking if GTC risk text is visible")
        if hpgtc.isGTCriskTextVisible() == True:

            hpgtc.clickGTCTab()
            logger.info(f"Clicked on GTC tab")

            hpgtc.selectEndCustomerENACheckbox_2()
            logger.info(f"Selected End Customer ENA checkbox")

            if is_valid_data(test_case["DR Override Justification"]):
                hpgtc.enterDROverrideJustification(
                    test_case["DR Override Justification"]
                )
                logger.info(
                    f"Entered DR Override Justification: {test_case['DR Override Justification']}"
                )

            hpgtc.selectOverrideImportControlCheckbox()
            logger.info(f"Selected Override Import Control checkbox")

            hpgtc.selectShipToCustomerENACheckbox()
            logger.info(f"Selected Ship To Customer ENA checkbox")

            hpgtc.clickOverrideGTCButton()
            logger.info(f"Clicked on Override GTC button")

            hpc.clickSaveIcon()
            ss.capture_screenshot("Captured Account Information details")
            logger.info(f"Clicked on Save button")

        # ======================================Approval Request Tab=================================================================================
        ar = ApprovalRequestPage(thirdTab)
        logger.info(f"ApprovalRequestPage instance created for the new tab")

        ar.clickApprovalRequestTab()
        logger.info(f"Clicked on Approval request tab")

        ar.clickInitiateApproval()
        ss.capture_screenshot("Captured Approval Tab details")
        logger.info(f"Clicked on Initiate Approval button")

        # =====================================Attachments Tab=================================================================================
        ap = AttachmentsPage(thirdTab)
        logger.info(f"AttachmentsPage instance created for the new tab")

        ap.clickAttachmentsTab()
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

        ap.clickUploadButton()
        logger.info(f"Clicked on upload button")

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured Attachment Tab details")
        logger.info(f"Clicked on Save button")

        # =============================Purchase Order Tab=================================================================================
        po = PurchaseOrderPage(thirdTab)
        logger.info(f"PurchaseOrderPage instance created for the new tab")

        po.clickPurchaseOrderTab()
        logger.info(f"Clicked on Purchase order tab")

        po.enterPONumber(quote_number)
        logger.info(f"Entered PO number: {quote_number}")

        po.enterPODate()
        logger.info(f"Entered PO date")

        if is_valid_data(test_case["PO Email"]):
            po.enterPOEmail(test_case["PO Email"])
            logger.info(f"Entered PO email: {test_case['PO Email']}")

        if is_valid_data(test_case["PO Comments"]):
            po.enterPOComments(test_case["PO Comments"])
            logger.info(f"Entered PO comments: {test_case['PO Comments']}")

        po.clickSubmitPO()
        logger.info(f"Clicked on Submit PO button")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured PO submission quote status")
        logger.info(f"Quote Status: {quote_status}")

        # =========================================Capture Test Result and Write To Excel==============================================
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
                "Copied Quote successfully",
            ],
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        logger.info(f"***{script_name} Test Script Execution Completed Successfully***")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
