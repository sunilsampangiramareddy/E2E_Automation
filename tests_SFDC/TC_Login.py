import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults

logger = logging.getLogger('playwright_pytest')
# Load test data from Excel
relative_file_path = os.path.join('testData', 'TC_Login.xlsx')
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]

@pytest.mark.parametrize('test_case', test_data.to_dict(orient='records'))
@pytest.mark.smoke
@pytest.mark.master
def test_login(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    test_id="TC_Login"; boolean_status="Pass"
   
    try:    
        page.goto(base_url)
        logger.info(f"Launching application URL: {base_url}")
        logger.info(f"***TC_Login Test Script Execution Started***")
    

        lp.enterUserName(test_case['User Name'])
        ss.capture_screenshot("Username entered") 
        logger.info(f"Username entered: {test_case['User Name']}")
            
        #lp.enterUserName(config.get_username())
        #ss.capture_screenshot("Username entered") 
        #logger.info("Username entered")
       
        ss.capture_screenshot("Clicked on next button") 
        lp.clickNextButton()    
        logger.info("Clicked on next button")

        #lp.enterPassword(os.getenv("PASSWORD"))
        lp.enterPassword(config.get_encodedString())
        logger.info("Entered password")

        ss.capture_screenshot("Signin button clicked") 
        lp.clickSigninButton()    
        logger.info("Signin button clicked")
    
        lp.clickYesButton()
        logger.info("Yes button clicked")
    
        hp.isOpportunitiesLabelVisible()
        logger.info("Opportunities label has been verified on the homepage")
    
        # Capture test result and write to Excel
        test_results = [
            ["Test Case ID", "Execution Status", "Details"],
            [test_id, boolean_status, "Logged in successfully"]
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot("Error")
        raise e