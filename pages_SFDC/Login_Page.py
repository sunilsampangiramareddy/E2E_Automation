from asyncio.log import logger

from playwright.sync_api import Page, expect
import time
import json
from utils.utils import wait_for_element


class LoginPage:
    nw = 3
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page, locators_file: str = "locators/locators.json"):
        self.page = page
        with open(locators_file, "r") as file:
            locators = json.load(file)["LoginPage"]

        self.usernameInput = page.locator(locators["username_Input"])
        self.nextButton = page.get_by_role(**locators["next_Button"])
        self.passwordInput = page.get_by_role(**locators["password_Input"])
        self.signinButton = page.get_by_role(**locators["signin_Button"])
        self.yesButton = page.get_by_role(**locators["yes_Button"])

    def enterUserName(self, username: str):
        wait_for_element(self.usernameInput)
        self.usernameInput.fill(username)

    def clickNextButton(self):
        wait_for_element(self.nextButton)
        self.nextButton.click()

    def enterPassword(self, password: str):
        wait_for_element(self.passwordInput)
        self.passwordInput.fill(password)

    def clickSigninButton(self):
        wait_for_element(self.signinButton)
        self.signinButton.click()

    def clickYesButton(self):
        self.yesButton.wait_for(state="visible", timeout=5000)
        # wait_for_element(self.yesButton)
        self.yesButton.click()
