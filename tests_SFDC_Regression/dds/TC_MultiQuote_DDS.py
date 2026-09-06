import pytest
import logging
import os
from decimal import Decimal
from playwright.sync_api import Page
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.Developer_Console import DeveloperConsole
from pages_SFDC.MultiQuotePage import MultiQuotePage
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from common_Methods.Common_Methods import CommonMethods
 
 
# =========================================================================================================================
# Test Metadata
# =========================================================================================================================

# Test Scenario: 550145 - Validate DDS Multi Quote Deal Score Calculation from Child Quotes with UCPQ Aggregation and Dynamic Recalculation on Quote Changes.
#                550146 - Verify removal of legacy color rating UI elements, addition of DDS guidance section, and proper display of MQ Deal Score summary information across DDS-enabled multi Quotes.

# Test Description:
#                 1. Create or navigate to a Salesforce opportunity and add products to enable DDS multi-quote flow.
#                 2. Create child quote records in CPQ, save them, and sync them back to Salesforce.
#                 3. Launch the Multi Quote wizard, add the child quotes, and validate the MQ summary page.
#                 4. Verify the legacy color rating is removed and the DDS guidance section is displayed.
#                 5. Confirm the MQ Deal Score labels are visible for Deal Score to 2/3/4/5.
#                 6. Read the displayed Multi Quote deal scores and percentages from the page.
#                 7. Query the child quote records in Developer Console and aggregate the net Deal Score values.
#                 8. Compare cumulative child quote values with the displayed MQ values and validate percentage calculations.
#                 9. Fail the test if any mismatch is detected across DDS summary fields or UI validations.

# Author: Alok Kumar Gupta
# Reviewed by: Sunil Reddy
# =========================================================================================================================
 
 
logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_MultiQuote_DDS.xlsx")
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
def test_MultiQuote_DDS(page: Page, base_url, config, test_case) -> None:
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    mq = MultiQuotePage(page)
    boolean_status = "Pass"
    validation_failures = []
    direct_Oppty = "Direct"
    oppty_name = ""
    oppty_number = ""
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"
 
    try:
        # =================================Login to SFDC==========================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(f"***{script_name} - Test Script Execution Started for Iteration - {test_case['Iteration']} and {test_case['Test Case ID']} ***")
            print(f"ℹ️ ***{script_name} - Test Script Execution Started for Iteration - {test_case['Iteration']} and {test_case['Test Case ID']} ***")

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
                logger.info(f"Opportunities label has been verified on the homepage")
                print(f"✅ Opportunities label verified on the homepage")
            else:
                print(f"❌ Opportunities label is not visible on the homepage")
                validation_failures.append("Opportunities label is not visible on the homepage")

            ss.capture_screenshot("Captured Homepage details")

            if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":
                if test_case["Create Opportunity"].strip().lower() == "yes":
               
                    cm.clickElement("HomePage", "opportunities_Tab")
                    logger.info(f"Clicked on opportunities tab")

                    cm.clickElement("HomePage", "new_Opportunity_Button")
                    logger.info(f"Clicked on new opportunity button")

                    if is_valid_data(test_case["Account Name"]):
                        co.enterAccount(test_case["Account Name"])
                        logger.info(f"Entered and selected account: {test_case['Account Name']}")

                    cm.clickElement("CreateOpportunity", "next_Button")
                    logger.info(f"Clicked on next button")

                    if test_case["Channel"] == direct_Oppty or test_case["Channel"] == indirect_Oppty or test_case["Opportunity Type"] == x1p_Oppty:
                        if is_valid_data(test_case["Opportunity Type"]):
                            cm.selectOptionInListbox("CreateOpportunity", "opportunity_Type", test_case["Opportunity Type"])
                            logger.info(f"Selected opportunity type: {test_case['Opportunity Type']}")

                        if test_case["Opportunity Type"] == std_Oppty:
                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName(test_case["Opportunity Name"])
                                logger.info(f"Entered opportunity name: {test_case['Opportunity Name']}")
                            if is_valid_data(test_case["Primary Contact"]):
                                co.select_PrimaryContact(test_case["Primary Contact"])
                                logger.info(f"Selected primary contact: {test_case['Primary Contact']}")
                            if is_valid_data(test_case["Sales Play"]):
                                cm.clickElement("CreateOpportunity", "sales_Play_Combobox")
                                cm.clickByText(test_case["Sales Play"])
                                logger.info(f"Selected sales play: {test_case['Sales Play']}")
                            if is_valid_data(test_case["Channel"]):
                                cm.selectOptionInListbox("CreateOpportunity", "channel", test_case["Channel"])
                                logger.info(f"Selected channel: {test_case['Channel']}")

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName_1p(test_case["Opportunity Name"])
                                logger.info(f"Entered 1P opportunity name: {test_case['Opportunity Name']}")
                            if is_valid_data(test_case["Sales Type"]):
                                cm.selectOptionInListbox("CreateOpportunity", "sales_Type_1P_new", test_case["Sales Type"])
                                logger.info(f"Selected 1P sales type: {test_case['Sales Type']}")
                            if is_valid_data(test_case["Primary Contact"]):
                                co.select_PrimaryContact(test_case["Primary Contact"])
                                logger.info(f"Selected 1P primary contact: {test_case['Primary Contact']}")
                            if is_valid_data(test_case["Hyperscaler"]):
                                cm.selectOptionInListbox("CreateOpportunity", "hyperscaler", test_case["Hyperscaler"])
                                logger.info(f"Selected hyperscaler: {test_case['Hyperscaler']}")

                        if test_case["Channel"] == indirect_Oppty and test_case["Opportunity Type"] != x1p_Oppty:
                            if is_valid_data(test_case["Reseller Account"]):
                                co.selectReseller(test_case["Reseller Account"])
                                logger.info(f"Entered reseller account: {test_case['Reseller Account']}")

                        if test_case["Opportunity Type"] == std_Oppty and test_case["Opportunity Type"] != x1p_Oppty:
                            if is_valid_data(test_case["Sales Type"]):
                                cm.selectOptionInListbox("CreateOpportunity", "sales_Type", test_case["Sales Type"])
                                logger.info(f"Selected sales type: {test_case['Sales Type']}")
                            if is_valid_data(test_case["Installed Base Type"]):
                                co.selectInstalledBaseType(test_case["Installed Base Type"])                          
                                logger.info(f"Selected installed base type: {test_case['Installed Base Type']}")                                                                                     
                            if is_valid_data(test_case["Currency"]):
                                cm.selectOptionInListbox("CreateOpportunity", "currency", test_case["Currency"])
                                ss.capture_screenshot("Captured Create Opportunity details")
                                logger.info(f"Selected currency: {test_case['Currency']}")
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")
            
                        if test_case["Channel"] == indirect_Oppty and test_case["Opportunity Type"] != x1p_Oppty:
                            if is_valid_data(test_case["Pathway"]):
                                cm.selectOptionInListbox("CreateOpportunity", "pathway", test_case["Pathway"])
                                logger.info(f"Selected pathway: {test_case['Pathway']}")
                            if is_valid_data(test_case["Partner Sales Model"]):
                                cm.selectOptionInListbox("CreateOpportunity", "partner_Sales_Model", test_case["Partner Sales Model"])
                                logger.info(f"Selected partner sales model: {test_case['Partner Sales Model']}")
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")
                            
                    
                        if cm.isElementVisible("CreateOpportunity", "end_Customer_Label", 10000):
                            if test_case["Opportunity Type"] == std_Oppty and test_case["Opportunity Type"] != x1p_Oppty:
                                if is_valid_data(test_case["End Customer Usage"]):
                                    cm.selectOptionInListbox("CreateOpportunity","end_Customer_Usage",test_case["End Customer Usage"])
                                    logger.info(f"Selected end customer usage: {test_case['End Customer Usage']}")                                           
                                    cm.clickElement("CreateOpportunity", "next_Button")
                                    logger.info(f"Clicked on next button")

                        if test_case["Channel"] == indirect_Oppty and test_case["Opportunity Type"] != x1p_Oppty:
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                            if is_valid_data(test_case["Reseller Sales Rep"]):
                                cm.selectOptionInListbox("CreateOpportunity", "reseller_Sales_Rep", test_case["Reseller Sales Rep"])
                                logger.info(f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}")
                            if is_valid_data(test_case["Reseller SE"]):
                                cm.selectOptionInListbox("CreateOpportunity", "reseller_SE", test_case["Reseller SE"])
                                logger.info(f"Selected reseller SE: {test_case['Reseller SE']}")
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

                    cm.clickElement("OpportunityDetailPage", "details_Tab")
                    spark_url = cm.getCurrentURL()
                    logger.info(f"Captured Spark URL: {spark_url}")
                    print(f"ℹ️ Captured Spark URL: {spark_url}")
                    
                else:
                    logger.info(f"Create Opportunity flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}")
                    print(f"➡️ Create Opportunity flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}")
            else:
                logger.info(f"Navigate To Opportunities Screen flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}")
                print(f"➡️ Navigate To Opportunities Screen flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}")

            # =======================Add Product in SFDC=================================================================================
            if test_case["Add Products"].strip().lower() == "yes":
    
                if is_valid_data(test_case["Product Name"]):
                    cm.clickElement("HomePage", "products_Link")
                    cm.clickElement("HomePage", "add_Products_Button")
                    cm.clickElement("HomePage", "search_Products_Input")
                    cm.enterText("HomePage", "search_Products_Input", test_case["Product Name"])
                    cm.pressEnter("HomePage", "search_Products_Input")
                    cm.clickElement("HomePage", "product_Search_Result")
                    cm.clickElement("HomePage", "product_Next_Button")
                    logger.info(f"Selected product: {test_case['Product Name']}")

                if is_valid_data(test_case["Product Price"]):
                    cm.clickElement("HomePage", "edit_Sales_Price_Button")
                    cm.enterText("HomePage", "sales_Price_Input", str(test_case["Product Price"]))
                    cm.clickElement("HomePage", "save_Button")
                    ss.capture_screenshot("Captured Product in SFDC Details")
                    logger.info(f"Entered product price: {test_case['Product Price']}")

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")              


        # ========================Create Quote=======================================================================================
            if test_case["Create Quote"].strip().lower() == "yes": 

                cm.clickElement("HomePage", "create_Quote_1")
                cm.clickElement("HomePage", "create_Quote_2")          
                second_Tab = cm.switchToTab(page.context, tab_index= 1 , expected_tab_count=2)
                logger.info(f"Clicked on create quote")
                ss = ScreenshotUtil(second_Tab)
                logger.info(f"ScreenshotUtil instance created for the Second tab")
                cm = CommonMethods(second_Tab, locator_manager)
                cm.waitForStable(2)
                quote_numbers = []

                cm.clickElementAndWait("HomePage_CPQ", "save_Button",10)
                logger.info(f"Clicked on save button")

            if test_case["Configure Product"].strip().lower() == "yes":

                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                cm.clickElement("ProductsPage", "configure_Button")
                logger.info(f"Clicked on Configure button")

                cm.clickElement("ConfigurePage", "fast_Quotes_Option")
                cm.clickByTextByPosition("Add To Quote", "nth", 0)
                
                cm.waitForStable(20)
                cm.clickElement("HomePage_CPQ", "save_Icon")
                logger.info(f"Clicked on Save button")
                cm.waitForStable(10)

                quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                quote_numbers.append(str(quote_number).strip())
                logger.info(f"Quote Number: {quote_number}")
                print(f"ℹ️ Quote Number: {quote_number}")

                cm.clickElement("QuoteInfoPage", "quote_Info_Tab")
                cm.waitForStable(2)
                cm.clickElement("HomePage_CPQ", "more_Actions_Button")
                cm.waitForStable(2)
                cm.clickElementAndWait("HomePage_CPQ", "sync_Quote_To_SFDC_Menuitem", 10)
                logger.info(f"Clicked on Sync Quote to SFDC button")
                
                first_Tab = cm.closeCurrentTabAndSwitchToPreviousTab(page.context)
                cm = CommonMethods(first_Tab, locator_manager)

                if test_case["MQ mixed behavior validation"].strip().lower() == "no":

                    cm.clickElement("HomePage", "create_Quote_1")
                    cm.clickElement("HomePage", "create_Quote_2")
                    
                    second_Tab = cm.switchToTab(page.context, tab_index= 1 , expected_tab_count=2)
                    logger.info(f"Clicked on create quote")
                    ss = ScreenshotUtil(second_Tab)
                    logger.info(f"ScreenshotUtil instance created for the Second tab")
                    cm = CommonMethods(second_Tab, locator_manager)
                    cm.waitForStable(2)

                    cm.clickElementAndWait("HomePage_CPQ", "save_Button",10)
                    logger.info(f"Clicked on save button")

                    cm.clickElement("ProductsPage", "products_Tab")
                    logger.info(f"Clicked on Products tab")

                    cm.clickElement("ProductsPage", "configure_Button")
                    logger.info(f"Clicked on Configure button")

                    cm.clickElement("ConfigurePage", "fast_Quotes_Option")
                    cm.clickByTextByPosition("Add To Quote", "nth", 1)
                    
                    cm.waitForStable(20)
                    cm.clickElement("HomePage_CPQ", "save_Icon")
                    logger.info(f"Clicked on Save button")
                    cm.waitForStable(5)

                    quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                    quote_numbers.append(str(quote_number).strip())
                    logger.info(f"Quote Number: {quote_number}")
                    print(f"ℹ️ Quote Number: {quote_number}")

                    cm.clickElement("QuoteInfoPage", "quote_Info_Tab")
                    cm.waitForStable(2)
                    cm.clickElement("HomePage_CPQ", "more_Actions_Button")
                    cm.waitForStable(2)
                    cm.clickElementAndWait("HomePage_CPQ", "sync_Quote_To_SFDC_Menuitem", 10)
                    logger.info(f"Clicked on Sync Quote to SFDC button")

                    first_Tab = cm.closeCurrentTabAndSwitchToPreviousTab(page.context)
                    cm = CommonMethods(first_Tab, locator_manager)

            if test_case["User Persona Login"].strip().lower() == "yes":

                cm.clickElement("HomePage", "setup_Icon")
                cm.clickElement("HomePage", "setup_menu_item")
                secondTab = cm.switchToTab(page.context, tab_index=1, expected_tab_count=2)
                cm.waitForPageLoad(secondTab)
                logger.info("Clicked on Setup icon")    
                cm = CommonMethods(secondTab, locator_manager)
                cm.clickElement("GeneralSetup", "search_Setup_Input")
                cm.enterText(
                    "GeneralSetup", "search_Setup_Input", test_case["User Persona"]
                )
                cm.clickByLinkText(
                    test_case["User Persona"], partial_match=True, occurrence=1
                )
                logger.info("Searched for user in Setup")

                frame_locator_setup = locator_manager.get_locator("HomePage", "frame_Locator")
                cm.switchToFrame(frame_locator_setup)
                cm.page.get_by_role("button", name="Login", exact=True).nth(1).click()
                logger.info("Clicked Login button from Setup frame")
                cm = CommonMethods(secondTab, locator_manager)

            if test_case["MQ mixed behavior validation"].strip().lower() == "yes":
            
                cm.clickElement("MultiQuoteWizard", "multi_Quotes_Link")
                cm.waitForStable(5)
                cm.clickElement("MultiQuoteWizard", "search_Searchbox")
                legacy_mq_id = str(int(float(test_case["Legacy MQ ID"]))).strip()
                cm.enterText("MultiQuoteWizard", "search_Searchbox", legacy_mq_id)
                cm.pressKey("MultiQuoteWizard", "search_Searchbox", "Enter")
                cm.waitForStable(3)
                cm.clickByLinkText(legacy_mq_id, partial_match=True)
                cm.clickElement("MultiQuoteWizard", "add_Remove_Quotes_Button")
                cm.waitForStable(3)
                cm.clickElement("MultiQuoteWizard", "add_Quotes_Button")
                cm.clickElement("MultiQuoteWizard", "fields_Combobox")
                cm.clickElement("MultiQuoteWizard", "quote_Number_Option")
                cm.clickElement("MultiQuoteWizard", "search_Searchbox")
                single_quote_number = str(quote_numbers[0]).strip()
                cm.enterText("MultiQuoteWizard", "search_Searchbox", single_quote_number)
                cm.waitForStable(5)
                cm.pressKey("MultiQuoteWizard", "search_Searchbox", "Enter")
                cm.waitForStable(5)
                cm.clickElement("MultiQuoteWizard", "first_Quote_Selection_Indicator_Tbody")
                cm.waitForStable(5)
                cm.clickElement("MultiQuoteWizard", "next_Button")
                cm.waitForStable(3)
                cm.clickElement("MultiQuoteWizard", "save_Button")
                cm.waitForStable(10)
               
                if cm.isElementVisible("MultiQuotePage", "mq_Aggregated_Deal_Score_Message", 10000):
                    logger.info("MQ Aggregated Deal Score guidance message for transition from Color Rating to Deal Score is visible.")
                    print("✅ MQ Aggregated Deal Score guidance message for transition from Color Rating to Deal Score is visible.")
                else:
                    logger.error("MQ Aggregated Deal Score guidance message is not visible.")
                    print("❌ MQ Aggregated Deal Score guidance message is not visible.")
                    validation_failures.append("MQ Aggregated Deal Score guidance message is not visible.")

                cm.clickElement("MultiQuoteWizard", "add_Remove_Quotes_Button")
                cm.waitForStable(3)
                cm.clickElement("MultiQuoteWizard", "last_Quote_Selection_Indicator_Tbody")
                cm.clickElement("MultiQuoteWizard", "remove_Button")
                cm.clickElement("MultiQuoteWizard", "save_Button")
                cm.waitForStable(5)
                

            if test_case["Multi Quote Setup"].strip().lower() == "yes":

                cm.clickElement("MultiQuoteWizard", "multi_Quotes_Link")
                cm.waitForStable(5)
                cm.clickElement("MultiQuoteWizard", "new_Button")
                cm.clickElement("MultiQuoteWizard", "name_Textbox")
                cm.enterText("MultiQuoteWizard", "name_Textbox", test_case["Multi Quote Name"])
                cm.clickElement("MultiQuoteWizard", "next_Button")
                cm.clickElement("MultiQuoteWizard", "save_And_Add_Quotes_Button")
                cm.clickElement("MultiQuoteWizard", "next_Button")
                cm.waitForStable(5) 
                cm.clickElement("MultiQuoteWizard", "fields_Combobox")
                cm.clickElement("MultiQuoteWizard", "quote_Number_Option")
                cm.clickElement("MultiQuoteWizard", "search_Searchbox")
                
                for quote_number in quote_numbers:
                    cm.enterText("MultiQuoteWizard", "search_Searchbox", str(quote_number))
                    cm.waitForStable(5)
                    cm.pressKey("MultiQuoteWizard", "search_Searchbox", "Enter")
                    cm.waitForStable(5)
                    cm.clickElement("MultiQuoteWizard", "first_Quote_Selection_Indicator")
                    cm.waitForStable(5)
                cm.clickElement("MultiQuoteWizard", "next_Button")
                cm.waitForStable(3)
                cm.clickElement("MultiQuoteWizard", "save_Button")
                cm.waitForStable(10)

            if test_case["Multi Quote DDS Validation"].strip().lower() == "yes":
               

                if cm.isElementVisible("MultiQuotePage", "aggregate_Deal_Score_Label", 10000):
                    logger.info("Removal of legacy color Rating validated successfully.")
                    print("✅ Removal of legacy color Rating validated successfully.")
                else:
                    logger.error("Aggregate Deal Score element is not visible. Removal of legacy color Rating validation failed.")
                    print("❌ Aggregate Deal Score element is not visible. Removal of legacy color Rating validation failed.")
                    validation_failures.append("Aggregate Deal Score element is not visible. Removal of legacy color Rating validation failed.")

                if cm.isElementVisible("MultiQuotePage", "dds_Guidance_Section_Label", 10000):
                    logger.info("Addition of DDS guidence section validated successfully")
                    print("✅ Addition of DDS guidence section validated successfully")
                else:
                    logger.error("Target to Improve Deal Values element is not visible. Addition of DDS guidence section validation failed.")
                    print("❌ Target to Improve Deal Values element is not visible. Addition of DDS guidence section validation failed.")
                    validation_failures.append("Target to Improve Deal Values element is not visible. Addition of DDS guidence section validation failed.")

                required_labels = [
                    "deal_Score_To_2_Net_Label",
                    "deal_Score_To_3_Net_Label",
                    "deal_Score_To_4_Net_Label",
                    "deal_Score_To_5_Net_Label",
                ]
                all_labels_visible = cm.isElementVisibleInSequence(
                    "MultiQuotePage", required_labels, 10000
                )

                if all_labels_visible:
                    logger.info("Display of MQ Deal Score validated successfully")
                    print("✅ Display of MQ Deal Score validated successfully")
                else:
                    logger.error("One or more MQ Deal Score labels are not visible.")
                    print("❌ One or more MQ Deal Score labels are not visible.")
                    validation_failures.append(
                        "One or more MQ Deal Score labels are not visible."
                    )

                displayed_Total_List_Price = Decimal(str(cm.cleanCurrencyValue(cm.readText("MultiQuotePage", "Total_List_Price"))))
                displayed_Deal_Score_To_2 = Decimal(str(cm.cleanCurrencyValue(cm.readText("MultiQuotePage", "deal_Score_To_2_Net_Value"))))
                displayed_Deal_Score_To_3 = Decimal(str(cm.cleanCurrencyValue(cm.readText("MultiQuotePage", "deal_Score_To_3_Net_Value"))))
                displayed_Deal_Score_To_4 = Decimal(str(cm.cleanCurrencyValue(cm.readText("MultiQuotePage", "deal_Score_To_4_Net_Value"))))
                displayed_Deal_Score_To_5 = Decimal(str(cm.cleanCurrencyValue(cm.readText("MultiQuotePage", "deal_Score_To_5_Net_Value"))))
                displayed_Deal_Score_To_2_Percent = Decimal(cm.replaceStringValue(cm.replaceStringValue(cm.readText("MultiQuotePage", "deal_Score_To_2_Percent_Value"), "%", ""), " ", "").strip())
                displayed_Deal_Score_To_3_Percent = Decimal(cm.replaceStringValue(cm.replaceStringValue(cm.readText("MultiQuotePage", "deal_Score_To_3_Percent_Value"), "%", ""), " ", "").strip())
                displayed_Deal_Score_To_4_Percent = Decimal(cm.replaceStringValue(cm.replaceStringValue(cm.readText("MultiQuotePage", "deal_Score_To_4_Percent_Value"), "%", ""), " ", "").strip())
                displayed_Deal_Score_To_5_Percent = Decimal(cm.replaceStringValue(cm.replaceStringValue(cm.readText("MultiQuotePage", "deal_Score_To_5_Percent_Value"), "%", ""), " ", "").strip())


                cm.clickElement("HomePage", "setup_Icon")
                cm.clickElement("HomePage", "developer_Console_Option")
                developer_Tab = cm.switchToTab(page.context, tab_index=2, expected_tab_count=3)
                cm.waitForPageLoad(developer_Tab)
                cm = CommonMethods(developer_Tab, locator_manager)
                if cm.isElementVisible("DeveloperConsole", "logging_Disabled_Text",10000):
                    cm.clickElement("DeveloperConsole", "ok_Button")
                cm.waitForStable(5)
                cm.clickElement("DeveloperConsole", "file_Button")
                cm.clickElement("DeveloperConsole", "close_All_Link")
                cm.clickElement("DeveloperConsole", "query_Editor_Button")

                dc = DeveloperConsole(developer_Tab)

                cumulative_values = dc.get_cumulative_deal_score_values(
                    quote_numbers,
                    test_case["Column Name 1"],
                    test_case["Column Name 2"],
                    test_case["Column Name 3"],
                    test_case["Column Name 4"],
                )

                cumulative_Deal_Score_To_2 = cumulative_values["Deal_Score_To_2"]
                cumulative_Deal_Score_To_3 = cumulative_values["Deal_Score_To_3"]
                cumulative_Deal_Score_To_4 = cumulative_values["Deal_Score_To_4"]
                cumulative_Deal_Score_To_5 = cumulative_values["Deal_Score_To_5"]

                rounded_cumulative_Deal_Score_To_2 = cm.roundOff(cumulative_Deal_Score_To_2, 2)
                rounded_cumulative_Deal_Score_To_3 = cm.roundOff(cumulative_Deal_Score_To_3, 2)
                rounded_cumulative_Deal_Score_To_4 = cm.roundOff(cumulative_Deal_Score_To_4, 2)
                rounded_cumulative_Deal_Score_To_5 = cm.roundOff(cumulative_Deal_Score_To_5, 2)

                rounded_displayed_Deal_Score_To_2 = cm.roundOff(displayed_Deal_Score_To_2, 2)
                rounded_displayed_Deal_Score_To_3 = cm.roundOff(displayed_Deal_Score_To_3, 2)
                rounded_displayed_Deal_Score_To_4 = cm.roundOff(displayed_Deal_Score_To_4, 2)
                rounded_displayed_Deal_Score_To_5 = cm.roundOff(displayed_Deal_Score_To_5, 2)

                logger.info(f"Rounded Cumulative Deal_Score_To_2: {rounded_cumulative_Deal_Score_To_2}, Rounded Cumulative Deal_Score_To_3: {rounded_cumulative_Deal_Score_To_3}, Rounded Cumulative Deal_Score_To_4: {rounded_cumulative_Deal_Score_To_4}, Rounded Cumulative Deal_Score_To_5: {rounded_cumulative_Deal_Score_To_5}")
                logger.info(f"Rounded Displayed Deal_Score_To_2: {rounded_displayed_Deal_Score_To_2}, Rounded Displayed Deal_Score_To_3: {rounded_displayed_Deal_Score_To_3}, Rounded Displayed Deal_Score_To_4: {rounded_displayed_Deal_Score_To_4}, Rounded Displayed Deal_Score_To_5: {rounded_displayed_Deal_Score_To_5}")
                print(f"ℹ️ Rounded Cumulative Deal_Score_To_2: {rounded_cumulative_Deal_Score_To_2}, Rounded Cumulative Deal_Score_To_3: {rounded_cumulative_Deal_Score_To_3}, Rounded Cumulative Deal_Score_To_4: {rounded_cumulative_Deal_Score_To_4}, Rounded Cumulative Deal_Score_To_5: {rounded_cumulative_Deal_Score_To_5}")
                print(f"ℹ️ Rounded Displayed Deal_Score_To_2: {rounded_displayed_Deal_Score_To_2}, Rounded Displayed Deal_Score_To_3: {rounded_displayed_Deal_Score_To_3}, Rounded Displayed Deal_Score_To_4: {rounded_displayed_Deal_Score_To_4}, Rounded Displayed Deal_Score_To_5: {rounded_displayed_Deal_Score_To_5}")
        
                if cm.assertExpectedActualText(str(rounded_cumulative_Deal_Score_To_2), str(rounded_displayed_Deal_Score_To_2)):
                    logger.info("Deal_Score_To_2 comparison passed")
                    print("✅ Deal_Score_To_2 comparison passed")
                elif mq.isWithinTolerance(rounded_cumulative_Deal_Score_To_2, rounded_displayed_Deal_Score_To_2):
                    logger.info("Deal_Score_To_2 difference is within 0.01 tolerance")
                    print("✅ Deal_Score_To_2 difference is within 0.01 tolerance")
                else:
                    logger.error("Deal_Score_To_2 comparison failed")
                    print("❌ Deal_Score_To_2 comparison failed")
                    validation_failures.append(
                        f"Deal_Score_To_2 mismatch. Cumulative: {rounded_cumulative_Deal_Score_To_2}, Displayed: {rounded_displayed_Deal_Score_To_2}"
                    )

                if cm.assertExpectedActualText(str(rounded_cumulative_Deal_Score_To_3), str(rounded_displayed_Deal_Score_To_3)):
                    logger.info("Deal_Score_To_3 comparison passed")
                    print("✅ Deal_Score_To_3 comparison passed")
                elif mq.isWithinTolerance(rounded_cumulative_Deal_Score_To_3, rounded_displayed_Deal_Score_To_3):
                    logger.info("Deal_Score_To_3 difference is within 0.01 tolerance")
                    print("✅ Deal_Score_To_3 difference is within 0.01 tolerance")
                else:
                    logger.error("Deal_Score_To_3 comparison failed")
                    print("❌ Deal_Score_To_3 comparison failed")
                    validation_failures.append(
                        f"Deal_Score_To_3 mismatch. Cumulative: {rounded_cumulative_Deal_Score_To_3}, Displayed: {rounded_displayed_Deal_Score_To_3}"
                    )

                if cm.assertExpectedActualText(str(rounded_cumulative_Deal_Score_To_4), str(rounded_displayed_Deal_Score_To_4)):
                    logger.info("Deal_Score_To_4 comparison passed")
                    print("✅ Deal_Score_To_4 comparison passed")
                elif mq.isWithinTolerance(rounded_cumulative_Deal_Score_To_4, rounded_displayed_Deal_Score_To_4):
                    logger.info("Deal_Score_To_4 difference is within 0.01 tolerance")
                    print("✅ Deal_Score_To_4 difference is within 0.01 tolerance")
                else:
                    logger.error("Deal_Score_To_4 comparison failed")
                    print("❌ Deal_Score_To_4 comparison failed")
                    validation_failures.append(
                        f"Deal_Score_To_4 mismatch. Cumulative: {rounded_cumulative_Deal_Score_To_4}, Displayed: {rounded_displayed_Deal_Score_To_4}"
                    )

                if cm.assertExpectedActualText(str(rounded_cumulative_Deal_Score_To_5), str(rounded_displayed_Deal_Score_To_5)):
                    logger.info("Deal_Score_To_5 comparison passed")
                    print("✅ Deal_Score_To_5 comparison passed")
                elif mq.isWithinTolerance(rounded_cumulative_Deal_Score_To_5, rounded_displayed_Deal_Score_To_5):
                    logger.info("Deal_Score_To_5 difference is within 0.01 tolerance")
                    print("✅ Deal_Score_To_5 difference is within 0.01 tolerance")
                else:
                    logger.error("Deal_Score_To_5 comparison failed")
                    print("❌ Deal_Score_To_5 comparison failed")
                    validation_failures.append(
                        f"Deal_Score_To_5 mismatch. Cumulative: {rounded_cumulative_Deal_Score_To_5}, Displayed: {rounded_displayed_Deal_Score_To_5}"
                    )
                    
                if displayed_Total_List_Price == 0:
                    logger.error("Total List Price is 0. Cannot calculate Deal Score percentages.")
                    print("❌ Total List Price is 0. Cannot calculate Deal Score percentages.")
                    validation_failures.append("Total List Price is 0. Cannot calculate Deal Score percentages.")
                else:
                    print(f"ℹ️ Displayed Total List Price: {displayed_Total_List_Price}")

                    calculated_percentages = mq.calculateDealScorePercentages(
                        displayed_Total_List_Price,
                        displayed_Deal_Score_To_2,
                        displayed_Deal_Score_To_3,
                        displayed_Deal_Score_To_4,
                        displayed_Deal_Score_To_5,
                    )

                    calculated_Deal_Score_To_2_Percent = calculated_percentages["Deal_Score_To_2_Percent"]
                    calculated_Deal_Score_To_3_Percent = calculated_percentages["Deal_Score_To_3_Percent"]
                    calculated_Deal_Score_To_4_Percent = calculated_percentages["Deal_Score_To_4_Percent"]
                    calculated_Deal_Score_To_5_Percent = calculated_percentages["Deal_Score_To_5_Percent"]

                    rounded_displayed_Deal_Score_To_2_Percent = cm.roundOff(displayed_Deal_Score_To_2_Percent, 2)
                    rounded_displayed_Deal_Score_To_3_Percent = cm.roundOff(displayed_Deal_Score_To_3_Percent, 2)
                    rounded_displayed_Deal_Score_To_4_Percent = cm.roundOff(displayed_Deal_Score_To_4_Percent, 2)
                    rounded_displayed_Deal_Score_To_5_Percent = cm.roundOff(displayed_Deal_Score_To_5_Percent, 2)

                    logger.info(f"Calculated Deal_Score_To_2(%): {calculated_Deal_Score_To_2_Percent}, Displayed Deal_Score_To_2(%): {rounded_displayed_Deal_Score_To_2_Percent}")
                    logger.info(f"Calculated Deal_Score_To_3(%): {calculated_Deal_Score_To_3_Percent}, Displayed Deal_Score_To_3(%): {rounded_displayed_Deal_Score_To_3_Percent}")
                    logger.info(f"Calculated Deal_Score_To_4(%): {calculated_Deal_Score_To_4_Percent}, Displayed Deal_Score_To_4(%): {rounded_displayed_Deal_Score_To_4_Percent}")
                    logger.info(f"Calculated Deal_Score_To_5(%): {calculated_Deal_Score_To_5_Percent}, Displayed Deal_Score_To_5(%): {rounded_displayed_Deal_Score_To_5_Percent}")
                    print(f"ℹ️ Calculated Deal_Score_To_2(%): {calculated_Deal_Score_To_2_Percent}, Displayed Deal_Score_To_2(%): {rounded_displayed_Deal_Score_To_2_Percent}")
                    print(f"ℹ️ Calculated Deal_Score_To_3(%): {calculated_Deal_Score_To_3_Percent}, Displayed Deal_Score_To_3(%): {rounded_displayed_Deal_Score_To_3_Percent}")
                    print(f"ℹ️ Calculated Deal_Score_To_4(%): {calculated_Deal_Score_To_4_Percent}, Displayed Deal_Score_To_4(%): {rounded_displayed_Deal_Score_To_4_Percent}")
                    print(f"ℹ️ Calculated Deal_Score_To_5(%): {calculated_Deal_Score_To_5_Percent}, Displayed Deal_Score_To_5(%): {rounded_displayed_Deal_Score_To_5_Percent}")

                    if cm.assertExpectedActualText(str(calculated_Deal_Score_To_2_Percent), str(rounded_displayed_Deal_Score_To_2_Percent)):
                        logger.info("Deal_Score_To_2(%) comparison passed")
                        print("✅ Deal_Score_To_2(%) comparison passed")
                    else:
                        logger.error("Deal_Score_To_2(%) comparison failed")
                        print("❌ Deal_Score_To_2(%) comparison failed")
                        validation_failures.append(
                            f"Deal_Score_To_2(%) mismatch. Calculated: {calculated_Deal_Score_To_2_Percent}, Displayed: {rounded_displayed_Deal_Score_To_2_Percent}"
                        )

                    if cm.assertExpectedActualText(str(calculated_Deal_Score_To_3_Percent), str(rounded_displayed_Deal_Score_To_3_Percent)):
                        logger.info("Deal_Score_To_3(%) comparison passed")
                        print("✅ Deal_Score_To_3(%) comparison passed")
                    else:
                        logger.error("Deal_Score_To_3(%) comparison failed")
                        print("❌ Deal_Score_To_3(%) comparison failed")
                        validation_failures.append(
                            f"Deal_Score_To_3(%) mismatch. Calculated: {calculated_Deal_Score_To_3_Percent}, Displayed: {rounded_displayed_Deal_Score_To_3_Percent}"
                        )

                    if cm.assertExpectedActualText(str(calculated_Deal_Score_To_4_Percent), str(rounded_displayed_Deal_Score_To_4_Percent)):
                        logger.info("Deal_Score_To_4(%) comparison passed")
                        print("✅ Deal_Score_To_4(%) comparison passed")
                    else:
                        logger.error("Deal_Score_To_4(%) comparison failed")
                        print("❌ Deal_Score_To_4(%) comparison failed")
                        validation_failures.append(
                            f"Deal_Score_To_4(%) mismatch. Calculated: {calculated_Deal_Score_To_4_Percent}, Displayed: {rounded_displayed_Deal_Score_To_4_Percent}"
                        )

                    if cm.assertExpectedActualText(str(calculated_Deal_Score_To_5_Percent), str(rounded_displayed_Deal_Score_To_5_Percent)):
                        logger.info("Deal_Score_To_5(%) comparison passed")
                        print("✅ Deal_Score_To_5(%) comparison passed")
                    else:
                        logger.error("Deal_Score_To_5(%) comparison failed")
                        print("❌ Deal_Score_To_5(%) comparison failed")
                        validation_failures.append(
                            f"Deal_Score_To_5(%) mismatch. Calculated: {calculated_Deal_Score_To_5_Percent}, Displayed: {rounded_displayed_Deal_Score_To_5_Percent}"
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
            logger.info(f"***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}***")
            print(f"✅ ***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']} ***")

        else:
            logger.info(f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}")
            print(f"➡️ Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}")
            pytest.skip(f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}")
 
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
 