from playwright.sync_api import Page, expect, TimeoutError
import time
import logging
from datetime import datetime, timedelta

from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageKeystone:
    nw = 3
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.keystoneStorageAsServiceV3 = self.page.locator(
            "//span[text()='Keystone Storage-as-a-Service v3']"
        )
        self.orderType = self.page.locator("(//input[@role='combobox'])[3]")
        self.targetSiteDate = self.page.locator("(//input[@role='combobox'])[2]")
        self.targetStartDate = self.page.locator(
            "//input[@type='text' and @role='combobox' and @id='targetSiteReadinessDate_KFS|input']"
        )
        self.keystoneServicesTab = self.page.locator(
            "//a[normalize-space()='Keystone Services']"
        )
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")
        self.viewMoreLink = self.page.locator("//a[text()='View more']")
        self.errorMessage = self.page.locator(
            "(//div[@class='oj-messagebanner-detail'])[4]"
        )

    def clickProductName(self, productName: str):
        if productName == "Keystone Storage-as-a-Service v3":
            wait_for_element(self.keystoneStorageAsServiceV3)
            self.keystoneStorageAsServiceV3.click()
            time.sleep(self.nw)
            self.page.locator("(//a[text()='Configure'])[2]").click()
            time.sleep(self.mw)
        else:
            raise ValueError(f"Invalid product name: {productName}")

    def click_ProductName(self, product_name):
        # Dynamically create the XPath using the product_name argument
        locator = self.page.locator(
            f"(//*[normalize-space(text())='{product_name}'])[1]"
        )
        # Wait for the element to be visible
        locator.wait_for(state="visible", timeout=60000)
        # Click on the element
        locator.click()
        time.sleep(self.nw)

    def select_SubProduct(self, sub_Product):
        try:
            # Construct the XPath with the parameterized sub_Product
            xpath = f"//a[contains(@href, 'templateName={sub_Product}')]"
            # Wait for the element to be visible
            self.page.locator(xpath).wait_for(state="visible", timeout=60000)
            # Click the element
            self.page.locator(xpath).click()
            time.sleep(self.sw)
        except Exception as e:
            print(f"Error selecting sub product {sub_Product}: {e}")

    def selectOrderType(self, orderType: str):
        wait_for_element(self.orderType)
        self.orderType.click()
        time.sleep(self.nw)
        xpath = f"//span[text()='{orderType}']"
        self.page.locator(xpath).click()
        time.sleep(self.nw)

    def selectTargetSiteDate(self):
        # Get the current date in DD/MM/YYYY format
        current_date = datetime.now().strftime(
            "%d/%m/%Y"
        )  # Format the date as DD/MM/YYYY
        wait_for_element(self.targetSiteDate)
        self.targetSiteDate.click()
        self.targetSiteDate.fill(current_date)
        self.targetSiteDate.press("Tab")
        time.sleep(self.nw)

    def selectTargetStartDate(self):
        # Calculate the current date + 10 days
        future_date = (datetime.now() + timedelta(days=10)).strftime(
            "%d/%m/%Y"
        )  # Format as DD/MM/YYYY
        wait_for_element(self.targetStartDate)
        self.targetStartDate.click()
        self.targetStartDate.fill(future_date)
        self.targetStartDate.press("Tab")
        time.sleep(self.nw)

    def clickKeystoneServicesTab(self):
        wait_for_element(self.keystoneServicesTab)
        self.keystoneServicesTab.click()
        time.sleep(self.nw)

    def selectDataType(self, dataType: str):
        self.page.locator(
            "//div[contains(@class, 'cpq-table-data-cell') and contains(@class, 'col-dataType_KS')]"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//div[contains(@class, 'cpq-table-data-cell') and contains(@class, 'col-dataType_KS')]"
        ).dblclick()
        time.sleep(self.nw)
        self.page.locator(
            "//input[@id='oj-searchselect-filter-dataType_KS|input' and @class='oj-inputtext-input oj-text-field-input oj-component-initnode' and @type='text']"
        ).click()
        self.page.locator(
            "//input[@id='oj-searchselect-filter-dataType_KS|input' and @class='oj-inputtext-input oj-text-field-input oj-component-initnode' and @type='text']"
        ).fill(dataType)
        xpath = f"//span[text()='{dataType}']"
        self.page.locator(xpath).click()
        time.sleep(self.sw)

    def selectServiceLevel(self, serviceLevel: str):
        self.page.get_by_role("gridcell").nth(2).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(2).click()
        time.sleep(self.nw)
        self.page.locator('[id="serviceLevel_KS|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-serviceLevel_KS|input"]').fill(
            serviceLevel
        )
        self.page.get_by_text(serviceLevel, exact=True).click()
        time.sleep(self.sw)

    def enterTotalCapacityCommitted(self, totalCapacity: str):
        self.page.locator(
            "//div[@role='gridcell' and contains(@class, 'col-quantity_KS')]"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "//div[@role='gridcell' and contains(@class, 'col-quantity_KS')]"
        ).dblclick()
        time.sleep(self.nw)
        self.page.locator(
            "//input[@id='quantity_KS|input' and @role='spinbutton' and @aria-invalid='true']"
        ).click()
        self.page.locator(
            "//input[@id='quantity_KS|input' and @role='spinbutton' and @aria-invalid='true']"
        ).fill(str(totalCapacity))
        time.sleep(self.sw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)

    def selectTargetReadinessDate(self):
        # Get the current date in DD/MM/YYYY format
        current_date = datetime.now().strftime(
            "%d/%m/%Y"
        )  # Format the date as DD/MM/YYYY
        self.page.get_by_text("Target Site Readiness Date").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_text("Target Site Readiness Date").click()
        self.page.get_by_role("textbox", name="Target Site Readiness Date").fill(
            current_date
        )
        self.page.get_by_role("textbox", name="Target Site Readiness Date").press("Tab")
        time.sleep(self.nw)

    def selectTarget_StartDate(self):
        # Calculate the current date + 10 days
        future_date = (datetime.now() + timedelta(days=10)).strftime(
            "%d/%m/%Y"
        )  # Format as DD/MM/YYYY
        self.page.get_by_text("Target Start Date").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_text("Target Start Date").click()
        self.page.get_by_role("textbox", name="Target Start Date").fill(future_date)
        self.page.get_by_role("textbox", name="Target Start Date").press("Tab")
        time.sleep(self.nw)

    def clickViewMoreLink(self):
        wait_for_element(self.viewMoreLink)
        self.viewMoreLink.click()
        time.sleep(self.nw)

    def getErrorMessage(self):
        wait_for_element(self.errorMessage)
        error_message_text = self.errorMessage.text_content()
        return error_message_text

    def clickBillOfMaterials(self):
        self.page.locator("//span[text()='Bill of Materials']").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("//span[text()='Bill of Materials']").click()
        time.sleep(self.nw)

    def clickCloseButton(self):
        self.page.locator("(//oj-button[@title='Close'])[1]").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("(//oj-button[@title='Close'])[1]").click()
        time.sleep(self.nw)

    def validateSupportOwnership(self, xpath: str) -> None:
        try:
            # Check if the element exists
            element = self.page.query_selector(xpath)
            if element:
                logger.info(f"Element found using XPath: {xpath}")
                # Determine the tag name and role attribute of the element
                tag_name = element.evaluate("el => el.tagName").lower()
                role_attribute = element.get_attribute("role")
                # Handle combobox (dropdown)
                if tag_name == "input" and role_attribute == "combobox":
                    logger.info("Element is a combobox.")
                    # Click the combobox to expand it
                    element.click()
                    logger.info(f"Clicked combobox element: {xpath}")
                    # Locate the dropdown options
                    dropdown_list_id = element.get_attribute("aria-controls")
                    option_xpath = f"//div[@id='{dropdown_list_id}']//li"
                    options = self.page.query_selector_all(option_xpath)
                    for option in options:
                        option_text = option.inner_text()
                        logger.info(f"Dropdown option: {option_text}")
                        option.click()
                        # Handle specific dropdown values
                        if option_text == "Distributor":
                            self.validate_objects(
                                "xpath_for_object1", "xpath_for_object2"
                            )
                        elif option_text == "Reseller":
                            self.validate_objects(
                                "xpath_for_object1", "xpath_for_object2"
                            )
                # Handle label
                elif tag_name == "div" and role_attribute == "textbox":
                    logger.info("Element is a label.")
                    label_text = element.inner_text()
                    logger.info(f"Label text: {label_text}")
                    # Handle specific label values
                    if label_text == "Distributor":
                        self.validate_objects("xpath_for_object1", "xpath_for_object2")
                    elif label_text == "Reseller":
                        self.validate_objects("xpath_for_object1", "xpath_for_object2")
                else:
                    logger.warning(
                        "Element found, but it is neither a combobox nor a label."
                    )
            else:
                logger.warning(f"Element not found using XPath: {xpath}")
        except Exception as e:
            logger.error(f"An error occurred while handling the element: {e}")
            raise e

    def validate_objects(self, object1_xpath: str, object2_xpath: str):
        try:
            object1 = self.page.query_selector(object1_xpath)
            object2 = self.page.query_selector(object2_xpath)

            if object1:
                object1_text = object1.inner_text()
                logger.info(f"Fetched text for object 1: {object1_text}")
            else:
                logger.warning("Object 1 is not visible on the UI.")

            if object2:
                object2_text = object2.inner_text()
                logger.info(f"Fetched text for object 2: {object2_text}")
            else:
                logger.warning("Object 2 is not visible on the UI.")

            if object1 and object2:
                if object1_text == object2_text:
                    logger.info("Both objects are visible and their texts are equal.")
                else:
                    logger.info(
                        "Both objects are visible, but their texts are not equal."
                    )
        except Exception as e:
            logger.error(f"An error occurred while validating objects: {e}")
            raise e
