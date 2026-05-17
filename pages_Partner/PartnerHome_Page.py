from playwright.sync_api import Page, expect
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import time
import json

from utils.utils import wait_for_element


class PartnerHomePage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.selling = page.locator("//button[@title='Selling']")
        self.quoteConsole = page.locator("//a[@title='Quote Console']")
        self.popUp_1 = page.locator('//*[@id="84d92fcc-879d-def6-de3b-698f1462f805"]')
        self.pouUp_2 = page.locator(
            '//*[@id="border-aacd52ca-ab86-bc6b-7e1d-5646f3a53ae8"]'
        )

    def navigateToQuoteConsole(self):
        wait_for_element(self.selling)
        self.selling.click()
        self.quoteConsole.click()

    def handle_popup_1(self, max_wait_seconds: int = 30):
        end_time = time.time() + max_wait_seconds
        while time.time() < end_time:
            if self.popUp_1.is_visible():
                self.popUp_1.click()
                break
            time.sleep(0.5)  # poll every 0.5s

    def handle_popup_2(self, max_wait_seconds: int = 30):
        end_time = time.time() + max_wait_seconds
        while time.time() < end_time:
            if self.pouUp_2.is_visible():
                self.pouUp_2.click()
                break
            time.sleep(0.5)  # poll every 0.5s
