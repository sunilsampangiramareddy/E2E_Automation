import logging
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from utils.excel_read import read_test_data
from datetime import datetime

# Configure logging with timestamps for debugging parallel execution
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("playwright_pytest")
# Dynamically set MAX_WORKERS to the number of CPU cores
# MAX_WORKERS = os.cpu_count()
MAX_WORKERS = 3
logger.info(
    f"Number of CPU cores detected: {MAX_WORKERS}. Using this for parallel execution."
)
# Load test data from Excel
relative_file_path = os.path.join("testData", "Test_Orchestration.xlsx")
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)
# Define test script paths
TEST_SCRIPT_PATHS = {
    "TC_Login": "tests_SFDC/TC_Login.py",
    "TC_CreateOpportunity": "tests_SFDC/TC_CreateOpportunity.py",
    "TC_API_Validation": "tests_CPQ/TC_API_Validation.py",
    "TC_Copy_Quote": "tests_CPQ/TC_Copy_Quote.py",
    "TC_Open_Quote": "tests_CPQ/TC_Open_Quote.py",
    "TC_FAS_AFF_Cluster_Config": "tests_CPQ/TC_FAS_AFF_Cluster_Config.py",
    "E2E_UAT_003_Part_1": "tests_FTR/E2E_UAT_003_Part_1.py",
    "E2E_UAT_003_Part_2": "tests_FTR/E2E_UAT_003_Part_2.py",
    "E2E_UAT_017": "tests_FTR/E2E_UAT_017.py",
    "E2E_UAT_018": "tests_FTR/E2E_UAT_018.py",
    "E2E_UAT_022_Part_1": "tests_FTR/E2E_UAT_022_Part_1.py",
    "E2E_UAT_022_Part_2": "tests_FTR/E2E_UAT_022_Part_2.py",
    "E2E_UAT_024": "tests_FTR/E2E_UAT_024.py",
    "E2E_UAT_025_Part_1": "tests_FTR/E2E_UAT_025_Part_1.py",
    "E2E_UAT_025_Part_2": "tests_FTR/E2E_UAT_025_Part_2.py",
    "E2E_UAT_026_Part_1": "tests_FTR/E2E_UAT_026_Part_1.py",
    "E2E_UAT_026_Part_2": "tests_FTR/E2E_UAT_026_Part_2.py",
    "E2E_UAT_038": "tests_FTR/E2E_UAT_038.py",
    "E2E_UAT_051": "tests_FTR/E2E_UAT_051.py",
    "TC_FAS_AFF_ASA_AFX_Multiple_Cluster_Config_001": "tests_FTR/TC_FAS_AFF_ASA_AFX_Multiple_Cluster_Config_001.py",
    "TC_PartnerLogin": "tests_Partner/TC_PartnerLogin.py",
    "TC_Partner_Copy_Quote": "tests_Partner/TC_Partner_Copy_Quote.py",
    "TC_Partner_Open_Quote": "tests_Partner/TC_Partner_Open_Quote.py",
    # Add more test cases and their paths as needed
}


def execute_test(test_name, script_path):
    """
    Executes a single test script using subprocess.
    """
    try:
        logger.info(f"Starting execution of {test_name} at path: {script_path}...")
        # FIX: Added microseconds to avoid filename collision
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        report_file = f"report_{test_name}_{timestamp}.html"
        logger.info(f"Running command: pytest {script_path} --html={report_file}")
        result = subprocess.run(
            ["pytest", script_path, f"--html={report_file}"],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Finished execution of {test_name}. HTML report: {report_file}")
        logger.debug(f"Output for {test_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Test script {test_name} failed with error: {e}")
        logger.error(f"Standard Error Output:\n{e.stderr}")
    except FileNotFoundError:
        logger.error(f"Test script file not found: {script_path}")
    except Exception as e:
        logger.error(f"Unexpected error while executing {test_name}: {e}")


def test_orchestration():
    """
    Orchestrates test execution based on Excel file.
    Runs tests in parallel.
    """
    logger.info("Test Orchestration Execution Started")
    executed_any_test = False
    # Filter tests where Execute = Yes
    test_cases_to_execute = [
        test_case
        for test_case in test_data.to_dict(orient="records")
        if test_case.get("Execute", "").lower() == "yes"
    ]
    if not test_cases_to_execute:
        logger.info("No test scripts marked for execution. Exiting.")
        return
    logger.info(f"Executing {len(test_cases_to_execute)} test scripts in parallel...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for test_case in test_cases_to_execute:
            test_name = test_case.get("Test Name")
            script_path = TEST_SCRIPT_PATHS.get(test_name)
            if script_path:
                logger.info(f"Preparing to execute: {test_name}")
                futures.append(executor.submit(execute_test, test_name, script_path))
                executed_any_test = True
            else:
                logger.warning(f"Script path not found for {test_name}. Skipping...")
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"Parallel execution error: {e}")
    if not executed_any_test:
        logger.info("No test scripts executed. Check Excel data.")
    logger.info("Test Orchestration Execution Completed")


if __name__ == "__main__":
    test_orchestration()
