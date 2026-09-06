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
        self.addOnServicesTab = self.page.get_by_role("tab", name="Add-On Services")
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

    def selectAdvancedDataProtect(self, yesOrNo: str):
        if yesOrNo.lower() == "no":
            self.page.get_by_role("option", name="No").wait_for(
                state="visible", timeout=60000
            )
            self.page.get_by_role("option", name="No").click()
            time.sleep(self.nw)
        elif yesOrNo.lower() == "yes":
            self.page.get_by_role("option", name="Yes").wait_for(
                state="visible", timeout=60000
            )
            self.page.get_by_role("option", name="Yes").click()
            time.sleep(self.nw)
        else:
            raise ValueError(f"Invalid option for Advanced Data Protect: {yesOrNo}")

    def enterADPTotalQuantity(self, totalQuantity: str):
        self.page.get_by_role("spinbutton", name="Total Quantity", exact=True).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("spinbutton", name="Total Quantity", exact=True).click()
        self.page.get_by_role("spinbutton", name="Total Quantity", exact=True).click()
        self.page.get_by_role("spinbutton", name="Total Quantity", exact=True).fill(
            str(totalQuantity)
        )
        self.page.get_by_role("spinbutton", name="Total Quantity", exact=True).press(
            "Tab"
        )
        time.sleep(self.nw)

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

    def clickAddFileAndBlockStorageServices(self):
        self.page.get_by_label("File and Block Storage").get_by_role(
            "button", name="Add"
        ).wait_for(state="visible", timeout=60000)
        self.page.get_by_label("File and Block Storage").get_by_role(
            "button", name="Add"
        ).click()
        time.sleep(self.nw)

    def selectDataType_FileAndBlockStorageServices(self, dataType: str):
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

    def selectDataType_FileAndBlockStorageServices_2(self, dataType: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-dataType_KS.type-menu.has-errors"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-dataType_KS.type-menu.has-errors"
        ).click()
        self.page.locator('[id="dataType_KS|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-dataType_KS|input"]').fill(
            dataType
        )
        self.page.get_by_text(dataType, exact=True).first.click()
        time.sleep(self.nw)

    def selectServiceLevel_FileAndBlockStorageServices(self, serviceLevel: str):
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

    def selectServiceLevel_FileAndBlockStorageServices_2(self, serviceLevel: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-serviceLevel_KS.type-menu.oj-selected"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-serviceLevel_KS.type-menu.oj-selected"
        ).click()
        self.page.locator('[id="serviceLevel_KS|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-serviceLevel_KS|input"]').fill(
            serviceLevel
        )
        self.page.get_by_text(serviceLevel, exact=True).click()
        time.sleep(self.nw)

    def enterTotalCapacityCommitted_FileAndBlockStorageServices(
        self, totalCapacity: str
    ):
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

    def enterTotalCapacityCommitted_FileAndBlockStorageServices_2(
        self, totalCapacity: str
    ):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-quantity_KS.type-number.oj-inputnumber-hide-spinbutton.oj-selected"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-quantity_KS.type-number.oj-inputnumber-hide-spinbutton.oj-selected"
        ).click()
        self.page.locator('[id="quantity_KS|input"]').click()
        self.page.locator('[id="quantity_KS|input"]').click()
        self.page.locator('[id="quantity_KS|input"]').fill(str(totalCapacity))
        self.page.locator('[id="quantity_KS|input"]').press("Tab")
        time.sleep(self.nw)

    def selectOptionalFeatures(self, optionalFeature: str):
        self.page.get_by_role("combobox", name="Optional Features").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Optional Features").click()
        self.page.get_by_role("combobox", name="Optional Features").click()
        self.page.get_by_role("combobox", name="Optional Features").fill(
            optionalFeature
        )
        self.page.get_by_text(optionalFeature).click()
        self.page.get_by_role("combobox", name="Optional Features").press("Tab")
        time.sleep(self.nw)

    def enterTotalQuantity_OptionalFeatures(self, totalQuantity: str):
        self.page.get_by_role("spinbutton", name="Total Quantity (TiB)").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("spinbutton", name="Total Quantity (TiB)").click()
        self.page.get_by_role("spinbutton", name="Total Quantity (TiB)").click()
        self.page.get_by_role("spinbutton", name="Total Quantity (TiB)").fill(
            str(totalQuantity)
        )
        self.page.get_by_role("spinbutton", name="Total Quantity (TiB)").press("Tab")
        time.sleep(self.nw)

    def selectDataType_ObjectStorageServices(self, dataType: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-dataTypeObject_KS"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-dataTypeObject_KS"
        ).click()
        self.page.locator('[id="dataTypeObject_KS|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-dataTypeObject_KS|input"]').fill(
            dataType
        )
        self.page.get_by_text(dataType, exact=True).click()
        time.sleep(self.nw)

    def selectServiceLevel_ObjectStorageServices(self, serviceLevel: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-serviceLevelObject_KS"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-serviceLevelObject_KS"
        ).click()
        self.page.locator('[id="serviceLevelObject_KS|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-serviceLevelObject_KS|input"]'
        ).fill(serviceLevel)
        self.page.get_by_text(serviceLevel, exact=True).first.click()
        time.sleep(self.nw)

    def selectTotalCapacity_ObjectStorageServices(self, totalCapacity: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-quantityObject_KS"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-quantityObject_KS"
        ).click()
        self.page.locator('[id="quantityObject_KS|input"]').click()
        self.page.locator('[id="quantityObject_KS|input"]').fill(str(totalCapacity))
        self.page.locator('[id="quantityObject_KS|input"]').press("Tab")
        time.sleep(self.nw)

    def selectBillingFrequency(self, billingFrequency: str):
        self.page.get_by_role("combobox", name="Required Billing Frequency").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Required Billing Frequency").click()
        self.page.get_by_role("combobox", name="Billing Frequency").fill(
            billingFrequency
        )
        self.page.get_by_text(billingFrequency, exact=True).last.click()
        time.sleep(self.nw)

    def selectTerm(self, term: str):
        term = str(int(float(term)))
        self.page.get_by_role("combobox", name="Required Term (Months)").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Required Term (Months)").click()
        self.page.get_by_role("combobox", name="Term (Months)").fill(term)
        self.page.get_by_text(term, exact=True).click()
        self.page.get_by_role("combobox", name="Term (Months)").press("Tab")
        time.sleep(self.nw)

    def clickAddOnServicesTab(self):
        wait_for_element(self.addOnServicesTab)
        self.addOnServicesTab.click()
        time.sleep(self.nw)

    def selectDataInfrastructureInsights(self, dataInfrastructureInsights: str):
        if dataInfrastructureInsights.lower() == "no":
            self.page.get_by_role(
                "listbox", name="Required Data Infrastructure"
            ).get_by_label("No").wait_for(state="visible", timeout=60000)
            self.page.get_by_role(
                "listbox", name="Required Data Infrastructure"
            ).get_by_label("No").click()
            time.sleep(self.nw)
        elif dataInfrastructureInsights.lower() == "yes":
            self.page.get_by_role(
                "listbox", name="Required Data Infrastructure"
            ).get_by_label("Yes").wait_for(state="visible", timeout=60000)
            self.page.get_by_role(
                "listbox", name="Required Data Infrastructure"
            ).get_by_label("Yes").click()
            time.sleep(self.nw)
        else:
            raise ValueError(
                f"Invalid option for Data Infrastructure Insights: {dataInfrastructureInsights}"
            )

    def enterKeystoneSupplementalServices_Subscription(
        self, keystoneSupplementalServices: str
    ):
        self.page.get_by_role(
            "spinbutton", name="Keystone Supplemental Services"
        ).wait_for(state="visible", timeout=60000)
        self.page.get_by_role(
            "spinbutton", name="Keystone Supplemental Services"
        ).click()
        self.page.get_by_role(
            "spinbutton", name="Keystone Supplemental Services"
        ).click()
        self.page.get_by_role("spinbutton", name="Keystone Supplemental Services").fill(
            str(keystoneSupplementalServices)
        )
        self.page.get_by_role(
            "spinbutton", name="Keystone Supplemental Services"
        ).press("Tab")
        time.sleep(self.nw)

    def enterTotalQuantity_Networking(self, totalQuantity: str):
        self.page.get_by_role("spinbutton", name="Total Quantity").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("spinbutton", name="Total Quantity").click()
        self.page.get_by_role("spinbutton", name="Total Quantity").click()
        self.page.get_by_role("spinbutton", name="Total Quantity").fill(
            str(totalQuantity)
        )
        self.page.get_by_role("spinbutton", name="Total Quantity").press("Tab")
        time.sleep(self.nw)

    def selectNRDType_Support(self, nrdType: str):
        self.page.get_by_role("combobox", name="Non-Returnable Drives (NRD)").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Non-Returnable Drives (NRD)").click()
        self.page.get_by_role("combobox", name="NRD Type").fill(nrdType)
        self.page.get_by_text(nrdType, exact=True).click()
        time.sleep(self.nw)

    def selectManagedServices_ProfessionalServices(self, managedServices: str):
        self.page.get_by_role("combobox", name="Managed Services").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Managed Services").click()
        self.page.get_by_role("combobox", name="Managed Services").click()
        self.page.get_by_role("combobox", name="Managed Services").fill(managedServices)
        self.page.get_by_text(managedServices, exact=True).click()
        time.sleep(self.nw)

    def selectCountry(self, country: str):
        self.page.get_by_role("combobox", name="Country").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Country").click()
        self.page.get_by_role("combobox", name="Country").clear()
        self.page.get_by_role("combobox", name="Country").fill(country)
        self.page.get_by_text(country, exact=True).click()
        time.sleep(self.nw)

    def enterMigrationServices_DataMigrationAsService(self, migrationServices: str):
        self.page.locator("//*[@id='dMaaS_KS|input']").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("//*[@id='dMaaS_KS|input']").click()
        self.page.locator("//*[@id='dMaaS_KS|input']").fill(str(migrationServices))
        self.page.locator("//*[@id='dMaaS_KS|input']").press("Tab")
        time.sleep(self.nw)

    def selectOnsiteDelivery_TravelAndExpense(self, onsiteDelivery: str):
        if onsiteDelivery.lower() == "check":
            self.page.locator('[id="dMaaSTE_KStrue|cb"]').wait_for(
                state="visible", timeout=60000
            )
            self.page.locator('[id="dMaaSTE_KStrue|cb"]').check()
            time.sleep(self.nw)
        elif onsiteDelivery.lower() == "uncheck":
            self.page.locator('[id="dMaaSTE_KStrue|cb"]').wait_for(
                state="visible", timeout=60000
            )
            self.page.locator('[id="dMaaSTE_KStrue|cb"]').uncheck()
            time.sleep(self.nw)

    def enterTimeAndMaterials_Days(self, timeAndMaterials: str):
        self.page.get_by_role("spinbutton", name="Time & Materials (Days)").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("spinbutton", name="Time & Materials (Days)").click()
        self.page.get_by_role("spinbutton", name="Time & Materials (Days)").click()
        self.page.get_by_role("spinbutton", name="Time & Materials (Days)").fill(
            str(timeAndMaterials)
        )
        self.page.get_by_role("spinbutton", name="Time & Materials (Days)").press("Tab")
        time.sleep(self.nw)

    def selectOnsiteDelivery_TravelAndExpense_2(self, onsiteDelivery: str):
        if onsiteDelivery.lower() == "check":
            self.page.locator('[id="tnMTE_KStrue|cb"]').wait_for(
                state="visible", timeout=60000
            )
            self.page.locator('[id="tnMTE_KStrue|cb"]').check()
            time.sleep(self.nw)
        elif onsiteDelivery.lower() == "uncheck":
            self.page.locator('[id="tnMTE_KStrue|cb"]').wait_for(
                state="visible", timeout=60000
            )
            self.page.locator('[id="tnMTE_KStrue|cb"]').uncheck()
            time.sleep(self.nw)

    def selectSAMService(self, samService: str):
        if samService.lower() == "no":
            self.page.locator("#sAMService_KS-no").wait_for(
                state="visible", timeout=60000
            )
            self.page.locator("#sAMService_KS-no").click()
            time.sleep(self.nw)
        elif samService.lower() == "yes":
            self.page.locator("#sAMService_KS-yes").wait_for(
                state="visible", timeout=60000
            )
            self.page.locator("#sAMService_KS-yes").click()
            time.sleep(self.nw)

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

    def validateEligibleDiscountForInternalEngineering(self, page) -> bool:
        """
        Validates the Eligible Discount for rows where Eligible Discount Source matches 'Internal Engineering'.

        Args:
            page (Page): The Playwright page object.

        Returns:
            bool: True if all validations pass, False otherwise.
        """
        logger.info(
            "Starting validation for Eligible Discount Source and Eligible Discount for Internal Engineering Quote."
        )
        # Define constants
        EXPECTED_DISCOUNT = 100
        COLUMN_XPATHS = {
            "Eligible Discount Source": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-eligibleDiscountSource_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Eligible Discount": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-eligibleDiscount_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
        }
        # Locate elements for both columns
        source_locator = page.locator(COLUMN_XPATHS["Eligible Discount Source"])
        discount_locator = page.locator(COLUMN_XPATHS["Eligible Discount"])
        # Get the number of rows
        row_count = source_locator.count()
        if row_count == 0:
            logger.warning("No rows found in the table. Skipping validation.")
            print("No rows found in the table. Skipping validation.")
            return True  # No rows to validate, consider it passed
        logger.info(f"Found {row_count} rows in the table.")
        print(f"Found {row_count} rows in the table.")

        # Initialize a flag to track overall validation status
        validation_passed = True

        # Iterate through each row
        for i in range(row_count):
            try:
                # Read the "Eligible Discount Source" value
                source_value = (
                    source_locator.nth(i).inner_text().strip()
                )  # Strip whitespace to handle blank values
                logger.info(
                    f"Row {i + 1}: Eligible Discount Source value: '{source_value}'"
                )
                # Check if the source value is empty (blank or whitespace)
                if not source_value:
                    logger.info(
                        f"Row {i + 1}: Eligible Discount Source is empty or blank. Skipping row."
                    )
                    continue
                # Check if the source value matches "Internal Engineering"
                if source_value == "Internal Engineering":
                    logger.info(
                        f"Row {i + 1}: Found matching Eligible Discount Source: {source_value}"
                    )
                    # Read the corresponding "Eligible Discount" value
                    discount_value = discount_locator.nth(i).inner_text().strip()
                    logger.info(
                        f"Row {i + 1}: Eligible Discount value: '{discount_value}'"
                    )
                    # Validate the discount value
                    try:
                        numeric_discount_value = float(discount_value)
                        if numeric_discount_value == EXPECTED_DISCOUNT:
                            logger.info(
                                f"Row {i + 1}: Eligible Discount validation passed (100%)."
                            )
                            print(
                                f"\033[92m✅ Row {i + 1}: Eligible Discount validation passed (100%).\033[0m"
                            )
                        else:
                            logger.warning(
                                f"Row {i + 1}: Eligible Discount validation failed. Expected: {EXPECTED_DISCOUNT}, Found: {numeric_discount_value}"
                            )
                            print(
                                f"\033[91m❌ Row {i + 1}: Eligible Discount validation failed. Expected: {EXPECTED_DISCOUNT}, Found: {numeric_discount_value}\033[0m"
                            )
                            validation_passed = False
                    except ValueError:
                        logger.error(
                            f"Row {i + 1}: Invalid Eligible Discount value: '{discount_value}'. Cannot convert to number."
                        )
                        print(
                            f"\033[91m❌ Row {i + 1}: Invalid Eligible Discount value: '{discount_value}'. Cannot convert to number.\033[0m"
                        )
                        validation_passed = False
                else:
                    logger.debug(
                        f"Row {i + 1}: Eligible Discount Source does not match 'Internal Engineering'."
                    )
                    print(
                        f"\033[91m❌ Row {i + 1}: Eligible Discount Source does not match 'Internal Engineering'.\033[0m"
                    )
            except Exception as e:
                logger.error(
                    f"Row {i + 1}: An error occurred during validation. Error: {e}"
                )
                print(
                    f"\033[91m❌ Row {i + 1}: An error occurred during validation. Error: {e}\033[0m"
                )
                validation_passed = False

        logger.info(
            "Validation for Eligible Discount Source and Eligible Discount completed."
        )
        return validation_passed
