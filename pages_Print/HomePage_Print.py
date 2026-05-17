import os
import shutil
from tracemalloc import start
from numpy import rint
from playwright.sync_api import Page, expect, sync_playwright
import time
import logging
import random

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePagePrint:
    nw = 2
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.printTab = self.page.locator("(//span[normalize-space()='Print'])[2]")

    def clickPrintTab(self):
        wait_for_element(self.printTab)
        self.printTab.click()
        time.sleep(self.sw)

    def operationGenerateB2BXmlExportAndSubmit(self):
        try:
            self.page.locator("(//*[text()='More Actions'])[1]").wait_for(
                state="visible", timeout=60000
            )
            self.page.locator("(//*[text()='More Actions'])[1]").click()
            time.sleep(self.nw)
            self.page.locator("(//*[text()='Generate B2B XML Export'])[1]").click()
            time.sleep(self.mw)
            logger.info(
                f"Clicked More Actions button and Generate B2B XML Export operation"
            )
            self.page.locator(
                "//span[@slot='startIcon' and contains(@class, 'oj-ux-ico-document-attachment')]"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator(
                "//span[@slot='startIcon' and contains(@class, 'oj-ux-ico-document-attachment')]"
            ).click()
            time.sleep(self.mw)
            # Get all open tabs in the browser context
            tabs = self.page.context.pages
            # Close the third tab (assuming it is the most recently opened tab)
            if len(tabs) >= 3:  # Ensure there are at least 3 tabs
                tabs[2].close()  # Index 2 corresponds to the third tab (0-based index)
            else:
                logging.info(f"The third tab is not available.")

            # Use Computer Downloads folder to save the downloaded file
            # download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            # OR Use the project's working directory Downloads folder to save the downloaded file
            download_dir = os.path.join(os.getcwd(), "Downloads")
            with self.page.expect_download() as download_info:
                self.page.locator("//a[contains(., '.xml')]").click()
            download = download_info.value

            # Save the downloaded file to the desired location
            file_path = os.path.join(download_dir, download.suggested_filename)
            download.save_as(file_path)
            # Print the filename and file path
            print(f"Downloaded file name: {download.suggested_filename}")
            logging.info(f"Downloaded file name: {download.suggested_filename}")
            print(f"Downloaded to: {file_path}")
            logging.info(f"Downloaded to: {file_path}")
            time.sleep(self.nw)

            # Copy the file to the network location
            network_location = (
                r"\\cordelia.hq.netapp.com\corp\Synergy\POSubProd\STG1\QuoteXMLs"
            )
            destination_path = os.path.join(
                network_location, download.suggested_filename
            )

            # Wait for the network location to be accessible
            logging.info("Waiting for the network location to be accessible...")
            time.sleep(
                20
            )  # Wait for 20 seconds to ensure the network location is ready

            # Copy the file
            shutil.copy(file_path, destination_path)
            logging.info(f"Copied file to: {destination_path}")
            print(f"Copied file to: {destination_path}")

            # Wait for the FTP process to handle the file
            logging.info("Waiting for the FTP process to handle the file...")
            time.sleep(
                30
            )  # Wait for 30 seconds for the background FTP process to complete

            # Confirm the file has disappeared (optional)
            if not os.path.exists(destination_path):
                logging.info(
                    f"The file {destination_path} has been processed and disappeared."
                )
            else:
                logging.warning(f"The file {destination_path} is still present.")

            self.page.locator("//span[@class='oj-ux-ico-close']").click()
            time.sleep(self.mw)
        except Exception as e:
            logging.error(f"An error occurred during the operation: {e}")
            raise
