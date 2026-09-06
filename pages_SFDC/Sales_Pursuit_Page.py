from playwright.sync_api import Page, expect
import re
import time
from utils.utils import wait_for_element


class SalesPursuitPage:

    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page

    def selectOpportunity(self, opptynumber):
        wait_for_element(self.page.get_by_role("combobox", name="Select Opportunity"))
        self.page.get_by_role("combobox", name="Select Opportunity").click()
        self.page.get_by_title(opptynumber, exact=True).click()
        self.page.get_by_role("button", name="Save").click()
