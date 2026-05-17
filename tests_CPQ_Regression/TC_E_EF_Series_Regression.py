import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_CPQ.Products_Page import ProductsPage
from pages_CPQ.Quote_Info_Page import QuoteInfoPage
from pages_EAndEF_Series.HomePage_EAndEF_Series import HomePageEAndEFSeries
from pages_Print.HomePage_Print import HomePagePrint
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_CloudAndDataServices.HomePage_CloudAndDataServices import (
    HomePageCloudAndDataServices,
)
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
# Test Scenario:
# Test Description:
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData", "TC_E_EF_Series_Regression.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize("test_case", test_data.to_dict(orient="records"))
@pytest.mark.master
@pytest.mark.regression
def test_E_EF_Series_Regression(page: Page, base_url, config, test_case) -> None:
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
        if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":
            if test_case["Create Opportunity"].strip().lower() == "yes":

                hp.clickOpportunitiesTab()
                logger.info(f"Clicked on opportunities tab")

                hp.clickNewOpportunityButton()
                logger.info(f"Clicked on new opportunity button")

                if is_valid_data(test_case["Account Name"]):
                    co.enterAccount(test_case["Account Name"])
                    logger.info(
                        f"Entered and selected account: {test_case['Account Name']}"
                    )

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
                            logger.info(
                                f"Selected sales play: {test_case['Sales Play']}"
                            )
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
                            logger.info(
                                f"Selected 1P sales type: {test_case['Sales Type']}"
                            )
                        if is_valid_data(test_case["Primary Contact"]):
                            co.selectPrimaryContact_1p(test_case["Primary Contact"])
                            logger.info(
                                f"Selected 1P primary contact: {test_case['Primary Contact']}"
                            )
                        if is_valid_data(test_case["Hyperscaler"]):
                            co.selectHyperscaler(test_case["Hyperscaler"])
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
                            co.selectSalesType(test_case["Sales Type"])
                            logger.info(
                                f"Selected sales type: {test_case['Sales Type']}"
                            )
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
                    """
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
                    """
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
                            logger.info(
                                f"Selected reseller SE: {test_case['Reseller SE']}"
                            )
                        if is_valid_data(test_case["Distrubutor"]):
                            co.selectDistributor(test_case["Distrubutor"])
                            logger.info(
                                f"Selected distributor: {test_case['Distrubutor']}"
                            )
                        co.clickNextButton_2()
                        logger.info(f"Clicked on next button")

                    oppty_number = co.captureOpportunityNumber()
                    logger.info(f"Opportunity Number: {oppty_number}")

                    oppty_name = co.captureOpportunityName()
                    logger.info(f"Opportunity Name: {oppty_name}")

                spark_url = hp.getCurrentURL()
                logger.info(f"Captured Spark URL: {spark_url}")

        # =======================Add Product in SFDC=================================================================================
        if test_case["Add Products"].strip().lower() == "yes":
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
        if test_case["Create Quote"].strip().lower() == "yes":
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

            logger.info(
                f"Checking for the dynamic popup, if exists then closed the popup"
            )
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

        # ===================Configure Product E/EF-Series=======================================================================
        if test_case["Configure Product"].strip().lower() == "yes":
            pp = ProductsPage(new_tab)
            logger.info(f"ProductsPage instance created for the new tab")

            pp.clickProductsTab()
            logger.info(f"Clicked on Products tab")

            logger.info(
                f"Checking for the dynamic popup, if exists then closed the popup"
            )
            hpc.closePopUp_2()

            pp.clickConfigureButton()
            logger.info(f"Clicked on Configure button")

            hpeefs = HomePageEAndEFSeries(new_tab)
            logger.info(f"HomePageEAndEFSeries instance created for the new tab")

            if is_valid_data(test_case["Product"]):
                hpeefs.clickProductName(test_case["Product"])
                logger.info(f"Clicked on product: {test_case['Product']}")

            if is_valid_data(test_case["Sub Product"]):
                hpeefs.select_SubProduct(test_case["Sub Product"])
                logger.info(f"Clicked on sub product: {test_case['Sub Product']}")

            if test_case["Access"].strip().lower() == "Select All":
                hpeefs.access_SelectAll()
                logger.info(f"Accessed select all option under access tab")

            if is_valid_data(test_case["Model_System"]):
                hpeefs.selectModel_System(test_case["Model_System"])
                logger.info(f"Selected Model as: {test_case['Model_System']}")

            if is_valid_data(test_case["Controller Memory_System"]):
                hpeefs.selectControllerMemory_System(
                    test_case["Controller Memory_System"]
                )
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

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
