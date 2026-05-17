from playwright.sync_api import Page, expect
import time
import json

from utils.utils import wait_for_element


class PartnerLoginPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("//*[@id='signInName']")
        self.next_button = page.locator('//*[@id="next"]')
        self.enter_OTP = page.locator('//*[@id="verificationCode"]')
        self.continue_button = page.locator(
            '//*[@id="emailVerificationControl-Verify_but_verify_code"]'
        )
        self.home_page_label = page.locator("//a[@title='Home']")

    def navigateToUrl(self, url):
        self.page.goto(url)
        time.sleep(self.sw)

    def getCurrentURL(self):
        current_url = self.page.url
        return current_url

    def enterUserName(self, username: str):
        wait_for_element(self.username_input)
        self.username_input.fill(username)

    def clickNextButton(self):
        wait_for_element(self.next_button)
        self.next_button.click()
        time.sleep(self.lw)
        time.sleep(self.lw)

    def enterOTP(self, otp: str):
        wait_for_element(self.enter_OTP)
        self.enter_OTP.click()
        self.enter_OTP.fill(otp)

    def clickContinueButton(self):
        wait_for_element(self.continue_button)
        self.continue_button.click()

    def isHomeLabelDisplayed(self):
        wait_for_element(self.home_page_label)
        expect(self.home_page_label).to_be_visible()
        return self.home_page_label.is_visible()
