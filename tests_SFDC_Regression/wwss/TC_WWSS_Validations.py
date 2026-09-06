import pytest
import logging
import os
from playwright.sync_api import Page
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.Opportunity_Detail_Page import OpportunityDetailPage
from pages_SFDC.Wwss_Forecasting_Request import WWSSForecastingRequest
from utils.locator_manager import LocatorManager
from utils.screenshot_util import ScreenshotUtil
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults
from utils.data_validation import is_valid_data

# =========================================================================================================================
# Test Metadata
# =========================================================================================================================
# ADO Test ID : 483721, 473942, 486042, 481688
# Test Scenario:
# 1. Verify Creation and validations of WWSS Forecasting Request & Service Category records_ Base Sales CE User_Std In Direct Oppty
# 2. Verify Creation and validations of WWSS Forecasting Request & Service Category records_ Base Sales CE User_Std Direct Oppty
# 3. TC_Verify Opportunity Owner, Stage, Close Date, Number on WWSS Forecasting Request
# 4. validation WWSS forecasting request for indirect opty_Internal user
# Test Description:
# 1. Logging into the Salesforce application.
# 2. Creating opportunities with various configurations (Direct, Indirect, Standard, 1P).
# 3. Adding WWSS Forecasting Requests to opportunities.
# 4. Validating WWSS Forecasting Request owner and booking amounts.
# 5. Performing actions on WWSS Forecasting Requests, including adding service categories and editing amounts.
# 6. Capturing test results and writing them to an Excel file for reporting purposes.
# Author & Modifier: Aswathy S
# Reviewer: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")

# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_WWSS_Validations.xlsx"
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
def test_WWSS_Validations(page: Page, base_url, config, test_case) -> None:
    cm = CommonMethods(page, locator_manager)
    ss = ScreenshotUtil(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    od = OpportunityDetailPage(page)
    wwss = WWSSForecastingRequest(page)
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
                            if is_valid_data(test_case["Sales Type"]):
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

                        if test_case["Opportunity Type"] == x1p_Oppty:
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

                        
                        if (
                            test_case["Channel"] == indirect_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):
                            # cm.clickElement("CreateOpportunity", "next_Button")
                            # logger.info(f"Clicked on next button")
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

                        oppty_owner = cm.readText("HomePage", "owner_Label")
                        logger.info(f"Opportunity Owner: {oppty_owner}")

                spark_url = cm.getCurrentURL()
                logger.info(f"Captured Spark URL: {spark_url}")
                print(f"\033[94mℹ️ Captured Spark URL: {spark_url}\033[0m")

            if test_case["Add WWSS Forecasting Request"].strip().lower() == "yes":
                od.selectWWSSForecastingRequest(test_case["Deal Option"], oppty_owner)
                logger.info("WWSS option selected and added")

            if (
                test_case["Validate WWSS Forecasting Request Owner"].strip().lower()
                == "yes"
            ):
                owner = cm.readText("HomePage", "owner_Label_WWSS")
                logger.info(f"Validated WWSS Forecasting Request owner: {owner}")

                validation_result = cm.compareExpectedActualText(owner, oppty_owner)
                if not validation_result:
                    failure_message = f"WWSS Forecasting Request Owner Validation Failed: Expected '{oppty_owner}' but got '{owner}'"
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(f"WWSS Forecasting Request owner validation passed")
                    print(
                        f"\033[92m✅ WWSS Forecasting Request owner validation passed\033[0m"
                    )

                wwss_url = cm.getCurrentURL()
                logger.info(f"Captured WWSS Forecasting Request URL: {wwss_url}")

            if test_case["Add Service Category"].strip().lower() == "yes":
                cm.clickElementByPosition(
                    "HomePage", "service_Categories_Link", "nth", 0
                )
                logger.info("Clicked on Service Categories link")

                cm.clickElement("HomePage", "new_Button")
                logger.info("Clicked on New button to add service category")

                wwss.addServiceCategory(
                    test_case["FST Code"],
                    test_case["Parent Category"],
                    str(test_case["Estimated TeraBytes (TBs)"]),
                    test_case["Source Storage"],
                )
                logger.info(
                    f"Added service category with FST Code: {test_case['FST Code']} and Parent Category: {test_case['Parent Category']}"
                )

                cm.clickElementByPosition("HomePage", "save_Button", "nth", 1)
                logger.info("Service category added")

            if test_case["Edit Service Category"].strip().lower() == "yes":

                cm.clickElementByPosition("HomePage", "service_Category_Link", "nth", 0)
                logger.info("Clicked on Service Category link")

                cm.clickElement("HomePage", "edit_Override_Discount_Button")
                logger.info("Clicked on Edit Override Discount button")

                cm.enterText(
                    "HomePage", "override_Discount_Input", str(test_case["Quantity1"])
                )
                logger.info(f"Entered quantity: {test_case['Quantity1']}")

                cm.enterText(
                    "HomePage", "gross_Booking_Amount_Input", str(test_case["Amount1"])
                )
                logger.info(f"Entered amount: {test_case['Amount1']}")

                cm.clickElementByPosition("HomePage", "save_Button", "nth", 0)
                logger.info("Service category amounts edited")

                cm.navigateToUrl(wwss_url)
                logger.info(
                    f"Navigated back to WWSS Forecasting Request URL: {wwss_url}"
                )

            if test_case["Verify Booking Amounts"].strip().lower() == "yes":
                booking_amount = cm.readText("HomePage", "booking_Amount_Label")
                logger.info(f"Captured booking amount: {booking_amount}")

                validation_result = cm.compareExpectedActualText(
                    booking_amount, str(test_case["Amount_1"])
                )
                if not validation_result:
                    failure_message = f"Booking Amount Validation Failed: Expected '{test_case['Amount_1']}' but got '{booking_amount}'"
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(f"Booking amount validation passed")
                    print(f"\033[92m✅ Booking amount validation passed\033[0m")

            if test_case["Add Service Category"].strip().lower() == "yes":

                cm.clickElementByPosition(
                    "HomePage", "service_Categories_Link", "nth", 0
                )
                logger.info("Clicked on Service Categories link")

                cm.clickElement("HomePage", "new_Button")
                logger.info("Clicked on New button to add service category")

                wwss.addServiceCategory(
                    test_case["FST Code"],
                    test_case["Parent Category"],
                    str(test_case["Estimated TeraBytes (TBs)"]),
                    test_case["Source Storage"],
                )
                logger.info(
                    f"Added service category with FST Code: {test_case['FST Code']} and Parent Category: {test_case['Parent Category']}"
                )

                cm.clickElementByPosition("HomePage", "save_Button", "nth", 1)
                logger.info("Service category added second time")

            if test_case["Edit Service Category"].strip().lower() == "yes":
                cm.clickElementByPosition("HomePage", "service_Category_Link", "nth", 1)
                logger.info("Clicked on Service Category link")

                cm.clickElement("HomePage", "edit_Override_Discount_Button")
                logger.info("Clicked on Edit Override Discount button")

                cm.enterText(
                    "HomePage", "override_Discount_Input", str(test_case["Quantity2"])
                )
                logger.info(f"Entered override discount: {test_case['Quantity2']}")

                cm.enterText(
                    "HomePage", "gross_Booking_Amount_Input", str(test_case["Amount2"])
                )
                logger.info(f"Entered amount: {test_case['Amount2']}")

                cm.clickElement("HomePage", "save_Button")
                logger.info("Service category amounts edited second time")

                cm.navigateToUrl(wwss_url)
                logger.info(
                    f"Navigated back to WWSS Forecasting Request URL: {wwss_url}"
                )

            if test_case["Verify Booking Amounts"].strip().lower() == "yes":
                booking_amount = cm.readText("HomePage", "booking_Amount_Label")
                logger.info(f"Captured booking amount: {booking_amount}")

                validation_result = cm.compareExpectedActualText(
                    booking_amount, str(test_case["Amount_2"])
                )
                if not validation_result:
                    failure_message = f"Booking Amount Validation Failed: Expected '{test_case['Amount_2']}' but got '{booking_amount}'"
                    validation_failures.append(failure_message)
                    logger.warning(failure_message)
                    print(f"\033[91m❌ {failure_message}\033[0m")
                else:
                    logger.info(f"Booking amount validation passed")
                    print(f"\033[92m✅ Booking amount validation passed\033[0m")

            if test_case["Delete WWSS Forecasting Request"].strip().lower() == "yes":
                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")
                cm.waitForStable(5)

                cm.mouseWheel("HomePage",800, scrolls=1, wait_time=2)

                cm.scrollAndClick("HomePage", "show_All_Details_Button")
                logger.info("Clicked show all")

                cm.clickElementAndWait("HomePage", "wwss_Forecasting_Request_Tab", 5)
                logger.info("Opened WWSS Forecasting Request tab")

                cm.scrollAndForceClick("HomePage", "show_Actions")
                logger.info("Show actions clicked successfully")

                cm.clickElement("HomePage", "delete_Menuitem")
                logger.info("WWSS Forecasting Request deleted")

                cm.clickElement("HomePage", "delete_Button")
                logger.info("Deleted request")
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
