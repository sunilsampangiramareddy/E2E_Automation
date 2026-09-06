import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.write_excel_results import WriteExcelResults
from utils.excel_read import read_test_data
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# ADO Test ID - 469373
# Test Scenario:
# Verify deal registration for existing opportunity on Indirect opportunity
# Test Description:
# 1. Logging into the Salesforce application.
# 2 . Navigating to the Opportunities screen and selecting an existing indirect opportunity with base sales (CE).
# 3. Navigating to the Deal Registration section.
# 4. Filling in the necessary details for deal registration (e.g., Deal Name, Partner Information, Registration Details).
# 5. Submitting the deal registration.
# 6. Validating that the deal registration is successfully submitted and the status is updated correctly.
# 7. Capturing test results and writing them to an Excel file for reporting purposes.
# Author & Modifier: Ayushee
# Reviewer : Sunil Reddy
# =========================================================================================================================


logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_DealRegistration.xlsx"
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
def test_DealRegistration(page: Page, base_url, config, test_case) -> None:
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
                                co.selectInstalledBaseType(
                                    test_case["Installed Base Type"]
                                )
                                logger.info(
                                    f"Selected installed base type: {test_case['Installed Base Type']}"
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

                        if test_case["Opportunity Type"] == x1p_Oppty:
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

            spark_url = hp.getCurrentURL()
            logger.info(f"Captured Spark URL: {spark_url}")

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

            # ============== Converting Direct oppty to Indirect oppty ==================================
            if test_case["Convert To Indirect"].strip().lower() == "yes":
                second_Tab = cm.switchToTab(
                    page.context, tab_index=0, expected_tab_count=1
                )
                logger.info("Switched to the new tab")
                od = OpportunityDetailPage(second_Tab)
                cm.clickElement("HomePage", "show_more_actions")
                logger.info(f"Cliked on More Actions")
                cm.clickElement("HomePage", "convert_to_Indirect")
                logger.info(f"Cliked on Convert to Indirect oppty")
                if is_valid_data(test_case["Partner Sales Model"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "partner_Sales_Model",
                        test_case["Partner Sales Model"],
                    )
                    logger.info(
                        f"Selected partner sales model: {test_case['Partner Sales Model']}"
                    )
                if is_valid_data(test_case["Ship to or install in different country"]):
                    cm.selectOptionInListbox(
                        "HomePage",
                        "Ship_to_or_install_in_different_country",
                        test_case["Ship to or install in different country"],
                    )
                    logger.info(
                        f"Selected Ship to or install in different country: {test_case['Ship to or install in different country']}"
                    )
                if is_valid_data(test_case["Pathway"]):
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "pathway",
                        test_case["Pathway"],
                    )
                    logger.info(f"Selected pathway: {test_case['Pathway']}")
                cm.clickElement("HomePage", "save_Button")
                logger.info(f"Clicked on Save button")
                if is_valid_data(test_case["Reseller Account"]):
                    co.selectReseller(test_case["Reseller Account"])
                    logger.info(
                        f"Selected Reseller Account: {test_case["Reseller Account"]}"
                    )
                cm.clickElement("HomePage", "save_Button")
                logger.info(f"Clicked on Save button")
                cm.clickElementAndWait("HomePage", "save_Button", 5)
                logger.info(f"Clicked on Save button")

                if is_valid_data(test_case["Expected Channel"]):
                    cm.refreshPage()
                    logger.info(
                        f"Opportunity channel is: {test_case["Expected Channel"]}"
                    )
                if test_case["Opportunity Channel Validation"].strip().lower() == "yes":
                    if is_valid_data(test_case["Expected Channel"]):
                        opportunity_channel = cm.readTextAndWait(
                            "CreateOpportunity", "indirect_Opporty_Channel", wait_time=3
                        )
                        logger.info(
                            f"Captured opportunity channel: {opportunity_channel}"
                        )
                        channel_validation = cm.checkExpectedTextInActual(
                            actual_text=opportunity_channel,
                            expected_text=test_case["Expected Channel"],
                        )
                        if not channel_validation:
                            failure_message = f"Opportunity Channel Validation Failed: Expected '{test_case['Expected Channel']}' but got '{opportunity_channel}'"
                            validation_failures.append(
                                failure_message
                            )  # Add failure to the list
                            logger.warning(failure_message)
                            print(f"\033[91m❌ {failure_message}\033[0m")
                        else:
                            logger.info(
                                f"Compared actual opportunity channel: {opportunity_channel} with expected opportunity channel: {test_case['Expected Channel']}"
                            )
                            print(
                                f"\033[92m✅ Compared actual opportunity channel: {opportunity_channel} with expected opportunity channel: {test_case['Expected Channel']}\033[0m"
                            )

                # =======================================Deal Registration Creation====================================#
                if test_case["Create Deal Registration"].strip().lower() == "yes":
                    cm.clickElement("CreateOpportunity", "deal_Registration_Button")
                    logger.info(f"Clicked on Deal registration Button")

                    cm.clickElement("CreateOpportunity", "deal_Origination")
                    cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "deal_Origination",
                        test_case["Deal Origination"],
                    )
                    logger.info(f"Selected the option {test_case['Deal Origination']}")

                    cm.clickElement("CreateOpportunity", "planned_Activities_Checkbox")
                    logger.info(f"Selected the Planned Activities")

                    cm.clickElement(
                        "CreateOpportunity", "last_Meeting_Held_With_Customer"
                    )
                    logger.info(f"Clicked on Last Meeting Help With Customer button")

                    cm.clickElement(
                        "CreateOpportunity", "last_Meeting_Held_Date_Selection"
                    )
                    logger.info(f"Last Meeting Date got selected")

                    cm.clickElement("CreateOpportunity", "next_Meeting_Date_Button")
                    logger.info(f"Clicked on Next Meeting Date with customer button")

                    cm.clickElement("CreateOpportunity", "next_Month_Button")
                    logger.info(f"Clicked on Next Month Button")

                    cm.clickElement("CreateOpportunity", "next_Meeting_Date_Selection")
                    logger.info(f"Next meeting with customer date selected")

                    cm.enterText(
                        "CreateOpportunity",
                        "project_Description",
                        test_case["Project Description"],
                    )
                    logger.info(f"Project Description Entered")

                    cm.clickElementAndWait("CreateOpportunity", "next_Button_DR", 10)

                    deal_registration_number = cm.readText(
                        "CreateOpportunity", "deal_Registration_Number"
                    )
                    logger.info(f"Deal Registration Number: {deal_registration_number}")
                    print(
                        f"\033[94mℹ️ Deal Registration Number: {deal_registration_number}\033[0m"
                    )

                    if deal_registration_number:
                        logger.info("DR Created successfully")
                        print("\033[92m✅ DR Created successfully\033[0m")
                    else:
                        failure_message = f"Deal Registration is not created"
                        validation_failures.append(failure_message)
                        logger.warning(failure_message)
                        print(f"\033[91m❌ {failure_message}\033[0m")

            cm.navigateToUrl(spark_url)
            logger.info(f"Navigated back to Spark URL: {spark_url}")

            cm.mouseWheel("HomePage", 800, scrolls=1, wait_time=2)
            cm.scrollAndClick("HomePage", "show_All_Details_Button")
            logger.info("Clicked show all")
            cm.clickElement("CreateOpportunity", "deal_Reg_Oppty")

            cm.assertTrue(
                deal_registration_number, "Deal Registration is successfully verified"
            )
            logger.info(
                f"Deal Registration is successfully verified: {deal_registration_number}"
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
