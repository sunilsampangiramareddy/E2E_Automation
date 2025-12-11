from playwright.sync_api import Page, expect
import time
import logging

logger = logging.getLogger('playwright_pytest')

class HomePageFAS_AFF_ASA_AFX:
    nw=3; sw=5; mw=10; lw=20
    
    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()        
        
    def _initialize_locators(self):  
        self.productName = self.page.locator("#im-selectTemplateType").get_by_text("FAS/AFF/ASA/AFX")
        self.addHaPair = self.page.get_by_role("button", name="Add HA Pair")
        self.configureButton = self.page.get_by_role("button", name="Configure")
        self.storageTab = self.page.get_by_role("tab", name="Storage")
        self.tabNICsandAdapters = self.page.get_by_role("tab", name="NICs and Adapters")
        self.backToClusterManager = self.page.get_by_role("button", name="Back To Cluster Manager")
        self.servicesTab = self.page.get_by_role("tab", name="Services")
        self.IsThisATechRefresh =  self.page.get_by_role("group", name="Is this a tech refresh?").get_by_label("No", exact=True)
        self.doesYourCustomerRequireBlueXP  = self.page.get_by_role("group", name="Does your Customer require").get_by_label("No", exact=True)
        self.doesYourCustomerNeedPSONTAP = self.page.get_by_role("group", name="Does your Customer need PS to").get_by_label("No", exact=True)
        self.doYouWantToAddRansomwareRecoveryAssurance =  self.page.get_by_role("group", name="Do you want to add the").get_by_label("No", exact=True)
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")
        self.saveButton = self.page.get_by_role("button", name="Save")
    
    def clickProductName(self, product_name):
        if product_name == "FAS/AFF/ASA/AFX":
            expect(self.productName).to_be_visible()
            self.productName.click()
            time.sleep(self.nw) 
        else:
            raise ValueError(f"Invalid product name: {product_name}") 
        
    
    def selectSubProduct(self, sub_Product):
        if sub_Product == "FAS/AFF Advanced Configure Flow":
            self.page.get_by_role("option", name="FAS/AFF/ASA/AFX").click()    
            self.page.get_by_role("row", name="FAS/AFF Advanced Configure").get_by_role("link").click()
            time.sleep(self.nw) 
        else:
            raise ValueError(f"Invalid sub product name: {sub_Product}") 
    
    def configureCluster(self, cluster):
        if cluster == "Configure New Cluster":
            self.page.get_by_text("Configure New Cluster").click()
            self.page.get_by_role("button", name="Next").click()
            time.sleep(self.mw) 
        else:
            raise ValueError(f"Invalid cluster name: {cluster}")
        
        
    def selectSystemModel(self, model: str):
        if model == "AFF A20":
            self.page.get_by_role("combobox", name="Model", exact=True).click()
            self.page.get_by_role("combobox", name="Model", exact=True).fill(model)
            self.page.get_by_text(model).click()
            time.sleep(self.nw) 
        else:
            raise ValueError(f"Invalid model name: {model}")
    
    def clickAddHaPair(self):
            expect(self.addHaPair).to_be_visible()
            self.addHaPair.click()
            time.sleep(self.nw) 
       
    def clickConfigureButton(self):
            expect(self.configureButton).to_be_visible()
            self.configureButton.click()
            time.sleep(self.lw) 
            
    def clickStorageTab(self):
            expect(self.storageTab).to_be_visible()
            self.storageTab.click()
            time.sleep(self.nw) 
            
    def selectDriveType_BaseStorage(self, driveType: str):
        self.page.get_by_role("combobox", name="Drive Type").click()
        self.page.get_by_role("combobox", name="Drive Type").fill(driveType)
        self.page.get_by_text(driveType).click()
        time.sleep(self.sw)
        
    def enterDrivePackQty_BaseStorage(self, qty: int):
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").click()
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").fill(str(qty))
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").press("Tab")
        time.sleep(self.sw)
    
    def clickTabNICsandAdapters(self):
            expect(self.tabNICsandAdapters).to_be_visible()
            self.tabNICsandAdapters.click()
            time.sleep(self.nw)  
            
    def selectCableType(self, cable: str):
        self.page.locator(".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableType").first.dblclick()
        #self.page.locator("[id=\"networkAdapterCableType|input\"]").dblclick()
        self.page.locator("[id=\"oj-searchselect-filter-networkAdapterCableType|input\"]").click()
        self.page.locator("[id=\"oj-searchselect-filter-networkAdapterCableType|input\"]").fill(cable)
        self.page.get_by_text(cable, exact=True).click()
        time.sleep(self.sw)
        
        
    def selectCableLength(self, cableLength: str):
        self.page.locator(".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableLength").first.click()
        self.page.locator(".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableLength").first.dblclick()
        #self.page.locator("[id=\"networkAdapterCableLength|input\"]").dblclick()
        self.page.locator("[id=\"oj-searchselect-filter-networkAdapterCableLength|input\"]").click()
        self.page.locator("[id=\"oj-searchselect-filter-networkAdapterCableLength|input\"]").fill(cableLength)
        self.page.get_by_text(cableLength).click()
        time.sleep(self.sw)
        
    
    def clickBackToClusterManager(self):
            expect(self.backToClusterManager).to_be_visible()
            self.backToClusterManager.click()
            time.sleep(self.lw)     
            
    def clickServicesTab(self):
            expect(self.servicesTab).to_be_visible()
            self.servicesTab.click()
            time.sleep(self.nw) 
            
    def clickIsThisATechRefresh(self):
            expect(self.IsThisATechRefresh).to_be_visible()
            self.IsThisATechRefresh.click()
            time.sleep(self.nw) 
            
    def clickDoesYourCustomerRequireBlueXP(self):
            expect(self.doesYourCustomerRequireBlueXP).to_be_visible()
            self.doesYourCustomerRequireBlueXP.click()
            time.sleep(self.nw) 
            
    def clickDoesYourCustomerNeedPSONTAP(self):
            expect(self.doesYourCustomerNeedPSONTAP).to_be_visible()
            self.doesYourCustomerNeedPSONTAP.click()
            time.sleep(self.nw) 
            
    def clickDoYouWantToAddRansomwareRecoveryAssurance(self):
            expect(self.doYouWantToAddRansomwareRecoveryAssurance).to_be_visible()
            self.doYouWantToAddRansomwareRecoveryAssurance.click()
            time.sleep(self.nw)   
            
    def clickAddToQuote(self):
            expect(self.addToQuote).to_be_visible()
            self.addToQuote.click()
            time.sleep(self.lw)   
            time.sleep(self.mw)  
            time.sleep(self.lw)  
    
    def clickSaveButton(self):
            expect(self.saveButton).to_be_visible()
            self.saveButton.click()
            time.sleep(self.mw)  
      
        
            
                