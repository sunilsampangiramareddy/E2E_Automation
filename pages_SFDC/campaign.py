from playwright.sync_api import Page, expect

from utils.utils import wait_for_element


class Campaign:
    def __init__(self, page: Page):
        self.page = page

    def select_User_Persona(self, contact: str):
        self.page.locator("a[role='option']").filter(has_text=contact).nth(1).click()

    def capture_Existing_Campaign_Name(self, row_index: int = 0) -> str:
        wait_for_element(self.page.locator('th[data-label="Campaign Name"] a').nth(row_index))
        campaign_cell = self.page.locator('th[data-label="Campaign Name"] a').nth(row_index)
        name = campaign_cell.get_attribute("title")
        return name.strip()
    
    def verify_Lead_Association_With_Campaign(self, lead_name: str):
        # wait_for_element(self.page.get_by_role("tab", name="Related"))
        # self.page.get_by_role("tab", name="Related").click()
        expect(self.page.get_by_role("link", name=lead_name).first).to_be_visible()

    def remove_Association(self):
        wait_for_element(self.page.locator('article[aria-label="Campaign Members"]').first)
        campaign_members_card = self.page.locator('article[aria-label="Campaign Members"]').first
        wait_for_element(campaign_members_card.get_by_role("button", name="Show Actions").first)
        campaign_members_card.get_by_role("button", name="Show Actions").first.click()
        wait_for_element(self.page.get_by_role("menuitem", name="Delete"))
        self.page.get_by_role("menuitem", name="Delete").click()
        wait_for_element(self.page.get_by_role("button", name="Delete"))
        self.page.get_by_role("button", name="Delete").click()