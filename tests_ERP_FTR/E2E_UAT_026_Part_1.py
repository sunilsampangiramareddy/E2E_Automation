import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_CPQ.Products_Page import ProductsPage
from pages_CPQ.Quote_Info_Page import QuoteInfoPage
from pages_CloudAndDataServices.HomePage_CloudAndDataServices import (
    HomePageCloudAndDataServices,
)
from pages_EAndEF_Series.HomePage_EAndEF_Series import HomePageEAndEFSeries
from pages_Print.HomePage_Print import HomePagePrint
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_FAS_AFF_ASA_AFX.HomePage_FAS_AFF_ASA_AFX import HomePageFAS_AFF_ASA_AFX
from pages_CPQ.Account_Information_Page import AccountInformationPage
from pages_CPQ.Approval_Request_Page import ApprovalRequestPage
from pages_GTC.HomePage_GTC import HomePageGTC
from pages_CPQ.Attachments_Page import AttachmentsPage
from pages_CPQ.Purchase_Order_Page import PurchaseOrderPage
from pages_StorageGrid.HomePage_StorageGrid import HomePageStorageGrid
from pages_TPD.TPD_Home_Page import TPDHomePage
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# Test Scenario: Verify that a user can configure multiple products E-Series(E5700), Cloud and Data Services
#                (Data Infrastructure Insights)) and Storage Grid(SG5812), submit a quote, and approve the quote in TPD
# Test Description: This test script automates the process of logging into Salesforce, creating a Indirect opportunity
#                   using Distrubutor, configuring multiple products E-Series(E5700), Cloud and Data Services
#                   (Data Infrastructure Insights)) and Storage Grid(SG5812), updating its details in the Account Information,
#                   Override Invalid/LOD Part, Initiate Approval Request, Attachments and Purchase Order tabs and
#                   validating the quote status by approving the quote in TPD.
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "E2E_UAT_026_Part_1.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_E2E_UAT_026_Part_1(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
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

        # =======================Create Opportunity===========================================================================
        hp.clickOpportunitiesTab()
        logger.info(f"Clicked on opportunities tab")

        hp.clickNewOpportunityButton()
        logger.info(f"Clickecd on new opportunity button")

        if is_valid_data(test_case["Account Name"]):
            co.enterAccount(test_case["Account Name"])
            logger.info(f"Entered and selected account: {test_case['Account Name']}")

        co.clickNextButton()
        logger.info(f"Clicked on next button")

        if (
            test_case["Channel"] == direct_Oppty
            or test_case["Channel"] == indirect_Oppty
            or test_case["Opportunity Type"] == x1p_Oppty
        ):
            if is_valid_data(test_case["Opportunity Type"]):
                co.selectOpportunityType(test_case["Opportunity Type"])
                logger.info(
                    f"Selected opportunity type: {test_case['Opportunity Type']}"
                )

            if test_case["Opportunity Type"] == std_Oppty:
                if is_valid_data(test_case["Opportunity Name"]):
                    co.enterOpportunityName(test_case["Opportunity Name"])
                    logger.info(
                        f"Entered opportunity name: {test_case['Opportunity Name']}"
                    )
                if is_valid_data(test_case["Primary Contact"]):
                    co.selectPrimaryContact(test_case["Primary Contact"])
                    logger.info(
                        f"Selected primary contact: {test_case['Primary Contact']}"
                    )
                if is_valid_data(test_case["Sales Play"]):
                    co.selectSalesPlay(test_case["Sales Play"])
                    logger.info(f"Selected sales play: {test_case['Sales Play']}")
                if is_valid_data(test_case["Channel"]):
                    co.selectChannel(test_case["Channel"])
                    logger.info(f"Selected channel: {test_case['Channel']}")

            if test_case["Opportunity Type"] == x1p_Oppty:
                if is_valid_data(test_case["Opportunity Name"]):
                    co.enterOpportunityName_1p(test_case["Opportunity Name"])
                    logger.info(
                        f"Entered 1P opportunity name: {test_case['Opportunity Name']}"
                    )
                if is_valid_data(test_case["Sales Type"]):
                    co.selectSalesType_1p(test_case["Sales Type"])
                    logger.info(f"Selected 1P sales type: {test_case['Sales Type']}")
                if is_valid_data(test_case["Primary Contact"]):
                    co.selectPrimaryContact_1p(test_case["Primary Contact"])
                    logger.info(
                        f"Selected 1P primary contact: {test_case['Primary Contact']}"
                    )
                if is_valid_data(test_case["Hyperscaler"]):
                    co.selectHyperscaler(test_case["Hyperscaler"])
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
                    co.selectSalesType(test_case["Sales Type"])
                    logger.info(f"Selected sales type: {test_case['Sales Type']}")
                    """
                if is_valid_data(test_case["Installed Base Type"]):
                    co.selectInstalledBaseType(test_case["Installed Base Type"])
                    logger.info(f"Selected installed base type: {test_case['Installed Base Type']}")
                    """
                if is_valid_data(test_case["Currency"]):
                    co.selectCurrency(test_case["Currency"])
                    ss.capture_screenshot("Captured Create Opportunity details")
                    logger.info(f"Selected currency: {test_case['Currency']}")
                co.clickNextButton()
                logger.info(f"Clicked on next button")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["Pathway"]):
                    co.selectPathway(test_case["Pathway"])
                    logger.info(f"Selected pathway: {test_case['Pathway']}")
                if is_valid_data(test_case["Partner Sales Model"]):
                    co.selectPartnerSalesModel(test_case["Partner Sales Model"])
                    logger.info(
                        f"Selected partner sales model: {test_case['Partner Sales Model']}"
                    )
                co.clickNextButton()
                logger.info(f"Clicked on next button")

            if (
                test_case["Opportunity Type"] == std_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                if is_valid_data(test_case["End Customer Usage"]):
                    co.selectEndCustomerUsage_option(test_case["End Customer Usage"])
                    logger.info(
                        f"Selected end customer usage: {test_case['End Customer Usage']}"
                    )

            if (
                test_case["Channel"] == direct_Oppty
                or test_case["Opportunity Type"] == x1p_Oppty
            ):
                co.clickNextButton_2()
                logger.info(f"Clicked on next button")

            if (
                test_case["Channel"] == indirect_Oppty
                and test_case["Opportunity Type"] != x1p_Oppty
            ):
                co.clickNextButton()
                logger.info(f"Clicked on next button")
                if is_valid_data(test_case["Reseller Sales Rep"]):
                    co.selectResellerSalesRep(test_case["Reseller Sales Rep"])
                    logger.info(
                        f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}"
                    )
                if is_valid_data(test_case["Reseller SE"]):
                    co.selectResellerSE(test_case["Reseller SE"])
                    logger.info(f"Selected reseller SE: {test_case['Reseller SE']}")
                if is_valid_data(test_case["Distrubutor"]):
                    co.selectDistributor(test_case["Distrubutor"])
                    logger.info(f"Selected distributor: {test_case['Distrubutor']}")
                co.clickNextButton_2()
                logger.info(f"Clicked on next button")

            oppty_number = co.captureOpportunityNumber()
            logger.info(f"Opportunity Number: {oppty_number}")

            oppty_name = co.captureOpportunityName()
            logger.info(f"Opportunity Name: {oppty_name}")

        spark_url = hp.getCurrentURL()
        logger.info(f"Captured Spark URL: {spark_url}")

        # =======================Add Product in SFDC=================================================================================
        if is_valid_data(test_case["Product Name"]):
            hp.selectProduct(test_case["Product Name"])
            logger.info(f"Selected product: {test_case['Product Name']}")

        if is_valid_data(test_case["Product Price"]):
            hp.enterProductPrice(test_case["Product Price"])
            ss.capture_screenshot("Captured Product in SFDC Details")
            logger.info(f"Entered product price: {test_case['Product Price']}")

        hp.navigateToUrl(spark_url)
        logger.info(f"Navigated back to Spark URL: {spark_url}")

        # ========================Create Quote=======================================================================================
        new_tab = hp.create_Quote()
        logger.info(f"Clicked on create quote")

        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(new_tab)
        logger.info(f"HomePageCPQ instance created for the new tab")
        ss = ScreenshotUtil(new_tab)
        logger.info(f"ScreenshotUtil instance created for the new tab")
        hp = HomePage(new_tab)
        logger.info(f"HomePage instance created for the new tab")

        hpc.clickSaveButton()
        logger.info(f"Clicked on save button")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp()
        ss.capture_screenshot("Captured Quote details")

        # ============================Capture Quote Details==========================================================================
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

        # ===================Configure First Product E-Series(E5700)================================================================

        pp = ProductsPage(new_tab)
        logger.info(f"ProductsPage instance created for the new tab")

        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp_2()

        pp.clickConfigureButton()
        logger.info(f"Clicked on Configure button")

        hpeefs = HomePageEAndEFSeries(new_tab)
        logger.info(f"HomePageEAndEFSeries instance created for the new tab")

        if is_valid_data(test_case["Product"]):
            hpeefs.clickProductName(test_case["Product"])
            logger.info(f"Clicked on product: {test_case['Product']}")

        if is_valid_data(test_case["Sub Product"]):
            hpeefs.selectSubProduct(test_case["Sub Product"])
            logger.info(f"Clicked on sub product: {test_case['Sub Product']}")

        hpeefs.access_SelectAll()
        logger.info(f"Accessed select all option under access tab")

        if is_valid_data(test_case["Model_System"]):
            hpeefs.selectModel_System(test_case["Model_System"])
            logger.info(f"Selected Model as: {test_case['Model_System']}")

        if is_valid_data(test_case["Controller Memory_System"]):
            hpeefs.selectControllerMemory_System(test_case["Controller Memory_System"])
            logger.info(
                f"Selected Controller Memory as: {test_case['Controller Memory_System']}"
            )

        if is_valid_data(test_case["Enclosure_Base Storage Options"]):
            hpeefs.selectEnclosure_BaseStorageOptions(
                test_case["Enclosure_Base Storage Options"]
            )
            logger.info(
                f"Selected Enclosure under Base Storage Options as: {test_case['Enclosure_Base Storage Options']}"
            )

        if is_valid_data(test_case["Encryption_Storage"]):
            hpeefs.selectEncryption_Storage(test_case["Encryption_Storage"])
            logger.info(
                f"Selected Encryption under Storage as: {test_case['Encryption_Storage']}"
            )

        if is_valid_data(test_case["Capacity_Storage"]):
            hpeefs.selectCapacityStorage(test_case["Capacity_Storage"])
            logger.info(
                f"Selected Capacity_Storage as: {test_case['Capacity_Storage']}"
            )

        if is_valid_data(test_case["Qty Per Enclosure_Storage"]):
            hpeefs.enterQtyPerEnclosure_Storage_2(
                test_case["Qty Per Enclosure_Storage"]
            )
            logger.info(
                f"Entered Quantity per Enclosure_Storage as: {test_case['Qty Per Enclosure_Storage']}"
            )

        if is_valid_data(test_case["Card_HIC"]):
            hpeefs.selectCard_HIC(test_case["Card_HIC"])
            logger.info(f"Selected Card_HIC as: {test_case['Card_HIC']}")

        hpeefs.clickAddToQuote()
        ss.capture_screenshot("Captured Product configuration details")
        logger.info(f"Clicked on Add to Quote button")

        # =============Configure Second Product Cloud and Data Services(Data Infrastructure Insights))================================================================
        pp = ProductsPage(new_tab)
        logger.info(f"ProductsPage instance created for the new tab")

        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        pp.clickConfigureButton()
        logger.info(f"Clicked on Configure button")

        hpcads = HomePageCloudAndDataServices(new_tab)
        logger.info(f"HomePageCloudAndDataServices instance created for the new tab")

        if is_valid_data(test_case["Product_2"]):
            hpcads.clickProductName(test_case["Product_2"])
            logger.info(f"Clicked on product: {test_case['Product_2']}")

        if is_valid_data(test_case["Sub Product_2"]):
            hpcads.selectSubProduct(test_case["Sub Product_2"])
            logger.info(f"Clicked on sub-product: {test_case['Sub Product_2']}")

        hpcads.enterTenantSN()
        logger.info(f"Entered Tenant SN Random Number")

        if is_valid_data(test_case["New Qty_High Performance_2"]):
            hpcads.enterNewQty_HighPerformance(test_case["New Qty_High Performance_2"])
            logger.info(
                f"Entered New Qty for High Performance: {test_case['New Qty_High Performance_2']}"
            )

        if is_valid_data(test_case["Billing Frequency_2"]):
            hpcads.selectBillingFrequency(test_case["Billing Frequency_2"])
            logger.info(
                f"Selected Billing Frequency: {test_case['Billing Frequency_2']}"
            )

        if is_valid_data(test_case["Term (Months)_2"]):
            hpcads.enterTermMonths(test_case["Term (Months)_2"])
            logger.info(f"Entered Term in months: {test_case['Term (Months)_2']}")

        hpcads.clickAddToQuote()
        ss.capture_screenshot("Captured Product configuration details")
        logger.info(f"Clicked on Add to Quote button")

        # =============Configure Third Product Storage Grid(SG5812)=========================================================

        pp = ProductsPage(new_tab)
        logger.info(f"ProductsPage instance created for the new tab")

        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        pp.clickConfigureButton()
        logger.info(f"Clicked on Configure button")

        hpsg = HomePageStorageGrid(new_tab)
        logger.info(f"HomePageStorageGrid instance created for the new tab")

        if is_valid_data(test_case["Product_3"]):
            hpsg.clickProductName(test_case["Product_3"])
            logger.info(f"Clicked on product: {test_case['Product_3']}")

        if is_valid_data(test_case["Sub Product_3"]):
            hpsg.selectSubProduct(test_case["Sub Product_3"])
            logger.info(f"Clicked on sub-product: {test_case['Sub Product_3']}")

        hpsg.access_SelectAll()
        logger.info(f"Accessed select all option under access tab")

        hpsg.selectModel_StorageNodes(test_case["Model_Storage Nodes_3"])
        logger.info(f"Selected Model as: {test_case['Model_Storage Nodes_3']}")

        hpsg.selectDriveType_StorageNodes(test_case["Drive Type_Storage Nodes_3"])
        logger.info(
            f"Selected Drive Type as: {test_case['Drive Type_Storage Nodes_3']}"
        )

        hpsg.enterQty_StorageNodes(test_case["Qty_Storage Nodes_3"])
        logger.info(f"Entered Quantity as: {test_case['Qty_Storage Nodes_3']}")

        hpsg.clickAddToQuote()
        ss.capture_screenshot("Captured Product configuration details")
        logger.info(f"Clicked on Add to Quote button")

        # =============================Read LIG Product Table=========================================================================
        pp.clickProductsTab()
        logger.info(f"Clicked on Products tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp_2()

        pp.expandAllProducts()
        logger.info(f"Expanded all products in the LIG product table")

        hpc.readProductTable(new_tab, "Product")
        logger.info(f"Reading Product column values from product LIG table")

        hpc.readProductTable(new_tab, "List Price")
        logger.info(f"Reading List Price column values from product LIG table")

        hpc.readProductTable(new_tab, "Net Price")
        logger.info(f"Reading Net Price column values from product LIG table")

        pp.collapseAllProducts()
        logger.info(f"Collapsed all products in the LIG product table")

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured LIG Product table details")
        logger.info(f"Clicked on Save button")

        # ==============================Account Information Tab=================================================================================
        aip = AccountInformationPage(new_tab)
        logger.info(f"AccountInformationPage instance created for the new tab")

        aip.clickAccountInformationTab()
        logger.info(f"Clicked on Account Information Tab")

        logger.info(f"Checking for the dynamic popup, if exists then closed the popup")
        hpc.closePopUp_2()

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

        aip.enterServiceCustomer_2()
        logger.info(f"Entered Service Customer details")

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

        # ==================Override Invalid/LOD Part in Quote Info Page================================================================================

        qip = QuoteInfoPage(new_tab)
        logger.info(f"QuoteInfoPage instance created for the new tab")

        qip.clickQuoteInfoTab()
        logger.info(f"Clicked on Quote Info tab")

        qip.check_OverrideInvalidLODPart()
        logger.info(f"Checked Override Invalid/LOD Part checkbox")

        hpc.clickSaveIcon()
        logger.info(f"Clicked on Save button")

        # ======================================Approval Request Tab=================================================================================
        ar = ApprovalRequestPage(new_tab)
        logger.info(f"ApprovalRequestPage instance created for the new tab")

        ar.clickApprovalRequestTab()
        logger.info(f"Clicked on Approval request tab")

        ar.clickInitiateApproval()
        ss.capture_screenshot("Captured Approval Tab details")
        logger.info(f"Clicked on Initiate Approval button")

        hpc.clickSaveIcon()
        ss.capture_screenshot("Captured Account Information details")
        logger.info(f"Clicked on Save button")

        # =====================================Attachments Tab=================================================================================
        ap = AttachmentsPage(new_tab)
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

        # ============================Capture Quote Details==========================================================================
        quote_number = hpc.getQuoteNumber()
        logger.info(f"Quote Number: {quote_number}")

        quote_name = hpc.getQuoteName()
        logger.info(f"Quote Name: {quote_name}")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured Quote details")
        logger.info(f"Quote Status: {quote_status}")

        cpq_url = hp.getCurrentURL()
        logger.info(f"CPQ URL: {cpq_url}")

        # =============================Purchase Order Tab=================================================================================
        po = PurchaseOrderPage(new_tab)
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

        if is_valid_data(test_case["Fulfilment Method"]):
            po.selectFulfillmentMethod(test_case["Fulfilment Method"])
            logger.info(f"Selected Fulfilment Method: {test_case['Fulfilment Method']}")

        if is_valid_data(test_case["Fulfilment Justification"]):
            po.selectFulfillmentJustification(test_case["Fulfilment Justification"])
            logger.info(
                f"Selected Fulfilment Justification: {test_case['Fulfilment Justification']}"
            )

        if is_valid_data(test_case["Fulfilment Reqested By"]):
            po.selfFulfillmentRequestedBy(test_case["Fulfilment Reqested By"])
            logger.info(
                f"Selected Fulfilment Requested By: {test_case['Fulfilment Reqested By']}"
            )

        po.clickSubmitPO()
        logger.info(f"Clicked on Submit PO button")

        quote_status = hpc.getQuoteStatus()
        ss.capture_screenshot("Captured PO submission quote status")
        logger.info(f"Quote Status: {quote_status}")

        # =====================================TPD=========================================================================================
        thp = TPDHomePage(new_tab)
        logger.info(f"TPDHomePage instance created for the new tab")

        if is_valid_data(test_case["TPD URL"]):
            thp.navigateToUrl(test_case["TPD URL"])
            logger.info(f"Navigated to TPD URL: {test_case['TPD URL']}")

        thp.clickGlobalSearch()
        logger.info(f"Clicked on global search")

        thp.searchByTransactionNumber(quote_number)
        logger.info(f"Searched by transaction number: {quote_number}")

        thp.searchByPONumber(quote_number)
        logger.info(f"Searched by PO number: {quote_number}")

        thp.clickGoButton()
        logger.info(f"Clicked on Go button")

        tpd_subProcessStatus = thp.getSubProcessStatus()
        logger.info(f"Captured subprocess status: {tpd_subProcessStatus}")

        tpd_orderStatus = thp.getOrderStatus()
        logger.info(f"Captured order status: {tpd_orderStatus}")

        thp.clickRPAReview()
        logger.info(f"Clicked on RPA Review")

        thp.searchByTransactionNumber(quote_number)
        logger.info(f"Searched by transaction number in RPA review: {quote_number}")

        thp.clickGoButton()
        logger.info(f"Clicked on Go button in RPA review")

        thp.clickSearchQuote(quote_number)
        logger.info(f"Clicked on quote link in RPA review: {quote_number}")

        thp.select_ActionsDD(option_value="Accepted")
        logger.info(f"Selected Accepted from Actions dropdown")

        thp.clickActionsGoButton()
        logger.info(f"Clicked on Actions Go button")

        thp.clickYesButton()
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
