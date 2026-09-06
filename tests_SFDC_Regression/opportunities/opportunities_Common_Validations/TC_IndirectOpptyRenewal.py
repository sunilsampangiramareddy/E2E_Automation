from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_CPQ.Quote_Info_Page import QuoteInfoPage
import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Home_Page import HomePage
from pages_StorageGrid.HomePage_StorageGrid import HomePageStorageGrid
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from pages_SFDC.Developer_Console import DeveloperConsole

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# ADO Test ID - 473701,517138
# Test Scenario:
# Copy opportunity for Closed Indirect Opportunity - Internal user.
# Verify the Renewal Opportunity creation and ownership assigned to Retention Specialist
# Test Description:
# 1. Logging into the Salesforce application.
# 2. Navigating to the Opportunities screen and creating opportunities with various configurations (Direct, Indirect, Standard, 1P).
# 3. Performing validations for Sales Type, including error handling and pre-filled values based on customer type.
# 4. Adding products to opportunities and validating product configurations.
# 5. Closing opportunities manually by progressing through different stages (Qualify, Design, Propose, Negotiate, and Closed).
# 6. Creating quotes, capturing quote details, and validating prebuild configurations.
# 7. Interacting with the Developer Console to mark quotes as booked.
# 8. Capturing test results and writing them to an Excel file for reporting purposes.
# Author & Modifier: Aswathy S
# Reviewer: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_IndirectOpptyRenewal.xlsx"
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
def test_IndirectOpptyRenewal(page: Page, base_url, config, test_case) -> None:
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    od = OpportunityDetailPage(page)
    boolean_status = "Pass"
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"
    validation_failures = []

    try:
        # ==================================Login to SFDC=================================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']} and for the test case id {test_case['Test Case ID']}*****"
            )
            print(
                f"\033[94mℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']} and for the test case id {test_case['Test Case ID']}*****\033[0m"
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
                                co.selectPrimaryContactFirst(
                                    test_case["Primary Contact"]
                                )
                                logger.info(
                                    f"Selected primary contact: {test_case['Primary Contact']}"
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
                                co.enterOpportunityName(test_case["Opportunity Name"])
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
                                co.selectPrimaryContactFirst(
                                    test_case["Primary Contact"]
                                )
                                logger.info(
                                    f"Selected primary contact: {test_case['Primary Contact']}"
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
                            if is_valid_data(
                                test_case["Sales Type"] and test_case["Sales Type"]
                            ):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Type",
                                    test_case["Sales Type"],
                                )
                                logger.info(
                                    f"Selected sales type: {test_case['Sales Type']}"
                                )

                            if is_valid_data(test_case["Installed Base Type"]):
                                cm.clickElement(
                                    "CreateOpportunity", "installed_base_renewal"
                                )
                                cm.clickByTextByPosition(test_case["Installed Base Type"],'last',0)                                
                                logger.info(
                                    f"Selected installed base type: {test_case['Installed Base Type']}"
                                )

                            if is_valid_data(test_case["Sales Play"]):
                                cm.clickElement(
                                    "CreateOpportunity", "sales_Play_Combobox"
                                )
                                cm.clickByText(test_case["Sales Play"])
                                logger.info(
                                    f"Selected sales play: {test_case['Sales Play']}"
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
                        if cm.isElementVisible(
                            "CreateOpportunity", "end_Customer_Label"
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

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")
                        if (
                            test_case["Channel"] == indirect_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):
                            if is_valid_data(test_case["Reseller Sales Rep"]):
                                cm.selectDropdownByIndex("CreateOpportunity","reseller_Sales_Rep",1)
                                logger.info(
                                    f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}"
                                )
                            if is_valid_data(test_case["Reseller SE"]):
                                cm.selectDropdownByIndex("CreateOpportunity","reseller_SE",1)
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

            spark_url = hp.getCurrentURL()
            logger.info(f"Captured Spark URL: {spark_url}")

            if test_case["Sales Type"].strip().lower() == "renewal":
                cm.mouseWheel("HomePage", 800, scrolls=1, wait_time=2)
                                    
                cm.clickElementAndWait("HomePage","opportunity_Teams_Link",2)
                logger.info("Clicked on opportunity teams link")
    
                comparison_result2 = cm.assertContainsText("HomePage", "grid_Body_Renewal_Specialist", "Renewal Specialist")
                if not comparison_result2:
                    failure_message = f"Expected 'Renewal Specialist' but not visible"
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info( "Expected 'Renewal Specialist' is visible")
                    print(
                        f"\033[92m✅ Expected 'Renewal Specialist' is visible\033[0m\n"                                                            
                    )

                if test_case["Edit Sales Type"].strip().lower() == "yes":

                    cm.navigateToUrl(spark_url)
                    logger.info(f"Navigated back to Spark URL: {spark_url}")

                    cm.clickElement("CreateOpportunity", "edit_Sales_Type_Button")
                    logger.info(f"Clicked on edit sales type button")

                    cm.clickElement("CreateOpportunity", "sales_Type_Combobox")
                    logger.info(f"Clicked on sales type combobox")
                    cm.clickByText(test_case["New sales type"])

                    cm.clickElement("CreateOpportunity", "sales_Play_Combobox")
                    logger.info(f"Clicked on sales play combobox")
                    cm.clickByText(test_case["Sales Play New"])

                    cm.clickElement("HomePage", "save_Button")
                    logger.info(
                        f"Edited opportunity sales type to {test_case['New sales type']}"
                    )
                if test_case["Error message Validation"].strip().lower() == "yes":
                    result = cm.assertContainsText(
                        "HomePage",
                        "error_Label_1",
                        (test_case["Error Message"]),
                    )
                    if result:
                        logger.info("Validated error message")
                        print(
                            f"✅ Error message validated: {test_case['Error Message']}"
                        )
                    else:
                        print(
                            f"❌ Expected error message to contain '{test_case['Error Message']}'"
                        )
                        validation_failures.append(
                            f"Expected error message to contain '{test_case['Error Message']}'"
                        )

                    cm.clickElement("HomePage", "cancel_Button")

            # =======================Add Product in SFDC=================================================================================
            if test_case["Add Products"].strip().lower() == "yes":
                if is_valid_data(test_case["Product Name"]):
                    hp.selectProduct(test_case["Product Name"])
                    logger.info(f"Selected product: {test_case['Product Name']}")

                if is_valid_data(test_case["Product Price"]):
                    hp.enterProductPrice(test_case["Product Price"])
                    logger.info(f"Entered product price: {test_case['Product Price']}")

            hp.navigateToUrl(spark_url)
            logger.info(f"Navigated back to Spark URL: {spark_url}")
            # =======================Closing Opportunity=================================================================================
            if test_case["Manual Opportunity Closure"].strip().lower() == "yes":
                cm.clickElementAndWait(
                    "HomePage", "mark_Stage_As_Complete_Button", wait_time=5
                )
                logger.info(f"Marked stage as complete")

                if test_case["Opportunity Stage Validation"].strip().lower() == "yes":
                    opportunity_stage = cm.readText(
                        "HomePage", "opportunity_Stage_Label_1"
                    )
                    logger.info(f"Captured opportunity stage: {opportunity_stage}")

                    stage_validation = cm.checkExpectedTextInActual(
                        actual_text=opportunity_stage,
                        expected_text=test_case["Qualify Stage"],
                    )

                    if not stage_validation:
                        failure_message = f"Opportunity Stage Validation Failed: Expected '{test_case['Qualify Stage']}' but got '{opportunity_stage}'"
                        validation_failures.append(
                            failure_message
                        )  # Add failure to the list
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Qualify Stage']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Qualify Stage']}\033[0m"
                        )

                od.editSalesPlay(test_case["Sales Play New"])
                logger.info(f"Edited sales play to {test_case['Sales Play New']}")

                od.editFlexpod(test_case["Flexpod"])
                logger.info(f"Edited flexpod to {test_case['Flexpod']}")

                cm.clickElementAndWait(
                    "HomePage", "mark_Stage_As_Complete_Button", wait_time=5
                )
                logger.info(f"Marked stage as complete")

                opportunity_stage = cm.readText("HomePage", "opportunity_Stage_Label_1")
                logger.info(f"Captured opportunity stage: {opportunity_stage}")

                stage_validation = cm.checkExpectedTextInActual(
                    actual_text=opportunity_stage,
                    expected_text=test_case["Design Stage"],
                )

                if not stage_validation:
                    failure_message = f"Opportunity Stage Validation Failed: Expected '{test_case['Design Stage']}' but got '{opportunity_stage}'"
                    validation_failures.append(
                        failure_message
                    )  # Add failure to the list
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Design Stage']}"
                    )
                    print(
                        f"\033[92m✅ Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Design Stage']}\033[0m"
                    )

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")

                # =========================Create Quote===========================================================================================
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
                    hpsg = HomePageStorageGrid(second_Tab)
                    logger.info(f"HomePageStorageGrid instance created for the new tab")

                    cm.clickElementAndWait(
                        page_name="QuoteInfoPage",
                        element_name="save_Button",
                        wait_time=5,
                    )
                    logger.info(f"Clicked on save button")

                    cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=30000)
                    logger.info(
                        f"Checking for the dynamic popup, if exists then closed the popup"
                    )

                    cm.clickElement("ProductsPage", "products_Tab")
                    logger.info(f"Clicked on Products tab")

                    logger.info(
                        f"Checking for the dynamic popup, if exists then closed the popup"
                    )
                    cm.closePopUp("QuoteInfoPage", "pop_Up", timeout=3000)

                    cm.clickElement("ProductsPage", "configure_Button")
                    logger.info(f"Clicked on Configure button")

                    if is_valid_data(test_case["Product"]):
                        hpsg.clickProductName(test_case["Product"])
                        logger.info(f"Clicked on product: {test_case['Product']}")

                    if is_valid_data(test_case["Sub Product"]):
                        hpsg.selectSubProduct(test_case["Sub Product"])
                        logger.info(
                            f"Clicked on sub-product: {test_case['Sub Product']}"
                        )

                    hpsg.selectModel_StorageNodes(test_case["Model_Storage Nodes"])
                    logger.info(
                        f"Selected Model as: {test_case['Model_Storage Nodes']}"
                    )

                    hpsg.selectDriveType_StorageNodes(
                        test_case["Drive Type_Storage Nodes"]
                    )
                    logger.info(
                        f"Selected Drive Type as: {test_case['Drive Type_Storage Nodes']}"
                    )

                    hpsg.enterQty_StorageNodes(test_case["Qty_Storage Nodes"])
                    logger.info(
                        f"Entered Quantity as: {test_case['Qty_Storage Nodes']}"
                    )

                    hpsg.clickAddToQuote()
                    logger.info(f"Clicked on Add to Quote button")

                # =============================Capture Quote Details==============================================================================
                # Perform actions on the new tab
                if test_case["Capture Quote Details"].strip().lower() == "yes":
                    quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                    logger.info(f"Quote Number: {quote_number}")
                    print(f"\033[94mℹ️ Quote Number: {quote_number}\033[0m")

                    quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                    logger.info(f"Quote Name: {quote_name}")
                    print(f"\033[94mℹ️  Quote Name: {quote_name}\033[0m")

                    cpq_url = cm.getCurrentURL()
                    logger.info(f" CPQ URL: {cpq_url}")
                    print(f"\033[94mℹ️  CPQ URL: {cpq_url}\033[0m")

                first_Tab = cm.switchToTab(
                    page.context, tab_index=0, expected_tab_count=2
                )
                logger.info(
                    "Switched to the new tab after clicking on Create Quote option"
                )
                # Create an instance of HomePageCPQ for the new tab
                ss = ScreenshotUtil(first_Tab)
                logger.info(f"ScreenshotUtil instance created for the new tab")
                hp = HomePage(first_Tab)
                logger.info(f"HomePage instance created for the new tab")
                cm = CommonMethods(first_Tab, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")
                hpsg = HomePageStorageGrid(first_Tab)
                logger.info(f"HomePageStorageGrid instance created for the new tab")

                cm.refreshPage()
                logger.info(f"Refreshed the page to ensure all changes are saved")

                if is_valid_data(
                    test_case["Business Solution Areas"]
                    and test_case["Customer Workloads"]
                    and test_case["AI Customer Workload"]
                    and test_case["Solution Protocols"]
                ):
                    od.configureSEValues(
                        test_case["Business Solution Areas"],
                        test_case["Customer Workloads"],
                        test_case["AI Customer Workload"],
                        test_case["Solution Protocols"],
                    )
                    logger.info(
                        f"Configured SE values: Business Solution Areas: {test_case['Business Solution Areas']}, Customer Workloads: {test_case['Customer Workloads']}, AI Customer Workload: {test_case['AI Customer Workload']}, Solution Protocols: {test_case['Solution Protocols']}"
                    )

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")

                cm.clickElementAndWait(
                    "HomePage", "mark_Stage_As_Complete_Button", wait_time=5
                )
                logger.info(f"Marked stage as complete")

                if test_case["Opportunity Stage Validation"].strip().lower() == "yes":
                    opportunity_stage = cm.readText(
                        "HomePage", "opportunity_Stage_Label_1"
                    )
                    logger.info(f"Captured opportunity stage: {opportunity_stage}")

                    stage_validation = cm.checkExpectedTextInActual(
                        actual_text=opportunity_stage,
                        expected_text=test_case["Propose Stage"],
                    )

                    if not stage_validation:
                        failure_message = f"Opportunity Stage Validation Failed: Expected '{test_case['Propose Stage']}' but got '{opportunity_stage}'"
                        validation_failures.append(
                            failure_message
                        )  # Add failure to the list
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Propose Stage']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Propose Stage']}\033[0m"
                        )

                od.addCompetitors(test_case["Hyperscaler"])
                logger.info(f"Added competitor: {test_case['Hyperscaler']}")

                cm.clickElementAndWait(
                    "HomePage", "mark_Stage_As_Complete_Button", wait_time=5
                )
                logger.info(f"Marked stage as complete")

                if test_case["Opportunity Stage Validation"].strip().lower() == "yes":
                    opportunity_stage = cm.readText(
                        "HomePage", "opportunity_Stage_Label_1"
                    )
                    logger.info(f"Captured opportunity stage: {opportunity_stage}")

                    stage_validation = cm.checkExpectedTextInActual(
                        actual_text=opportunity_stage,
                        expected_text=test_case["Negotiate Stage"],
                    )

                    if not stage_validation:
                        failure_message = f"Opportunity Stage Validation Failed: Expected '{test_case['Negotiate Stage']}' but got '{opportunity_stage}'"
                        validation_failures.append(
                            failure_message
                        )  # Add failure to the list
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Negotiate Stage']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Negotiate Stage']}\033[0m"
                        )

                cm.clickElement("HomePage", "setup_Icon")
                logger.info(f"Clicked on setup icon")

                cm.clickElement("HomePage", "developer_Console_Option")
                logger.info(f"Clicked on developer console")

                second_Window_First_Page = cm.switchToTab(
                    page.context, tab_index=2, expected_tab_count=3
                )
                logger.info(f"Switched to developer console window")

                dc = DeveloperConsole(second_Window_First_Page)
                cm = CommonMethods(second_Window_First_Page, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")

                cm.waitForStable(3)

                if cm.isElementVisible("HomePage", "ok_Button", timeout=3000):
                    cm.clickElement("HomePage", "ok_Button")
                    logger.info(f"Clicked on OK button in developer console")

                dc.markQuoteAsBooked(
                    quote_name, test_case["Quote Status"], test_case["Order Status"]
                )
                logger.info(f"Marked quote as booked in Developer Console")

                first_Tab = cm.switchToTab(
                    page.context, tab_index=0, expected_tab_count=3
                )
                logger.info(f"Switched to first tab")

                cm = CommonMethods(first_Tab, locator_manager)
                logger.info(f"CommonMethods instance created for the new tab")

                cm.refreshPage(first_Tab)
                logger.info(f"Reloaded the page to ensure all changes are saved")

                cm.scrollAndClick("HomePage", "quotes_Link")
                logger.info(f"Clicked on quotes tab")

                cm.clickElementByPosition("HomePage", "seq_Number_Link", "nth", 0)
                logger.info(f"Clicked on quote number link to open quote details page")

                cm.clickElement("HomePage", "edit_FA_Verified_Button")
                logger.info(f"Clicked on edit FA verified button")

                cm.checkCheckbox("HomePage", "fa_Verified_Checkbox")
                logger.info(f"Checked FA verified checkbox")

                cm.clickElement("HomePage", "save_Button")
                logger.info(f"Clicked on save button")

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")

                cm.clickElementAndWait(
                    "HomePage", "mark_Stage_As_Complete_Button", wait_time=5
                )
                logger.info(f"Marked stage as complete")

                cm.selectOptionInListbox(
                    "HomePage", "opportunity_Stage_Listbox", test_case["Closed Stage"]
                )
                logger.info(
                    f"Selected opportunity stage as: {test_case['Closed Stage']}"
                )

                cm.clickElementAndWait("HomePage", "save_Button", wait_time=15)
                logger.info(f"Clicked on save button")

                if test_case["Opportunity Stage Validation"].strip().lower() == "yes":
                    opportunity_stage = cm.readText(
                        "HomePage", "opportunity_Stage_Label_1"
                    )
                    logger.info(f"Captured opportunity stage: {opportunity_stage}")

                    stage_validation = cm.checkExpectedTextInActual(
                        actual_text=opportunity_stage,
                        expected_text=test_case["Closed Stage"],
                    )

                    if not stage_validation:
                        failure_message = f"Opportunity Stage Validation Failed: Expected '{test_case['Closed Stage']}' but got '{opportunity_stage}'"
                        validation_failures.append(
                            failure_message
                        )  # Add failure to the list
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")
                    else:
                        logger.info(
                            f"Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Closed Stage']}"
                        )
                        print(
                            f"\033[92m✅ Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Closed Stage']}\033[0m"
                        )

            od.clickCopyOpportunity()
            logger.info(f"Clicked on copy opportunity button")

            cm.clickElementAndWait("HomePage", "continue_Button",10)
            logger.info(f"Clicked on continue button")

            if test_case["Opportunity Stage Validation"].strip().lower() == "yes":
                opportunity_stage = cm.readText(
                    "HomePage", "opportunity_Stage_Label"
                )
                logger.info(f"Captured opportunity stage: {opportunity_stage}")

                stage_validation = cm.checkExpectedTextInActual(
                    actual_text=opportunity_stage,
                    expected_text=test_case["Prospect Stage"],
                )

                if not stage_validation:
                    failure_message = f"Opportunity Stage Validation Failed: Expected '{test_case['Prospect Stage']}' but got '{opportunity_stage}'"
                    validation_failures.append(
                        failure_message
                    )  # Add failure to the list
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(
                        f"Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Prospect Stage']}"
                    )
                    print(
                        f"\033[92m✅ Compared actual opportunity stage: {opportunity_stage} with expected opportunity stage: {test_case['Prospect Stage']}\033[0m"
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
                f"*****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"\n\033[92m✅ *****{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']}*****\033[0m"
            )
            # If execution flag is not 'yes', explicitly skip the test
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
