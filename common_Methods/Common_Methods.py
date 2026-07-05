import logging
from socket import timeout
import time
from time import sleep
from playwright.sync_api import (
    Page,
    BrowserContext,
    TimeoutError as PlaywrightTimeoutError,
)
from utils.locator_manager import LocatorManager

logger = logging.getLogger("playwright_pytest")

"""
#======Below Generic Common Methods are available in this class======================================
getElement, enterText, clickElement, clickElementAndWait, isElementVisible, readText, selectOptionInListbox,
clickElementsInSequence, verifyElementStatus, closePopUp, getCurrentURL, navigateToUrl,
switchToTab, closeTab, assertTrue, assertAll
#====================================================================================================
"""


class CommonMethods:
    nw = 3

    def __init__(self, page: Page, locator_manager: LocatorManager):
        self.page = page
        self.locator_manager = locator_manager
        self.errors = []

    def getElement(self, locator, timeout: int = 60000):
        """
        Resolves the locator to a Playwright element.
        :param locator: The locator object or string.
        :param timeout: Timeout in milliseconds to wait for the element (default is 60000 ms).
        :return: The Playwright element.
        """
        if isinstance(locator, dict):
            if "role" in locator and "name" in locator:
                return self.page.get_by_role(locator["role"], name=locator["name"])
            elif "text" in locator:
                return self.page.get_by_text(locator["text"])
            elif "label" in locator:
                return self.page.get_by_label(locator["label"])
            elif "placeholder" in locator:
                return self.page.get_by_placeholder(locator["placeholder"])
            elif "alt_text" in locator:
                return self.page.get_by_alt_text(locator["alt_text"])
            elif "title" in locator:
                return self.page.get_by_title(locator["title"])
            elif "test_id" in locator:
                return self.page.get_by_test_id(locator["test_id"])
            else:
                raise Exception(f"Unsupported locator type in {locator}")
        else:
            # Handle XPath or CSS selectors
            self.page.wait_for_selector(locator, timeout=timeout)
            return self.page.locator(locator)

    def enterText(
        self,
        page_name: str,
        element_name: str,
        text: str,
        clear_first: bool = True,
        timeout: int = 60000,
    ):
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            if clear_first:
                element.fill("")  # Clear field
            element.fill(text)
        except Exception as e:
            raise Exception(
                f"Failed to enter text '{text}' in the field '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def enterTextAndWait(
        self,
        page_name: str,
        element_name: str,
        text: str,
        wait_time: int,
        clear_first: bool = True,
        timeout: int = 60000,
    ):
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            if clear_first:
                element.fill("")  # Clear field
            element.fill(text)
            time.sleep(wait_time)
        except Exception as e:
            raise Exception(
                f"Failed to enter text '{text}' in the field '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def clickElement(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ):
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.click()
        except Exception as e:
            raise Exception(
                f"Failed to click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def clickElementAndWait(
        self,
        page_name: str,
        element_name: str,
        wait_time: int,
        timeout: int = 60000,
    ):
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.click()
            time.sleep(wait_time)
        except Exception as e:
            raise Exception(
                f"Failed to click on element '{element_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def isElementVisible(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            return element.is_visible()
        except Exception as e:
            raise Exception(
                f"Failed to check visibility of element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def readText(self, page_name: str, element_name: str, timeout: int = 60000) -> str:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            if not element.is_visible():
                raise Exception(
                    f"Element '{element_name}' is not visible on page '{page_name}'."
                )
            text_content = element.text_content()
            if text_content is None:
                raise Exception(
                    f"Failed to read text from element '{element_name}' on page '{page_name}'."
                )
            return text_content.strip()
        except Exception as e:
            raise Exception(
                f"Failed to read text from element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def selectOptionInListbox(
        self,
        page_name: str,
        element_name: str,
        option_value: str,
        timeout: int = 60000,
    ) -> None:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.wait_for(state="visible", timeout=timeout)
            element.select_option(value=option_value)
        except Exception as e:
            raise Exception(
                f"Failed to select option '{option_value}' in listbox '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def clickElementsInSequence(self, locators: list, timeout: int = 60000) -> None:
        try:
            for locator in locators:
                element = self.getElement(locator, timeout)
                element.wait_for(state="visible", timeout=timeout)
                element.click()
                logger.info(f"Clicked element: {locator}")
        except Exception as e:
            raise Exception(f"Failed to click elements in sequence. Error: {e}")

    def verifyElementStatus(
        self,
        page_name: str,
        element_name: str,
        expected_status: str,
        timeout: int = 60000,
    ) -> bool:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.wait_for(state="visible", timeout=timeout)
            actual_status = element.inner_text().strip().lower()
            expected_status = expected_status.strip().lower()
            if actual_status == expected_status:
                logger.info(
                    f"Element '{element_name}' status is in expected state: {actual_status}"
                )
                return True
            else:
                logger.warning(
                    f"Element '{element_name}' status is not in expected state. Current status: {actual_status}"
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to verify status of element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def closePopUp(
        self, page_name: str, element_name: str, timeout: int = 60000
    ) -> None:
        """
        Closes a popup if it becomes visible within the specified timeout.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the popup element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the popup to become visible (default is 60000 ms).
        """
        try:
            locator = self.locator_manager.get_locator(page_name, element_name)
            popup_element = self.page.locator(locator)
            popup_element.wait_for(state="visible", timeout=timeout)
            popup_element.click()
        except PlaywrightTimeoutError:
            logger.warning(
                f"Timeout while waiting for the popup: {element_name} to be visible."
            )
        except Exception as e:
            logger.error(
                f"An error occurred while closing the popup: {element_name}. Error: {e}"
            )

    def getCurrentURL(self) -> str:
        """
        Fetches the current URL of the page.
        :return: The current URL of the page as a string.
        """
        try:
            current_url = self.page.url
            return current_url
        except Exception as e:
            raise Exception(f"Failed to fetch the current URL. Error: {e}")

    def navigateToUrl(self, url: str, timeout: int = 60000) -> None:
        """
        Navigates to the specified URL.
        Args:
            url (str): The URL to navigate to.
            timeout (int): Timeout in milliseconds to wait for the navigation to complete (default is 60000 ms).
        """
        try:
            self.page.goto(url, timeout=timeout)
        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout navigating to URL: {url}. Error: {e}")
            raise Exception(
                f"Failed to navigate to URL: {url} within {timeout} ms. Error: {e}"
            )
        except Exception as e:
            logger.error(
                f"An error occurred while navigating to URL: {url}. Error: {e}"
            )
            raise Exception(f"Failed to navigate to URL: {url}. Error: {e}")

    def switchToTab(
        self,
        context: BrowserContext,
        tab_index: int,
        expected_tab_count: int,
        timeout: int = 20000,
    ) -> Page:
        """
        Validate the number of tabs and switch to the specified tab index.
        Args:
            context (BrowserContext): The browser context containing the tabs.
            tab_index (int): The index of the tab to switch to (starts at 0).
            expected_tab_count (int): The expected total number of tabs open after an action.
            timeout (int): The maximum time to wait for the new tab to open (in milliseconds).
        Returns:
            Page: The page object of the tab at the specified index.
        Raises:
            Exception: If the expected number of tabs is not met or the tab index is out of range.
        """
        current_tab_count = len(context.pages)
        logger.info(f"Current number of tabs: {current_tab_count}")
        # Wait for a new tab only if the expected tab count is greater than the current tab count
        if expected_tab_count > current_tab_count:
            try:
                logger.info(
                    f"Waiting for a new tab to open, expecting {expected_tab_count} tabs."
                )
                context.wait_for_event("page", timeout=timeout)
            except TimeoutError:
                logger.error(
                    f"Timeout waiting for new tab. Expected at least {expected_tab_count} tabs, but only {current_tab_count} tabs are open."
                )
                raise Exception(
                    f"Failed to open new tab within {timeout} ms. Expected {expected_tab_count} tabs, but only {current_tab_count} tabs are open."
                )

            # Update the current tab count after waiting
            current_tab_count = len(context.pages)
            logger.info(f"Updated number of tabs: {current_tab_count}")
        # Validate the total number of tabs
        if current_tab_count >= expected_tab_count:
            logger.info(f"Switching to tab index {tab_index}")
            pages = context.pages
            if tab_index < len(pages):
                target_page = pages[tab_index]
                # Bring the tab to the foreground
                target_page.bring_to_front()
                return target_page
            else:
                logger.error(
                    f"Tab index {tab_index} out of range. There are only {len(pages)} tabs open."
                )
                raise IndexError(
                    f"Tab index {tab_index} out of range. There are only {len(pages)} tabs open."
                )
        else:
            logger.error(
                f"Expected at least {expected_tab_count} tabs, but only {current_tab_count} tabs are open."
            )
            raise Exception(
                f"Failed to open new tab. Expected {expected_tab_count} tabs, but only {current_tab_count} tabs are open."
            )

    def closeTab(self, context: BrowserContext, tab_index: int) -> None:
        """
        Close the tab at the specified index.
        Args:
        context (BrowserContext): The browser context containing the tabs.
        tab_index (int): The index of the tab to close (starts at 0).
        Raises:
        IndexError: If the tab index is out of range.
        """
        pages = context.pages
        logger.info(
            f"Attempting to close tab at index {tab_index}. Total tabs open: {len(pages)}"
        )
        # Validate the tab index
        if tab_index < len(pages):
            target_page = pages[tab_index]
            target_page.close()
            logger.info(f"Tab at index {tab_index} has been successfully closed.")
        else:
            logger.error(
                f"Tab index {tab_index} out of range. There are only {len(pages)} tabs open."
            )
            raise IndexError(
                f"Tab index {tab_index} out of range. There are only {len(pages)} tabs open."
            )

    def assertTrue(self, condition, message):
        if not condition:
            self.errors.append(message)

    def assertAll(self):
        if self.errors:
            raise AssertionError("\n".join(self.errors))

    def compareExpectedActualText(
        self,
        actual_text: str,
        expected_text: str,
    ) -> None:
        try:
            if not expected_text:
                raise ValueError("Expected text is invalid or missing.")
            if expected_text == actual_text:
                logger.info(f"Expected text is displayed: {expected_text}")
            else:
                logger.warning(
                    f"Expected text does not match. "
                    f"Expected: '{expected_text}', Actual: '{actual_text}'"
                )
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
        except Exception as e:
            logger.error(f"An error occurred during text comparison: {e}")

    def checkExpectedTextInActual(
        self,
        actual_text: str,
        expected_text: str,
    ) -> None:
        try:
            if not expected_text:
                raise ValueError("Expected text is invalid or missing.")
            if expected_text in actual_text:
                logger.info(f"Expected text is found in actual text: {expected_text}")
            else:
                logger.warning(
                    f"Expected text is NOT found in actual text. "
                    f"Expected substring: '{expected_text}', Actual: '{actual_text}'"
                )
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
        except Exception as e:
            logger.error(f"An error occurred during text comparison: {e}")

    def waitForStable(self, seconds: int = 3):
        logger.info(f"Waiting for {seconds} seconds to ensure application stability...")
        sleep(seconds)
