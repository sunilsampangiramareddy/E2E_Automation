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

        self.username_input = page.locator(locators["usernameInput"])
        self.next_button = page.get_by_role(**locators["nextButton"])
        self.password_input = page.get_by_role(**locators["passwordInput"])
        self.signin_button = page.get_by_role(**locators["signinButton"])
        self.yes_button = page.get_by_role(**locators["yesButton"])

    def enterUserName(self, username: str):
        wait_for_element(self.username_input)
        self.username_input.fill(username)

    def clickNextButton(self):
        wait_for_element(self.next_button)
        self.next_button.click()

    def enterPassword(self, password: str):
        wait_for_element(self.password_input)
        self.password_input.fill(password)

    def clickSigninButton(self):
        wait_for_element(self.signin_button)
        self.signin_button.click()

    def clickYesButton(self):
        self.yes_button.wait_for(state="visible", timeout=5000)
        # wait_for_element(self.yes_button)
        self.yes_button.click()
