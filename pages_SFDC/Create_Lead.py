from datetime import datetime
import logging
import random
import time
from playwright.sync_api import Page, expect

logger = logging.getLogger("playwright_pytest")


class CreateLead:
    # Wait presets
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page

        # Top-level buttons
        self.btn_new = page.get_by_role("button", name="New")
        self.btn_save = page.get_by_role("button", name="Save", exact=True)

        # Salutation & name
        self.cmb_salutation = page.get_by_role("combobox", name="Salutation")
        self.txt_first_name = page.get_by_role("textbox", name="First Name", exact=True)
        self.txt_last_name = page.get_by_role("textbox", name="Last Name", exact=True)

        # Contact / Account
        self.cmb_contact = page.get_by_role("combobox", name="Contact")
        self.cmb_lead_account = page.get_by_role("combobox", name="Lead Account")

        # Company
        self.company_label = page.locator("lightning-input").filter(has_text="*Company")
        self.txt_company = page.get_by_role("textbox", name="Company", exact=True)

        # Communication
        self.txt_mobile = page.get_by_role("textbox", name="Mobile")
        self.txt_email = page.get_by_role("textbox", name="Email", exact=True)

        # Address search
        self.cmb_address_search = page.get_by_role("combobox", name="Address Search")

        # Address details
        self.cmb_country = page.get_by_role("combobox", name="Country")
        self.opt_country_us = page.get_by_text("United States", exact=True)
        self.txt_street = page.get_by_role("textbox", name="Street")
        self.txt_city = page.get_by_role("textbox", name="City")
        self.cmb_state = page.get_by_role("combobox", name="State/Province")
        self.txt_zip = page.get_by_role("textbox", name="Zip/Postal Code")

        # Meeting details
        self.grp_meeting_set_date = page.get_by_role(
            "group", name="Meeting Set Date"
        ).get_by_label("Date")
        self.grp_meeting_set_time = page.get_by_role(
            "group", name="Meeting Set Date"
        ).get_by_label("Time")
        self.cmb_meeting_type = page.locator(
            "button[role='combobox'][aria-label='Meeting Type'][data-value='--None--']"
        )
        self.txt_qualification_criteria = page.get_by_role(
            "textbox", name="Qualification Criteria"
        )
        self.txt_meeting_link = page.get_by_role("textbox", name="Zoom/Teams Link")
        self.cmb_meeting_category = page.locator(
            "button[role='combobox'][aria-label='Meeting Category'][data-value='--None--']"
        )

        # Product
        self.cmb_product = page.get_by_role("combobox", name="Product", exact=True)

    def createNewLead(
        self,
        salutation,
        contact,
        lead,
        company,
        mobile,
        address,
        street,
        city,
        zip_code,
        meeting_type,
        criteria,
        link,
        product,
        meeting_category,
    ):
        # New
        self.btn_new.click()
        self.fill_personal_details(salutation, contact, lead, company, mobile)
        logger.info("Personal details filled")

        self.fill_address_details(address, street, city, zip_code)
        logger.info("Address details filled")

        self.fill_meeting_details(
            meeting_type, criteria, link, product, meeting_category
        )
        logger.info("Meeting details filled")

        # Save
        self.btn_save.click()
        time.sleep(self.nw)

    def fill_personal_details(self, salutation, contact, lead, company, mobile):
        self.cmb_salutation.click()
        self.page.get_by_text(salutation, exact=True).click()

        self.txt_first_name.click()
        self.txt_first_name.fill(contact)

        self.txt_last_name.click()
        random_last_name = f"User_{random.randint(10000, 99999)}"
        self.txt_last_name.fill(random_last_name)

        # Contact / Account
        self.cmb_contact.click()
        self.cmb_contact.fill(contact)
        self.cmb_contact.click()
        self.page.get_by_role("option", name=contact).nth(1).wait_for(state="visible")
        self.page.get_by_role("option", name=contact).nth(1).click()

        self.cmb_lead_account.click()
        self.cmb_lead_account.fill(lead)
        self.page.get_by_role("option", name="Search Show more results for").locator(
            "svg"
        ).click()
        self.page.locator(
            "//tr[1]/td[1]/lightning-primitive-cell-checkbox/span/label/span[1]"
        ).click()
        self.page.get_by_role("button", name="Select").click()

        # Company
        self.company_label.click()
        self.txt_company.fill(company)

        # Communication
        self.txt_mobile.click()
        self.txt_mobile.fill(str(mobile))

        random_email = f"user_{random.randint(10000, 99999)}@netapp.com"
        self.txt_email.click()
        self.txt_email.fill(random_email)

    def fill_address_details(self, address, street, city, zip_code):
        # Address search (type + defocus)
        self.cmb_address_search.click()
        self.cmb_address_search.fill(address)

        # Address details
        self.cmb_country.click()
        self.opt_country_us.click()

        self.txt_street.click()
        self.txt_street.fill(street)

        self.txt_city.click()
        self.txt_city.fill(city)

        self.cmb_state.click()
        self.page.get_by_text(city).click()

        self.txt_zip.click()
        self.txt_zip.fill(str(zip_code))

    def fill_meeting_details(
        self, meeting_type, criteria, link, product, meeting_category
    ):
        # Meeting
        # NOTE: On Windows, %#m/%#d/%Y is OK; on Linux/macOS use %-m/%-d/%Y
        try:
            self.grp_meeting_set_date.fill(datetime.now().strftime("%#m/%#d/%Y"))
        except ValueError:
            self.grp_meeting_set_date.fill(datetime.now().strftime("%-m/%-d/%Y"))

        self.grp_meeting_set_time.click()

        # Meeting Type
        self.cmb_meeting_type.scroll_into_view_if_needed()
        self.cmb_meeting_type.click()
        self.page.get_by_text(meeting_type).click()

        self.txt_qualification_criteria.fill(criteria)
        self.txt_meeting_link.click()
        self.txt_meeting_link.fill(link)

        # Product
        self.cmb_product.click()
        self.cmb_product.fill(product)
        self.cmb_product.click()
        self.page.get_by_role("option", name=product).nth(1).wait_for(state="visible")
        self.page.get_by_role("option", name=product).nth(1).click()

        # Meeting category
        self.cmb_meeting_category.scroll_into_view_if_needed()
        self.cmb_meeting_category.click()
        self.page.get_by_role("option", name=meeting_category).click()
