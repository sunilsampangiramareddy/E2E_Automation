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
# Test Scenario: 528720 - Verify Engagement Scores on Site, DP Accounts & Associated Opportunities
# Test Scenario: 522145 - TC1.Validate Suger Engagement Scores by Hyperscaler on the DP & SITE Account

# Test Description: This test verifies Propensity Engagement Scores (Overall, AWS, GCP, Azure) on SITE/DP Accounts
#                   and their Associated Opportunities in SFDC. It logs in via a User Persona, navigates to the Account
#                   page to validate Engagement Score labels and values, creates a new Opportunity (Direct/Indirect/1P),
#                   and confirms that the same Engagement Score fields are correctly displayed on the Opportunity Details tab.

# Author : Alok Kumar Gupta
# Reviewed By: Sunil Reddy
# =========================================================================================================================

logger = logging.getLogger("playwright_pytest")
# Load test data from Excel
relative_file_path = os.path.join(
    "testData/tests_SFDC_Regression", "TC_Verify_Engagement_Scores.xlsx"
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
def test_Verify_Engagement_Scores(page: Page, base_url, config, test_case) -> None:
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
                f"*****{script_name} Test Script Execution Started for Iteration - {test_case['Iteration']} and {test_case['Test Case ID']} ***"
            )
            print(
                f"ℹ️ *****{script_name} Test Script Execution Started for Iteration - {test_case['Iteration']} and {test_case['Test Case ID']}*****"
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

            if test_case["Navigate To Opportunities Screen"].strip().lower() == "yes":

                if (
                    test_case["Accounts Propensity Engagement Score"].strip().lower()
                    == "yes"
                ):

                    cm.clickElementAndWait("HomePage", "accounts_Tab", wait_time=2)
                    cm.clickElement("HomePage", "search_Bar")
                    logger.info(f"Clicked on search bar")
                    cm.enterText(
                        "HomePage", "search_Bar", str(int(test_case["Account CMAT ID"]))
                    )
                    logger.info(
                        f"Entered Account CMAT ID: {test_case['Account CMAT ID']} in search bar"
                    )
                    cm.pressEnter("HomePage", "search_Bar")
                    cm.clickByLinkText(test_case["Account Name"], partial_match=True)
                    logger.info(
                        f"Navigated to Account: {test_case['Account CMAT ID']} - {test_case['Account Name']}"
                    )
                    cm.waitForStable(5)
                    cm.mouseWheelToBottom(1000, scrolls=10, wait_time=0)

                    engagement_score_labels = [
                        "propensity_Engagement_Score_Label",
                        "aws_Engagement_Score_Label",
                        "gcp_Engagement_Score_Label",
                        "azure_Engagement_Score_Label",
                    ]
                    all_labels_visible = cm.isElementVisibleInSequence(
                        "Propensity_Accounts", engagement_score_labels
                    )
                    if all_labels_visible:
                        logger.info("All Engagement Score labels are visible")
                        print(
                            "✅ All Engagement Score labels verified (Propensity, AWS, GCP, Azure)"
                        )
                    else:
                        logger.warning(
                            "One or more Engagement Score labels are not visible"
                        )
                        print("❌ One or more Engagement Score labels are not visible")
                        validation_failures.append(
                            "One or more Engagement Score labels are not visible"
                        )

                    aws_actual = cm.readText(
                        "Propensity_Accounts", "aws_Engagement_Score_Value"
                    )
                    if cm.assertExpectedInActualText(
                        aws_actual, str(test_case["AWS Engagement Score"])
                    ):
                        print(f"✅ AWS Engagement Score matched: {aws_actual}")
                    else:
                        print(
                            f"❌ AWS Engagement Score mismatch — Expected: {test_case['AWS Engagement Score']}, Actual: {aws_actual}"
                        )
                        validation_failures.append(
                            f"AWS Engagement Score mismatch — Expected: {test_case['AWS Engagement Score']}, Actual: {aws_actual}"
                        )

                    gcp_actual = cm.readText(
                        "Propensity_Accounts", "gcp_Engagement_Score_Value"
                    )
                    if cm.assertExpectedInActualText(
                        gcp_actual, str(test_case["GCP Engagement Score"])
                    ):
                        print(f"✅ GCP Engagement Score matched: {gcp_actual}")
                    else:
                        print(
                            f"❌ GCP Engagement Score mismatch — Expected: {test_case['GCP Engagement Score']}, Actual: {gcp_actual}"
                        )
                        validation_failures.append(
                            f"GCP Engagement Score mismatch — Expected: {test_case['GCP Engagement Score']}, Actual: {gcp_actual}"
                        )

                    azure_actual = cm.readText(
                        "Propensity_Accounts", "azure_Engagement_Score_Value"
                    )
                    if cm.assertExpectedInActualText(
                        azure_actual, str(test_case["Azure Engagement Score"])
                    ):
                        print(f"✅ Azure Engagement Score matched: {azure_actual}")
                    else:
                        print(
                            f"❌ Azure Engagement Score mismatch — Expected: {test_case['Azure Engagement Score']}, Actual: {azure_actual}"
                        )
                        validation_failures.append(
                            f"Azure Engagement Score mismatch — Expected: {test_case['Azure Engagement Score']}, Actual: {azure_actual}"
                        )

                # =======================Create Opportunity===========================================================================

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
                                logger.info(
                                    f"Entered opportunity name: {test_case['Opportunity Name']}"
                                )
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
                                    "CreateOpportunity", "channel", test_case["Channel"]
                                )
                                logger.info(f"Selected channel: {test_case['Channel']}")

                        if test_case["Opportunity Type"] == x1p_Oppty:
                            if is_valid_data(test_case["Opportunity Name"]):
                                co.enterOpportunityName_1p(
                                    test_case["Opportunity Name"]
                                )
                                logger.info(
                                    f"Entered 1P opportunity name: {test_case['Opportunity Name']}"
                                )
                            if is_valid_data(test_case["Sales Type"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "sales_Type_1P_new",
                                    test_case["Sales Type"],
                                )
                                logger.info(
                                    f"Selected 1P sales type: {test_case['Sales Type']}"
                                )
                            if is_valid_data(test_case["Primary Contact"]):
                                co.select_PrimaryContact(test_case["Primary Contact"])
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
                            if is_valid_data(test_case["Confidential"]):
                                cm.selectOptionInListbox(
                                    "CreateOpportunity",
                                    "Confidential",
                                    test_case["Confidential"],
                                )
                                logger.info(
                                    f"Confidential type: {test_case['Confidential']}"
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
                                ss.capture_screenshot(
                                    "Captured Create Opportunity details"
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
                            cm.clickElement("CreateOpportunity", "next_Button")
                            logger.info(f"Clicked on next button")

                        if (
                            test_case["Details Propensity Engagement Score"]
                            .strip()
                            .lower()
                            == "yes"
                        ):
                            cm.clickElement("OpportunityDetailPage", "details_Tab")
                            cm.mouseWheelToBottom(400, scrolls=2, wait_time=0)

                            engagement_score_labels = [
                                "propensity_Engagement_Score_Label",
                                "aws_Engagement_Score_Label",
                                "gcp_Engagement_Score_Label",
                                "azure_Engagement_Score_Label",
                            ]
                            all_labels_visible = cm.isElementVisibleInSequence(
                                "Propensity_Details", engagement_score_labels
                            )
                            if all_labels_visible:
                                logger.info("All Engagement Score labels are visible")
                                print(
                                    "✅ All Engagement Score labels verified (Propensity, AWS, GCP, Azure)"
                                )
                            else:
                                logger.warning(
                                    "One or more Engagement Score labels are not visible"
                                )
                                print(
                                    "❌ One or more Engagement Score labels are not visible"
                                )
                                validation_failures.append(
                                    "One or more Engagement Score labels are not visible"
                                )

                            aws_actual = cm.readText(
                                "Propensity_Details", "aws_Engagement_Score_Value"
                            )
                            if cm.assertExpectedInActualText(
                                aws_actual, str(test_case["AWS Engagement Score"])
                            ):
                                print(f"✅ AWS Engagement Score matched: {aws_actual}")
                            else:
                                print(
                                    f"❌ AWS Engagement Score mismatch — Expected: {test_case['AWS Engagement Score']}, Actual: {aws_actual}"
                                )
                                validation_failures.append(
                                    f"AWS Engagement Score mismatch — Expected: {test_case['AWS Engagement Score']}, Actual: {aws_actual}"
                                )

                            gcp_actual = cm.readText(
                                "Propensity_Details", "gcp_Engagement_Score_Value"
                            )
                            if cm.assertExpectedInActualText(
                                gcp_actual, str(test_case["GCP Engagement Score"])
                            ):
                                print(f"✅ GCP Engagement Score matched: {gcp_actual}")
                            else:
                                print(
                                    f"❌ GCP Engagement Score mismatch — Expected: {test_case['GCP Engagement Score']}, Actual: {gcp_actual}"
                                )
                                validation_failures.append(
                                    f"GCP Engagement Score mismatch — Expected: {test_case['GCP Engagement Score']}, Actual: {gcp_actual}"
                                )

                            azure_actual = cm.readText(
                                "Propensity_Details", "azure_Engagement_Score_Value"
                            )
                            if cm.assertExpectedInActualText(
                                azure_actual, str(test_case["Azure Engagement Score"])
                            ):
                                print(
                                    f"✅ Azure Engagement Score matched: {azure_actual}"
                                )
                            else:
                                print(
                                    f"❌ Azure Engagement Score mismatch — Expected: {test_case['Azure Engagement Score']}, Actual: {azure_actual}"
                                )
                                validation_failures.append(
                                    f"Azure Engagement Score mismatch — Expected: {test_case['Azure Engagement Score']}, Actual: {azure_actual}"
                                )

                    spark_url = cm.getCurrentURL()
                    logger.info(f"Captured Spark URL: {spark_url}")
                    print(f"ℹ️ Captured Spark URL: {spark_url}")

                else:
                    logger.info(
                        f"Create Opportunity flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
                    )
                    print(
                        f"➡️ Create Opportunity flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
                    )
            else:
                logger.info(
                    f"Navigate To Opportunities Screen flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
                )
                print(
                    f"➡️ Navigate To Opportunities Screen flag is set to 'No'. Skipping the test case for the Test Case ID:{test_case['Test Case ID']}"
                )

            # =======================Add Product in SFDC=================================================================================
            if test_case["Add Products"].strip().lower() == "yes":

                if is_valid_data(test_case["Product Name"]):
                    cm.clickElement("HomePage", "products_Link")
                    cm.clickElement("HomePage", "add_Products_Button")
                    cm.clickElement("HomePage", "search_Products_Input")
                    cm.enterText(
                        "HomePage", "search_Products_Input", test_case["Product Name"]
                    )
                    cm.pressEnter("HomePage", "search_Products_Input")
                    cm.clickElement("HomePage", "product_Search_Result")
                    cm.clickElement("HomePage", "product_Next_Button")
                    logger.info(f"Selected product: {test_case['Product Name']}")

                if is_valid_data(test_case["Product Price"]):
                    cm.clickElement("HomePage", "edit_Sales_Price_Button")
                    cm.enterText(
                        "HomePage", "sales_Price_Input", str(test_case["Product Price"])
                    )
                    cm.clickElement("HomePage", "save_Button")
                    ss.capture_screenshot("Captured Product in SFDC Details")
                    logger.info(f"Entered product price: {test_case['Product Price']}")

                cm.navigateToUrl(spark_url)
                logger.info(f"Navigated back to Spark URL: {spark_url}")

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
                    "Details",
                ],
                [
                    script_name,
                    boolean_status,
                    "Test executed successfully without any validation failures.",
                ],
            ]

            excel_writer = WriteExcelResults(script_name)
            excel_writer.write_data(test_results)
            logger.info(
                f"***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}***"
            )
            print(
                f"✅ ***{script_name} Test Script Execution Completed Successfully for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}***"
            )

        else:
            logger.info(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}***"
            )
            print(
                f"\033[93m➡️ Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}\033[0m"
            )
            pytest.skip(
                f"Execution flag is set to 'No'. Skipping the test case for the Iteration:{test_case['Iteration']} and Test Case ID: {test_case['Test Case ID']}***"
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot(f"{script_name}_Failed Screenshot")
        raise e
