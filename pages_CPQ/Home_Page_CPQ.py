from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

logger = logging.getLogger('playwright_pytest')

class HomePageCPQ:
    nw=3; sw=5; mw=10; lw=20
            
    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()
       
    def _initialize_locators(self):  
        self.saveButton = self.page.get_by_role("button", name="Save Quote")
        self.popUp = self.page.locator('//*[@id="border-8dbf786c-7da0-4898-aa4b-f1b836878c53"]')
        self.quoteNumber = self.page.locator('//div[3]/div[1]/div[2]')
        self.quoteName = self.page.locator('//div[2]/div[1]/div[2]/div')
        self.quoteStatus = self.page.locator('//div[3]/div[2]/div[2]')
        self.productsTab = self.page.get_by_role("tab", name=" Products")
        self.configureButton = self.page.get_by_role("button", name="Configure Product")
           
    def clickSaveButton(self):
        expect(self.saveButton).to_be_visible()
        self.saveButton.click()
        time.sleep(self.lw)    
        
    def closePopUp(self):
        try:
            # Wait for up to 10 seconds for the popup to be visible
            self.popUp.wait_for(state="visible", timeout=10000)  # Wait up to 10 seconds        
            # Click the popup close button if it becomes visible
            self.popUp.click()   
        except TimeoutError:
            logger.warning("Timeout while waiting for the popup to be visible.")
        except Exception as e:
            logger.error(f"An error occurred while closing the popup: {e}")                    
    
    def getQuoteNumber(self):
        expect(self.quoteNumber).to_be_visible()
        quote_number = self.quoteNumber.inner_text()
        return quote_number
        
    def getQuoteName(self):
        expect(self.quoteName).to_be_visible()
        quote_Name = self.quoteName.inner_text()
        return quote_Name
    
    def getQuoteStatus(self):
        expect(self.quoteStatus).to_be_visible()
        quote_Status = self.quoteStatus.inner_text()
        return quote_Status
               
    def clickProductsTab(self):
        expect(self.productsTab).to_be_visible()
        self.productsTab.click()
        time.sleep(self.sw)
    
    def clickConfigureButton(self):
        expect(self.configureButton ).to_be_visible()
        self.configureButton.click()
        time.sleep(self.mw)
        
    def readProductTable(self, page, column_name):
        if column_name == "Product":
            logger.info(f"Reading product table for column: {column_name}")
            # Locate elements using the provided XPath
            locator  = self.page.locator("//div[contains(@class, 'oj-flex-bar oj-sm-12 oj-sm-align-self-center oj-sm-flex-wrap-nowrap oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate cx-cpq-line-item-row')]")
            count = locator.count()
            logger.info(f"Found {count} elements with the specified XPath")
            # Extract and print text of each element
            for i in range(count):
                element = locator.nth(i)
                text = element.inner_text()
                if text:
                    logger.info(f"Extracted text: {text}")
                    print(text, end="\t")
                else:
                    logger.warning(f"Empty text found for element: {element}")
            print() 
        if column_name == "List Price":
            logger.info(f"Reading product table for column: {column_name}")
            # Locate elements using the provided XPath
            locator  = self.page.locator("//div[contains(@class, 'oj-flex oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate oj-fa-cx-cpq-field-listPrice_l_c')]")
            count = locator.count()
            logger.info(f"Found {count} elements with the specified XPath")
            # Extract and print text of each element
            for i in range(count):
                element = locator.nth(i)
                text = element.inner_text()
                if text:
                    logger.info(f"Extracted text: {text}")
                    print(text, end="\t")
                else:
                    logger.warning(f"Empty text found for element: {element}")
            print() 
        if column_name == "Net Price":
            logger.info(f"Reading product table for column: {column_name}")
            # Locate elements using the provided XPath
            locator  = self.page.locator("//div[contains(@class, 'oj-flex oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate oj-fa-cx-cpq-field-netPrice_l_c')]")
            count = locator.count()
            logger.info(f"Found {count} elements with the specified XPath")
            # Extract and print text of each element
            for i in range(count):
                element = locator.nth(i)
                text = element.inner_text()
                if text:
                    logger.info(f"Extracted text: {text}")
                    print(text, end="\t")
                else:
                    logger.warning(f"Empty text found for element: {element}")
            print() 
        
    
            
        