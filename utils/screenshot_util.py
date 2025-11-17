import os
from datetime import datetime
from playwright.sync_api import Page

class ScreenshotUtil:
    def __init__(self, page: Page):
        self.page = page
        self.screenshots_dir = 'C:\Automation_Project\E2E_Automation\screenshots'  # Specify your desired path here
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def capture_screenshot(self, test_name: str) -> str:
        """
        Capture a screenshot using the given Playwright Page instance.

        :param test_name: The name of the test.
        :return: The path to the saved screenshot.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_path = os.path.join(self.screenshots_dir, f'{test_name}_{timestamp}.png')
        self.page.screenshot(path=screenshot_path)
        return screenshot_path
