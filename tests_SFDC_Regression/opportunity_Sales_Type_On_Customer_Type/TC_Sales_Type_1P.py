import pytest
import logging
import os
from playwright.sync_api import Page
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
# Test Scenario: 547146 - 491228 - 1P Opportunity from 1P Account – Customer Type = Expand and Protect
# Test Scenario: 547145 - 491228 TC07 – Sales Type automation for 1P Opportunity from Site Account – Customer Type = Land.

# Test Description: This test verifies Sales Type prefill logic, mandatory validation when Sales Type is cleared,
#                   and lock behavior of the Edit Sales Type option after opportunity creation/copy.

# Author:Ashwathy Sreelekha
# Modified By: Alok
# Review By: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_Sales_Type_1P.xlsx"
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
def test_Sales_Type_1P(page: Page, base_url, config, test_case) -> None:
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    cm = CommonMethods(page, locator_manager)
    boolean_status = "Pass"
    validation_failures = []
    direct_Oppty = "Direct"
    indirect_Oppty = "Indirect"
    std_Oppty = "Standard"
    x1p_Oppty = "1P"

    try:
        # ==================================Login to SFDC=================================================================================
        if test_case["Execution"].strip().lower() == "yes":
            page.goto(base_url)
            logger.info(f"Launching application URL: {base_url}")
            logger.info(
                f"*****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****"
            )
            print(
                f"ℹ️ *****{script_name} Test Script Execution Started for the Iteration:{test_case['Iteration']}*****"
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
            if is_visible:
                logger.info(
                    f"Opportunities label has been verified on the homepage: {is_visible}"
                )
                print(f"✅ Opportunities label verified on the homepage")
            else:
                print(f"❌ Opportunities label is not visible on the homepage")
                validation_failures.append(
                    "Opportunities label is not visible on the homepage"
                )

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

            frame_locator_setup = locator_manager.get_locator(
                "HomePage", "frame_Locator"
            )
            cm.switchToFrame(frame_locator_setup)

            cm.page.get_by_role("button", name="Login", exact=True).nth(1).click()
            logger.info("Clicked Login button from Setup frame")

            cm = CommonMethods(secondTab, locator_manager)
            logger.info(f"created instance of CommonMethods class with secondTab")
            co = CreateOpportunity(secondTab)
            logger.info(f"Created instance of CreateOpportunity class with secondTab")

            spark_url_home = cm.getCurrentURL()
            logger.info(f"Spark URL: {spark_url_home}")
            print(f"ℹ️ Spark URL: {spark_url_home}")

            # =======================Create Opportunity===========================================================================

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
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Play",
                                    test_case["Sales Play"],
                                )
                                logger.info(
                                    f"Selected sales play: {test_case['Sales Play']}"
                                )
                            if is_valid_data(test_case["Channel"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity", "channel", test_case["Channel"]
                                )
                                logger.info(f"Selected channel: {test_case['Channel']}")

                        if test_case["Opportunity Type"] == x1p_Oppty:

                            customer_type = (
                                str(test_case["Customer Type"]).strip().lower()
                            )

                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName_1p(
                                    test_case["Opportunity Name"]
                                )
                                logger.info(
                                    f"Entered 1P opportunity name: {test_case['Opportunity Name']}"
                                )

                            if (
                                is_valid_data(test_case["Sales Type"])
                                and customer_type == "land"
                            ):
                                result = cm.assertSelectedDropdownText(
                                    "CreateOpportunity",
                                    "1p_Sales_Type_Prefilled",
                                    test_case["Sales Type"],
                                )
                                if result:
                                    logger.info(
                                        f"Verified 1P sales type is prefilled based on customer type: {test_case['Sales Type']}"
                                    )
                                    print(
                                        f"✅ 1P Sales Type prefilled validated: {test_case['Sales Type']}"
                                    )
                                else:
                                    print(
                                        f"❌ Expected 1P sales type prefilled value to be '{test_case['Sales Type']}'"
                                    )
                                    validation_failures.append(
                                        f"Expected 1P sales type prefilled value to be '{test_case['Sales Type']}'"
                                    )

                                if (
                                    test_case["Sales Type Error"].strip().lower()
                                    == "yes"
                                ):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "sales_Type_1P_new",
                                        "--None--",
                                    )
                                    cm.clickElement("CreateOpportunity", "next_Button")
                                    sales_type_error_text = cm.getInnerText(
                                        "CreateOpportunity", "sales_Type_1P_Error"
                                    )
                                    result = cm.assertContainsText(
                                        "CreateOpportunity",
                                        "sales_Type_1P_Error",
                                        test_case["Error Text"],
                                    )
                                    if result:
                                        logger.info(
                                            f"Verified sales type cannot be empty"
                                        )
                                        print(
                                            f"✅ Sales Type empty validation error confirmed"
                                        )
                                    else:
                                        print(
                                            f"❌ Expected sales type validation error to contain 'Please select a choice.', but got '{sales_type_error_text}'"
                                        )
                                        validation_failures.append(
                                            f"Expected sales type validation error to contain 'Please select a choice.', but got '{sales_type_error_text}'"
                                        )

                                if is_valid_data(test_case["Sales Type Invalid"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "sales_Type_1P_new",
                                        test_case["Sales Type Invalid"],
                                    )
                                    logger.info(
                                        f"Selected sales type: {test_case['Sales Type Invalid']}"
                                    )

                            if is_valid_data(
                                test_case["Sales Type"]
                            ) and customer_type in ["expand", "protect"]:

                                result = cm.assertSelectedDropdownText(
                                    "CreateOpportunity",
                                    "sales_Type_Prefilled2",
                                    test_case["Sales Type"],
                                )
                                if result:
                                    logger.info(
                                        f"Verified sales type is prefilled based on customer type: {test_case['Sales Type']}"
                                    )
                                    print(
                                        f"✅ Sales Type prefilled validated: {test_case['Sales Type']}"
                                    )
                                else:
                                    print(
                                        f"❌ Expected sales type prefilled value to be '{test_case['Sales Type']}'"
                                    )
                                    validation_failures.append(
                                        f"Expected sales type prefilled value to be '{test_case['Sales Type']}'"
                                    )

                                if (
                                    test_case["Sales Type Error"].strip().lower()
                                    == "yes"
                                ):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity", "sales_Type_2", "--None--"
                                    )
                                    cm.clickElement("CreateOpportunity", "next_Button")
                                    sales_type_error_text = cm.getInnerText(
                                        "CreateOpportunity", "sales_Type_1P_Error"
                                    )
                                    result = cm.assertContainsText(
                                        "CreateOpportunity",
                                        "sales_Type_1P_Error",
                                        test_case["Error Text"],
                                    )
                                    if result:
                                        logger.info(
                                            f"Verified sales type cannot be empty"
                                        )
                                        print(
                                            f"✅ Sales Type empty validation error confirmed"
                                        )
                                    else:
                                        print(
                                            f"❌ Expected sales type validation error to contain '{test_case['Error Text']}', but got '{sales_type_error_text}'"
                                        )
                                        validation_failures.append(
                                            f"Expected sales type validation error to contain '{test_case['Error Text']}', but got '{sales_type_error_text}'"
                                        )

                                if is_valid_data(test_case["Sales Type Invalid"]):
                                    cm.selectOptionInListbox(
                                        "CreateOpportunity",
                                        "sales_Type_2",
                                        test_case["Sales Type Invalid"],
                                    )
                                    logger.info(
                                        f"Selected sales type: {test_case['Sales Type Invalid']}"
                                    )

                            if is_valid_data(test_case["Primary Contact"]):
                                co.select_PrimaryContact(test_case["Primary Contact"])
                                logger.info(
                                    f"Selected 1P primary contact: {test_case['Primary Contact']}"
                                )

                            if is_valid_data(test_case["Confidential"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "Confidential",
                                    test_case["Confidential"],
                                )
                                logger.info(
                                    f"Confidential type: {test_case['Confidential']}"
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
                                cm.clickElement("CreateOpportunity", "reseller")
                                cm.enterText(
                                    "CreateOpportunity",
                                    "reseller",
                                    str(test_case["Reseller Account"]),
                                )
                                cm.clickElement(
                                    "CreateOpportunity", "reseller_Show_More_Results"
                                )
                                cm.clickElement(
                                    "CreateOpportunity", "reseller_First_Row_Checkbox"
                                )
                                cm.clickElement(
                                    "CreateOpportunity", "reseller_Select_Button"
                                )
                                logger.info(
                                    f"Entered reseller account: {test_case['Reseller Account']}"
                                )

                        if (
                            test_case["Opportunity Type"] == std_Oppty
                            and test_case["Opportunity Type"] != x1p_Oppty
                        ):

                            result = cm.assertSelectedDropdownText(
                                "CreateOpportunity",
                                "sales_Type_Prefilled",
                                test_case["Sales Type"],
                            )
                            if result:
                                logger.info(
                                    f"Verified sales type is prefilled based on customer type: {test_case['Sales Type']}"
                                )
                                print(
                                    f"✅ Sales Type prefilled validated: {test_case['Sales Type']}"
                                )
                            else:
                                print(
                                    f"❌ Expected sales type prefilled value to be '{test_case['Sales Type']}'"
                                )
                                validation_failures.append(
                                    f"Expected sales type prefilled value to be '{test_case['Sales Type']}'"
                                )

                            if test_case["Sales Type Error"].strip().lower() == "yes":
                                cm.selectOptionInListbox(
                                    "CreateOpportunity", "sales_Type", "--None--"
                                )
                                cm.clickElement("CreateOpportunity", "next_Button")
                                sales_type_error_text = cm.getInnerText(
                                    "CreateOpportunity", "sales_Type_1P_Error"
                                )
                                result = cm.assertContainsText(
                                    "CreateOpportunity",
                                    "sales_Type_1P_Error",
                                    test_case["Error Text"],
                                )
                                if result:
                                    logger.info(f"Verified sales type cannot be empty")
                                    print(
                                        f"✅ Sales Type empty validation error confirmed"
                                    )
                                else:
                                    print(
                                        f"❌ Expected sales type validation error to contain '{test_case['Error Text']}', but got '{sales_type_error_text}'"
                                    )
                                    validation_failures.append(
                                        f"Expected sales type validation error to contain '{test_case['Error Text']}', but got '{sales_type_error_text}'"
                                    )

                            if is_valid_data(test_case["Sales Type Invalid"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Type",
                                    test_case["Sales Type Invalid"],
                                )
                                logger.info(
                                    f"Selected sales type: {test_case['Sales Type Invalid']}"
                                )

                            if is_valid_data(test_case["Installed Base Type"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "installed_Base_Type",
                                    test_case["Installed Base Type"],
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
                                    "CreateOpportunity", "pathway", test_case["Pathway"]
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
                        print(f"ℹ️ Opportunity Number: {oppty_number}")

                        oppty_name = cm.readText(
                            "CreateOpportunity", "opportunity_Name"
                        )
                        logger.info(f"Opportunity Name: {oppty_name}")
                        print(f"ℹ️ Opportunity Name: {oppty_name}")

                        oppty_sales_type = cm.readText(
                            "CreateOpportunity", "opportunity_Sales_Type"
                        )
                        logger.info(f"Opportunity Sales Type: {oppty_sales_type}")
                        print(f"ℹ️ Opportunity Sales Type: {oppty_sales_type}")

                        result = cm.assertExpectedActualText(
                            oppty_sales_type, test_case["Sales Type"]
                        )
                        if result:
                            logger.info(
                                f"Validated opportunity sales type is {test_case['Sales Type']}"
                            )
                            print(f"✅ Sales Type validated: {oppty_sales_type}")
                        else:
                            print(
                                f"❌ Expected sales type '{test_case['Sales Type']}' but got '{oppty_sales_type}'"
                            )
                            validation_failures.append(
                                f"Expected sales type '{test_case['Sales Type']}' but got '{oppty_sales_type}'"
                            )

                        is_edit_disabled = cm.isElementHidden(
                            "CreateOpportunity", "edit_Sales_Type_Button"
                        )
                        if is_edit_disabled:
                            logger.info("Validated edit option is not available")
                            print(f"✅ Edit Sales Type button is disabled")
                        else:
                            print(
                                f"❌ Edit Sales Type button should be disabled after creation"
                            )
                            validation_failures.append(
                                "Edit Sales Type button should be disabled after creation"
                            )

                        spark_url = cm.getCurrentURL()
                        logger.info(f"Captured Spark URL: {spark_url}")
                        print(f"ℹ️ Captured Spark URL: {spark_url}")

                        cm.clickElement("CreateOpportunity", "copy_Opportunity_Button")
                        logger.info("Clicked on Copy Opportunity button")

                        cm.clickElement("CreateOpportunity", "continue_Button")
                        logger.info("Clicked on Continue button")

                        oppty_sales_type = cm.readText(
                            "CreateOpportunity", "opportunity_Sales_Type"
                        )
                        logger.info(f"Opportunity Sales Type: {oppty_sales_type}")
                        print(
                            f"ℹ️ Opportunity Sales Type on copied opportunity: {oppty_sales_type}"
                        )

                        result = cm.assertExpectedActualText(
                            oppty_sales_type, test_case["Sales Type"]
                        )
                        if result:
                            logger.info(
                                f"Validated opportunity sales type is {test_case['Sales Type']}"
                            )
                            print(
                                f"✅ Sales Type validated on copied opportunity: {oppty_sales_type}"
                            )
                        else:
                            print(
                                f"❌ Expected sales type '{test_case['Sales Type']}' but got '{oppty_sales_type}' on copied opportunity"
                            )
                            validation_failures.append(
                                f"Expected sales type '{test_case['Sales Type']}' but got '{oppty_sales_type}' on copied opportunity"
                            )

                        is_edit_disabled = cm.isElementHidden(
                            "CreateOpportunity", "edit_Sales_Type_Button"
                        )
                        if is_edit_disabled:
                            logger.info("Validated edit option is not available")
                            print(
                                f"✅ Edit Sales Type button is disabled on copied opportunity"
                            )
                        else:
                            print(
                                f"❌ Edit Sales Type button should be disabled after copy"
                            )
                            validation_failures.append(
                                "Edit Sales Type button should be disabled after copy"
                            )

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
            logger.info(
                f"***{script_name} Test Script Execution Completed Successfully***"
            )
            print(
                f"✅ ***{script_name} Test Script Execution Completed Successfully***"
            )

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
