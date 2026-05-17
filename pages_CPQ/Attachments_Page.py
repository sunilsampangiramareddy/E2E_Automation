from allure import attachment_type
from playwright.sync_api import Page, expect, TimeoutError
import time
import logging
import os

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class AttachmentsPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.attachmentsTab = self.page.get_by_role("tab", name=" Attachments")
        self.dragAndDrop = self.page.get_by_role(
            "button", name="Add Files. Drag and Drop."
        )
        self.attachmentType = self.page.get_by_text("Attachment Type")
        self.attachmentDescription = self.page.get_by_text("Attachment Description")
        self.uploadButton = self.page.get_by_role("button", name="Upload")

    def clickAttachmentsTab(self):
        wait_for_element(self.attachmentsTab)
        self.attachmentsTab.click()
        time.sleep(self.sw)

    def selectDragAndDrop(self):
        # Path to the file in the resources folder
        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )  # Get the current directory of this file
        file_path = os.path.join(
            current_dir, "../resources/test.txt"
        )  # Relative path to the txt file
        # Normalize the path for cross-platform support (Windows, Linux, macOS)
        file_path = os.path.normpath(file_path)
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

    def selectAttachmentType(self, attachment_type):
        wait_for_element(self.attachmentType)
        self.attachmentType.click()
        self.attachmentType.fill(attachment_type)
        # Construct the XPath dynamically using the provided attachment_type
        xpath = f"(//span[text()='{attachment_type}'])[1]"
        attachment_element = self.page.locator(xpath)
        expect(attachment_element).to_be_visible()
        attachment_element.click()
        time.sleep(self.nw)

    def enterAttachmentDescription(self, attachment_description):
        wait_for_element(self.attachmentDescription)
        self.attachmentDescription.click()
        self.page.get_by_role("textbox", name="Attachment Description").fill(
            attachment_description
        )
        time.sleep(self.nw)

    def clickUploadButton(self):
        wait_for_element(self.uploadButton)
        self.uploadButton.click()
        time.sleep(self.mw)
