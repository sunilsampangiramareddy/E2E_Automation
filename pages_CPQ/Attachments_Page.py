from playwright.sync_api import Page, expect, TimeoutError
import time
import logging
import os

logger = logging.getLogger('playwright_pytest')

class AttachmentsPage:
    nw=3; sw=5; mw=10; lw=20
            
    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()
        
    def _initialize_locators(self):  
        self.attachmentsTab = self.page.get_by_role("tab", name=" Attachments")
        self.dragAndDrop = self.page.get_by_role("button", name="Add Files. Drag and Drop.")
        self.attachmentType = self.page.get_by_text("Attachment Type")
        self.attachmentDescription = self.page.get_by_text("Attachment Description")
        self.uploadButton = self.page.get_by_role("button", name="Upload")
        
    
    def clickAttachmentsTab(self):
        expect(self.attachmentsTab).to_be_visible()
        self.attachmentsTab.click()
        time.sleep(self.sw)
        
    def selectDragAndDrop(self):        
        # Path to the file to be uploaded
        file_path = r"C:\Users\sunilr2\OneDrive - NetApp Inc\Desktop\Attachment\txt.txt"
        file_name = os.path.basename(file_path)        
        # Safety check
        assert os.path.exists(file_path), f"File not found: {file_path}"        
        # Wait for Drag & Drop button
        expect(self.dragAndDrop).to_be_visible(timeout=30000)
        expect(self.dragAndDrop).to_be_enabled()        
        # Click button and wait for native file chooser
        with self.page.expect_file_chooser(timeout=30000) as fc_info:
            self.dragAndDrop.click()        
        # Set file
        # (This internally fills "File name" field and clicks Open)
        fc_info.value.set_files(file_path)        
        time.sleep(self.sw)
        
    def selectAttachmentType(self):
        expect(self.attachmentType).to_be_visible()
        self.attachmentType.click()
        self.page.get_by_role("option", name="Purchase Order").locator("div").nth(2).click()
        time.sleep(self.nw)
        
    def enterAttachmentDescription(self):
        expect(self.attachmentDescription).to_be_visible()
        self.attachmentDescription.click()
        self.page.get_by_role("textbox", name="Attachment Description").fill("Test")
        time.sleep(self.nw)
    
    def clickUploadButton(self):
        expect(self.uploadButton).to_be_visible()
        self.uploadButton.click()
        time.sleep(self.mw)
    





        
        

            
