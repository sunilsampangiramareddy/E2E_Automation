from playwright.sync_api import Page, expect, TimeoutError
import time
import logging

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageCPQ:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.saveButton = self.page.get_by_role("button", name="Save Quote")
        self.saveIcon = self.page.locator(
            "//span[@slot='startIcon' and contains(@class, 'oj-ux-ico-save')]"
        )
        self.popUp = self.page.locator(
            '//*[@id="border-8dbf786c-7da0-4898-aa4b-f1b836878c53"]'
        )
        self.quoteNumber = self.page.locator("//div[3]/div[1]/div[2]")
        self.quoteName = self.page.locator("//div[2]/div[1]/div[2]/div")
        self.quoteStatus = self.page.locator("//div[3]/div[2]/div[2]")
        self.productsTab = self.page.get_by_role("tab", name=" Products")

    def clickSaveButton(self):
        wait_for_element(self.saveButton)
        self.saveButton.click()
        time.sleep(self.mw)

    def clickSaveIcon(self):
        wait_for_element(self.saveIcon)
        self.saveIcon.click()
        time.sleep(self.mw)

    def navigateToUrl(self, url):
        self.page.goto(url)

    def closePopUp(self):
        try:
            # Wait for up to 30 seconds for the popup to be visible
            self.popUp.wait_for(state="visible", timeout=30000)  # Wait up to 30 seconds
            # Click the popup close button if it becomes visible
            self.popUp.click()
            logger.info(f"Closed the dynamic popup")
        except TimeoutError:
            logger.warning("Timeout while waiting for the popup to be visible.")
        except Exception as e:
            logger.error(f"An error occurred while closing the popup: {e}")

    def closePopUp_2(self):
        try:
            # Wait for up to 3 seconds for the popup to be visible
            self.popUp.wait_for(state="visible", timeout=3000)  # Wait up to 3 seconds
            # Click the popup close button if it becomes visible
            self.popUp.click()
            logger.info(f"Closed the dynamic popup")
        except TimeoutError:
            logger.warning("Timeout while waiting for the popup to be visible.")
        except Exception as e:
            logger.error(f"An error occurred while closing the popup: {e}")

    def getQuoteNumber(self):
        wait_for_element(self.quoteNumber)
        time.sleep(self.sw)
        quote_number = self.quoteNumber.inner_text()
        return quote_number

    def getQuoteName(self):
        wait_for_element(self.quoteName)
        quote_Name = self.quoteName.inner_text()
        return quote_Name

    def getQuoteStatus(self):
        wait_for_element(self.quoteStatus)
        quote_Status = self.quoteStatus.inner_text()
        return quote_Status

    def verifyQuoteStatus(self, expected_status):
        wait_for_element(self.quoteStatus)
        quote_Status = self.quoteStatus.inner_text()
        actual_status = quote_Status.strip().lower()
        if actual_status == expected_status.strip().lower():
            logger.info(f"Quote status is in expected state: {actual_status}")
            return True
        else:
            logger.warning(
                f"Quote status is not in expected state. Current quote status: {actual_status}"
            )
            return False

    def clickProductsTab(self):
        wait_for_element(self.productsTab)
        expect(self.productsTab).to_be_visible()
        self.productsTab.click()

    def readProductTable(self, page, column_name):
        logger.info(f"Reading product table for column: {column_name}")
        # Define a dictionary for column XPaths
        column_xpaths = {
            "Product": "//div[contains(@class, 'oj-fa-cx-cpq-fragmentsUI-lineItems-rowHeader oj-sm-align-self-center cx-cpq-line-item-row')]",
            "Part Description": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-partDescription_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Qty": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-unitQuantity_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Ext Qty": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-extendedQuantity_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "List Price": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-listPrice_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Extended List Price": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-extendedListPrice_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Treshold Group": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-thresholdGroup_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Eligible Discount Source": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-eligibleDiscountSource_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Eligible Discount": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-eligibleDiscount_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Current Discount": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-currentDiscount_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Net Price": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-netPrice_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Extended Net Price": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-extendedNetPrice_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Serial Number": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-serialNumber_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Service Start Date": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-serviceStartDate_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Service End Date": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-serviceEndDate_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Service Duration": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-serviceDuration_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
        }
        # Get the XPath for the requested column
        xpath = column_xpaths.get(column_name)
        if not xpath:
            logger.error(f"Invalid column name provided: {column_name}")
            return
        # Locate elements using the XPath
        locator = page.locator(xpath)
        count = locator.count()
        logger.info(
            f"Found {count} elements with the specified XPath for column: {column_name}"
        )
        # Extract and print text of each element
        for i in range(count):
            element = locator.nth(i)
            text = element.inner_text()
            if text:
                logger.info(f"Extracted text: {text}")
                print(text, end="\t")
            else:
                logger.warning(
                    f"Empty text found for element index {i} in column: {column_name}"
                )
        print()
