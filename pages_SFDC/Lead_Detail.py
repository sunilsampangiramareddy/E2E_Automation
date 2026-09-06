import re
import time
from playwright.sync_api import Page, expect

from utils.utils import wait_for_element


class LeadDetail:
    # wait presets
    nw = 2
    sw = 5
    mw = 10
    lw = 20
    hw = 30

    def __init__(self, page: Page):
        self.page = page
        self.converted_status = page.get_by_title("Converted")
        self.select_converted_button = page.locator("button").filter(
            has_text="Select Converted Status"
        )
        self.status_dropdown = page.get_by_label("Status*")
        self.save_status = page.get_by_role("button", name="Save")
        self.lead_heading = page.locator(
            "lightning-formatted-name[slot='primaryField']"
        )
        self.opportunity_field = page.locator(
            '[data-field-id="RecordConverted_Opportunity_ID_cField"]'
        )
        self.opportunity_name = self.opportunity_field.locator("a")

    def capture_Existing_Lead_Name(self, row_index: int = 0) -> str:
        wait_for_element(self.page.locator('th[data-label="Name"] a').nth(row_index))
        lead_cell = self.page.locator('th[data-label="Name"] a').nth(row_index)
        name = lead_cell.get_attribute("title")
        return name.strip() 

    def verify_Campaign_Association_Removed(self, campaign_name: str) -> bool: 
        # wait_for_element(self.page.get_by_role("link", name=campaign_name))
        campaign_link = self.page.get_by_role("link", name=campaign_name)
        # assert campaign_link.count() == 0, f"Campaign {campaign_name} is still associated with the lead"
        if campaign_link.count() == 0:
            return True
        else:
            return False
