from email.mime import message
import re
import time
from playwright.sync_api import Page, expect

from conftest import page
from utils.utils import wait_for_element


class OpportunityDetailPage:
    nw = 2
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.opportunity_name = page.locator(
            '[data-output-element-id="output-field"]'
        ).nth(0)
        self.opportunity_heading = page.locator("h1 slot[name='primaryField']")
        self.show_more_actions_button = page.get_by_role(
            "button", name="Show more actions"
        )
        self.create_quote_button = page.get_by_role(
            "button", name="Create Quote", exact=True
        )
        self.paragraph_locator = page.get_by_role("paragraph")
        self.proceed_button = page.get_by_role("button", name="Proceed")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.trigger_active_quote_menuitem = page.get_by_role(
            "menuitem", name="Trigger Active Quote Sync"
        )

    def validate_opportunity_details(
        self, account_name: str, opportunity_name: str, primary_contact: str
    ):
        time.sleep(self.sw)
        body = self.page.locator("body")
        expect(body).to_contain_text(account_name)
        expect(body).to_contain_text(opportunity_name)

    def validate_opportunity_url_heading(self, lead: str, company: str):
        time.sleep(self.mw)
        expect(self.page).to_have_url(re.compile("Opportunity"))
        body = self.page.locator("body")
        expect(body).to_contain_text(lead)
        expect(body).to_contain_text(company)

    def open_show_more_actions(self):
        time.sleep(self.nw)
        self.show_more_actions_button.click()
        time.sleep(self.nw)

    def convert_to_indirect(self):
        self.page.get_by_role("menuitem", name="Convert to Indirect").click()

    def click_create_quote_and_capture_popup(self):
        # Opens the Create Quote action and returns the popup page
        self.create_quote_button.click()
        time.sleep(self.nw)
        with self.page.context.expect_page() as popup_info:
            self.create_quote_button.click()
        popup = popup_info.value
        popup.wait_for_load_state()
        return popup

    def trigger_active_quote_sync(self):
        target_text = "AQS process has completed successfully"
        while True:
            self.page.reload()
            self.open_show_more_actions()
            self.trigger_active_quote_menuitem.click()
            self.proceed_button.click()
            try:
                time.sleep(self.sw)
                expect(self.paragraph_locator).to_contain_text(target_text)
                self.finish_button.click()
                break
            except Exception:
                time.sleep(self.sw)
                self.finish_button.click()
                time.sleep(self.lw)

    def markStageAsComplete(self):
        wait_for_element(self.page.get_by_role("button", name="Mark Stage as Complete"))
        self.page.get_by_role("button", name="Mark Stage as Complete").click()
        time.sleep(self.sw)

    def update_solutions(self, use_case: str, solutions: str):
        self.page.get_by_role("button", name="Edit Use Case (1P)").click()
        self.page.get_by_role("combobox", name="Use Case (1P)").click()
        self.page.get_by_text(use_case, exact=True).click()
        self.page.get_by_role("combobox", name="Solution (1P)").click()
        self.page.get_by_role("option", name=solutions).click()
        self.page.get_by_role("combobox", name="Confidential").click()
        self.page.get_by_text("No", exact=True).click()
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Save", exact=True).click()
        time.sleep(self.nw)

    def addCompetitors(self, competitor_name: str):
        try:
            wait_for_element(self.page.get_by_role("button", name="Show more actions"))
            self.page.get_by_role("button", name="Show more actions").click()
            self.page.get_by_role("menuitem", name="Add Competitor").click()
            self.page.get_by_role("button", name="Competitor").click()
            self.page.get_by_role("option", name=competitor_name, exact=True).click()
            self.page.get_by_role("button", name="Save").click()
        except Exception:
            wait_for_element(self.page.get_by_role("button", name="Add Competitor"))
            self.page.get_by_role("button", name="Add Competitor").click()
            self.page.get_by_role("button", name="1P Competitor and Product").click()
            self.page.get_by_role("option", name=competitor_name, exact=True).click()
            self.page.get_by_role("button", name="Save").click()

    def select_closed_stage(self, stage_name: str):
        self.page.locator("label:has-text('Stage') + select").select_option(
            label=stage_name
        )
        self.page.get_by_role("button", name="Save").click()
        time.sleep(self.nw)

    def goto_oppty_account(self, account_name: str):
        account_link = self.page.locator(f"//span[text()='{account_name}']/ancestor::a")
        account_link.click()

    def open_account_party(self):
        for _ in range(3):
            self.page.mouse.wheel(0, 800)
        account_party_link = self.page.get_by_role(
            "link", name=re.compile(r"Account Parties", re.IGNORECASE)
        )
        wait_for_element(account_party_link)
        account_party_link.click()
        wait_for_element(self.page.get_by_role("button", name="Show Actions"))

    def delete_account_party(self):
        show_actions = self.page.get_by_role("button", name="Show Actions")
        wait_for_element(show_actions)
        while show_actions.count() > 0:
            show_actions.first.click()
            delete_menu_item = self.page.get_by_role("menuitem", name="Delete")
            wait_for_element(delete_menu_item)
            delete_menu_item.click()
            delete_button = self.page.get_by_role("button", name="Delete")
            wait_for_element(delete_button)
            delete_button.click()

    def add_account_party(self, partner_name: str):
        new_button = self.page.get_by_role("button", name="New")
        wait_for_element(new_button)
        new_button.click()
        account_box = self.page.get_by_role("combobox", name="Account")
        wait_for_element(account_box)
        account_box.click()
        account_box.fill(partner_name)
        try:
            partner_option = self.page.get_by_text(partner_name, exact=True)
            wait_for_element(partner_option)
            partner_option.click()
        except Exception:
            recent_item = self.page.get_by_label("Recent Items").get_by_title(
                partner_name
            )
            wait_for_element(recent_item)
            recent_item.click()
        role_combo = self.page.get_by_role("combobox", name="Role")
        wait_for_element(role_combo)
        role_combo.click()
        reseller_option = self.page.get_by_label("New Account Parties").get_by_text(
            "Reseller", exact=True
        )
        wait_for_element(reseller_option)
        reseller_option.click()
        save_button = self.page.get_by_role("button", name="Save", exact=True)
        wait_for_element(save_button)
        save_button.click()

    def goto_partner_tab(self):
        partner_tab = self.page.get_by_role("tab", name="Partner")
        wait_for_element(partner_tab)
        partner_tab.click()

    def update_reseller(self, partner_account: str):
        edit_reseller_btn = self.page.get_by_role(
            "button", name="Edit Reseller", exact=True
        )
        wait_for_element(edit_reseller_btn)
        edit_reseller_btn.click()
        reseller_combo = self.page.get_by_role("combobox", name="Reseller", exact=True)
        wait_for_element(reseller_combo)
        reseller_combo.press("Delete")
        reseller_combo.fill(partner_account)
        reseller_combo.press("Enter")
        account_icon = self.page.locator(
            ".slds-media__figure > .slds-icon-standard-account > span > lightning-primitive-icon > .slds-icon"
        ).first
        wait_for_element(account_icon)
        account_icon.click()
        save_button = self.page.get_by_role("button", name="Save", exact=True)
        wait_for_element(save_button)
        save_button.click()

    def editSalesPlay(self, salesplay):
        wait_for_element(self.page.get_by_role("button", name="Edit Sales Play"))
        self.page.get_by_role("button", name="Edit Sales Play").click()
        self.page.get_by_role("combobox", name="Sales Play").click()
        self.page.get_by_role("option", name=salesplay).click()
        self.page.get_by_role("button", name="Save").click()

    def editFlexpod(self, flexpod):
        wait_for_element(self.page.get_by_role("button", name="Edit Flexpod"))
        self.page.get_by_role("button", name="Edit Flexpod").click()
        wait_for_element(self.page.get_by_role("combobox", name="Flexpod"))
        self.page.get_by_role("combobox", name="Flexpod").click()
        self.page.get_by_role("option", name=flexpod, exact=True).click()
        self.page.get_by_role("button", name="Save").click()

    def selectWWSSForecastingRequest(self, option, user):
        try:
            wait_for_element(self.page.get_by_role("button", name="Show more actions"))
            self.page.get_by_role("button", name="Show more actions").click()
            self.page.get_by_role("menuitem", name="WWSS Forecasting Request").click()
            self.page.get_by_role("button", name="WWSS Deal --None--").click()
            self.page.get_by_role("option", name=option, exact=True).click()
            self.page.get_by_role("combobox", name="Service Account Executive").click()
            self.page.get_by_role("combobox", name="Service Account Executive").fill(user)
            self.page.get_by_role("option", name=user).nth(1).click()
            self.page.get_by_role("button", name="Save").click()
            self.page.get_by_role("link", name='WWSS Forecasting Request "').click()
        except Exception:
            wait_for_element(self.page.get_by_role("button", name="WWSS Forecasting Request"))
            self.page.get_by_role("button", name="WWSS Forecasting Request").click()
            self.page.get_by_role("button", name="WWSS Deal --None--").click()
            self.page.get_by_role("option", name=option, exact=True).click()
            self.page.get_by_role("combobox", name="Service Account Executive").click()
            self.page.get_by_role("combobox", name="Service Account Executive").fill(user)
            self.page.get_by_role("option", name=user).nth(1).click()
            self.page.get_by_role("button", name="Save").click()
            self.page.get_by_role(
                "heading", name='WWSS Forecasting Request "WWSS-'
            ).click()
            

    def validate_split_edit(self):
        try:
            self.page.get_by_role("button", name="Show more actions").click()
            menu_item = self.page.get_by_role(
                "menuitem", name="Edit Opportunity Splits"
            )
            wait_for_element(menu_item)
            expect(menu_item).to_be_visible()
            return True
        except Exception:
            return False

    def click_split_edit(self):
        try:
            self.page.get_by_role("button", name="Edit Opportunity Splits").click()
            time.sleep(self.nw)
            return
        except Exception:
            try:
                self.page.get_by_role("button", name="Show more actions").click()
                self.page.get_by_role(
                    "menuitem", name="Edit Opportunity Splits"
                ).click()
                time.sleep(self.nw)
                return
            except Exception as e:
                raise Exception("Unable to open Edit Opportunity Splits: %s" % e)

    def open_wwss_request(self):
        for _ in range(3):
            self.page.mouse.wheel(0, 800)
        self.page.get_by_role("link", name="Show All").click()
        request_link = self.page.get_by_role(
            "link", name=re.compile(r"WWSS Forecasting Request", re.IGNORECASE)
        )
        wait_for_element(request_link)
        request_link.click()

    def validate_wwss_actions_and_delete(self):
        self.grid = self.page.get_by_role("grid")
        self.grid.get_by_role("button", name="Show Actions").first.click()

        # Validate Edit option is visible
        expect(self.page.get_by_role("menuitem", name="Edit")).to_be_visible()

        # Validate Delete option is visible
        delete_option = self.page.get_by_role("menuitem", name="Delete")
        expect(delete_option).to_be_visible()

        # Click Delete
        delete_option.click()
        self.page.get_by_role("button", name="Delete", exact=True).click()

    def validate_prebuild_option(self):
        self.page.get_by_role("button", name="Show more actions").click()
        expect(self.page.get_by_role("menuitem", name="Prebuilds")).not_to_be_visible()

    def validatePrebuildCreation(self, quote_name: str, option: str, reason: str):
        wait_for_element(self.page.get_by_role("button", name="Show more actions"))
        self.page.get_by_role("button", name="Show more actions").click()
        self.page.get_by_role("menuitem", name="Prebuilds").click()
        self.page.get_by_role("combobox", name="Quote Help Quote").click()
        self.page.get_by_role("combobox", name="Quote Help Quote").fill(quote_name)
        self.page.get_by_role("option", name=quote_name).nth(1).click()
        self.page.get_by_role("button", name="Eligible Prebuild Quote --").click()
        self.page.get_by_role("option", name=option, exact=True).click()
        self.page.get_by_role(
            "button", name="Eligible Prebuild Quote Status --None--"
        ).click()
        self.page.get_by_role("option", name=reason).click()
        self.page.get_by_role("button", name="Save").click()

    def editPurchaseType(self, purchase_type: str):
        self.page.get_by_role("button", name="Edit Purchase Type").click()
        self.page.get_by_role("combobox", name="Purchase Type").click()
        self.page.get_by_role("option", name=purchase_type).click()
        self.page.get_by_role("button", name="Save").click()

    def validate_linked_opptyoption(self, option: str = "True"):
        label = self.page.locator("label.slds-checkbox__label").filter(
            has_text="Link Source Opportunity (Private Offer Only)"
        )
        if option == "True":
            wait_for_element(label)
            label.click()
            time.sleep(self.nw)
            return True
        else:
            expect(label).not_to_be_visible()
            return False

    def clickCopyOpportunity(self):
        try:
            self.page.get_by_role("button", name="Copy Opportunity").click()
        except Exception:
            self.page.get_by_role(
                "button", name="Show more actions", exact=True
            ).click()
            self.page.get_by_role("menuitem", name="Copy Opportunity").click()

    def clickcontinuebutton(self):
        self.page.get_by_role("button", name="Continue").click()

    def validate_linked_opty_present(self, linked_opty_name: str):
        linked_opty_link = self.page.get_by_role("link", name=linked_opty_name)
        wait_for_element(linked_opty_link)
        try: 
            expect(linked_opty_link).to_be_visible()
            return True
        except Exception:
            return False

    def configureSEValues(
        self,
        business_solution_areas: str,
        customer_workloads: str,
        ai_customer_workload: str,
        solution_protocols: str,
    ):
        wait_for_element(self.page.get_by_role("tab", name="SE"))
        self.page.get_by_role("tab", name="SE").click()
        self.page.get_by_role("button", name="Edit Customer Workloads").click()
        self.page.get_by_text(customer_workloads, exact=True).click()
        self.page.get_by_label("Customer Workloads").get_by_role(
            "button", name="Move selection to Chosen"
        ).click()
        self.page.get_by_text(solution_protocols, exact=True).click()
        self.page.get_by_label("Solution Protocols").get_by_role(
            "button", name="Move selection to Chosen"
        ).click()
        self.page.get_by_text(business_solution_areas, exact=True).click()
        self.page.get_by_label("Business Solution Areas").get_by_role(
            "button", name="Move selection to Chosen"
        ).click()
        self.page.get_by_role("combobox", name="AI Customer Workload Stage").click()
        self.page.locator("span").filter(has_text=ai_customer_workload).first.click()
        self.page.get_by_role("textbox", name="AI Customer Stage Evidence").click()
        self.page.get_by_role("textbox", name="AI Customer Stage Evidence").fill(
            ai_customer_workload
        )
        self.page.get_by_role("button", name="Save").click()

    def complete_resource_request(
        self, request_team_options, comment="test automation"
    ):
        self.page.get_by_role("button", name="Show more actions").click()
        self.page.get_by_role("menuitem", name="Request a Resource").click()
        request_team_dropdown = self.page.get_by_role("combobox", name="Request Team")
        wait_for_element(request_team_dropdown)
        request_team_dropdown.click()

        for option in request_team_options:
            expect(self.page.get_by_text(option)).to_be_visible()

        self.page.get_by_text(request_team_options[1]).click()
        self.page.locator("input[name='Requested_Activity']").click()
        self.page.locator("input[name='Requested_Activity']").fill(comment)
        self.page.get_by_role("button", name="Submit", exact=True).click()

    def validate_request_status(self, expected_status):
        time.sleep(self.sw)
        expect(self.page.get_by_text(expected_status)).to_be_visible()
        time.sleep(self.sw)

    def create_quote_request(
        self,
        subject: str,
        support_service_level: str,
        option: str,
        fpvr_required: str,
        quote_currency: str,
        renewal_term: str,
    ):
        try:
            self.page.get_by_role("button", name="Create Quote Request").click()
        except Exception:
            self.page.get_by_role("button", name="Show more actions").click()
            self.page.get_by_role("menuitem", name="Create Quote Request").click()
        self.page.locator(".slds-radio_faux").first.click()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("textbox", name="Subject").click()
        self.page.get_by_role("textbox", name="Subject").fill(subject)
        self.page.get_by_role("combobox", name="Support Service Level").click()
        self.page.get_by_text(support_service_level).click()
        self.page.get_by_role("option", name=option).click()
        self.page.get_by_role("button", name="Move selection to Chosen").click()
        self.page.get_by_label("FPVR Required?").select_option(fpvr_required)
        self.page.get_by_label("Quote Currency").select_option(quote_currency)
        self.page.get_by_label("Renewal Term Under 12 Months?").select_option(
            renewal_term
        )
        time.sleep(self.nw)
        self.page.get_by_role("button", name="Save").click()
        time.sleep(self.nw)

    def verify_sla_fields_visible(self):
        expect(self.page.get_by_text("SLA", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Revision SLA", exact=True)).to_be_visible()

    def validateSalesType(self, actual_sales_type: str, expected_sales_type: str):
        assert (
            actual_sales_type == expected_sales_type
        ), f"Sales Type mismatch: Expected '{expected_sales_type}' but got '{actual_sales_type}'"

    def editSalesType(self, sales_type: str):
        wait_for_element(self.page.get_by_role("button", name="Edit Sales Type"))
        self.page.get_by_role("button", name="Edit Sales Type").click()
        if sales_type == "Renewal":
            wait_for_element(
                self.page.get_by_role("combobox", name="Installed Base Type")
            )
            self.page.get_by_role("combobox", name="Installed Base Type").click()
            self.page.get_by_role("option", name="Service Renewal").click()
            self.page.get_by_role("combobox", name="Sales Play").click()
            self.page.get_by_role("option", name="Renew").click()
        self.page.get_by_role("combobox", name="Sales Type").click()
        self.page.get_by_role("option", name=sales_type, exact=True).click()
        self.page.get_by_role("button", name="Save").click()

    def validateErrorMessage(self, error_text: str):
        error_message = self.page.locator(".errorsList li", has_text=error_text)
        expect(error_message).to_be_visible()

    def discard_changes(self):
        self.page.get_by_role("button", name="Cancel").click()

    def validateeditoptionlocked(self, field: str):
        expect(
            self.page.get_by_role("button", name=f"Edit {field}")
        ).not_to_be_visible()

    def validate_sales_type(self, actual_sales_type: str, expected_sales_type: str):
        assert (
            actual_sales_type == expected_sales_type
        ), f"Sales Type mismatch: Expected '{expected_sales_type}' but got '{actual_sales_type}'"
