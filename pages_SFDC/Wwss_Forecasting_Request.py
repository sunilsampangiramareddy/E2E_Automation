from playwright.sync_api import Page, expect
import re

from utils.utils import wait_for_element

class WWSSForecastingRequest:
    def __init__(self, page: Page):
        self.page = page

    def openServiceCategories(self):
        self.page.get_by_role("link", name="Service Categories").first.click()

    def addServiceCategory(self, fst_code: str, parent_category: str, estimated_tbs: str, source_storage: str):
        wait_for_element(self.page.get_by_role("combobox", name="FST Code"))
        self.page.get_by_role("combobox", name="FST Code").click()
        self.page.get_by_role("option", name=fst_code).click()
        self.page.get_by_role("combobox", name="Service Category Parent").click()
        self.page.get_by_role("option", name=parent_category).click()
        if(parent_category=="Migrations"):
            wait_for_element(self.page.get_by_role("spinbutton", name="Estimated TeraBytes (TBs)"))
            self.page.get_by_role("spinbutton", name="Estimated TeraBytes (TBs)").click()
            self.page.get_by_role("spinbutton", name="Estimated TeraBytes (TBs)").fill(estimated_tbs)
            self.page.get_by_role("textbox", name="Source Storage").click()
            self.page.get_by_role("textbox", name="Source Storage").fill(source_storage)


    def validateServiceCategoryCount(self, expected_count: int):
        expect(self.page.get_by_role("heading", name=f"Service Categories ({expected_count})")).to_be_visible()

    def editServiceCategoryAmounts(self,percent,amount):
        self.page.get_by_role("link", name="SC-").first.click()
        self.page.get_by_role("button", name="Edit Override Discount %").click()
        self.page.get_by_role("spinbutton", name="Override Discount %").fill(percent)
        self.page.get_by_role("spinbutton", name="Gross Booking Amount Local").click()
        self.page.get_by_role("spinbutton", name="Gross Booking Amount Local").fill(amount)
        self.page.get_by_role("button", name="Save").click()

    def getFieldValue(self, field_name):
        field = self.page.locator(
            f"div.slds-form-element:has(span.test-id__field-label:text-is('{field_name}'))"
        )     
        if field_name == "Opportunity Owner":
            return field.locator("lightning-formatted-text").first.text_content().strip()
        return field.locator("span.test-id__field-value").text_content().strip()

    
    def validateowner(self, expected_owner):
        actual_owner = self.getFieldValue("Opportunity Owner")
        assert actual_owner, "Opportunity Owner is empty"
        assert actual_owner == expected_owner, (
            f"Expected Opportunity Owner '{expected_owner}', "
            f"but found '{actual_owner}'"
        )

    def verifyBookingAmountsAreFilled(self,amount):
        for field in [
            "Gross Booking Amount Local Currency",
            "Gross Booking Amount USD",
            "Net Booking Amount Local Currency",
            "Net Booking Amount USD",
        ]:
            value = self.getFieldValue(field)
            assert value, f"{field} is empty"       
            if field == "Gross Booking Amount Local Currency":
                        assert value == amount, (
                            f"Expected {amount} for {field}, but got {value}"
                        )
