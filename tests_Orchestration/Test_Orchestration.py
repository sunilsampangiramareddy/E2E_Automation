import logging
import os
import subprocess
from utils.excel_read import (
    read_test_data,
)

# ========================================================================================================================
# Test Metadata
# ========================================================================================================================
# Orchestration Script: Test_Orchestration.py
#
#    Purpose:
#    - Dynamically orchestrates the execution of test scripts based on external data (Excel file).
#    - Provides centralized control, logging, and error handling for test execution.
#
#    Key Features:
#    - Data-driven execution: Reads test names and execution flags from an Excel file.
#    - Dynamic path resolution: Maps test names to their corresponding file paths.
#    - Centralized logging: Logs all actions, errors, and outputs.
#    - Extensible: Easily add new test scripts or modify orchestration logic.
#
#    Use Case:
#    - Ideal for running multiple test scripts in a controlled and flexible manner.
#
#    Execution Flow:
#    1. Reads test names and execution flags from the Excel file.
#    2. Checks the `Execute` flag for each test case:
#       - If `Yes`, resolves the test script path and executes the test using `subprocess.run()`.
#       - If `No`, skips the test case and logs the action.
#    3. Logs the output and errors for each test script execution.
#    4. If no test scripts are executed, logs a message indicating that no tests were run.
#
#    Dependencies:
#    - utils.excel_read.read_test_data: Utility function to read test data from an Excel file.
#    - subprocess: Used to execute test scripts dynamically.
#    - Logging: For centralized logging of actions and errors.
# ========================================================================================================================


# Configure logging
logger = logging.getLogger("playwright_pytest")
logging.basicConfig(level=logging.INFO)

# Load test data from Excel
relative_file_path = os.path.join(
    "testData", "Test_Orchestration.xlsx"
)  # Update with your Excel file path
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(
    file_path
)  # Assuming this returns a DataFrame or list of dictionaries


def test_orchestration():

    logger.info("Test Orchestration Test Execution Started")

    executed_any_test = False  # Track if any test script was executed

    # Iterate through each row in the Excel sheet
    for test_case in test_data.to_dict(orient="records"):
        test_name = test_case.get("Test Name")  # Column in Excel with test names
        execute_flag = test_case.get("Execute")  # Column in Excel with 'Yes' or 'No'

        if execute_flag.lower() == "yes":
            logger.info(f"Executing {test_name} test script...")

            # Get the test script path from the dictionary
            script_path = TEST_SCRIPT_PATHS.get(test_name)

            if script_path:
                try:
                    # Dynamically execute the test script using subprocess
                    result = subprocess.run(
                        ["pytest", script_path],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    logger.info(
                        f"Output for {test_name}:\n{result.stdout}"
                    )  # Log standard output
                    executed_any_test = True
                except subprocess.CalledProcessError as e:
                    logger.error(f"Test script {test_name} failed with error: {e}")
                    logger.error(f"Standard Error Output:\n{e.stderr}")
                except Exception as e:
                    logger.error(f"Unexpected error while executing {test_name}: {e}")
            else:
                logger.warning(
                    f"Test script path for {test_name} not found. Skipping..."
                )
        else:
            logger.info(
                f"Skipping {test_name} test script as Execute flag is set to 'No'."
            )

    # Final else condition
    if not executed_any_test:
        logger.info("No test scripts were executed. Please check your Excel sheet.")

    logger.info("Test Orchestration Test Execution Completed Successfully")


# Define test script paths based on test names
TEST_SCRIPT_PATHS = {
    "TC_Login": "tests_SFDC_Base/TC_Login.py",
    "TC_CreateOpportunity": "tests_SFDC_Base/TC_CreateOpportunity.py",
    "TC_API_Validation": "tests_CPQ_Base/TC_API_Validation.py",
    "TC_Copy_Quote": "tests_CPQ_Base/TC_Copy_Quote.py",
    "TC_Open_Quote": "tests_CPQ_Base/TC_Open_Quote.py",
    "TC_FAS_AFF_Cluster_Config": "tests_CPQ_Base/TC_FAS_AFF_Cluster_Config.py",    
    "TC_E_EF_Series_Regression": "tests_CPQ_Regression/TC_E_EF_Series_Regression.py",    
    "E2E_UAT_003_Part_1": "tests_ERP_FTR/E2E_UAT_003_Part_1.py",
    "E2E_UAT_003_Part_2": "tests_ERP_FTR/E2E_UAT_003_Part_2.py",
    "E2E_UAT_017": "tests_ERP_FTR/E2E_UAT_017.py",
    "E2E_UAT_018": "tests_ERP_FTR/E2E_UAT_018.py",
    "E2E_UAT_022_Part_1": "tests_ERP_FTR/E2E_UAT_022_Part_1.py",
    "E2E_UAT_022_Part_2": "tests_ERP_FTR/E2E_UAT_022_Part_2.py",
    "E2E_UAT_024": "tests_ERP_FTR/E2E_UAT_024.py",
    "E2E_UAT_025_Part_1": "tests_ERP_FTR/E2E_UAT_025_Part_1.py",
    "E2E_UAT_025_Part_2": "tests_ERP_FTR/E2E_UAT_025_Part_2.py",
    "E2E_UAT_026_Part_1": "tests_ERP_FTR/E2E_UAT_026_Part_1.py",
    "E2E_UAT_026_Part_2": "tests_ERP_FTR/E2E_UAT_026_Part_2.py",
    "E2E_UAT_038": "tests_ERP_FTR/E2E_UAT_038.py",
    "E2E_UAT_051": "tests_ERP_FTR/E2E_UAT_051.py",
    "TC_FAS_AFF_ASA_AFX_Multiple_Cluster_Config_001": "tests_ERP_FTR/TC_FAS_AFF_ASA_AFX_Multiple_Cluster_Config_001.py",
    "TC_PartnerLogin": "tests_Partner_Base/TC_PartnerLogin.py",
    "TC_Partner_Copy_Quote": "tests_Partner_Base/TC_Partner_Copy_Quote.py",
    "TC_Partner_Open_Quote": "tests_Partner_Base/TC_Partner_Open_Quote.py",
    # Add more test cases and their paths as needed
}
