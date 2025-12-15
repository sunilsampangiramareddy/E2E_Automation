import pytest
import time
import logging
import json
import os
from playwright.sync_api import Page
from pages_SFDC.Login_Page import LoginPage
from pages_SFDC.Home_Page import HomePage
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_CPQ.Home_Page_CPQ import HomePageCPQ
from pages_FAS_AFF_ASA_AFX.HomePage_FAS_AFF_ASA_AFX import HomePageFAS_AFF_ASA_AFX
from pages_CPQ.Account_Information_Page import AccountInformationPage
from pages_CPQ.Approval_Request_Page import ApprovalRequestPage
from pages_CPQ.Attachments_Page import AttachmentsPage
from pages_CPQ.Purchase_Order_Page import PurchaseOrderPage
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader
from utils.excel_read import read_test_data
from utils.write_excel_results import WriteExcelResults

logger = logging.getLogger('playwright_pytest')
# Load test data from Excel
relative_file_path = os.path.join('testData', 'TC_FAS_AFF_Cluster_Config.xlsx')
working_directory = os.getcwd()
file_path = os.path.join(working_directory, relative_file_path)
test_data = read_test_data(file_path)

# Get the test script name without the extension
script_name = os.path.splitext(os.path.basename(__file__))[0]


@pytest.mark.parametrize('test_case', test_data.to_dict(orient='records'))
@pytest.mark.master
@pytest.mark.regression
def test_FAS_AFF_ConfigureQuote(page: Page, base_url, config, test_case) -> None:
    lp = LoginPage(page)
    hp = HomePage(page)
    co = CreateOpportunity(page)
    ss = ScreenshotUtil(page)
    
    test_id="TC_FAS_AFF_Cluster_Config"; boolean_status="Pass"
   
    try:
        page.goto(base_url)
        logger.info(f"Launching application URL: {base_url}")
        logger.info(f"***TC_FAS_AFF_Cluster_Config Test Script Execution Started***")

        lp.enterUserName(test_case['User Name'])
        ss.capture_screenshot("Username entered") 
        logger.info(f"Username entered: {test_case['User Name']}") 
    
        #lp.enterUserName(config.get_username())
        #ss.capture_screenshot("Username entered") 
        #logger.info("Username entered")
       
        ss.capture_screenshot("Clicked on next button") 
        lp.clickNextButton()    
        logger.info(f"Clicked on next button")

        #lp.enterPassword(os.getenv("PASSWORD"))
        lp.enterPassword(config.get_encodedString())
        logger.info(f"Entered password")

        ss.capture_screenshot("Signin button clicked") 
        lp.clickSigninButton()    
        logger.info(f"Signin button clicked")
    
        lp.clickYesButton()
        logger.info(f"Yes button clicked")
    
        hp.isOpportunitiesLabelVisible()
        logger.info(f"Opportunities label has been verified on the homepage")
    
        hp.clickOpportunitiesTab()
        logger.info(f"Clicked on opportunities tab")
    
        hp.clickNewOpportunityButton()
        logger.info(f"Clickecd on new opportunity button")
    
        co.enterAccount(test_case['Account Name'])
        logger.info(f"Entered and selected account: {test_case['Account Name']}")
    
        co.clickNextButton()
        logger.info(f"Clicked on next button")
    
        co.enterOpportunityName(test_case['Opportunity Name'])
        logger.info(f"Entered opportunity name: {test_case['Opportunity Name']}")
    
        co.selectPrimaryContact_option(test_case['Primary Contact'])
        logger.info(f"Selected primary contact: {test_case['Primary Contact']}")
    
        co.clickNextButton()
        logger.info(f"Clicked on next button")
        time.sleep(20)
    
        hp.selectProduct(test_case['Product Name'])
        logger.info(f"Selected product")
    
        hp.enterProductPrice(test_case['Product Price'])
        logger.info(f"Entered product price")    
    
        new_tab = hp.create_Quote()
        logger.info(f"Clicked on create quote") 
    
        # Create an instance of HomePageCPQ for the new tab
        hpc = HomePageCPQ(new_tab)
        logger.info(f"HomePageCPQ instance created for the new tab")
    
        hpc.clickSaveButton()
        logger.info(f"Clicked on save button")
        
        hpc.closePopUp()
        logger.info(f"Closed pop up message")
           
        # Perform actions on the new tab
        quote_number = hpc.getQuoteNumber()
        logger.info(f"Quote Number: {quote_number}")
        
        quote_name = hpc.getQuoteName()
        logger.info(f"Quote Name: {quote_name}")
        
        quote_status = hpc.getQuoteStatus()
        logger.info(f"Quote Status: {quote_status}")
      
        hpc.clickProductsTab()
        logger.info(f"Clicked on Products tab")
           
        hpc.clickConfigureButton()
        logger.info(f"Clicked on Configure button")
        
        hpFAS=HomePageFAS_AFF_ASA_AFX(new_tab)
        logger.info(f"HomePageFAS_AFF_ASA_AFX instance created for the new tab")
        
        hpFAS.clickProductName(test_case['Product'])
        logger.info(f"Clicked on product: {test_case['Product']}")
        
        hpFAS.selectSubProduct(test_case['Sub Product'])
        logger.info(f"Clicked on sub-product: {test_case['Sub Product']}")
        
        hpFAS.configureCluster(test_case['Cluster'])
        logger.info(f"Clicked on cluster: {test_case['Cluster']}")
        
        hpFAS.selectSystemModel(test_case['Model'])
        logger.info(f"Selected Model: {test_case['Model']}")
        
        hpFAS.clickAddHaPair()
        logger.info(f"Clicked on Add HA Pair button")
        
        hpFAS.clickConfigureButton()
        logger.info(f"Clicked on configure button")
        
        hpFAS.clickStorageTab()
        logger.info(f"Clicked on storage tab")
        
        hpFAS.selectDriveType_BaseStorage(test_case['Drive Type'])
        logger.info(f"Selected drive type: {test_case['Drive Type']}")
        
        hpFAS.enterDrivePackQty_BaseStorage(test_case['Drive Pack Qty'])
        logger.info(f"Selected drive pack qty: {test_case['Drive Pack Qty']}")
        
        hpFAS.clickTabNICsandAdapters()
        logger.info(f"Clicked on Nics and Adapters tab")
        
        hpFAS.selectCableType(test_case['Cable Type'])
        logger.info(f"Selected cable type: {test_case['Cable Type']}")
        
        hpFAS.selectCableLength(test_case['Cable Length'])
        logger.info(f"Selected cable length: {test_case['Cable Length']}")
        
        hpFAS.clickBackToClusterManager()
        logger.info(f"Clicked on Back to Cluster manager button")
        
        hpFAS.clickServicesTab()
        logger.info(f"Clicked on Services tab")
        
        hpFAS.clickIsThisATechRefresh()
        logger.info(f"Clicked No button for Is this a tech refresh")
        
        hpFAS.clickDoesYourCustomerRequireBlueXP()
        logger.info(f"Clicked No button for Does your Customer require BlueXP to be deployed by the Professional Services Team")
        
        hpFAS.clickDoesYourCustomerNeedPSONTAP()
        logger.info(f"Clicked No button for Does your Customer need PS to fully design and configure their ONTAP system")
        
        hpFAS.clickDoYouWantToAddRansomwareRecoveryAssurance()
        logger.info(f"Clicked No button for Do you want to add the Ransomware Recovery Assurance Service")
        
        hpFAS.clickAddToQuote()
        logger.info(f"Clicked on Add to Quote button")
        
        hpc.readProductTable(new_tab, "Product")
        logger.info(f"Reading Product column values from product LIG table")
        
        hpc.readProductTable(new_tab, "List Price")
        logger.info(f"Reading List Price column values from product LIG table")
        
        hpc.readProductTable(new_tab, "Net Price")
        logger.info(f"Reading Net Price column values from product LIG table")
        
        hpFAS.clickSaveButton()
        logger.info(f"Clicked on Save button")
        
        
        
        
        aip=AccountInformationPage(new_tab)
        logger.info(f"AccountInformationPage instance created for the new tab")
        
        aip.clickAccountInformationTab()
        logger.info(f"Clicked on Account Information Tab")
        
        aip.enterAccountInformation()
        logger.info(f"Entered account information details")
        
        aip.selectShippingMethod()
        logger.info(f"Selected shipping method")
        
        aip.enterShippingInstructions()
        logger.info(f"Entered shipping instructions")
        
        hpFAS.clickSaveButton()
        logger.info(f"Clicked on Save button")
        
        ar=ApprovalRequestPage(new_tab)
        logger.info(f"ApprovalRequestPage instance created for the new tab")
        
        ar.clickApprovalRequestTab()
        logger.info(f"Clicked on Approval request tab")
        
        ar.clickInitiateApproval()
        logger.info(f"Clicked on Initiate Approval button")
        
        ap=AttachmentsPage(new_tab)
        logger.info(f"AttachmentsPage instance created for the new tab")
        
        ap.clickAttachmentsTab()
        logger.info(f"Clicked on Attachments tab")
        
        ap.selectDragAndDrop()
        logger.info(f"Selected file to upload")
        
        ap.selectAttachmentType()
        logger.info(f"Selected attachment type")
        
        ap.enterAttachmentDescription()
        logger.info(f"Enter attachment description")
        
        ap.clickUploadButton()
        logger.info(f"Clicked on upload button")
        
        po=PurchaseOrderPage(new_tab)
        logger.info(f"PurchaseOrderPage instance created for the new tab")
        
        po.clickPurchaseOrderTab()
        logger.info(f"Clicked on Purchase order tab")
        
        po.enterPONumber()
        logger.info(f"Entered PO number")
        
        po.enterPODate()
        logger.info(f"Entered PO date")
        
        po.enterPOEmail()
        logger.info(f"Entered PO email address")
        
        po.enterPOComments()
        logger.info(f"Entered PO comments")
        
        hpFAS.clickSaveButton()
        logger.info(f"Clicked on Save button")
        
        po.clickSubmitPO()
        logger.info(f"Clicked on Submit PO button")
        
        
        
        
        
        
        
        
    
        
        # Capture test result and write to Excel
        test_results = [
            ["Test Case ID", "Quote Number", "Quote Name", "Quote Status", "Execution Status", "Details"],
            [test_id, quote_number, quote_name, quote_status, boolean_status, "Configured Quote successfully"]
        ]
        excel_writer = WriteExcelResults(script_name)
        excel_writer.write_data(test_results)
        
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ss.capture_screenshot("Error")
        raise e