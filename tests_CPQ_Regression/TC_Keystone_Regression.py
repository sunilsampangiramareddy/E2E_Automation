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
# Test Description: This test script automates the regression testing of the Keystone product workflow.
#                   It validates the end-to-end process for creating opportunities, configuring products,
#                   generating quotes, and submitting purchase orders, while ensuring data integrity across
#                   BOM and LIG tables. The script also performs validations for error handling,
#                   subscription management and integration with TPD.
# Author: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_CPQ_Regression", "TC_Keystone_Regression.xlsx"
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
    # Initialize BOM lists
    bom_list_part_number = []
    bom_list_quantity = []
    bom_list_description = []
    validation_failures = []

    try:
        # ==================================Login to SFDC=================================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****\033[0m"
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
            cm.assertTrue(
                is_visible, "Opportunities label is not visible on the homepage"
            )
            logger.info(
                f"Opportunities label has been verified on the homepage: {is_visible}"
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

            # ========================Add Product in SFDC=====================================================================================
            if test_case["Add Products"].strip().lower() == "yes":
                if is_valid_data(test_case["Product Name"]):
                    hp.selectProduct(test_case["Product Name"])
                    logger.info(f"Selected product: {test_case['Product Name']}")

                if is_valid_data(test_case["Product Price"]):
                    hp.enterProductPrice(test_case["Product Price"])
                    logger.info(f"Entered product price: {test_case['Product Price']}")

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")
                ss.capture_screenshot("Captured Opportunity details")

            # =========================Create Quote for Keystone===========================================================================================
            if test_case["Create Quote"].strip().lower() == "yes":

                hp.createQuote()
                logger.info(f"Clicked on create quote")

                second_Tab = cm.switchToTab(
                    page.context, tab_index=1, expected_tab_count=2
                )
                logger.info(
                    "Switched to the new tab after clicking on Create Quote option"
                )

                # Create an instance of HomePageCPQ for the new tab
                hpc = HomePageCPQ(second_Tab)
                logger.info(f"HomePageCPQ instance created for the new tab")
                ss = ScreenshotUtil(second_Tab)
                logger.info(f"ScreenshotUtil instance created for the new tab")
                hp = HomePage(second_Tab)
                logger.info(f"HomePage instance created for the new tab")
                cm = CommonMethods(second_Tab, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")
                qip = QuoteInfoPage(second_Tab)
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
                ss.capture_screenshot("Captured Keystone Quote details")

            # =============================Capture Quote Details for Keystone==============================================================================
            # Perform actions on the new tab
            if test_case["Capture Quote Details"].strip().lower() == "yes":
                keystone_quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                logger.info(f"Quote Number: {keystone_quote_number}")
                print(
                    f"\033[94mℹ️ Keystone Quote Number: {keystone_quote_number}\033[0m"
                )

                keystone_quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                logger.info(f"Quote Name: {keystone_quote_name}")
                print(f"\033[94mℹ️ Keystone Quote Name: {keystone_quote_name}\033[0m")

                keystone_cpq_url = cm.getCurrentURL()
                logger.info(f"Keystone CPQ URL: {keystone_cpq_url}")
                print(f"\033[94mℹ️ Keystone CPQ URL: {keystone_cpq_url}\033[0m")

                print(
                    f"\n\033[94mℹ️ ================Validating Keystone Quote for Draft Status================================================================================================\033[0m"
                )
                keystone_quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                logger.info(f"Keystone Quote Status: {keystone_quote_status}")
                print(
                    f"\033[94mℹ️ Keystone Quote Status: {keystone_quote_status}\033[0m"
                )

                if test_case["Quote Status Validation"].strip().lower() == "yes":
                    keystone_quote_status = cm.verifyElementStatus(
                        "HomePage_CPQ", "quote_Status", test_case["Quote Status_Draft"]
                    )
                    if not keystone_quote_status:
                        failure_message = (
                            f"Keystone Quote status is not in expected state: "
                            f"Expected '{test_case['Quote Status_Draft']}', but found something else."
                        )
                        validation_failures.append(
                            failure_message
                        )  # Add failure to the list
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Verified Keystone quote status is in expected state {test_case['Quote Status_Draft']}: {keystone_quote_status}"
                        )
                        print(
                            f"\033[92m✅ Verified Keystone quote status is in expected state {test_case['Quote Status_Draft']}: {keystone_quote_status}\033[0m"
                        )

            # ====================Configure Keystone Product=================================================================================
            pp = ProductsPage(second_Tab)
            logger.info(f"ProductsPage instance created for the new tab")
            kp = HomePageKeystone(second_Tab)
            logger.info(f"Keystone Page instance created for the new tab")
            cv = CommonValidations(second_Tab)
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

                    if is_valid_data(test_case["Advanced Data Protect"]):
                        kp.selectAdvancedDataProtect(test_case["Advanced Data Protect"])
                        logger.info(
                            f"Selected Advanced Data Protect: {test_case['Advanced Data Protect']}"
                        )

                    if is_valid_data(test_case["Advanced Data Protect Total Quantity"]):
                        kp.enterADPTotalQuantity(
                            test_case["Advanced Data Protect Total Quantity"]
                        )
                        logger.info(
                            f"Entered Advanced Data Protect Total Quantity: {test_case['Advanced Data Protect Total Quantity']}"
                        )

                    if (
                        test_case["Add_File and Block Storage Services_1"]
                        .strip()
                        .lower()
                        == "yes"
                    ):
                        if is_valid_data(
                            test_case["Data Type_File and Block Storage Services_1"]
                        ):
                            kp.selectDataType_FileAndBlockStorageServices(
                                test_case["Data Type_File and Block Storage Services_1"]
                            )
                            logger.info(
                                f"Selected data type: {test_case['Data Type_File and Block Storage Services_1']}"
                            )

                        if is_valid_data(
                            test_case["Service Level_File and Block Storage Services_1"]
                        ):
                            kp.selectServiceLevel_FileAndBlockStorageServices(
                                test_case[
                                    "Service Level_File and Block Storage Services_1"
                                ]
                            )
                            logger.info(
                                f"Selected service level: {test_case['Service Level_File and Block Storage Services_1']}"
                            )

                        if is_valid_data(
                            test_case[
                                "Total Capacity Committed_File and Block Storage Services_1"
                            ]
                        ):
                            kp.enterTotalCapacityCommitted_FileAndBlockStorageServices(
                                test_case[
                                    "Total Capacity Committed_File and Block Storage Services_1"
                                ]
                            )
                            logger.info(
                                f"Entered total capacity committed: {test_case['Total Capacity Committed_File and Block Storage Services_1']}"
                            )

                    if (
                        test_case["Add_File and Block Storage Services_2"]
                        .strip()
                        .lower()
                        == "yes"
                    ):

                        kp.clickAddFileAndBlockStorageServices()
                        logger.info(
                            f"Clicked on Add File and Block Storage Services button"
                        )

                        if is_valid_data(
                            test_case["Data Type_File and Block Storage Services_2"]
                        ):
                            kp.selectDataType_FileAndBlockStorageServices_2(
                                test_case["Data Type_File and Block Storage Services_2"]
                            )
                            logger.info(
                                f"Selected data type: {test_case['Data Type_File and Block Storage Services_2']}"
                            )

                        if is_valid_data(
                            test_case["Service Level_File and Block Storage Services_2"]
                        ):
                            kp.selectServiceLevel_FileAndBlockStorageServices_2(
                                test_case[
                                    "Service Level_File and Block Storage Services_2"
                                ]
                            )
                            logger.info(
                                f"Selected service level: {test_case['Service Level_File and Block Storage Services_2']}"
                            )

                        if is_valid_data(
                            test_case[
                                "Total Capacity Committed_File and Block Storage Services_2"
                            ]
                        ):
                            kp.enterTotalCapacityCommitted_FileAndBlockStorageServices_2(
                                test_case[
                                    "Total Capacity Committed_File and Block Storage Services_2"
                                ]
                            )
                            logger.info(
                                f"Entered total capacity committed: {test_case['Total Capacity Committed_File and Block Storage Services_2']}"
                            )
                    if (
                        test_case["Add_File and Block Storage Services_3"]
                        .strip()
                        .lower()
                        == "yes"
                    ):
                        kp.clickAddFileAndBlockStorageServices()
                        logger.info(
                            f"Clicked on Add File and Block Storage Services button"
                        )

                        if is_valid_data(
                            test_case["Data Type_File and Block Storage Services_3"]
                        ):
                            kp.selectDataType_FileAndBlockStorageServices_2(
                                test_case["Data Type_File and Block Storage Services_3"]
                            )
                            logger.info(
                                f"Selected data type: {test_case['Data Type_File and Block Storage Services_3']}"
                            )

                        if is_valid_data(
                            test_case["Service Level_File and Block Storage Services_3"]
                        ):
                            kp.selectServiceLevel_FileAndBlockStorageServices_2(
                                test_case[
                                    "Service Level_File and Block Storage Services_3"
                                ]
                            )
                            logger.info(
                                f"Selected service level: {test_case['Service Level_File and Block Storage Services_3']}"
                            )

                        if is_valid_data(
                            test_case[
                                "Total Capacity Committed_File and Block Storage Services_3"
                            ]
                        ):
                            kp.enterTotalCapacityCommitted_FileAndBlockStorageServices_2(
                                test_case[
                                    "Total Capacity Committed_File and Block Storage Services_3"
                                ]
                            )
                            logger.info(
                                f"Entered total capacity committed: {test_case['Total Capacity Committed_File and Block Storage Services_3']}"
                            )

                    if (
                        test_case["Add_File and Block Storage Services_4"]
                        .strip()
                        .lower()
                        == "yes"
                    ):
                        kp.clickAddFileAndBlockStorageServices()
                        logger.info(
                            f"Clicked on Add File and Block Storage Services button"
                        )

                        if is_valid_data(
                            test_case["Data Type_File and Block Storage Services_4"]
                        ):
                            kp.selectDataType_FileAndBlockStorageServices_2(
                                test_case["Data Type_File and Block Storage Services_4"]
                            )
                            logger.info(
                                f"Selected data type: {test_case['Data Type_File and Block Storage Services_4']}"
                            )

                        if is_valid_data(
                            test_case["Service Level_File and Block Storage Services_4"]
                        ):
                            kp.selectServiceLevel_FileAndBlockStorageServices_2(
                                test_case[
                                    "Service Level_File and Block Storage Services_4"
                                ]
                            )
                            logger.info(
                                f"Selected service level: {test_case['Service Level_File and Block Storage Services_4']}"
                            )

                        if is_valid_data(
                            test_case[
                                "Total Capacity Committed_File and Block Storage Services_4"
                            ]
                        ):
                            kp.enterTotalCapacityCommitted_FileAndBlockStorageServices_2(
                                test_case[
                                    "Total Capacity Committed_File and Block Storage Services_4"
                                ]
                            )
                            logger.info(
                                f"Entered total capacity committed: {test_case['Total Capacity Committed_File and Block Storage Services_4']}"
                            )

                    if is_valid_data(test_case["Optional Features"]):
                        kp.selectOptionalFeatures(test_case["Optional Features"])
                        logger.info(
                            f"Selected optional features: {test_case['Optional Features']}"
                        )

                    if is_valid_data(test_case["Total Quantity_Optional Features"]):
                        kp.enterTotalQuantity_OptionalFeatures(
                            test_case["Total Quantity_Optional Features"]
                        )
                        logger.info(
                            f"Entered total quantity: {test_case['Total Quantity_Optional Features']}"
                        )

                    if is_valid_data(test_case["Data Type_Object Storage Services"]):
                        kp.selectDataType_ObjectStorageServices(
                            test_case["Data Type_Object Storage Services"]
                        )
                        logger.info(
                            f"Selected data type: {test_case['Data Type_Object Storage Services']}"
                        )

                    if is_valid_data(
                        test_case["Service Level_Object Storage Services"]
                    ):
                        kp.selectServiceLevel_ObjectStorageServices(
                            test_case["Service Level_Object Storage Services"]
                        )
                        logger.info(
                            f"Selected service level: {test_case['Service Level_Object Storage Services']}"
                        )

                    if is_valid_data(
                        test_case["Total Capacity_Object Storage Services"]
                    ):
                        kp.selectTotalCapacity_ObjectStorageServices(
                            test_case["Total Capacity_Object Storage Services"]
                        )
                        logger.info(
                            f"Entered total capacity: {test_case['Total Capacity_Object Storage Services']}"
                        )

                    if is_valid_data(test_case["Billing Frequency"]):
                        kp.selectBillingFrequency(test_case["Billing Frequency"])
                        logger.info(
                            f"Selected billing frequency: {test_case['Billing Frequency']}"
                        )

                    if is_valid_data(test_case["Term"]):
                        kp.selectTerm(test_case["Term"])
                        logger.info(f"Selected term: {test_case['Term']}")

                if test_case["Add-On Services"].strip().lower() == "yes":
                    kp.clickAddOnServicesTab()
                    logger.info(f"Clicked on Add-On Services tab")

                    kp.selectDataInfrastructureInsights(
                        test_case["Data Infrastructure Insights"]
                    )
                    logger.info(
                        f"Selected Data Infrastructure Insights: {test_case['Data Infrastructure Insights']}"
                    )

                    kp.enterKeystoneSupplementalServices_Subscription(
                        test_case["Keystone Supplemental Services_Subscription"]
                    )
                    logger.info(
                        f"Entered Keystone Supplemental Services: {test_case['Keystone Supplemental Services_Subscription']}"
                    )

                    kp.enterTotalQuantity_Networking(
                        test_case["Total Quantity_Networking"]
                    )
                    logger.info(
                        f"Entered Total Quantity Networking: {test_case['Total Quantity_Networking']}"
                    )

                    kp.selectNRDType_Support(test_case["NRD Type_Support"])
                    logger.info(
                        f"Selected NRD Type Support: {test_case['NRD Type_Support']}"
                    )

                    kp.selectManagedServices_ProfessionalServices(
                        test_case["Managed Services_Professional Services"]
                    )
                    logger.info(
                        f"Selected Managed Services Professional Services: {test_case['Managed Services_Professional Services']}"
                    )

                    kp.selectCountry(test_case["Country"])
                    logger.info(f"Selected Country: {test_case['Country']}")

                    kp.enterMigrationServices_DataMigrationAsService(
                        test_case["Migration Services_Data Migration as a Service"]
                    )
                    logger.info(
                        f"Entered Migration Services Data Migration as a Service: {test_case['Migration Services_Data Migration as a Service']}"
                    )

                    kp.selectOnsiteDelivery_TravelAndExpense(
                        test_case["Onsite Delivery_Travel and Expense"]
                    )
                    logger.info(
                        f"Entered Onsite Delivery Travel and Expense: {test_case['Onsite Delivery_Travel and Expense']}"
                    )

                    kp.enterTimeAndMaterials_Days(test_case["Time and Materials_Days"])
                    logger.info(
                        f"Entered Time and Materials Days: {test_case['Time and Materials_Days']}"
                    )

                    kp.selectOnsiteDelivery_TravelAndExpense_2(
                        test_case["Onsite Delivery_Travel and Expense_2"]
                    )
                    logger.info(
                        f"Entered Onsite Delivery Travel and Expense 2: {test_case['Onsite Delivery_Travel and Expense_2']}"
                    )

                    kp.selectSAMService(test_case["SAM Service"])
                    logger.info(f"Selected SAM Service: {test_case['SAM Service']}")

                # =====For Commerce validations reading BOM table details and saving to list for Keystone product=================================================================================
                if test_case["BOM Validation_Commerce"].strip().lower() == "yes":
                    cm.clickElementAndWait(
                        page_name="ConfigurePage",
                        element_name="bill_Of_Materials",
                        wait_time=5,
                    )
                    logger.info(f"Clicked on Bill of Materials tab")

                    print(
                        f"\n\033[94mℹ️ ================Capturing BOM Table Details and Saving to List for Keystone Product======================================================================\033[0m"
                    )
                    print(
                        f"\033[94mℹ️ Capturing BOM Table Details for Part Number and Saving to List\033[0m"
                    )
                    bom_list_part_number = cv.readBOMTable_SaveToList("Part Number")
                    logger.info(f"Read the BOM table details for Part Number")

                    print(
                        f"\n\033[94mℹ️ Capturing BOM Table Details for Quantity and Saving to List\033[0m"
                    )
                    bom_list_quantity = cv.readBOMTable_SaveToList("Quantity")
                    logger.info(f"Read the BOM table details for Quantity")

                    print(
                        f"\n\033[94mℹ️ Capturing BOM Table Details for Description and Saving to List\033[0m"
                    )
                    bom_list_description = cv.readBOMTable_SaveToList("Description")
                    logger.info(f"Read the BOM table details for Description")

                    cm.clickElement("ConfigurePage", "close_Button")
                    logger.info(f"Clicked on Close button in BOM table")
                    # =========================================================================================================================

                # =============Config BOM Validations for Keystone product==================================================================================
                if test_case["BOM Validation_Config"].strip().lower() == "yes":
                    cm.clickElementAndWait(
                        page_name="ConfigurePage",
                        element_name="bill_Of_Materials",
                        wait_time=5,
                    )
                    logger.info(f"Clicked on Bill of Materials tab")

                    bom_data_part_number = cv.readBOMTable("Part Number")
                    if bom_data_part_number:
                        logger.info(
                            f"Extracted Part Number from BOM table: {bom_data_part_number}"
                        )
                    else:
                        logger.info("No data extracted from the Part Number column.")

                    bom_data_quantity = cv.readBOMTable("Quantity")
                    if bom_data_quantity:
                        logger.info(
                            f"Extracted Quantity from BOM table: {bom_data_quantity}"
                        )
                    else:
                        logger.info("No data extracted from the Quantity column.")

                    bom_data_description = cv.readBOMTable("Description")
                    if bom_data_description:
                        logger.info(
                            f"Extracted Description from BOM table: {bom_data_description}"
                        )
                    else:
                        logger.info("No data extracted from the Description column.")

                    print(
                        f"\n\033[94mℹ️ ================Config BOM Validations for Keystone product===============================================================================================\033[0m"
                    )
                    print(f"\033[94mℹ️ Config BOM Validations Started: \033[0m\n")
                    # Validate BOM Table for Keystone Service 1
                    if is_valid_data(
                        test_case["OP_KeystoneService1"]
                    ) and is_valid_data(test_case["OQ_KeystoneService1"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}"
                        )
                        bom_validation_result_1 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_KeystoneService1"],
                            quantity=test_case["OQ_KeystoneService1"],
                        )
                        if bom_validation_result_1:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Keystone Service 2
                    if is_valid_data(
                        test_case["OP_KeystoneService2"]
                    ) and is_valid_data(test_case["OQ_KeystoneService2"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}"
                        )
                        bom_validation_result_2 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_KeystoneService2"],
                            quantity=test_case["OQ_KeystoneService2"],
                        )
                        if bom_validation_result_2:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Keystone Service 3
                    if is_valid_data(
                        test_case["OP_KeystoneService3"]
                    ) and is_valid_data(test_case["OQ_KeystoneService3"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}"
                        )
                        bom_validation_result_3 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_KeystoneService3"],
                            quantity=test_case["OQ_KeystoneService3"],
                        )
                        if bom_validation_result_3:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Keystone Service 4
                    if is_valid_data(
                        test_case["OP_KeystoneService4"]
                    ) and is_valid_data(test_case["OQ_KeystoneService4"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}"
                        )
                        bom_validation_result_4 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_KeystoneService4"],
                            quantity=test_case["OQ_KeystoneService4"],
                        )
                        if bom_validation_result_4:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                        # Validate BOM Table for Service Level DT
                    if is_valid_data(test_case["OP_ServiceLevelDT"]) and is_valid_data(
                        test_case["OQ_ServiceLevelDT"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}"
                        )
                        bom_validation_result_5 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_ServiceLevelDT"],
                            quantity=test_case["OQ_ServiceLevelDT"],
                        )
                        if bom_validation_result_5:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                        # Validate BOM Table for Object Service
                    if is_valid_data(test_case["OP_ObjectService"]) and is_valid_data(
                        test_case["OQ_ObjectService"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}"
                        )
                        bom_validation_result_6 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_ObjectService"],
                            quantity=test_case["OQ_ObjectService"],
                        )
                        if bom_validation_result_6:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for ADP Quantity
                    if is_valid_data(test_case["OP_ADPQty"]) and is_valid_data(
                        test_case["OQ_ADPQty"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}"
                        )
                        bom_validation_result_7 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_ADPQty"],
                            quantity=test_case["OQ_ADPQty"],
                        )
                        if bom_validation_result_7:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DIIEXT Quantity
                    if is_valid_data(test_case["OP_DIIEXT"]) and is_valid_data(
                        test_case["OQ_DIIEXT"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}"
                        )
                        bom_validation_result_8 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DIIEXT"],
                            quantity=test_case["OQ_DIIEXT"],
                        )
                        if bom_validation_result_8:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DIIPREM Quantity
                    if is_valid_data(test_case["OP_DIIPREM"]) and is_valid_data(
                        test_case["OQ_DIIPREM"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}"
                        )
                        bom_validation_result_9 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DIIPREM"],
                            quantity=test_case["OQ_DIIPREM"],
                        )
                        if bom_validation_result_9:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DIISTD Quantity
                    if is_valid_data(test_case["OP_DIISTD"]) and is_valid_data(
                        test_case["OQ_DIISTD"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}"
                        )
                        bom_validation_result_10 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DIISTD"],
                            quantity=test_case["OQ_DIISTD"],
                        )
                        if bom_validation_result_10:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DIIVAL Quantity
                    if is_valid_data(test_case["OP_DIIVAL"]) and is_valid_data(
                        test_case["OQ_DIIVAL"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}"
                        )
                        bom_validation_result_11 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DIIVAL"],
                            quantity=test_case["OQ_DIIVAL"],
                        )
                        if bom_validation_result_11:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DIIOBJSTD Quantity
                    if is_valid_data(test_case["OP_DIIOBJSTD"]) and is_valid_data(
                        test_case["OQ_DIIOBJSTD"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}"
                        )
                        bom_validation_result_12 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DIIOBJSTD"],
                            quantity=test_case["OQ_DIIOBJSTD"],
                        )
                        if bom_validation_result_12:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DIIOBJVAL Quantity
                    if is_valid_data(test_case["OP_DIIOBJVAL"]) and is_valid_data(
                        test_case["OQ_DIIOBJVAL"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}"
                        )
                        bom_validation_result_13 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DIIOBJVAL"],
                            quantity=test_case["OQ_DIIOBJVAL"],
                        )
                        if bom_validation_result_13:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Expedited Activation Quantity
                    if is_valid_data(
                        test_case["OP_ExpeditedActivation"]
                    ) and is_valid_data(test_case["OQ_ExpeditedActivation"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}"
                        )
                        bom_validation_result_14 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_ExpeditedActivation"],
                            quantity=test_case["OQ_ExpeditedActivation"],
                        )
                        if bom_validation_result_14:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Networking Quantity
                    if is_valid_data(test_case["OP_Networking"]) and is_valid_data(
                        test_case["OQ_Networking"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}"
                        )
                        bom_validation_result_15 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_Networking"],
                            quantity=test_case["OQ_Networking"],
                        )
                        if bom_validation_result_15:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for NRD Quantity
                    if is_valid_data(test_case["OP_NRD"]) and is_valid_data(
                        test_case["OQ_NRD"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}"
                        )
                        bom_validation_result_16 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_NRD"],
                            quantity=test_case["OQ_NRD"],
                        )
                        if bom_validation_result_16:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for USCS Quantity
                    if is_valid_data(test_case["OP_USCS"]) and is_valid_data(
                        test_case["OQ_USCS"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}"
                        )
                        bom_validation_result_17 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_USCS"],
                            quantity=test_case["OQ_USCS"],
                        )
                        if bom_validation_result_17:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for SAM Service Quantity
                    if is_valid_data(test_case["OP_SAMService"]) and is_valid_data(
                        test_case["OQ_SAMService"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}"
                        )
                        bom_validation_result_18 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_SAMService"],
                            quantity=test_case["OQ_SAMService"],
                        )
                        if bom_validation_result_18:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Fixed Scope Extreme Quantity
                    if is_valid_data(
                        test_case["OP_FixedScopeExtreme"]
                    ) and is_valid_data(test_case["OQ_FixedScopeExtreme"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}"
                        )
                        bom_validation_result_19 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_FixedScopeExtreme"],
                            quantity=test_case["OQ_FixedScopeExtreme"],
                        )
                        if bom_validation_result_19:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Fixed Scope Premium Quantity
                    if is_valid_data(
                        test_case["OP_FixedScopePremium"]
                    ) and is_valid_data(test_case["OQ_FixedScopePremium"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}"
                        )
                        bom_validation_result_20 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_FixedScopePremium"],
                            quantity=test_case["OQ_FixedScopePremium"],
                        )
                        if bom_validation_result_20:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Fixed Scope Standard Quantity
                    if is_valid_data(
                        test_case["OP_FixedScopeStandard"]
                    ) and is_valid_data(test_case["OQ_FixedScopeStandard"]):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}"
                        )
                        bom_validation_result_21 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_FixedScopeStandard"],
                            quantity=test_case["OQ_FixedScopeStandard"],
                        )
                        if bom_validation_result_21:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Fixed Scope Value Quantity
                    if is_valid_data(test_case["OP_FixedScopeValue"]) and is_valid_data(
                        test_case["OQ_FixedScopeValue"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}"
                        )
                        bom_validation_result_22 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_FixedScopeValue"],
                            quantity=test_case["OQ_FixedScopeValue"],
                        )
                        if bom_validation_result_22:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Custom Scope Quantity
                    if is_valid_data(test_case["OP_CustomeScope"]) and is_valid_data(
                        test_case["OQ_CustomeScope"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}"
                        )
                        bom_validation_result_23 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_CustomeScope"],
                            quantity=test_case["OQ_CustomeScope"],
                        )
                        if bom_validation_result_23:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for DMAAS Quantity
                    if is_valid_data(test_case["OP_DMAAS"]) and is_valid_data(
                        test_case["OQ_DMAAS"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}"
                        )
                        bom_validation_result_24 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_DMAAS"],
                            quantity=test_case["OQ_DMAAS"],
                        )
                        if bom_validation_result_24:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for T&M Quantity
                    if is_valid_data(test_case["OP_T&M"]) and is_valid_data(
                        test_case["OQ_T&M"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}"
                        )
                        bom_validation_result_25 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_T&M"],
                            quantity=test_case["OQ_T&M"],
                        )
                        if bom_validation_result_25:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    # Validate BOM Table for Partner Part Quantity
                    if is_valid_data(test_case["OP_PartnerPart"]) and is_valid_data(
                        test_case["OQ_PartnerPart"]
                    ):
                        logger.info(
                            f"Validating BOM Table for Part Number: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}"
                        )
                        bom_validation_result_26 = cv.validateBOMTable_Config(
                            part_number=test_case["OP_PartnerPart"],
                            quantity=test_case["OQ_PartnerPart"],
                        )
                        if bom_validation_result_26:
                            logger.info(
                                f"Validation passed for Part Number: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Part Number: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}\033[0m\n"
                            )
                        else:
                            failure_message = f"Validation failed for Part Number: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")

                    cm.clickElement("ConfigurePage", "close_Button")
                    logger.info(f"Clicked on Close button in BOM table")
                    # ===========================================================================================================================

                cm.clickElement("ConfigurePage", "add_To_Quote")
                logger.info(f"Clicked on Add to Quote button")

                if test_case["Target Site Readiness Date"].strip().lower() == "yes":
                    kp.selectTargetReadinessDate()
                    logger.info(f"Selected target readiness date")

                if test_case["Target Start Date"].strip().lower() == "yes":
                    kp.selectTarget_StartDate()
                    logger.info(f"Selected target start date")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

            # =============================Read LIG Product Table for Keystone===============================================================================
            if test_case["Capture LIG Table Details"].strip().lower() == "yes":
                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                pp.expandAllProducts()
                logger.info(f"Expanded all products in the LIG product table")

                # Download the Excel file containing the product table details
                file_path = cv.download_excel_file()
                logger.info(
                    f"Downloaded the Excel file containing the product table details: {file_path}"
                )

                # hpc.readProductTable(second_Tab, "Product")
                # logger.info(f"Reading Product column values from product LIG table")

                # hpc.readProductTable(second_Tab, "List Price")
                # logger.info(f"Reading List Price column values from product LIG table")

                # hpc.readProductTable(second_Tab, "Net Price")
                # logger.info(f"Reading Net Price column values from product LIG table")

                # ==================Reading Product table details and saving to list for Keystone=================================================================================
                if test_case["BOM Validation_Commerce"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Capturing LIG Table Details and Saving to List for Keystone Product=======================================================================\033[0m"
                    )
                    print(
                        f"\033[94mℹ️ Capturing LIG Table Details for Product Column and Saving to List\033[0m"
                    )
                    product_list_product = cv.readProductTable_Excel_SaveToList(
                        file_path, "Product"
                    )
                    logger.info(f"Read Product column values from product LIG table")

                    print(
                        f"\n\033[94mℹ️ Capturing LIG Table Details for Qty Column and Saving to List\033[0m"
                    )
                    product_list_qty = cv.readProductTable_Excel_SaveToList(
                        file_path, "Qty."
                    )
                    logger.info(f"Read Quantity column values from product LIG table")

                    print(
                        f"\n\033[94mℹ️ Capturing LIG Table Details for Part Description Column and Saving to List\033[0m"
                    )
                    product_list_part_description = (
                        cv.readProductTable_Excel_SaveToList(
                            file_path, "Part Description"
                        )
                    )
                    logger.info(
                        f"Read Part Description column values from product LIG table"
                    )
                # ==========================================================================================================================

                pp.collapseAllProducts()
                logger.info(f"Collapsed all products in the LIG product table")

                if test_case["Quote Status Validation"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Validating Keystone Quote Configured Status=================================================================================================\033[0m"
                    )
                    keystone_quote_status = cm.verifyElementStatus(
                        "HomePage_CPQ",
                        "quote_Status",
                        test_case["Quote Status_Configured"],
                    )
                    if not keystone_quote_status:
                        failure_message = (
                            f"Keystone Quote status is not in expected state: "
                            f"Expected '{test_case['Quote Status_Configured']}', but found something else."
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Verified Keystone quote status is in expected state {test_case['Quote Status_Configured']}: {keystone_quote_status}"
                        )
                        print(
                            f"\033[92m✅ Verified Keystone quote status is in expected state {test_case['Quote Status_Configured']}: {keystone_quote_status}\033[0m"
                        )
                # =============Config LIG table Validations for Keystone product==================================================================================
                if test_case["LIG Validation_Config"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Capturing LIG Table Details for Keystone Product============================================================================================\033[0m"
                    )
                    print(
                        f"\033[94mℹ️ Capturing LIG Table Details for Product Column\033[0m"
                    )
                    # Read Product column values from product LIG table
                    lig_product_column_data = cv.readProductTable_Excel(
                        file_path, "Product"
                    )
                    logger.info(
                        f"Read Product column values from product LIG table: {lig_product_column_data}"
                    )

                    print(
                        f"\n\033[94mℹ️ Capturing LIG Table Details for Qty Column\033[0m"
                    )
                    # Read Quantity column values from product LIG table
                    lig_quantity_column_data = cv.readProductTable_Excel(
                        file_path, "Qty."
                    )
                    logger.info(
                        f"Read Quantity column values from product LIG table: {lig_quantity_column_data}"
                    )

                    print(
                        f"\n\033[94mℹ️ ================Config LIG Validations for Keystone product=================================================================================================\033[0m"
                    )
                    print(f"\033[94mℹ️ Config LIG Validations Started: \033[0m\n")
                    # Validate BOM Table for Keystone Service 1 Quantity
                    if is_valid_data(
                        test_case["OP_KeystoneService1"]
                    ) and is_valid_data(test_case["OQ_KeystoneService1"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_KeystoneService1"],
                            test_case["OQ_KeystoneService1"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_KeystoneService1']} and Quantity: {test_case['OQ_KeystoneService1']}\033[0m\n"
                            )

                    # Validate BOM Table for Keystone Service 2 Quantity
                    if is_valid_data(
                        test_case["OP_KeystoneService2"]
                    ) and is_valid_data(test_case["OQ_KeystoneService2"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_KeystoneService2"],
                            test_case["OQ_KeystoneService2"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_KeystoneService2']} and Quantity: {test_case['OQ_KeystoneService2']}\033[0m\n"
                            )

                    # Validate BOM Table for Keystone Service 3 Quantity
                    if is_valid_data(
                        test_case["OP_KeystoneService3"]
                    ) and is_valid_data(test_case["OQ_KeystoneService3"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_KeystoneService3"],
                            test_case["OQ_KeystoneService3"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_KeystoneService3']} and Quantity: {test_case['OQ_KeystoneService3']}\033[0m\n"
                            )

                    # Validate BOM Table for Keystone Service 4 Quantity
                    if is_valid_data(
                        test_case["OP_KeystoneService4"]
                    ) and is_valid_data(test_case["OQ_KeystoneService4"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_KeystoneService4"],
                            test_case["OQ_KeystoneService4"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_KeystoneService4']} and Quantity: {test_case['OQ_KeystoneService4']}\033[0m\n"
                            )

                    # Validate BOM Table for Service Level DT Quantity
                    if is_valid_data(test_case["OP_ServiceLevelDT"]) and is_valid_data(
                        test_case["OQ_ServiceLevelDT"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_ServiceLevelDT"],
                            test_case["OQ_ServiceLevelDT"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_ServiceLevelDT']} and Quantity: {test_case['OQ_ServiceLevelDT']}\033[0m\n"
                            )

                    # Validate BOM Table for Object Service Quantity
                    if is_valid_data(test_case["OP_ObjectService"]) and is_valid_data(
                        test_case["OQ_ObjectService"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_ObjectService"],
                            test_case["OQ_ObjectService"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_ObjectService']} and Quantity: {test_case['OQ_ObjectService']}\033[0m\n"
                            )

                    # Validate BOM Table for ADP Quantity
                    if is_valid_data(test_case["OP_ADPQty"]) and is_valid_data(
                        test_case["OQ_ADPQty"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_ADPQty"],
                            test_case["OQ_ADPQty"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_ADPQty']} and Quantity: {test_case['OQ_ADPQty']}\033[0m\n"
                            )

                    # Validate BOM Table for DIIEXT Quantity
                    if is_valid_data(test_case["OP_DIIEXT"]) and is_valid_data(
                        test_case["OQ_DIIEXT"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DIIEXT"],
                            test_case["OQ_DIIEXT"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DIIEXT']} and Quantity: {test_case['OQ_DIIEXT']}\033[0m\n"
                            )

                    # Validate BOM Table for DIIPREM Quantity
                    if is_valid_data(test_case["OP_DIIPREM"]) and is_valid_data(
                        test_case["OQ_DIIPREM"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DIIPREM"],
                            test_case["OQ_DIIPREM"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DIIPREM']} and Quantity: {test_case['OQ_DIIPREM']}\033[0m\n"
                            )

                    # Validate BOM Table for DIISTD Quantity
                    if is_valid_data(test_case["OP_DIISTD"]) and is_valid_data(
                        test_case["OQ_DIISTD"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DIISTD"],
                            test_case["OQ_DIISTD"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DIISTD']} and Quantity: {test_case['OQ_DIISTD']}\033[0m\n"
                            )

                    # Validate BOM Table for DIIVAL Quantity
                    if is_valid_data(test_case["OP_DIIVAL"]) and is_valid_data(
                        test_case["OQ_DIIVAL"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DIIVAL"],
                            test_case["OQ_DIIVAL"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DIIVAL']} and Quantity: {test_case['OQ_DIIVAL']}\033[0m\n"
                            )

                    # Validate BOM Table for DIIOBJSTD Quantity
                    if is_valid_data(test_case["OP_DIIOBJSTD"]) and is_valid_data(
                        test_case["OQ_DIIOBJSTD"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DIIOBJSTD"],
                            test_case["OQ_DIIOBJSTD"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DIIOBJSTD']} and Quantity: {test_case['OQ_DIIOBJSTD']}\033[0m\n"
                            )

                    # Validate BOM Table for DIIOBJVAL Quantity
                    if is_valid_data(test_case["OP_DIIOBJVAL"]) and is_valid_data(
                        test_case["OQ_DIIOBJVAL"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DIIOBJVAL"],
                            test_case["OQ_DIIOBJVAL"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DIIOBJVAL']} and Quantity: {test_case['OQ_DIIOBJVAL']}\033[0m\n"
                            )

                    # Validate BOM Table for Expedited Activation Quantity
                    if is_valid_data(
                        test_case["OP_ExpeditedActivation"]
                    ) and is_valid_data(test_case["OQ_ExpeditedActivation"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_ExpeditedActivation"],
                            test_case["OQ_ExpeditedActivation"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_ExpeditedActivation']} and Quantity: {test_case['OQ_ExpeditedActivation']}\033[0m\n"
                            )

                    # Validate BOM Table for Networking Quantity
                    if is_valid_data(test_case["OP_Networking"]) and is_valid_data(
                        test_case["OQ_Networking"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_Networking"],
                            test_case["OQ_Networking"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_Networking']} and Quantity: {test_case['OQ_Networking']}\033[0m\n"
                            )

                    # Validate BOM Table for NRD Quantity
                    if is_valid_data(test_case["OP_NRD"]) and is_valid_data(
                        test_case["OQ_NRD"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_NRD"],
                            test_case["OQ_NRD"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_NRD']} and Quantity: {test_case['OQ_NRD']}\033[0m\n"
                            )

                    # Validate BOM Table for USCS Quantity
                    if is_valid_data(test_case["OP_USCS"]) and is_valid_data(
                        test_case["OQ_USCS"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_USCS"],
                            test_case["OQ_USCS"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_USCS']} and Quantity: {test_case['OQ_USCS']}\033[0m\n"
                            )

                    # Validate BOM Table for SAM Service Quantity
                    if is_valid_data(test_case["OP_SAMService"]) and is_valid_data(
                        test_case["OQ_SAMService"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_SAMService"],
                            test_case["OQ_SAMService"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_SAMService']} and Quantity: {test_case['OQ_SAMService']}\033[0m\n"
                            )

                    # Validate BOM Table for Fixed Scope Extreme Quantity
                    if is_valid_data(
                        test_case["OP_FixedScopeExtreme"]
                    ) and is_valid_data(test_case["OQ_FixedScopeExtreme"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_FixedScopeExtreme"],
                            test_case["OQ_FixedScopeExtreme"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_FixedScopeExtreme']} and Quantity: {test_case['OQ_FixedScopeExtreme']}\033[0m\n"
                            )

                    # Validate BOM Table for Fixed Scope Premium Quantity
                    if is_valid_data(
                        test_case["OP_FixedScopePremium"]
                    ) and is_valid_data(test_case["OQ_FixedScopePremium"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_FixedScopePremium"],
                            test_case["OQ_FixedScopePremium"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_FixedScopePremium']} and Quantity: {test_case['OQ_FixedScopePremium']}\033[0m\n"
                            )

                    # Validate BOM Table for Fixed Scope Standard Quantity
                    if is_valid_data(
                        test_case["OP_FixedScopeStandard"]
                    ) and is_valid_data(test_case["OQ_FixedScopeStandard"]):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_FixedScopeStandard"],
                            test_case["OQ_FixedScopeStandard"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_FixedScopeStandard']} and Quantity: {test_case['OQ_FixedScopeStandard']}\033[0m\n"
                            )

                    # Validate BOM Table for Fixed Scope Value Quantity
                    if is_valid_data(test_case["OP_FixedScopeValue"]) and is_valid_data(
                        test_case["OQ_FixedScopeValue"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_FixedScopeValue"],
                            test_case["OQ_FixedScopeValue"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_FixedScopeValue']} and Quantity: {test_case['OQ_FixedScopeValue']}\033[0m\n"
                            )

                    # Validate BOM Table for Custome Scope Quantity
                    if is_valid_data(test_case["OP_CustomeScope"]) and is_valid_data(
                        test_case["OQ_CustomeScope"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_CustomeScope"],
                            test_case["OQ_CustomeScope"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_CustomeScope']} and Quantity: {test_case['OQ_CustomeScope']}\033[0m\n"
                            )

                    # Validate BOM Table for DMAAS Quantity
                    if is_valid_data(test_case["OP_DMAAS"]) and is_valid_data(
                        test_case["OQ_DMAAS"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_DMAAS"],
                            test_case["OQ_DMAAS"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_DMAAS']} and Quantity: {test_case['OQ_DMAAS']}\033[0m\n"
                            )

                    # Validate BOM Table for T&M Quantity
                    if is_valid_data(test_case["OP_T&M"]) and is_valid_data(
                        test_case["OQ_T&M"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_T&M"],
                            test_case["OQ_T&M"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m\n")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_T&M']} and Quantity: {test_case['OQ_T&M']}\033[0m\n"
                            )

                    # Validate BOM Table for Partner Part Quantity
                    if is_valid_data(test_case["OP_PartnerPart"]) and is_valid_data(
                        test_case["OQ_PartnerPart"]
                    ):
                        validation_result = cv.validateProductTable_Excel_Config(
                            file_path,
                            test_case["OP_PartnerPart"],
                            test_case["OQ_PartnerPart"],
                        )
                        if not validation_result:
                            failure_message = f"Validation failed for Product: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}"
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Validated Product Table for Product: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}"
                            )
                            print(
                                f"\033[92m✅ Validation passed for Product: {test_case['OP_PartnerPart']} and Quantity: {test_case['OQ_PartnerPart']}\033[0m"
                            )
                # ====================================================================================================================================

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

            # ========================================Compare BOM and Product Table Details for Keystone=======================================================================
            if test_case["BOM Validation_Commerce"].strip().lower() == "yes":
                print(
                    f"\n\033[94mℹ️ ================Comparing BOM and LIG Table Details for Keystone Product==================================================================================\033[0m"
                )
                # Compare BOM and Product table details for Keystone
                comparison_result = cv.compareBomAndProduct_Tables(
                    bom_list_part_number,
                    bom_list_quantity,
                    bom_list_description,
                    product_list_product,
                    product_list_qty,
                    product_list_part_description,
                )
                if not comparison_result:
                    failure_message = "Comparison between BOM and Product table details for Keystone failed. Discrepancies found."
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        "Comparison between BOM and Product table details for Keystone passed successfully."
                    )
                    print(
                        "\033[92m✅ Comparison between BOM and Product table details for Keystone product verified successfully.\033[0m"
                    )

                # ==================Checking value presence in BOM Part Number list for Keystone==========================================
                if test_case["BOM Validation_Commerce"].strip().lower() == "yes":
                    if is_valid_data(test_case["BOM Part Number_Commerce"]):
                        print(
                            f"\n\033[94mℹ️ ================Validating Part Number in BOM Table for Keystone Product==================================================================================\033[0m"
                        )
                        print(
                            f"\033[94mℹ️ Verifying Part Number is present or not in BOM Table for Keystone Product\033[0m\n"
                        )
                        # Check if the text is present in the BOM Part Number list
                        is_present = cv.isValuePresentInList(
                            test_case["BOM Part Number_Commerce"],
                            bom_list_part_number,
                            "Part Number",
                        )
                        if is_present:
                            print(
                                f"\033[92m✅ '{test_case['BOM Part Number_Commerce']}' is present in the BOM Part Number list.\033[0m"
                            )
                            logger.info(
                                f"'{test_case['BOM Part Number_Commerce']}' is present in the BOM Part Number list."
                            )
                        else:
                            failure_message = f"'{test_case['BOM Part Number_Commerce']}' is NOT present in the BOM Part Number list."
                            validation_failures.append(
                                failure_message
                            )  # Add failure to the list
                            print(f"\033[91m❌ {failure_message}\033[0m")
                            logger.warning(failure_message)
                # =============================================================================================================
            """
            # ==================Expected Error Message Validation for Keystone(Internal Hardware Quote)=======================================================
            ar = ApprovalRequestPage(second_Tab)
            logger.info(f"ApprovalRequestPage instance created for the new tab")

            if test_case["Error Validation"].strip().lower() == "yes":
                if test_case["Initiate Approval_Keystone"].strip().lower() == "yes":
                    cm.clickElementAndWait(
                        page_name="ApprovalRequestPage",
                        element_name="initiate_Approval",
                        wait_time=10,
                    )
                    logger.info(f"Clicked on Initiate Approval button")

                cm.clickElement("HomePage_CPQ", "view_More_Link")
                logger.info(f"Clicked on View more link in Quote info section")

                actual_error_message = cm.readText("HomePage_CPQ", "error_Message")
                logger.info(f"Captured error message: {actual_error_message}")

                if is_valid_data(
                    test_case["Keystone Internal Hardware Quotes Error Message"]
                ):

                    print(
                        f"\n\033[94mℹ️ ================Validating Expected Error Message for Keystone(Internal Hardware Quote)==================================================================\033[0m"
                    )
                    comparison_result = cm.compareExpectedActualText(
                        actual_text=actual_error_message,
                        expected_text=test_case[
                            "Keystone Internal Hardware Quotes Error Message"
                        ],
                    )
                    if not comparison_result:
                        failure_message = f"Actual error message '{actual_error_message}' does not match expected error message '{test_case['Keystone Internal Hardware Quotes Error Message']}'."
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual error message: {actual_error_message} with expected error message: {test_case['Keystone Internal Hardware Quotes Error Message']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual error message: {actual_error_message} with expected error message: {test_case['Keystone Internal Hardware Quotes Error Message']}\033[0m"
                        )

                cm.clickElement("HomePage_CPQ", "close_Button")
                logger.info(f"Clicked on Close button in Home Page CPQ")

            # ==================Configure Internal Hardware Quote==============================================================
            if (
                test_case["Configure Intenal Engineering Quote"].strip().lower()
                == "yes"
            ):
                first_Tab = cm.switchToTab(
                    page.context, tab_index=0, expected_tab_count=2
                )
                logger.info("Switched to the first tab ")

                hp = HomePage(first_Tab)
                logger.info(f"HomePage instance created for the new tab")

                hp.createQuote()
                logger.info(f"Clicked on create quote")

                third_Tab = cm.switchToTab(
                    page.context, tab_index=2, expected_tab_count=3
                )
                logger.info(
                    "Switched to the new tab after clicking on Create Quote option"
                )

                # Create an instance of HomePageCPQ for the new tab
                hpc = HomePageCPQ(third_Tab)
                logger.info(f"HomePageCPQ instance created for the new tab")
                ss = ScreenshotUtil(third_Tab)
                logger.info(f"ScreenshotUtil instance created for the new tab")
                hp = HomePage(third_Tab)
                logger.info(f"HomePage instance created for the new tab")
                cm = CommonMethods(third_Tab, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")
                cv = CommonValidations(third_Tab)
                logger.info(f"CommonValidations instance created for the new tab")
                qip = QuoteInfoPage(third_Tab)
                logger.info(f"QuoteInfoPage instance created for the new tab")
                kp = HomePageKeystone(third_Tab)
                logger.info(f"Keystone Page instance created for the new tab")

                cm.clickElementAndWait(
                    page_name="QuoteInfoPage",
                    element_name="save_Button",
                    wait_time=5,
                )
                logger.info(f"Clicked on save button")

                # ========================Enter Quote Info tab details for Internal Engineering Quote========================================================
                qip.selectOrderType(test_case["Order Type"])
                logger.info(f"Selected order type: {test_case['Order Type']}")

                qip.selectSubQuoteType(test_case["Sub Quote Type"])
                logger.info(f"Selected sub quote type: {test_case['Sub Quote Type']}")

                qip.selectConfirmYourSelection(test_case["Confirm Your Selection"])
                logger.info(
                    f"Clicked on {test_case['Confirm Your Selection']} for Confirm your selection "
                )

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

                # =======================Capture Internal Engineering Quote Details==============================================================================
                # Perform actions on the new tab
                if test_case["Capture Quote Details_2"].strip().lower() == "yes":
                    internal_quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                    logger.info(
                        f"Internal Engineering Quote Number: {internal_quote_number}"
                    )
                    print(
                        f"\n\033[94mℹ️ ================Capturing Internal Engineering Quote Details=============================================================================================\033[0m"
                    )
                    print(
                        f"\033[94mℹ️ Internal Engineering Quote Number: {internal_quote_number}\033[0m"
                    )

                    internal_quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                    logger.info(
                        f"Internal Engineering Quote Name: {internal_quote_name}"
                    )
                    print(
                        f"\033[94mℹ️ Internal Engineering Quote Name: {internal_quote_name}\033[0m"
                    )

                    internal_quote_cpq_url = cm.getCurrentURL()
                    logger.info(
                        f"Internal Engineering CPQ URL: {internal_quote_cpq_url}"
                    )
                    print(
                        f"\033[94mℹ️ Internal Engineering CPQ URL: {internal_quote_cpq_url}\033[0m"
                    )

                    internal_quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                    logger.info(
                        f"Internal Engineering Quote Status: {internal_quote_status}"
                    )
                    ss.capture_screenshot("Captured Internal Quote details")

                    if test_case["Quote Status Validation"].strip().lower() == "yes":
                        print(
                            f"\n\033[94mℹ️ ================Validating Internal Engineering Quote for Draft Status=====================================================================================\033[0m"
                        )
                        internal_quote_status = cm.verifyElementStatus(
                            "HomePage_CPQ",
                            "quote_Status",
                            test_case["Quote Status_Draft"],
                        )
                        if not internal_quote_status:
                            failure_message = (
                                f"Internal Engineering Quote status is not in expected state: "
                                f"Expected '{test_case['Quote Status_Draft']}', but found something else."
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:  # Validation passed
                            logger.info(
                                f"Verified Internal Engineering quote status is in expected state {test_case['Quote Status_Draft']}: {internal_quote_status}"
                            )
                            print(
                                f"\033[92m✅ Verified Internal Engineering quote status is in expected state {test_case['Quote Status_Draft']}: {internal_quote_status}\033[0m"
                            )

                # ======================Configure FAS/AFF/ASA/AFX Product for Internal Quote================================================================
                pp = ProductsPage(third_Tab)
                logger.info(f"ProductsPage instance created for the new tab")

                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                cm.clickElement("ProductsPage", "configure_Button")
                logger.info(f"Clicked on Configure button")

                hpFAS = HomePageFAS_AFF_ASA_AFX(third_Tab)
                logger.info(f"HomePageFAS_AFF_ASA_AFX instance created for the new tab")

                if is_valid_data(test_case["Product_2"]):
                    hpFAS.clickProductName(test_case["Product_2"])
                    logger.info(f"Clicked on product: {test_case['Product_2']}")

                if is_valid_data(test_case["Sub Product_2"]):
                    hpFAS.selectSubProduct(test_case["Sub Product_2"])
                    logger.info(f"Clicked on sub-product: {test_case['Sub Product_2']}")

                if is_valid_data(test_case["Cluster_2"]):
                    hpFAS.configureCluster(test_case["Cluster_2"])
                    logger.info(f"Clicked on cluster: {test_case['Cluster_2']}")

                hpFAS.access_SelectAll()
                logger.info(f"Accessed select all option under access tab")

                if is_valid_data(test_case["Model_2"]):
                    hpFAS.selectSystemModel(test_case["Model_2"])
                    logger.info(f"Selected Model: {test_case['Model_2']}")

                hpFAS.clickAddHaPair()
                logger.info(f"Clicked on Add HA Pair button")

                hpFAS.clickConfigureButton()
                logger.info(f"Clicked on configure button")

                hpFAS.clickStorageTab()
                logger.info(f"Clicked on storage tab")

                if is_valid_data(test_case["Drive Type_Base Storage_2"]):
                    hpFAS.selectDriveType_BaseStorage(
                        test_case["Drive Type_Base Storage_2"]
                    )
                    logger.info(
                        f"Selected drive type: {test_case['Drive Type_Base Storage_2']}"
                    )

                if is_valid_data(test_case["Drive Pack Qty_Base Storage_2"]):
                    hpFAS.enterDrivePackQty_BaseStorage(
                        test_case["Drive Pack Qty_Base Storage_2"]
                    )
                    logger.info(
                        f"Selected drive pack qty: {test_case['Drive Pack Qty_Base Storage_2']}"
                    )

                hpFAS.clickTabNICsandAdapters()
                logger.info(f"Clicked on Nics and Adapters tab")

                # if is_valid_data(test_case["Cable Type_Adapters_2"]):
                # hpFAS.selectCableType_Adapters(test_case["Cable Type_Adapters_2"])
                # logger.info(
                # f"Selected cable type: {test_case['Cable Type_Adapters_2']}"
                # )

                # if is_valid_data(test_case["Cable Length_Adapters_2"]):
                # hpFAS.selectCableLength_Adapters(
                # test_case["Cable Length_Adapters_2"]
                # )
                # logger.info(
                # f"Selected cable length: {test_case['Cable Length_Adapters_2']}"
                # )

                if is_valid_data(test_case["Select Adapters to Add_1"]):
                    hpFAS.selectAdaptersToAdd(test_case["Select Adapters to Add_1"])
                    logger.info(
                        f"Selected Adapters to add as: {test_case['Select Adapters to Add_1']}"
                    )

                if is_valid_data(test_case["Select Adapters to Add_2"]):
                    hpFAS.selectAdaptersToAdd(test_case["Select Adapters to Add_2"])
                    logger.info(
                        f"Selected Adapters to add as: {test_case['Select Adapters to Add_2']}"
                    )

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

                hpFAS.clickNetappConsoleDeployment()
                logger.info(
                    f"Clicked No button for Do you want to add the NetApp Console Deployment Service"
                )

                hpFAS.clickAddToQuote()
                logger.info(f"Clicked on Add to Quote button")

                # =============================Read LIG Product Table for Internal Engineering Quote===============================================================================
                if test_case["Capture LIG Table Details_2"].strip().lower() == "yes":
                    cm.clickElement("ProductsPage", "products_Tab")
                    logger.info(f"Clicked on Products tab")

                    logger.info(
                        f"Checking for the dynamic popup, if exists then closed the popup"
                    )
                    cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                    pp.expandAllProducts()
                    logger.info(f"Expanded all products in the LIG product table")

                    # hpc.readProductTable(third_Tab, "Product")
                    # logger.info(f"Reading Product column values from product LIG table")

                    # hpc.readProductTable(third_Tab, "List Price")
                    # logger.info(
                    # f"Reading List Price column values from product LIG table"
                    # )

                    # hpc.readProductTable(third_Tab, "Net Price")
                    # logger.info(
                    # f"Reading Net Price column values from product LIG table"
                    # )
                    # =================Zero Net Price Validation for Internal Engineering Quote==============================
                    if test_case["Zero Net Price Validation"].strip().lower() == "yes":
                        print(
                            f"\n\033[94mℹ️ ================Validating Internal Engineering Quote for Zero Net Price=================================================================================\033[0m"
                        )
                        netPrice = cm.readText("HomePage_CPQ", "net_Price")
                        logger.info(f"Net Price value: {netPrice}")

                        cv.validateZeroNetPrice(netPrice)
                        logger.info(f"Validated that the Net Price is zero: {netPrice}")

                        # Validate Net Price for all rows in the table
                        validationResults = cv.readProductTableAndValidateZeroNetPrice(
                            third_Tab, "Net Price"
                        )
                        logger.info(
                            f"Validation results for Net Price column: {validationResults}"
                        )
                        # Check if all rows passed validation
                        if all(validationResults):
                            logger.info(
                                "All rows with Net Price values are correctly set to 0."
                            )
                            print(
                                f"\033[92m✅ All rows with Net Price values are correctly set to 0.\033[0m"
                            )
                        else:
                            failure_message = (
                                "Some rows with Net Price values are incorrect."
                            )
                            validation_failures.append(
                                failure_message
                            )  # Add failure to the list
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")

                        print(
                            f"\n\033[94mℹ️ ================Validating Internal Engineering Quote for Eligible Discount==============================================================================\033[0m"
                        )
                        validation_result = (
                            kp.validateEligibleDiscountForInternalEngineering(third_Tab)
                        )
                        if not validation_result:
                            failure_message = "Validation failed for Eligible Discount Source and Eligible Discount for Internal Engineering Quote."
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                "Completed validation for Eligible Discount Source and Eligible Discount for Internal Engineering Quote."
                            )
                            print(
                                "\033[92m✅ Completed validation for Eligible Discount Source and Eligible Discount for Internal Engineering Quote.\033[0m"
                            )

                    # =================================================================================================
                    pp.collapseAllProducts()
                    logger.info(f"Collapsed all products in the LIG product table")

                    if test_case["Quote Status Validation"].strip().lower() == "yes":
                        print(
                            f"\n\033[94mℹ️ ================Validating Internal Engineering Quote for Configured Status================================================================================\033[0m"
                        )
                        internal_quote_status = cm.verifyElementStatus(
                            "HomePage_CPQ",
                            "quote_Status",
                            test_case["Quote Status_Configured"],
                        )
                        if not internal_quote_status:
                            failure_message = (
                                f"Internal Engineering Quote status is not in expected state: "
                                f"Expected '{test_case['Quote Status_Configured']}', but found something else."
                            )
                            validation_failures.append(failure_message)
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:  # Validation passed
                            logger.info(
                                f"Verified Internal Engineering quote status is in expected state {test_case['Quote Status_Configured']}: {internal_quote_status}"
                            )
                            print(
                                f"\033[92m✅ Verified Internal Engineering quote status is in expected state {test_case['Quote Status_Configured']}: {internal_quote_status}\033[0m"
                            )

                    cm.clickElementAndWait(
                        page_name="HomePage_CPQ",
                        element_name="save_Icon",
                        wait_time=10,
                    )
                    logger.info(f"Clicked on Save button")

            # ==============Enter Internal Engineering Quote Number in Keystone Products tab======================================================
            if test_case["Add Internal Hardware Quote"].strip().lower() == "yes":

                second_Tab = cm.switchToTab(
                    page.context, tab_index=1, expected_tab_count=3
                )
                logger.info("Switched to the second tab")

                pp = ProductsPage(second_Tab)
                logger.info(f"ProductsPage instance created for the new tab")
                ss = ScreenshotUtil(second_Tab)
                logger.info(f"ScreenshotUtil instance created for the new tab")
                cm = CommonMethods(second_Tab, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")

                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                cm.enterText(
                    "ProductsPage",
                    "keystone_Internal_HardwareQuotes",
                    internal_quote_number,
                )
                logger.info(
                    f"Entered Keystone Internal Hardware Quotes: {internal_quote_number}"
                )

                cm.clickElementAndWait(
                    page_name="ProductsPage",
                    element_name="link_Hardware_Quote",
                    wait_time=5,
                )

            # ===============================Account Information Tab for Keystone=================================================================================
            aip = AccountInformationPage(second_Tab)
            logger.info(f"AccountInformationPage instance created for the new tab")

            if test_case["Add Account Information_Keystone"].strip().lower() == "yes":
                cm.refreshPage(timeout=10000)
                logger.info(f"Refreshed the page to load Account Information tab")

                cm.clickElement("AccountInformationPage", "account_Information_Tab")
                logger.info(f"Clicked on Account Information Tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                if test_case["Sold To_1"].strip().lower() == "yes":
                    if is_valid_data(test_case["First Name_Sold To_1"]):
                        aip.enterSoldTo(
                            test_case["First Name_Sold To_1"],
                            test_case["Last Name_Sold To_1"],
                        )
                        logger.info(
                            f"Entered Sold To details: {test_case['First Name_Sold To_1']}, {test_case['Last Name_Sold To_1']}"
                        )

                if test_case["Bill To_1"].strip().lower() == "yes":
                    aip.enterBillTo()
                    logger.info(f"Entered Bill To details")

                if test_case["End Customer_1"].strip().lower() == "yes":
                    if is_valid_data(test_case["First Name_End Customer_1"]):
                        aip.enterEndCustomer(
                            test_case["First Name_End Customer_1"],
                            test_case["Last Name_End Customer_1"],
                        )
                        logger.info(
                            f"Entered End Customer details: {test_case['First Name_End Customer_1']}, {test_case['Last Name_End Customer_1']}"
                        )

                if test_case["Service Customer_1"].strip().lower() == "yes":
                    aip.enterServiceCustomer()
                    logger.info(f"Entered Service Customer details")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

            # =======================================Approval Request Tab for Keystone=================================================================================
            ar = ApprovalRequestPage(second_Tab)
            logger.info(f"ApprovalRequestPage instance created for the new tab")

            if test_case["Initiate Approval_Keystone"].strip().lower() == "yes":
                cm.clickElement("ApprovalRequestPage", "approval_Request_Tab")
                logger.info(f"Clicked on Approval request tab")

                cm.clickElementAndWait(
                    page_name="ApprovalRequestPage",
                    element_name="initiate_Approval",
                    wait_time=10,
                )
                logger.info(f"Clicked on Initiate Approval button")

            # ======================================Attachments Tab for Keystone=================================================================================
            ap = AttachmentsPage(second_Tab)
            logger.info(f"AttachmentsPage instance created for the new tab")

            if test_case["Add Attachment_Keystone"].strip().lower() == "yes":
                cm.clickElement("AttachmentsPage", "attachments_Tab")
                logger.info(f"Clicked on Attachments tab")

                ap.selectDragAndDrop_PDF()
                logger.info(f"Selected file to upload")

                if is_valid_data(test_case["Attachment Type_1"]):
                    ap.selectAttachmentType(test_case["Attachment Type_1"])
                    logger.info(
                        f"Selected attachment type: {test_case['Attachment Type_1']}"
                    )

                if is_valid_data(test_case["Attachment Description_1"]):
                    ap.enterAttachmentDescription(test_case["Attachment Description_1"])
                    logger.info(
                        f"Entered attachment description: {test_case['Attachment Description_1']}"
                    )

                cm.clickElement("AttachmentsPage", "upload_Button")
                logger.info(f"Clicked on upload button")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

                if test_case["Quote Status Validation"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Validating Keystone Quote for Orderable Status============================================================================================\033[0m"
                    )
                    keystone_quote_status = cm.verifyElementStatus(
                        "HomePage_CPQ",
                        "quote_Status",
                        test_case["Quote Status_Orderable"],
                    )
                    if not keystone_quote_status:
                        failure_message = (
                            f"Keystone Quote status is not in expected state: "
                            f"Expected '{test_case['Quote Status_Orderable']}', but found something else."
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Verified Keystone quote status is in expected state {test_case['Quote Status_Orderable']}: {keystone_quote_status}"
                        )
                        print(
                            f"\033[92m✅ Verified Keystone quote status is in expected state {test_case['Quote Status_Orderable']}: {keystone_quote_status}\033[0m"
                        )

            # ==============================Purchase Order Tab for Keystone=================================================================================
            po = PurchaseOrderPage(second_Tab)
            logger.info(f"PurchaseOrderPage instance created for the new tab")

            if test_case["Submit PO_Keystone"].strip().lower() == "yes":
                cm.clickElement("PurchaseOrderPage", "purchase_Order_Tab")
                logger.info(f"Clicked on Purchase order tab")

                cm.enterTextAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="purchase_Order_Number",
                    text=keystone_quote_number,
                    wait_time=3,
                )
                logger.info(f"Entered PO number: {keystone_quote_number}")

                po.enterPODate()
                logger.info(f"Entered PO date")

                if is_valid_data(test_case["PO Email_1"]):
                    cm.enterText(
                        "PurchaseOrderPage", "po_Email", test_case["PO Email_1"]
                    )
                    logger.info(f"Entered PO email: {test_case['PO Email_1']}")

                if is_valid_data(test_case["PO Comments_1"]):
                    cm.enterText(
                        "PurchaseOrderPage", "po_Comments", test_case["PO Comments_1"]
                    )
                    logger.info(f"Entered PO comments: {test_case['PO Comments_1']}")

                cm.clickElementAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="submit_PO_Button",
                    wait_time=20,
                )
                logger.info(f"Clicked on Submit PO button")

                keystone_quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                logger.info(f"Quote Status: {keystone_quote_status}")

                print(
                    f"\n\033[94mℹ️ ================Validating Keystone Quote PO Submitted Status============================================================================================\033[0m"
                )
                keystone_quote_status = cm.verifyElementStatus(
                    "HomePage_CPQ", "quote_Status", "PO Submitted"
                )
                if not keystone_quote_status:
                    failure_message = (
                        f"Keystone Quote status is not in expected state: "
                        f"Expected 'PO Submitted', but found something else."
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Verified Keystone quote status is in expected state PO Submitted: {keystone_quote_status}"
                    )
                    print(
                        f"\033[92m✅ Verified Keystone quote status is in expected state PO Submitted: {keystone_quote_status}\033[0m"
                    )
                ss.capture_screenshot("Captured Keystone quote PO submission status")

            # ======================================TPD for Keystone=========================================================================================
            thp = TPDHomePage(second_Tab)
            logger.info(f"TPDHomePage instance created for the new tab")

            if test_case["Accept in TPD_Keystone"].strip().lower() == "yes":
                if is_valid_data(test_case["TPD URL"]):
                    cm.navigateToUrl(test_case["TPD URL"])
                    logger.info(f"Navigated to TPD URL: {test_case['TPD URL']}")

                cm.clickElement("HomePage_TPD", "global_Search")
                logger.info(f"Clicked on global search")

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", keystone_quote_number
                )
                logger.info(f"Searched by transaction number: {keystone_quote_number}")

                cm.enterText("HomePage_TPD", "po_Number", keystone_quote_number)
                logger.info(f"Searched by PO number: {keystone_quote_number}")

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

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", keystone_quote_number
                )
                logger.info(
                    f"Searched by transaction number in {tpd_subProcessStatus}: {keystone_quote_number}"
                )

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button in {tpd_subProcessStatus}")

                thp.clickSearchQuote(keystone_quote_number)
                logger.info(
                    f"Clicked on quote link in {tpd_subProcessStatus}: {keystone_quote_number}"
                )

                cm.selectOptionInListbox("HomePage_TPD", "actions_DD", "Accepted")
                logger.info(f"Selected Accepted from Actions dropdown")

                cm.clickElement("HomePage_TPD", "actions_Go_Button")
                logger.info(f"Clicked on Actions Go button")

                cm.clickElementAndWait(
                    "HomePage_TPD",
                    "yes_Button",
                    wait_time=5,
                )
                logger.info(f"Clicked on Yes button in confirmation pop-up")
                ss.capture_screenshot("Captured TPD details for Keystone quote")

                cm.clickElement("HomePage_TPD", "global_Search")
                logger.info(f"Clicked on global search")

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", keystone_quote_number
                )
                logger.info(f"Searched by transaction number: {keystone_quote_number}")

                cm.enterText("HomePage_TPD", "po_Number", keystone_quote_number)
                logger.info(f"Searched by PO number: {keystone_quote_number}")

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button")

                tpd_orderStatus = cm.readText("HomePage_TPD", "order_Status")
                logger.info(f"Captured order status: {tpd_orderStatus}")

                if test_case["TPD Validation"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Keystone TPD Validation for Order Status=================================================================================================\033[0m"
                    )
                    comparison_result = cm.checkExpectedTextInActual(
                        actual_text=tpd_orderStatus,
                        expected_text=test_case["Order Status"],
                    )
                    if not comparison_result:
                        failure_message = f"Actual order status '{tpd_orderStatus}' does not match expected order status '{test_case['Order Status']}'."
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual order status: {tpd_orderStatus} with expected order status: {test_case['Order Status']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual order status: {tpd_orderStatus} with expected order status: {test_case['Order Status']}\033[0m"
                        )

            # ========================Account Information Tab for Internal Engineering Quote=================================================================================
            third_Tab = cm.switchToTab(page.context, tab_index=2, expected_tab_count=3)
            logger.info("Switched to the third tab")

            aip = AccountInformationPage(third_Tab)
            logger.info(f"AccountInformationPage instance created for the new tab")
            cm = CommonMethods(third_Tab, locator_manager)
            logger.info(f"CommonMethods instance created for the new tab")
            ss = ScreenshotUtil(third_Tab)
            logger.info(f"ScreenshotUtil instance created for the new tab")

            if (
                test_case["Add Account Information_Internal Engineering"]
                .strip()
                .lower()
                == "yes"
            ):
                cm.refreshPage(timeout=10000)
                logger.info(f"Refreshed the page to load Account Information tab")

                cm.clickElement("AccountInformationPage", "account_Information_Tab")
                logger.info(f"Clicked on Account Information Tab")

                logger.info(
                    f"Checking for the dynamic popup, if exists then closed the popup"
                )
                cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                if test_case["Sold To_2"].strip().lower() == "yes":
                    if is_valid_data(test_case["First Name_Sold To_2"]):
                        aip.enterSoldTo(
                            test_case["First Name_Sold To_2"],
                            test_case["Last Name_Sold To_2"],
                        )
                        logger.info(
                            f"Entered Sold To details: {test_case['First Name_Sold To_2']}, {test_case['Last Name_Sold To_2']}"
                        )

                if test_case["Bill To_2"].strip().lower() == "yes":
                    aip.enterBillTo()
                    logger.info(f"Entered Bill To details")

                if test_case["End Customer_2"].strip().lower() == "yes":
                    if is_valid_data(test_case["First Name_End Customer_2"]):
                        aip.enterEndCustomer(
                            test_case["First Name_End Customer_2"],
                            test_case["Last Name_End Customer_2"],
                        )
                        logger.info(
                            f"Entered End Customer details: {test_case['First Name_End Customer_2']}, {test_case['Last Name_End Customer_2']}"
                        )

                if test_case["Software Delivery_2"].strip().lower() == "yes":
                    aip.enterSoftwareDelivery()
                    logger.info(f"Entered Software Delivery details")

                if test_case["Ship To Customer_2"].strip().lower() == "yes":
                    aip.enterShipToCustomer()
                    logger.info(f"Entered Ship To Customer details")

                if is_valid_data(test_case["Internal Order Type"]):
                    aip.selectInternalOrderType(test_case["Internal Order Type"])
                    logger.info(
                        f"Selected Internal Order Type: {test_case['Internal Order Type']}"
                    )

                if is_valid_data(test_case["GL Account"]):
                    aip.selectGLAccount(test_case["GL Account"])
                    logger.info(f"Selected GL Account: {test_case['GL Account']}")

                if is_valid_data(test_case["Project Code"]):
                    aip.selectProjectCode(test_case["Project Code"])
                    logger.info(f"Selected Project Code: {test_case['Project Code']}")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

            # ============================Approval Request Tab for Internal Engineering Quote=================================================================================
            ar = ApprovalRequestPage(third_Tab)
            logger.info(f"ApprovalRequestPage instance created for the new tab")

            if (
                test_case["Initiate Approval_Internal Engineering"].strip().lower()
                == "yes"
            ):
                cm.clickElement("ApprovalRequestPage", "approval_Request_Tab")
                logger.info(f"Clicked on Approval request tab")

                cm.clickElementAndWait(
                    page_name="ApprovalRequestPage",
                    element_name="initiate_Approval",
                    wait_time=10,
                )
                logger.info(f"Clicked on Initiate Approval button")

                # =====================Approval Status Validation for Internal Engineering Quote=========================
                if test_case["Approval Status Validation"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Approval Status Validation for Internal Engineering Quote================================================================================\033[0m"
                    )
                    internal_approval_status = cm.readText(
                        "HomePage_CPQ", "approval_Status"
                    )
                    logger.info(f"Approval Status: {internal_approval_status}")

                    comparison_result = cm.compareExpectedActualText(
                        actual_text=internal_approval_status,
                        expected_text=test_case["Approval Status"],
                    )
                    if not comparison_result:
                        failure_message = f"Actual approval status '{internal_approval_status}' does not match expected approval status '{test_case['Approval Status']}'."
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual approval status: {internal_approval_status} with expected approval status: {test_case['Approval Status']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual approval status: {internal_approval_status} with expected approval status: {test_case['Approval Status']}\033[0m"
                        )
                # ========================================================================================================

            # ======================================Attachments Tab for Internal Engineering=================================================================================
            ap = AttachmentsPage(third_Tab)
            logger.info(f"AttachmentsPage instance created for the new tab")

            if (
                test_case["Add Attachment_Internal Engineering"].strip().lower()
                == "yes"
            ):
                cm.refreshPage(timeout=10000)
                logger.info(f"Refreshed the page to load Account Information tab")

                cm.clickElement("AttachmentsPage", "attachments_Tab")
                logger.info(f"Clicked on Attachments tab")

                ap.selectDragAndDrop_PDF()
                logger.info(f"Selected file to upload")

                if is_valid_data(test_case["Attachment Type_2"]):
                    ap.selectAttachmentType(test_case["Attachment Type_2"])
                    logger.info(
                        f"Selected attachment type: {test_case['Attachment Type_2']}"
                    )

                if is_valid_data(test_case["Attachment Description_2"]):
                    ap.enterAttachmentDescription(test_case["Attachment Description_2"])
                    logger.info(
                        f"Entered attachment description: {test_case['Attachment Description_2']}"
                    )

                cm.clickElement("AttachmentsPage", "upload_Button")
                logger.info(f"Clicked on upload button")

                cm.clickElementAndWait(
                    page_name="HomePage_CPQ",
                    element_name="save_Icon",
                    wait_time=10,
                )
                logger.info(f"Clicked on Save button")

                if test_case["Quote Status Validation"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Validating Internal Engineering Quote for Orderable Status================================================================================\033[0m"
                    )
                    internal_quote_status = cm.verifyElementStatus(
                        "HomePage_CPQ",
                        "quote_Status",
                        test_case["Quote Status_Orderable"],
                    )
                    if not internal_quote_status:
                        failure_message = (
                            f"Internal Engineering Quote status is not in expected state: "
                            f"Expected '{test_case['Quote Status_Orderable']}', but found something else."
                        )
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Verified Internal Engineering quote status is in expected state {test_case['Quote Status_Orderable']}: {internal_quote_status}"
                        )
                        print(
                            f"\033[92m✅ Verified Internal Engineering quote status is in expected state {test_case['Quote Status_Orderable']}: {internal_quote_status}\033[0m"
                        )

            # ==========================Capture Subscription Number from TPD for Keystone =================================================================================
            second_Tab = cm.switchToTab(page.context, tab_index=1, expected_tab_count=3)
            logger.info("Switched to the second tab")

            thp = TPDHomePage(second_Tab)
            logger.info(f"TPDHomePage instance created for the new tab")
            cm = CommonMethods(second_Tab, locator_manager)
            logger.info(f"CommonMethods instance created for the new tab")

            if test_case["Accept in TPD_Keystone"].strip().lower() == "yes":
                if is_valid_data(test_case["TPD URL"]):
                    cm.navigateToUrl(test_case["TPD URL"])
                    logger.info(f"Navigated to TPD URL: {test_case['TPD URL']}")

                cm.clickElement("HomePage_TPD", "global_Search")
                logger.info(f"Clicked on global search")

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", keystone_quote_number
                )
                logger.info(f"Searched by transaction number: {keystone_quote_number}")

                cm.enterText("HomePage_TPD", "po_Number", keystone_quote_number)
                logger.info(f"Searched by PO number: {keystone_quote_number}")

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button")

                print(
                    f"\n\033[94mℹ️ ================Captured TPD Subscription Number for Keystone============================================================================================\033[0m"
                )
                keystone_subscription_number = cm.readText(
                    "HomePage_TPD", "subscription_Number"
                )
                logger.info(
                    f"Captured Keystone subscription number: {keystone_subscription_number}"
                )
                print(f"Captured subscription number: {keystone_subscription_number}")

            # ==========================Purchase Order Tab for Internal Engineering=================================================================================
            third_Tab = cm.switchToTab(page.context, tab_index=2, expected_tab_count=3)
            logger.info("Switched to the new tab after clicking on Create Quote option")

            po = PurchaseOrderPage(third_Tab)
            logger.info(f"PurchaseOrderPage instance created for the new tab")
            cm = CommonMethods(third_Tab, locator_manager)
            logger.info(f"CommonMethods instance created for the new tab")

            if test_case["Submit PO_Internal Engineering"].strip().lower() == "yes":
                cm.clickElement("PurchaseOrderPage", "purchase_Order_Tab")
                logger.info(f"Clicked on Purchase order tab")

                cm.enterTextAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="purchase_Order_Number",
                    text=internal_quote_number,
                    wait_time=3,
                )
                logger.info(f"Entered PO number: {internal_quote_number}")

                po.enterPODate()
                logger.info(f"Entered PO date")

                if is_valid_data(test_case["PO Comments_2"]):
                    cm.enterText(
                        "PurchaseOrderPage", "po_Comments", test_case["PO Comments_2"]
                    )
                    logger.info(f"Entered PO comments: {test_case['PO Comments_2']}")

                cm.enterText(
                    "PurchaseOrderPage",
                    "keystone_Subscription_Quotes",
                    keystone_quote_number,
                )
                logger.info(
                    f"Entered Keystone Subscription Quotes: {keystone_quote_number}"
                )

                cm.clickElementAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="fetch_Subscription_Details",
                    wait_time=10,
                )
                logger.info(f"Clicked on Fetch Subscription Details button")

                print(
                    f"\n\033[94mℹ️ ================Validation of Keystone Subscription Number in Internal Engineering Quote=================================================================\033[0m"
                )
                keystone_support_cmat_id = cm.readText(
                    "PurchaseOrderPage", "keystone_Support_Cmat_Id"
                )
                logger.info(
                    f"Captured Keystone Support CMAT ID: {keystone_support_cmat_id}"
                )
                print(f"Captured Keystone Support CMAT ID: {keystone_support_cmat_id}")

                keystone_support_ownership = cm.readText(
                    "PurchaseOrderPage", "keystone_Support_Ownership"
                )
                logger.info(
                    f"Captured Keystone Support Ownership: {keystone_support_ownership}"
                )
                print(
                    f"Captured Keystone Support Ownership: {keystone_support_ownership}"
                )

                keystone_subscription_id = cm.readText(
                    "PurchaseOrderPage", "keystone_Subscription_Id"
                )
                logger.info(
                    f"Captured Keystone Subscription ID: {keystone_subscription_id}"
                )
                print(f"Captured Keystone Subscription ID: {keystone_subscription_id}")

                if test_case["Subscription Number Validation"].strip().lower() == "yes":
                    comparison_result = cm.checkExpectedTextInActual(
                        actual_text=keystone_subscription_id,
                        expected_text=keystone_subscription_number,
                    )
                    if not comparison_result:
                        failure_message = f"Actual Keystone Subscription ID '{keystone_subscription_id}' does not match expected Keystone Subscription Number '{keystone_subscription_number}'."
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual Keystone Subscription ID: {keystone_subscription_id} with expected Keystone Subscription Number: {keystone_subscription_number}"
                        )
                        print(
                            f"\033[92m✅ Compared actual Keystone Subscription ID: {keystone_subscription_id} with expected Keystone Subscription Number: {keystone_subscription_number}\033[0m"
                        )

                cm.clickElementAndWait(
                    page_name="PurchaseOrderPage",
                    element_name="submit_PO_Button",
                    wait_time=20,
                )
                logger.info(f"Clicked on Submit PO button")

                internal_quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                logger.info(f"Quote Status: {internal_quote_status}")
                ss.capture_screenshot("Captured Internal quote PO submission status")

                print(
                    f"\n\033[94mℹ️ ================Validating Internal Engineering Quote for PO Submitted Status=============================================================================\033[0m"
                )
                internal_quote_status = cm.verifyElementStatus(
                    "HomePage_CPQ", "quote_Status", "PO Submitted"
                )
                if not internal_quote_status:
                    failure_message = (
                        f"Internal Engineering Quote status is not in expected state: "
                        f"Expected 'PO Submitted', but found something else."
                    )
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Verified Internal Engineering quote status is in expected state PO Submitted: {internal_quote_status}"
                    )
                    print(
                        f"\033[92m✅ Verified Internal Engineering quote status is in expected state PO Submitted: {internal_quote_status}\033[0m"
                    )

            # ======================================TPD for Internal Engineering=========================================================================================

            thp = TPDHomePage(third_Tab)
            logger.info(f"TPDHomePage instance created for the new tab")

            if test_case["Accept in TPD_Internal Engineering"].strip().lower() == "yes":
                if is_valid_data(test_case["TPD URL"]):
                    cm.navigateToUrl(test_case["TPD URL"])
                    logger.info(f"Navigated to TPD URL: {test_case['TPD URL']}")

                cm.clickElement("HomePage_TPD", "global_Search")
                logger.info(f"Clicked on global search")

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", internal_quote_number
                )
                logger.info(f"Searched by transaction number: {internal_quote_number}")

                cm.enterText("HomePage_TPD", "po_Number", internal_quote_number)
                logger.info(f"Searched by PO number: {internal_quote_number}")

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

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", internal_quote_number
                )
                logger.info(
                    f"Searched by transaction number in {tpd_subProcessStatus}: {internal_quote_number}"
                )

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button in {tpd_subProcessStatus}")

                thp.clickSearchQuote(internal_quote_number)
                logger.info(
                    f"Clicked on quote link in {tpd_subProcessStatus}: {internal_quote_number}"
                )

                thp.selectCostCenterAndGLAccountValidation()
                logger.info(
                    f"Selected Cost Center and GL Account Validation checkbox in Transaction Data section"
                )

                cm.selectOptionInListbox("HomePage_TPD", "actions_DD", "Accepted")
                logger.info(f"Selected Accepted from Actions dropdown")

                cm.clickElement("HomePage_TPD", "actions_Go_Button")
                logger.info(f"Clicked on Actions Go button")

                cm.clickElementAndWait(
                    "HomePage_TPD",
                    "yes_Button",
                    wait_time=5,
                )
                logger.info(f"Clicked on Yes button in confirmation pop-up")
                ss.capture_screenshot("Captured TPD details for Internal quote")

                cm.clickElement("HomePage_TPD", "global_Search")
                logger.info(f"Clicked on global search")

                cm.enterText(
                    "HomePage_TPD", "transaction_Number", internal_quote_number
                )
                logger.info(f"Searched by transaction number: {internal_quote_number}")

                cm.enterText("HomePage_TPD", "po_Number", internal_quote_number)
                logger.info(f"Searched by PO number: {internal_quote_number}")

                cm.clickElement("HomePage_TPD", "go_Button")
                logger.info(f"Clicked on Go button")

                tpd_orderStatus = cm.readText("HomePage_TPD", "order_Status")
                logger.info(f"Captured order status: {tpd_orderStatus}")

                if test_case["TPD Validation"].strip().lower() == "yes":
                    print(
                        f"\n\033[94mℹ️ ================Internal Engineering Quote TPD Validation for Order Status===============================================================================\033[0m"
                    )
                    comparison_result = cm.checkExpectedTextInActual(
                        actual_text=tpd_orderStatus,
                        expected_text=test_case["Order Status"],
                    )
                    if not comparison_result:
                        failure_message = f"Actual order status '{tpd_orderStatus}' does not match expected order status '{test_case['Order Status']}'."
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual order status: {tpd_orderStatus} with expected order status: {test_case['Order Status']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual order status: {tpd_orderStatus} with expected order status: {test_case['Order Status']}\033[0m"
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

            # =========================================Capture Test Result and Write To Excel================================================
            test_results = [
                [
                    "Test Case ID",
                    "Keystone Quote Number",
                    "Keystone Quote Name",
                    "Internal Quote Number",
                    "Internal Quote Name",
                    "Execution Status",
                    "Details",
                ],
                [
                    script_name,
                    keystone_quote_number,
                    keystone_quote_name,
                    internal_quote_number,
                    internal_quote_name,
                    boolean_status,
                    f"{script_name} Test Script Execution Completed Successfully",
                ],
            ]
            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)

            logger.info(
                f"*****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\n\033[92m✅ *****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****\033[0m"
            )
            """
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
