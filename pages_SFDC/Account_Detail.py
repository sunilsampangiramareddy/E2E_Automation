import re

from playwright.sync_api import Page, expect
import time

from conftest import page
from utils.utils import wait_for_element


class AccountDetail:
    nw = 2
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.show_all_link = page.get_by_role("link", name="Show All")
        self.partner_competencies_link = page.get_by_role(
            "link", name="Partner Competencies"
        )
        self.users_in_assigned_territories_link = page.get_by_role(
            "link", name="Users in Assigned Territories"
        )
        self.contacts_link = page.get_by_role("link", name="Contacts")
        self.related_contacts_link = page.get_by_role("link", name="Related Contacts")
        self.partner_status_value = page.locator(
            "//p[normalize-space()='Partner Status']/following-sibling::p"
        )
        self.new_opportunity_button = page.get_by_role("button", name="New Opportunity")

    def clickNewOpportunityButton(self):
        expect(self.new_opportunity_button).to_be_visible()
        self.new_opportunity_button.click()

    def completeResourceRequest(self, request_team_options, comment="test automation"):
        self.page.get_by_role("button", name="Request a Resource").click()
        request_team_dropdown = self.page.get_by_role("combobox", name="Request Team")
        wait_for_element(request_team_dropdown)
        request_team_dropdown.click()
        for option in request_team_options:
            expect(self.page.get_by_text(option)).to_be_visible()
        self.page.get_by_text(request_team_options[1]).click()
        self.page.locator("input[name='Requested_Activity']").click()
        self.page.locator("input[name='Requested_Activity']").fill(comment)
        self.page.get_by_role("button", name="Submit", exact=True).click()

    def validateRequestStatus(self, expected_status):
        time.sleep(self.sw)
        expect(self.page.get_by_text(expected_status)).to_be_visible()
        time.sleep(self.sw)

    def validateAccountStatus(self, status):
        time.sleep(self.sw)
        expect(self.partner_status_value).to_have_text(status)

    def clickShowAll(self):
        time.sleep(self.sw)
        for _ in range(8):
            self.page.mouse.wheel(0, 800)
        self.show_all_link.click()

    def clickPartnerComptenciesLink(self):
        self.partner_competencies_link.click()
        time.sleep(self.sw)

    def clickRelatedContactsLink(self):
        self.related_contacts_link.click()
        time.sleep(self.sw)

    def clickContactsLink(self):
        self.contacts_link.nth(1).click()
        time.sleep(self.sw)

    def selectSalutation(self, salutation):
        wait_for_element(self.page.get_by_role("combobox", name="Salutation"))
        self.page.get_by_role("combobox", name="Salutation").click()
        self.page.locator("span").filter(has_text=salutation).first.click()

    def selectAccountName(self, account_name):
        wait_for_element(self.page.get_by_role("combobox", name="Account Name"))
        self.page.get_by_role("combobox", name="Account Name").click()
        self.page.get_by_label("Recent Items").get_by_title(account_name, exact=True).click()

    def clickSaveButton(self):
        wait_for_element(self.page.get_by_role("button", name="Save", exact=True))
        self.page.get_by_role("button", name="Save", exact=True).click()
             
    def validateErrorMessage(self, expected_message):
        try:
            expect(self.page.get_by_text(expected_message)).to_be_visible()
            return True
        except Exception:
            return False
        
    def clickUsersInAssignedTerritoriesLink(self):
        self.users_in_assigned_territories_link.click()
        time.sleep(self.sw)

    def validateHyperscalerSsp(self, hyperscaler, oppty_owner):
        for _ in range(5):
            self.page.mouse.wheel(0, 500)
        azure_ssp_row = self.page.locator("tbody tr").filter(
                has=self.page.locator("td span.slds-truncate", has_text=hyperscaler + " SSP")
            ).first

        azure_ssp_row.scroll_into_view_if_needed()
        

            # Owner is in the <th> cell
        owner_locator = azure_ssp_row.locator("th a[title]")
        expect(owner_locator).to_be_visible()

        owner_name = owner_locator.inner_text().strip()

        assert owner_name == oppty_owner, (
                f"Expected owner '{oppty_owner}', but found '{owner_name}' for Azure SSP row"
            )
        
    def readAccountowner(self) -> str:
        return self.page.locator(
            "//p[@title='Account Owner']/following-sibling::p//a[contains(@href, '/lightning/r/User/')]"
        ).inner_text().strip()


    def readTerritory(self) -> str:
        self.page.get_by_role("tab", name="Hierarchy").click()

        territory_value = self.page.locator(
            "//span[text()='SE Territory']"
            "/ancestor::div[contains(@class,'slds-form-element')]"
            "//lightning-formatted-text"
        )

        expect(territory_value).to_be_visible()

        return (territory_value.text_content() or "").strip()

    def gotoNAGPaccount(self):
        self.page.get_by_role("tab", name="Hierarchy").click()
        for _ in range(5):
            self.page.mouse.wheel(0, 500)
        field = self.page.locator("div.slds-form-element").filter(
            has=self.page.locator(
                "span.test-id__field-label",
                has_text="NAGP Rep Site Link"
            )
        )
        field.wait_for(state="visible", timeout=60000)
        with self.page.expect_popup() as popup_info:
            field.locator("a").first.click()
        page1 = popup_info.value
        page1.wait_for_load_state()
        return page1
    
    def readTerritoryATS(self, territory: str) -> str:
        for _ in range(5):
            self.page.mouse.wheel(0, 500)
        ats_row = self.page.locator("tbody tr").filter(
            has=self.page.locator(
                "td",
                has_text="Account Technology Specialist(ATS)"
            )
        ).filter(
            has=self.page.locator(
                "td",
                has_text=territory
            )
        ).first

        ats_row.scroll_into_view_if_needed()

        owner_locator = ats_row.locator("th a[title]")
        expect(owner_locator).to_be_visible()

        return owner_locator.inner_text().strip()
            
    