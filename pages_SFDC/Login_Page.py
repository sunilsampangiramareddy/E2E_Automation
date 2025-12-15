from playwright.sync_api import Page, expect
import time

class LoginPage:
    nw=3; sw=5; mw=10; lw=20

    def __init__(self, page: Page):
        self.page = page
        self.usernameInput = page.get_by_role("textbox", name="Email Address")
        self.nextButton = page.get_by_role("button", name="Next")
        self.passwordInput = page.get_by_role("textbox", name="Enter the password for")
        self.signinButton = page.get_by_role("button", name="Sign in")
        self.yesButton = page.get_by_role("button", name="Yes")

    def enterUserName(self, username: str):
        expect(self.usernameInput).to_be_visible()
        self.usernameInput.fill(username)
        time.sleep(self.nw) 
        
    def clickNextButton(self):
        expect(self.nextButton).to_be_visible()
        self.nextButton.click()
        time.sleep(self.sw) 
        
    def enterPassword(self, password: str):
        expect(self.passwordInput).to_be_visible()
        self.passwordInput.fill(password)
        time.sleep(self.nw) 
        
    def clickSigninButton(self):
        expect(self.signinButton).to_be_visible()
        self.signinButton.click()
        time.sleep(self.sw) 
        
    def clickYesButton(self):
        expect(self.yesButton).to_be_visible()
        self.yesButton.click()
        time.sleep(self.lw)  
