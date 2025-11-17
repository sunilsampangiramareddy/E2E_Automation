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

logger = logging.getLogger('playwright_pytest')
# Load test data from Excel
relative_file_path = os.path.join('testData', 'TC_CreateOpportunity.xlsx')
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

@pytest.mark.parametrize('test_case', test_data.to_dict(orient='records'))
@pytest.mark.master
@pytest.mark.regression
def test_createOpportunity(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
   
    page.goto(base_url)
    logger.info(f"Launching application URL: {base_url}")

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
    
    hp.clickOpportunitiesTab()
    logger.info("Clicked on opportunities tab")
    
    hp.clickNewOpportunityButton()
    logger.info("Clickecd on new opportunity button")
    
    co.enterAccount(test_case['Account Name'])
    logger.info(f"Entered and selected account: {test_case['Account Name']}")
    
    co.clickNextButton()
    logger.info("Clicked on next button")
    
    co.enterOpportunityName(test_case['Opportunity Name'])
    logger.info(f"Entered opportunity name: {test_case['Opportunity Name']}")
    
    co.selectPrimaryContact_option(test_case['Primary Contact'])
    logger.info(f"Selected primary contact: {test_case['Primary Contact']}")
    
    co.clickNextButton()
    logger.info("Clicked on next button")
    time.sleep(20)

        
    
    




