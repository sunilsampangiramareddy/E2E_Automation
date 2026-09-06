import pytest
import logging
import os
from playwright.sync_api import Page
from pages_CPQ.Account_Information_Page import AccountInformationPage
from pages_CPQ.Approval_Request_Page import ApprovalRequestPage
from pages_CPQ.Products_Addition_Page import ProductsAdditionPage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data
from common_Methods.Common_Methods import CommonMethods
 
 
# =========================================================================================================================
# Test Metadata
# =========================================================================================================================

# Test Scenario: 526617  - Copy Private Offer Quote for Open Opportunity by Internal Sales Rep
#                525308  - Verify that the user can initiate a 'Request Private Offer' on the Quote only if all eligibility criteria are met.
#                527835  - Lock Hyperscaler Field When Private Offer Quote Exists
#                524828  - Verify all required fields are created on the Salesforce Quote object for Marketplace Private Offer details.
#                527315  - Verify that the 'Move Quote' action is disabled or restricted for Private Offer Quotes in the Quote Console.
#                525222  - TC1: Capture Private Offer Identifier on Quote from CPQ Integration & display flag on Spark

# Test Description:
#                1. Login to SFDC and create Opportunity (Standard/1P with channel-specific steps).
#                2. Add product in SFDC and create CPQ quote with Private Offer = Yes.
#                3. Configure products and capture quote details.
#                4. Validate hyperscaler lock behavior when related Private Offer quote exists.
#                5. Sync quote to SFDC and validate marketplace private-offer fields/flags on Salesforce Quote.
#                6. Submit and approve Approval Request (including justification and competition details).
#                7. Validate quote status and eligibility checks (Active + Private Offer Quote) before Request Private Offer.
#                8. Validate Private Offer quote governance actions in quote console (copy allowed, move restricted).

# Author: Ashwathy Sreelekha/Alok Kumar Gupta
# Modified by: Alok kumar Gupta
# Reviewed by: Sunil Reddy
# =========================================================================================================================
 
 
logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join("testData/tests_SFDC_Regression", "TC_Private_Offer_E2E.xlsx")
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
def test_Private_Offer_E2E(page: Page, base_url, config, test_case) -> None:
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []
    oppty_number = "N/A"
    oppty_name = "N/A"
    direct_Oppty = "Direct"
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

            # =======================Create Opportunity===========================================================================
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

                cm.clickElement("HomePage_CPQ", "private_Offer_Combobox")
                cm.clickElementAndWait("HomePage_CPQ", "private_Offer_Yes_Option",5)
                logger.info(f"Selected private offer option: Yes")

                if is_valid_data(test_case["Hyperscaler"]):
                    cm.scrollAndForceClick("HomePage_CPQ", "hyperscaler_Combobox")
                    cm.clickByText(test_case["Hyperscaler"])
                    logger.info(f"Selected hyperscaler: {test_case['Hyperscaler']}")

                cm.clickElementAndWait("HomePage_CPQ", "save_Button",10)
                logger.info(f"Clicked on save button")

                quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                logger.info(f"Quote Name: {quote_name}")
                print(f"ℹ️ Quote Name: {quote_name}")

                

                if test_case["Hyperscaler Error Validation"].strip().lower() == "yes":
                    first_Tab = cm.switchToTab(page.context, tab_index= 0, expected_tab_count=2)
                    cm = CommonMethods(first_Tab, locator_manager)
                    logger.info("Switched to main SFDC tab for hyperscaler validation")
                    cm.waitForStable(2)
                    cm.clickElement("CreateOpportunity", "edit_Hyperscaler_Button")
                    cm.waitForStable(2)
                    cm.scrollAndForceClick("CreateOpportunity", "hyperscaler_Dropdown_Button")
                    cm.clickElementsInSequence([{"title": test_case["Updated Hyperscaler"]}])
                    logger.info(f"Selected hyperscaler: {test_case['Updated Hyperscaler']}")

                    cm.clickElement("CreateOpportunity", "save_Edit_Button")
                    logger.info("Clicked Save Edit button")

                    error_message_text = cm.readText("CreateOpportunity", "hyperscaler_Error_Message")
                    logger.info(f"Error message text: {error_message_text}")
                    if cm.assertExpectedInActualText(error_message_text, test_case["Hyperscaler Error Text"]):
                        logger.info("Validated hyperscaler error message")
                        print(f"✅ Error message validated: Hyperscaler cannot be changed as related Private offer Quote exists.")
                    else:
                        print("❌ Expected error message: 'Hyperscaler cannot be changed as related Private offer Quote exists.'")
                        validation_failures.append("Expected error message: 'Hyperscaler cannot be changed as related Private offer Quote exists.'")

                    second_Tab = cm.switchToTab(page.context, tab_index= 1 , expected_tab_count=2)
                    logger.info(f"ScreenshotUtil instance created for the Second tab")
                    cm = CommonMethods(second_Tab, locator_manager)


                if test_case["MarketPlace PrivateOffer Validation"].strip().lower() == "yes":
                    cm.clickElement("HomePage_CPQ", "more_Actions_Button")
                    cm.clickElementAndWait("HomePage_CPQ", "sync_Quote_To_SFDC_Menuitem", 5)
                    logger.info(f"Clicked on Sync Quote to SFDC button")

                    first_Tab = cm.switchToTab(page.context, tab_index= 0, expected_tab_count=2)
                    cm = CommonMethods(first_Tab, locator_manager)
                    logger.info("Switched to main SFDC tab for marketplace private offer validation")
                    cm.waitForStable(30)
                    cm.refreshPage()
                    logger.info("Page refreshed")
                    cm.waitForStable(2)

                    cm.clickElement("HomePage", "global_Search_Button")
                    cm.enterText("HomePage", "global_Search_Input", quote_name)
                    cm.clickByTextByPosition(quote_name, "nth", 1)
                    logger.info(f"Searched for quote name: {quote_name}")
                    cm.waitForStable(3)

                    cm.mouseWheelToBottom(800, scrolls=8, wait_time=0)

                    private_offer_elements = [
                        ("Marketplace_Private_Offer_Text", "Marketplace Private Offer section"),
                        ("Edit_Marketplace_Private_Offer_ID_Button", "Edit Marketplace Private Offer ID button"),
                        ("Edit_Private_Offer_Creation_Date_Button", "Edit Private Offer Creation Date button"),
                        ("Edit_Private_Offer_Expiration_Date_Button", "Edit Private Offer Expiration Date button"),
                        ("Edit_Private_Offer_Acceptance_Date_Button", "Edit Private Offer Acceptance Date button"),
                        ("Edit_Private_Offer_End_Date_Button", "Edit Private Offer End Date button"),
                        ("Edit_Contract_End_Date_Button", "Edit Contract End Date button"),
                        ("Edit_Hyperscaler_Button", "Edit Hyperscaler button"),
                        ("Edit_Hyperscaler_Partner_ID_Button", "Edit Hyperscaler Partner ID button"),
                        ("Edit_Marketplace_Private_Offer_Name_Button", "Edit Marketplace Private Offer Name button"),
                        ("Edit_Private_Offer_Status_Button", "Edit Private Offer Status button"),
                        ("Edit_Private_Offer_Activation_Date_Button", "Edit Private Offer Activation Date button"),
                        ("Edit_Contract_Start_Date_Button", "Edit Contract Start Date button"),
                        ("Edit_Private_Offer_Quote_Button", "Edit Private Offer Quote button"),
                        ("Edit_Hyperscaler_Customer_ID_Button", "Edit Hyperscaler Customer ID button"),
                        ("Edit_Renewal_Existing_Private_Offer_Button", "Edit Renewal/Existing Private Offer button"),
                    ]

                    for locator_key, description in private_offer_elements:
                        if cm.isElementVisible("PrivateOfferPage", locator_key):
                            print(f"✅ {description} is visible")
                        else:
                            print(f"❌ {description} is not visible")
                            validation_failures.append(f"{description} is not visible")

                    cm.clickElement("PrivateOfferPage", "Edit_Private_Offer_Quote_Button")
                    logger.info("Clicked on Edit Private Offer Quote button")

                    is_selected = cm.isElementChecked("PrivateOfferPage", "Private_Offer_Quote_Checkbox")
                    if is_selected:
                        print("✅ The 'Private Offer Quote' checkbox is currently SELECTED, thus the Flag is displayed in Spark")
                    else:
                        print("❌ The 'Private Offer Quote' checkbox is NOT selected")
                        validation_failures.append("The 'Private Offer Quote' checkbox is not selected")

                    hyperscaler_actual = cm.getInputValue("PrivateOfferPage", "Hyperscaler_Input")
                    logger.info(f"Hyperscaler value on page: {hyperscaler_actual}")
                    if cm.assertExpectedInActualText(hyperscaler_actual, test_case["Hyperscaler"]):
                        print(f"✅ Hyperscaler validated: '{hyperscaler_actual}' matches expected '{test_case['Hyperscaler']}'")
                    else:
                        print(f"❌ Hyperscaler mismatch: expected '{test_case['Hyperscaler']}', got '{hyperscaler_actual}'")
                        validation_failures.append(f"Hyperscaler mismatch: expected '{test_case['Hyperscaler']}', got '{hyperscaler_actual}'")

                    second_Tab = cm.switchToTab(page.context, tab_index= 1 , expected_tab_count=2)
                    logger.info(f"ScreenshotUtil instance created for the Second tab")
                    cm = CommonMethods(second_Tab, locator_manager)



                if test_case["Copy Private Offer Quote Validation"].strip().lower() == "yes":
                    cm.clickElement("HomePage_CPQ", "more_Actions_Button")
                    cm.waitForStable(1)
                    cm.clickElementAndWait("HomePage_CPQ", "sync_Quote_To_SFDC_Menuitem", 5)
                    logger.info(f"Clicked on Sync Quote to SFDC button")
                    first_Tab = cm.switchToTab(page.context, tab_index= 0, expected_tab_count=2)
                    cm = CommonMethods(first_Tab, locator_manager)
                    logger.info("Switched to main SFDC tab for marketplace private offer validation")
                    cm.waitForStable(15)
                    cm.refreshPage()
                    cm.waitForStable(15)
                    cm.refreshPage()
                    logger.info("Page refreshed")

                    cm.clickElement("PrivateOfferQuotesPage", "quotes_Link_2")
                    logger.info("Clicked on Quotes link")
                    cm.waitForStable(30)
                    cm.clickElementByPosition("PrivateOfferQuotesPage", "combobox_Button_Quote_Type", "nth", 0)
                    logger.info("Clicked on combobox button for quote type")
                    cm.clickByText("Private Offer Quotes")
                    logger.info("Clicked on Private Offer Quotes")
                    cm.clickElementByPosition("PrivateOfferQuotesPage", "combobox_Button_Search_Field", "nth", 1)
                    logger.info("Clicked on combobox button for search field")
                    cm.clickElement("PrivateOfferQuotesPage", "quote_Name_Option")
                    logger.info("Selected Quote Name option")
                    cm.clickElement("PrivateOfferQuotesPage", "search_Input")
                    logger.info("Clicked on search input field")
                    cm.enterText("PrivateOfferQuotesPage", "search_Input", quote_name, clear_first=False)
                    logger.info(f"Filled search field with: {quote_name}")
                    cm.clickElement("PrivateOfferQuotesPage", "search_Button")
                    logger.info("Clicked Search button")
                    cm.waitForStable(8)
                    cm.clickElement("PrivateOfferQuotesPage", "show_Actions_Button")
                    logger.info("Clicked on Show actions button")
                    is_move_button_visible = cm.isElementVisible("PrivateOfferQuotesPage", "Move_Button")
                    if is_move_button_visible:
                        print("❌ Move button is available, but it should not be visible")
                        validation_failures.append("Move button is available after clicking Show actions")
                    else:
                        print("✅ Move action is not available for Private Offer Quotes")
                    cm.clickElement("PrivateOfferQuotesPage", "copy_Button")
                    logger.info("Clicked on Copy button to copy the private offer quote")
                    print("✅ Clicked Copy button to copy the private offer quote")

                    third_Tab = cm.switchToTab(page.context, tab_index= 2, expected_tab_count=3)
                    cm = CommonMethods(third_Tab, locator_manager)
                    logger.info("Switched to the third tab for the copied quote")

                    cm.waitForStable(5)
                    copy_tab_quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                    logger.info(f"Copied quote name: {copy_tab_quote_name}")
                    if cm.assertExpectedInActualText(copy_tab_quote_name, "Copy"):
                        print(f"✅ Copied quote name contains 'Copy': {copy_tab_quote_name}")
                    else:
                        print(f"❌ Copied quote name does not contain 'Copy': {copy_tab_quote_name}")
                        validation_failures.append(f"Copied quote name does not contain 'Copy': {copy_tab_quote_name}")
            

                    
                

            # ============================Capture Quote Details==========================================================================
        
            if test_case["Capture Quote Details"].strip().lower() == "yes":

                quote_number = cm.readText("HomePage_CPQ", "quote_Number")
                logger.info(f"Quote Number: {quote_number}")
                print(f"ℹ️ Quote Number: {quote_number}")

                quote_name = cm.readText("HomePage_CPQ", "quote_Name")
                logger.info(f"Quote Name: {quote_name}")
                print(f"ℹ️ Quote Name: {quote_name}")

                quote_status = cm.readText("HomePage_CPQ", "quote_Status")
                ss.capture_screenshot("Captured Quote details")
                logger.info(f"Quote Status: {quote_status}")
                print(f"ℹ️ Quote Status: {quote_status}")

                cpq_url = cm.getCurrentURL()
                logger.info(f"CPQ URL: {cpq_url}")
                print(f"ℹ️ CPQ URL: {cpq_url}")

            # =============================Configure Private Offer Product================================================================
            if test_case["Configure Product"].strip().lower() == "yes":
            
                cm.clickElement("ProductsPage", "products_Tab")
                logger.info(f"Clicked on Products tab")

                cm.clickElement("ProductsPage", "configure_Button")
                logger.info(f"Clicked on Configure button")

                pap = ProductsAdditionPage(second_Tab)
                pap.addProductListing(
                    test_case["Product listing"],
                    test_case["Terms"],
                    test_case["Cycle"],
                    test_case["Product Name Private Offer"],
                    test_case["Quantity"],
                )
                logger.info(f"Added product listing")

            # ==============================Account Information Tab=================================================================================
            if test_case["Account Information"].strip().lower() == "yes":
            
                aip = AccountInformationPage(second_Tab)
                logger.info(f"AccountInformationPage instance created for the new tab")

                cm.clickElement("AccountInformationPage", "account_Information_Tab")
                logger.info(f"Clicked on Account Information Tab")

                if is_valid_data(test_case["First Name_End Customer"]):
                    aip.enterEndCustomer_3(test_case["First Name_End Customer"], test_case["Last Name_End Customer"])
                    logger.info(f"Entered End Customer details: {test_case['First Name_End Customer']}, {test_case['Last Name_End Customer']}")
                    aip.enterServiceCustomer_3()
                    logger.info(f"Entered Service Customer details")

                cm.clickElement("HomePage_CPQ", "save_Icon")
                ss.capture_screenshot("Captured Account Information details")
                logger.info(f"Clicked on Save button")

                cm.waitForStable(5)
                logger.info(f"Waited for 5 seconds after saving Account Information details")

            # ======================================Approval Request Tab=================================================================================
            if test_case["Approval Request Tab"].strip().lower() == "yes":
            
                ar = ApprovalRequestPage(second_Tab)
                logger.info(f"ApprovalRequestPage instance created for the new tab")

                cm.clickElement("ApprovalRequestPage", "approval_Request_Tab")
                logger.info(f"Clicked on Approval request tab")

                cm.clickElement("ApprovalRequestPage", "justification_Combobox")
                cm.clickByText(test_case["Justification"])
                logger.info(f"Selected justification: {test_case['Justification']}")

                cm.enterText("ApprovalRequestPage", "justification_Details_Textbox", "Test")

                cm.clickElement("ApprovalRequestPage", "competition_Tab")
                cm.clickElement("ApprovalRequestPage", "competitor_Name_Combobox")
                cm.clickElement("ApprovalRequestPage", "competitor_Dell_Option")
                cm.enterText("ApprovalRequestPage", "competitor_Offering_Textbox", "test")
                cm.enterText("ApprovalRequestPage", "competitor_Pricing_Textbox", "10")

                cm.clickElementAndWait("ApprovalRequestPage", "initiate_Approval", 20)
                logger.info(f"Clicked on Initiate Approval button")

                cm.clickElementAndWait("ApprovalRequestPage", "submit_For_Approval_Button_2", 20)
                ar.approveRequest()
                logger.info(f"Approval request submitted and approved")

                
            # =========================================Sync quote to SFDC and SFDC Validations=================================================================
            if test_case["Request Private Offer Validation"].strip().lower() == "yes":

                cm.clickElement("QuoteInfoPage", "quote_Info_Tab")
                cm.clickElement("HomePage_CPQ", "more_Actions_Button")
                cm.clickElementAndWait("HomePage_CPQ", "sync_Quote_To_SFDC_Menuitem", 5)
                logger.info(f"Clicked on Sync Quote to SFDC button")

                first_Tab = cm.switchToTab(page.context, tab_index= 0, expected_tab_count=2)
                cm = CommonMethods(first_Tab, locator_manager)
                logger.info("Switched to main SFDC tab for marketplace private offer validation")
                cm.waitForStable(30)
                cm.refreshPage()
                logger.info("Page refreshed")
                cm.waitForStable(2)

                cm.clickElement("HomePage", "global_Search_Button")
                cm.enterText("HomePage", "global_Search_Input", quote_name)
                cm.clickByTextByPosition(quote_name, "nth", 1)
                logger.info(f"Searched for quote name: {quote_name}")
                cm.waitForStable(3)
                logger.info(f"Waiting for 3 seconds after searching for quote name: {quote_name}")

                actual_quote_status = cm.readText("OpportunityQuotesPage", "quote_Status")
                logger.info(f"Quote status in quote details page: {actual_quote_status}")
                result = cm.assertExpectedInActualText(actual_quote_status, test_case["Expected Quote Status"])
                if result:
                    logger.info(f"Validated quote status in quote details page")
                    print(f"✅ Quote status validated in quote details page: {actual_quote_status}")
                else:
                    print(f"❌ Expected quote status '{test_case['Expected Quote Status']}' in quote details page, got '{actual_quote_status}'")
                    validation_failures.append(f"Expected quote status '{test_case['Expected Quote Status']}' in quote details page, got '{actual_quote_status}'")

                cm.clickElement("PrivateOfferPage", "Edit_Active_Button")
                logger.info("Clicked on Edit Active button")

                is_active_selected = cm.isElementChecked("PrivateOfferPage", "Active_Checkbox")
                if is_active_selected:
                    print("✅ The 'Active' checkbox is currently SELECTED")
                else:
                    print("❌ The 'Active' checkbox is NOT selected")
                    validation_failures.append("The 'Active' checkbox is not selected")

                cm.mouseWheelToBottom(800, scrolls=8, wait_time=0)
                logger.info("Scrolled to the bottom of the page to check for Private Offer Quote checkbox")

                is_selected = cm.isElementChecked("PrivateOfferPage", "Private_Offer_Quote_Checkbox")
                if is_selected:
                    print("✅ The 'Private Offer Quote' checkbox is currently SELECTED")
                else:
                    print("❌ The 'Private Offer Quote' checkbox is NOT selected")
                    validation_failures.append("The 'Private Offer Quote' checkbox is not selected")

                if result and is_active_selected and is_selected:
                    cm.clickElement("OpportunityQuotesPage", "request_Private_Offer_Button")
                    logger.info("Clicked on Request Private Offer button")
                    is_request_private_offer_text_visible = cm.isElementVisible("OpportunityQuotesPage", "request_Private_Offer_Text")
                    if is_request_private_offer_text_visible:
                        print("✅ 'Request Private Offer' button is displayed")
                    else:
                        print("❌ 'Request Private Offer' button is not displayed")
                        validation_failures.append("'Request Private Offer' button is not displayed")
                else:
                    print("❌ Skipping 'Request Private Offer' button check, because prerequisite validations failed")

            
                
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
 