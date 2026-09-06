import logging
import os
from socket import timeout
import time
from time import sleep
from typing import Literal
import random
import string
from datetime import datetime
from typing import Union
from playwright.sync_api import (  # type: ignore
    Page,
    Frame,
    BrowserContext,
    TimeoutError as PlaywrightTimeoutError,
)
from utils.locator_manager import LocatorManager

logger = logging.getLogger("playwright_pytest")

"""
#======Below Generic Common Methods are available in this class============================================================================
getElement, enterText, enterTextAndWait, appendText, clearText, enterNumber, pressKey, pressEnter, pressTab, clickElement, 
clickElementAndWait, clickElementsInSequence, doubleClickElement, doubleClickElementAndWait, rightClick, validateElementCount, 
scrollToElement, scrollToTop, scrollToBottom, scrollAndClick,scrollAndForceClick, focusAndClick, forceClick, clickByText,
clickByTextAndWait, clickByTextByPosition, clickByTextByPositionAndWait, clickByLinkText, clickByLinkTextAndWait,
clickElementByPosition, clickElementByPositionAndWait, hoverOverElement, readText, readTextAndWait, 
getInputValue, getInnerText, getCSSValue, getInnerHTML, readDisabledFieldText, selectOptionInListbox, selectOptionInListboxAndWait, 
selectDropdownByText, selectDropdownByTextAndWait, selectDropdownByValue, selectDropdownByValueAndWait, selectDropdownByIndex, 
selectDropdownByIndexAndWait, getDropdownOptions, getDropdownSelectedOption, assertSelectedDropdownText, selectComboboxOption, 
selectComboboxOptionAndWait, selectComboboxOptionByPosition, selectComboboxOptionByPositionAndWait, checkCheckbox, uncheckCheckbox, 
toggle, selectRadioButtonOption, verifyRadioButtonOption, verifyElementStatus, waitForElementState, getElementAttribute, 
closePopUp, handlePopUp, acceptPopUp, dismissPopUp, getPopUpText, switchToFrame, switchToFrameByName, switchToFrameByIndex, 
switchToMainFrame, switchToParentFrame, getCurrentURL, navigateToUrl, refreshPage, goBack, goForward, maximizeWindow, 
waitForPageLoad, waitForURLChange, getPageTitle, clearCookies, captureTabCount, switchToTab, switchToFirstTab, 
switchToLastTab, closeTab, closeOtherTabs, closeCurrentTabAndSwitchToPreviousTab, captureWindowCount, switchToWindow, 
switchToOriginalWindow, closeWindowByIndex, assertTrue, assertAll, isElementVisible, isElementVisibleInSequence, 
isElementNotVisible, isElementHidden, isElementEnabled, isElementDisabled, isElementEditable, isElementChecked, 
isElementSelected, isElementPresent, compareExpectedActualText, checkExpectedTextInActual, assertText, assertContainsText, 
assertExpectedActualText, assertExpectedInActualText, assertAttribute, assertTitle, waitForStable, uploadFile, 
uploadMultipleFiles, downloadFile, dragAndDrop, takeScreenshot, takeElementScreenshot, getTableRowCount, 
getTableColumnCount, getTableCellValue, clickTableCell, doubleClickTableCell, enterTextInTableCell, searchTextInTable, 
generateRandomString, generateRandomNumber, generateRandomEmail, generateRandomAlphanumeric, generateDate, 
generateTimestamp, moveMouse, mouseClick,mouseWheelToElement, mouseWheelAndClickElement, mouseWheelAndDoubleClickElement, 
mouseWheelAndClickByText, mouseWheelAndEnterText, mouseWheelToTop, mouseWheelToBottom, convertStringToInt, 
convertStringToDouble, convertIntToString, convertDoubleToString, convertDoubleToInt
#==========================================================================================================================================
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

    def appendText(
        self, page_name: str, element_name: str, text: str, timeout: int = 60000
    ) -> bool:
        """
        Appends text to an existing value in an input field.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to append the text to.
            text (str): The text to append.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the text is appended successfully.
        Raises:
            Exception: If the append text action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Append the text to the existing value in the input field
            existing_text = element.input_value()
            element.fill(existing_text + text)
            logger.info(
                f"Successfully appended text '{text}' to element '{element_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to append text '{text}' to element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to append text '{text}' to element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def clearText(
        self, page_name: str, element_name: str, timeout: int = 60000
    ) -> bool:
        """
        Clears text from an input field.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to clear the text from.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the text is cleared successfully.
        Raises:
            Exception: If the clear text action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Clear the text in the input field
            element.fill("")
            logger.info(
                f"Successfully cleared text from element '{element_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to clear text from element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to clear text from element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def enterNumber(
        self,
        page_name: str,
        element_name: str,
        number: float,
        clear_first: bool = True,
        timeout: int = 60000,
    ) -> bool:
        """
        Enters a number (int, float, or double) into a specified input field.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to enter the number into.
            number (float): The number to enter into the input field.
            clear_first (bool): Whether to clear existing text before entering the number (default is True).
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the number is entered successfully.
        Raises:
            Exception: If entering the number fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Clear the element text if required
            if clear_first:
                element.fill("")
            # Enter the number
            element.fill(str(number))
            logger.info(
                f"Successfully entered number '{number}' in element '{element_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to enter number '{number}' in element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to enter number '{number}' in element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def pressKey(
        self, page_name: str, element_name: str, key: str, timeout: int = 60000
    ):
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Focus on the element
            element.focus()
            # Press the specified key
            element.press(key)
            logger.info(
                f"Successfully pressed key '{key}' on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to press key '{key}' on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to press key '{key}' on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def pressEnter(self, page_name: str, element_name: str, timeout: int = 60000):
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Focus on the element
            element.focus()
            # Press the Enter key
            element.press("Enter")
            logger.info(
                f"Successfully pressed the Enter key on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to press the Enter key on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to press the Enter key on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def pressTab(self, page_name: str, element_name: str, timeout: int = 60000):
        """
        Presses the Tab key on a specific element.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the Tab key press action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Focus on the element
            element.focus()
            # Press the Tab key
            element.press("Tab")
            logger.info(
                f"Successfully pressed the Tab key on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to press the Tab key on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to press the Tab key on element '{element_name}' on page '{page_name}'. Error: {e}"
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

    def clickElementsInSequence(
        self, page_name: str, locators: list, timeout: int = 60000
    ) -> None:
        try:
            for locator in locators:
                locator = self.locator_manager.get_locator(page_name, locator)
                element = self.getElement(locator, timeout)
                element.wait_for(state="visible", timeout=timeout)
                element.click()
                logger.info(f"Clicked element: {locator}")
        except Exception as e:
            raise Exception(f"Failed to click elements in sequence. Error: {e}")

    def doubleClickElement(
        self, page_name: str, element_name: str, timeout: int = 60000
    ):
        """
        Double-clicks on an element.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the double-click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Perform the double-click action
            element.dblclick()
            logger.info(
                f"Successfully double-clicked on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to double-click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to double-click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def doubleClickElementAndWait(
        self, page_name: str, element_name: str, wait_time: int, timeout: int = 60000
    ):
        """
        Double-clicks on an element and waits for a specified amount of time.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            wait_time (int): Time in seconds to wait after double-clicking the element.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the double-click action or waiting fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Perform the double-click action
            element.dblclick()
            logger.info(
                f"Successfully double-clicked on element '{element_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(
                f"Waited for {wait_time} seconds after double-clicking on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to double-click on element '{element_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )
            raise Exception(
                f"Failed to double-click on element '{element_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def rightClick(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> None:
        """
        Performs a right-click (context click) on a specific element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to right-click.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the right-click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.click(button="right")
            logger.info(
                f"Successfully performed right-click on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to perform right-click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to perform right-click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def validateElementCount(
        self,
        page_name: str,
        element_name: str,
        expected_count: int,
        timeout: int = 60000,
    ) -> bool:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            elements = self.page.locator(locator)
            actual_count = elements.count()
            if actual_count == expected_count:
                logger.info(
                    f"Element count matches for '{element_name}' on page '{page_name}'. Expected: {expected_count}, Actual: {actual_count}"
                )
                return True
            else:
                logger.warning(
                    f"Element count mismatch for '{element_name}' on page '{page_name}'. Expected: {expected_count}, Actual: {actual_count}"
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to validate element count for '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def scrollToElement(
        self, page_name: str, element_name: str, timeout: int = 60000
    ) -> bool:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.scroll_into_view_if_needed()
            return True
        except Exception as e:
            logger.error(
                f"Failed to scroll to element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def scrollToTop(self) -> bool:
        """
        Scrolls the page to the top.
        Returns:
            bool: True if the scroll action is successful, False otherwise.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to scroll to the top.")
            # Scroll to the top of the page using JavaScript
            self.page.evaluate("window.scrollTo(0, 0);")
            logger.info("Successfully scrolled to the top of the page.")
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to scroll to the top of the page. Error: {e}")
            return False

    def scrollToBottom(self) -> bool:
        """
        Scrolls the page to the bottom.
        Returns:
            bool: True if the scroll action is successful, False otherwise.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError(
                    "self.page must be a Page object to scroll to the bottom."
                )
            # Scroll to the bottom of the page using JavaScript
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("Successfully scrolled to the bottom of the page.")
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to scroll to the bottom of the page. Error: {e}")
            return False

    def scrollAndClick(self, page_name: str, element_name: str, timeout: int = 60000):
        """
        Scrolls to an element and clicks it.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the scroll or click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            element.click()
            logger.info(
                f"Successfully scrolled and clicked on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to scroll and click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to scroll and click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def scrollAndForceClick(
        self, page_name: str, element_name: str, timeout: int = 60000
    ):
        """
        Scrolls to an element and performs a force click on it.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the scroll or force click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Perform a force click
            element.click(force=True)
            logger.info(
                f"Successfully scrolled and performed a force click on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to scroll and perform a force click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to scroll and perform a force click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def focusAndClick(self, page_name: str, element_name: str, timeout: int = 60000):
        """
        Focuses on an element and clicks it.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the focus or click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Focus on the element
            element.focus()
            # Click the element
            element.click()
            logger.info(
                f"Successfully focused and clicked on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to focus and click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to focus and click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def forceClick(self, page_name: str, element_name: str, timeout: int = 60000):
        """
        Performs a force click on an element.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Raises:
            Exception: If the force click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Perform a force click
            element.click(force=True)
            logger.info(
                f"Successfully performed a force click on element '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to perform a force click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to perform a force click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def clickByText(self, text: str, timeout: int = 60000) -> bool:
        """
        Clicks on an element containing the specified text.
        Args:
            text (str): The text to locate the element by.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is clicked successfully.
        Raises:
            Exception: If the element is not found or the click operation fails.
        """
        try:
            # Locate the element containing the specified text
            element = self.page.get_by_text(text, exact=True)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Scroll the element into view if necessary
            element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            element.click()
            logger.info(
                f"Successfully clicked on the element containing text: '{text}'."
            )
            return True
        except PlaywrightTimeoutError:
            error_message = (
                f"Timeout while waiting for the element containing text: '{text}'."
            )
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = (
                f"Failed to click on the element containing text: '{text}'. Error: {e}"
            )
            logger.error(error_message)
            raise Exception(error_message)

    def clickByTextAndWait(
        self, text: str, wait_time: int, timeout: int = 60000
    ) -> bool:
        """
        Clicks on an element containing the specified text and waits for a given time.
        Args:
            text (str): The text of the element to locate and click.
            wait_time (int): The time (in seconds) to wait after clicking the element.
            timeout (int): The timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is clicked and the wait is successful.
        Raises:
            Exception: If the element is not found or the click operation fails.
        """
        try:
            # Locate the element containing the specified text
            element = self.page.get_by_text(text, exact=True)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Scroll the element into view if necessary
            element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            element.click()
            logger.info(
                f"Successfully clicked on the element containing text: '{text}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(f"Waited for {wait_time} seconds after clicking the element.")
            return True
        except PlaywrightTimeoutError:
            error_message = (
                f"Timeout while waiting for the element containing text: '{text}'."
            )
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = (
                f"Failed to click on the element containing text: '{text}'. Error: {e}"
            )
            logger.error(error_message)
            raise Exception(error_message)

    def clickByTextByPosition(
        self,
        text: str,
        match_type: Literal["first", "last", "nth"],
        occurrence: int = 0,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks on an element containing the specified text based on its position: first, last, or nth occurrence.
        Args:
            text (str): The text to locate the element by.
            match_type (Literal["first", "last", "nth"]): The type of match to perform: "first", "last", or "nth".
            occurrence (int): The occurrence index for "nth" match type (0-based index, must be provided explicitly).
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is clicked successfully.
        Raises:
            Exception: If the element is not found or the click operation fails.
        """
        try:
            # Locate the elements containing the specified text
            elements = self.page.locator(f"text={text}")
            # Determine the element based on the match type
            if match_type == "first":
                target_element = elements.first
            elif match_type == "last":
                target_element = elements.last
            elif match_type == "nth":
                target_element = elements.nth(occurrence)
            else:
                raise ValueError(
                    f"Invalid match_type: '{match_type}'. Use 'first', 'last', or 'nth'."
                )
            # Wait for the target element to be visible
            target_element.wait_for(state="visible", timeout=timeout)
            # Scroll the element into view if necessary
            target_element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            target_element.click()
            logger.info(
                f"Successfully clicked on the {match_type} element with text '{text}'."
            )
            return True
        except PlaywrightTimeoutError:
            error_message = f"Timeout while waiting for the {match_type} element with text '{text}'."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to click on the {match_type} element with text '{text}'. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def clickByTextByPositionAndWait(
        self,
        text: str,
        match_type: Literal["first", "last", "nth"],
        wait_time: int,
        occurrence: int = 0,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks on an element containing the specified text based on its position and waits for a specified amount of time after the click.
        Args:
            text (str): The text to locate the element by.
            match_type (Literal["first", "last", "nth"]): The type of match to perform: "first", "last", or "nth".
            wait_time (int): The time (in seconds) to wait after clicking the element.
            occurrence (int): The occurrence index for "nth" match type (0-based index, must be provided explicitly).
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is clicked successfully and the wait is completed.
        Raises:
            Exception: If the element is not found or the click operation fails.
        """
        try:
            # Locate the elements containing the specified text
            elements = self.page.locator(f"text={text}")
            # Determine the element based on the match type
            if match_type == "first":
                target_element = elements.first
            elif match_type == "last":
                target_element = elements.last
            elif match_type == "nth":
                target_element = elements.nth(occurrence)
            else:
                raise ValueError(
                    f"Invalid match_type: '{match_type}'. Use 'first', 'last', or 'nth'."
                )
            # Wait for the target element to be visible
            target_element.wait_for(state="visible", timeout=timeout)
            # Scroll the element into view if necessary
            target_element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            target_element.click()
            logger.info(
                f"Successfully clicked on the {match_type} element with text '{text}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(f"Waited for {wait_time} seconds after clicking the element.")
            return True
        except PlaywrightTimeoutError:
            error_message = f"Timeout while waiting for the {match_type} element with text '{text}'."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to click on the {match_type} element with text '{text}' and wait for {wait_time} seconds. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def clickByLinkText(
        self,
        link_text: str,
        partial_match: bool = False,
        occurrence: int = 0,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks on a link element (<a>) containing the specified text.
        Args:
            link_text (str): The text to locate the link element by.
            partial_match (bool): Whether to allow partial text matches (default is False).
            occurrence (int): The occurrence of the link to click (0-based index, default is 0).
            timeout (int): Timeout in milliseconds to wait for the link element (default is 60000).
        Returns:
            bool: True if the link is clicked successfully.
        Raises:
            Exception: If the link element is not found or the click operation fails.
        """
        try:
            # Locate the link element containing the specified text
            link_element = (
                self.page.locator(f"a:has-text('{link_text}')")
                if partial_match
                else self.page.locator(f"a:text('{link_text}')")
            )
            # Get the specific occurrence of the link element
            link_element = link_element.nth(occurrence)
            # Wait for the link element to be visible
            link_element.wait_for(state="visible", timeout=timeout)
            # Scroll the link element into view if necessary
            link_element.scroll_into_view_if_needed(timeout=timeout)
            # Click the link element
            link_element.click()
            logger.info(
                f"Successfully clicked on the {occurrence + 1}-th link containing text: '{link_text}'."
            )
            return True
        except PlaywrightTimeoutError:
            error_message = (
                f"Timeout while waiting for the link containing text: '{link_text}'."
            )
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to click on the link containing text: '{link_text}'. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def clickByLinkTextAndWait(
        self,
        link_text: str,
        wait_time: int,
        partial_match: bool = False,
        occurrence: int = 0,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks on a link element (<a>) containing the specified text and waits for a specified amount of time.
        Args:
            link_text (str): The text to locate the link element by.
            wait_time (int): The time (in seconds) to wait after clicking the element.
            partial_match (bool): Whether to allow partial text matches (default is False).
            occurrence (int): The occurrence of the link to click (0-based index, default is 0).
            timeout (int): Timeout in milliseconds to wait for the link element (default is 60000).
        Returns:
            bool: True if the link is clicked successfully.
        Raises:
            Exception: If the link element is not found or the click operation fails.
        """
        try:
            # Locate the link element containing the specified text
            link_element = (
                self.page.locator(f"a:has-text('{link_text}')")
                if partial_match
                else self.page.locator(f"a:text('{link_text}')")
            )
            # Get the specific occurrence of the link element
            link_element = link_element.nth(occurrence)
            # Wait for the link element to be visible
            link_element.wait_for(state="visible", timeout=timeout)
            # Scroll the link element into view if necessary
            link_element.scroll_into_view_if_needed(timeout=timeout)
            # Click the link element
            link_element.click()
            logger.info(
                f"Successfully clicked on the {occurrence + 1}-th link containing text: '{link_text}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(f"Waited for {wait_time} seconds after clicking the link.")
            return True
        except PlaywrightTimeoutError:
            error_message = (
                f"Timeout while waiting for the link containing text: '{link_text}'."
            )
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to click on the link containing text: '{link_text}'. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def clickElementByPosition(
        self,
        page_name: str,
        element_name: str,
        match_type: Literal["first", "last", "nth"],
        occurrence: int,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks on an element based on its position: first, last, or nth occurrence.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            match_type (Literal["first", "last", "nth"]): The type of match to perform: "first", "last", or "nth".
            occurrence (int): The occurrence index for "nth" match type (0-based index, must be provided explicitly).
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is clicked successfully.
        Raises:
            Exception: If the element is not found or the click operation fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Locate the element based on the match type
            if match_type == "first":
                element = self.getElement(locator, timeout).first
            elif match_type == "last":
                element = self.getElement(locator, timeout).last
            elif match_type == "nth":
                element = self.getElement(locator, timeout).nth(occurrence)
            else:
                raise ValueError(
                    f"Invalid match_type: {match_type}. Use 'first', 'last', or 'nth'."
                )
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Scroll the element into view if necessary
            element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            element.click()
            logger.info(
                f"Successfully clicked on the {match_type} element '{element_name}' on page '{page_name}'."
            )
            return True
        except PlaywrightTimeoutError:
            error_message = f"Timeout while waiting for the {match_type} element '{element_name}' on page '{page_name}'."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to click on the {match_type} element '{element_name}' on page '{page_name}'. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def clickElementByPositionAndWait(
        self,
        page_name: str,
        element_name: str,
        match_type: Literal["first", "last", "nth"],
        occurrence: int,
        wait_time: int,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks on an element based on its position: first, last, or nth occurrence, and waits for a specified duration.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON.
            match_type (Literal["first", "last", "nth"]): The type of match to perform: "first", "last", or "nth".
            occurrence (int): The occurrence index for "nth" match type (0-based index, must be provided explicitly).
            wait_time (int): Time in seconds to wait after clicking the element (must be provided explicitly).
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is clicked successfully.
        Raises:
            Exception: If the element is not found or the click operation fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Locate the element based on the match type
            if match_type == "first":
                element = self.getElement(locator, timeout).first
            elif match_type == "last":
                element = self.getElement(locator, timeout).last
            elif match_type == "nth":
                element = self.getElement(locator, timeout).nth(occurrence)
            else:
                raise ValueError(
                    f"Invalid match_type: {match_type}. Use 'first', 'last', or 'nth'."
                )
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Scroll the element into view if necessary
            element.scroll_into_view_if_needed(timeout=timeout)
            # Click the element
            element.click()
            logger.info(
                f"Successfully clicked on the {match_type} element '{element_name}' on page '{page_name}'. Waiting for {wait_time} seconds."
            )
            # Wait for the specified duration
            time.sleep(wait_time)
            logger.info(f"Waited for {wait_time} seconds after clicking the element.")
            return True
        except PlaywrightTimeoutError:
            error_message = f"Timeout while waiting for the {match_type} element '{element_name}' on page '{page_name}'."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to click on the {match_type} element '{element_name}' on page '{page_name}'. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def hoverOverElement(
        self, page_name: str, element_name: str, timeout: int = 60000
    ) -> bool:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.hover()
            return True
        except Exception as e:
            logger.error(
                f"Failed to hover over element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

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

    def readTextAndWait(
        self,
        page_name: str,
        element_name: str,
        wait_time: int,
        timeout: int = 60000,
    ) -> str:
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
            time.sleep(wait_time)
            return text_content.strip()
        except Exception as e:
            raise Exception(
                f"Failed to read text from element '{element_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def getInputValue(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> str:
        """
        Fetches the value of an input field or any element with a 'value' attribute.
        Args:
            page_name (str): The name of the page containing the input element.
            element_name (str): The name of the input element to fetch the value from.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            str: The value of the input element.
        Raises:
            Exception: If the value cannot be fetched.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Input element '{element_name}' not found on page '{page_name}'."
                )
            # Fetch the value of the input field
            input_value = (
                element.input_value()
            )  # Playwright's built-in method to get input values
            if input_value is None:
                raise Exception(
                    f"Failed to fetch the value of input element '{element_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully fetched value for input element '{element_name}' on page '{page_name}'. Value: '{input_value.strip()}'"
            )
            return input_value.strip()  # Return the input value as a string
        except Exception as e:
            logger.error(
                f"Failed to fetch value for input element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to fetch value for input element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def getInnerText(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> str:
        """
        Fetches the inner text of a web element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to fetch the inner text from.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            str: The inner text of the element.
        Raises:
            Exception: If the inner text cannot be fetched.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Fetch the inner text of the element
            inner_text = element.inner_text()
            if inner_text is None:
                raise Exception(
                    f"Failed to fetch inner text for element '{element_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully fetched inner text for element '{element_name}' on page '{page_name}'. Text: '{inner_text.strip()}'"
            )
            return inner_text.strip()  # Return the inner text as a string
        except Exception as e:
            logger.error(
                f"Failed to fetch inner text for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to fetch inner text for element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def getCSSValue(
        self,
        page_name: str,
        element_name: str,
        css_property: str,
        timeout: int = 60000,
    ) -> str:
        """
        Fetches the value of a specified CSS property from a web element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to fetch the CSS property from.
            css_property (str): The name of the CSS property to retrieve (e.g., 'color', 'font-size').
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            str: The value of the specified CSS property.
        Raises:
            Exception: If the CSS property cannot be fetched.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Use JavaScript to fetch the computed CSS property value
            css_value = self.page.evaluate(
                f"window.getComputedStyle(document.querySelector('{locator}')).getPropertyValue('{css_property}')"
            )
            if not css_value:
                raise Exception(
                    f"CSS property '{css_property}' not found for element '{element_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully fetched CSS property '{css_property}' for element '{element_name}' on page '{page_name}'. Value: {css_value.strip()}"
            )
            return css_value.strip()  # Return the CSS value as a string
        except Exception as e:
            logger.error(
                f"Failed to fetch CSS property '{css_property}' for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to fetch CSS property '{css_property}' for element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def getInnerHTML(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> str:
        """
        Fetches the inner HTML of a web element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to fetch the inner HTML from.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            str: The inner HTML of the element.
        Raises:
            Exception: If the inner HTML cannot be fetched.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Fetch the inner HTML of the element
            inner_html = element.inner_html()
            if inner_html is None:
                raise Exception(
                    f"Failed to fetch inner HTML for element '{element_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully fetched inner HTML for element '{element_name}' on page '{page_name}'. HTML: '{inner_html.strip()}'"
            )
            return inner_html.strip()  # Return the inner HTML as a string
        except Exception as e:
            logger.error(
                f"Failed to fetch inner HTML for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to fetch inner HTML for element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def readDisabledFieldText(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> str:
        """
        Reads the text from a disabled field element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to read the text from.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            str: The text of the disabled field element.
        Raises:
            Exception: If reading the text from the disabled field fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Check if the element is visible
            if not element.is_visible():
                raise Exception(
                    f"Element '{element_name}' is not visible on page '{page_name}'."
                )
            # Check if the element is disabled
            is_disabled = element.evaluate(
                "(el) => el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true'"
            )
            if not is_disabled:
                raise Exception(
                    f"Element '{element_name}' on page '{page_name}' is not disabled."
                )
            # Read the text from the disabled field (use 'value' or 'textContent' based on element type)
            text_content = element.evaluate("(el) => el.value || el.textContent")
            if text_content is None:
                raise Exception(
                    f"Failed to read text from disabled field '{element_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully read text from disabled field '{element_name}' on page '{page_name}'. Text: '{text_content.strip()}'"
            )
            return text_content.strip()
        except Exception as e:
            logger.error(
                f"Failed to read text from disabled field '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to read text from disabled field '{element_name}' on page '{page_name}'. Error: {e}"
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

    def selectOptionInListboxAndWait(
        self,
        page_name: str,
        element_name: str,
        option_value: str,
        wait_time: int,
        timeout: int = 60000,
    ) -> None:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.wait_for(state="visible", timeout=timeout)
            element.select_option(value=option_value)
            time.sleep(wait_time)
        except Exception as e:
            raise Exception(
                f"Failed to select option '{option_value}' in listbox '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def selectDropdownByText(
        self, page_name: str, dropdown_name: str, option_text: str, timeout: int = 60000
    ):
        """
        Selects an option in a dropdown by its visible text.
        Args:
            page_name (str): The name of the page in the locators JSON.
            dropdown_name (str): The name of the dropdown element in the locators JSON.
            option_text (str): The visible text of the option to select.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Raises:
            Exception: If the dropdown selection fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Select the option by visible text
            dropdown.select_option(label=option_text)
            logger.info(
                f"Successfully selected option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to select option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )

    def selectDropdownByTextAndWait(
        self,
        page_name: str,
        dropdown_name: str,
        option_text: str,
        wait_time: int,
        timeout: int = 60000,
    ):
        """
        Selects an option in a dropdown by its visible text and waits for a specified amount of time.
        Args:
            page_name (str): The name of the page in the locators JSON.
            dropdown_name (str): The name of the dropdown element in the locators JSON.
            option_text (str): The visible text of the option to select.
            wait_time (int): Time in seconds to wait after selecting the option.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Raises:
            Exception: If the dropdown selection or waiting fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Select the option by visible text
            dropdown.select_option(label=option_text)
            logger.info(
                f"Successfully selected option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(
                f"Waited for {wait_time} seconds after selecting option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )
            raise Exception(
                f"Failed to select option '{option_text}' in dropdown '{dropdown_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def selectDropdownByValue(
        self,
        page_name: str,
        dropdown_name: str,
        option_value: str,
        timeout: int = 60000,
    ):
        """
        Selects an option in a dropdown by its value.
        Args:
            page_name (str): The name of the page in the locators JSON.
            dropdown_name (str): The name of the dropdown element in the locators JSON.
            option_value (str): The value of the option to select.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Raises:
            Exception: If the dropdown selection fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Select the option by value
            dropdown.select_option(value=option_value)
            logger.info(
                f"Successfully selected option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to select option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )

    def selectDropdownByValueAndWait(
        self,
        page_name: str,
        dropdown_name: str,
        option_value: str,
        wait_time: int,
        timeout: int = 60000,
    ):
        """
        Selects an option in a dropdown by its value and waits for a specified amount of time.
        Args:
            page_name (str): The name of the page in the locators JSON.
            dropdown_name (str): The name of the dropdown element in the locators JSON.
            option_value (str): The value of the option to select.
            wait_time (int): Time in seconds to wait after selecting the option.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Raises:
            Exception: If the dropdown selection or waiting fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Select the option by value
            dropdown.select_option(value=option_value)
            logger.info(
                f"Successfully selected option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(
                f"Waited for {wait_time} seconds after selecting option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )
            raise Exception(
                f"Failed to select option with value '{option_value}' in dropdown '{dropdown_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def selectDropdownByIndex(
        self,
        page_name: str,
        dropdown_name: str,
        option_index: int,
        timeout: int = 60000,
    ):
        """
        Selects an option in a dropdown by its index.
        Args:
            page_name (str): The name of the page in the locators JSON.
            dropdown_name (str): The name of the dropdown element in the locators JSON.
            option_index (int): The index of the option to select (0-based).
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Raises:
            Exception: If the dropdown selection fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Select the option by index
            dropdown.select_option(index=option_index)
            logger.info(
                f"Successfully selected option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to select option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )

    def selectDropdownByIndexAndWait(
        self,
        page_name: str,
        dropdown_name: str,
        option_index: int,
        wait_time: int,
        timeout: int = 60000,
    ):
        """
        Selects an option in a dropdown by its index and waits for a specified amount of time.
        Args:
            page_name (str): The name of the page in the locators JSON.
            dropdown_name (str): The name of the dropdown element in the locators JSON.
            option_index (int): The index of the option to select (0-based).
            wait_time (int): Time in seconds to wait after selecting the option.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Raises:
            Exception: If the dropdown selection or waiting fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Select the option by index
            dropdown.select_option(index=option_index)
            logger.info(
                f"Successfully selected option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(
                f"Waited for {wait_time} seconds after selecting option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )
            raise Exception(
                f"Failed to select option at index '{option_index}' in dropdown '{dropdown_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def getDropdownOptions(
        self,
        page_name: str,
        dropdown_name: str,
        timeout: int = 60000,
    ) -> list:
        """
        Retrieves all options available in a dropdown menu.
        Args:
            page_name (str): The name of the page containing the dropdown.
            dropdown_name (str): The name of the dropdown element.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Returns:
            list: A list of strings representing the dropdown options.
        Raises:
            Exception: If retrieving the dropdown options fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Wait for the dropdown element to be visible
            self.page.wait_for_selector(locator, timeout=timeout)
            # Locate the dropdown element
            dropdown = self.page.locator(locator)
            # Retrieve all options within the dropdown
            options = dropdown.locator("option").all_text_contents()
            if options:
                logger.info(
                    f"Retrieved dropdown options for '{dropdown_name}' on page '{page_name}': {options}"
                )
                return options
            else:
                raise Exception(
                    f"No options found in dropdown '{dropdown_name}' on page '{page_name}'."
                )
        except Exception as e:
            logger.error(
                f"Failed to retrieve options for dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to retrieve options for dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )

    def getDropdownSelectedOption(
        self,
        page_name: str,
        dropdown_name: str,
        timeout: int = 60000,
    ) -> str:
        """
        Retrieves the selected option text from a dropdown element.
        Args:
            page_name (str): The name of the page containing the dropdown.
            dropdown_name (str): The name of the dropdown element.
            timeout (int): Timeout in milliseconds to wait for the dropdown (default is 60000).
        Returns:
            str: The text of the selected option.
        Raises:
            Exception: If retrieving the selected option fails.
        """
        locator = self.locator_manager.get_locator(page_name, dropdown_name)
        try:
            # Get the dropdown element using the locator
            dropdown = self.getElement(locator, timeout)
            if dropdown is None:
                raise Exception(
                    f"Dropdown '{dropdown_name}' not found on page '{page_name}'."
                )
            # Scroll the dropdown into view if it's not visible
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            # Check for selected option using 'option[selected]'
            selected_option = dropdown.locator("option[selected]").text_content()
            # If no option is found with 'option[selected]', check for 'option:checked'
            if not selected_option:
                selected_option = dropdown.locator("option:checked").text_content()
            # If still no option is selected, raise an exception
            if selected_option is None:
                raise Exception(
                    f"No option is selected in dropdown '{dropdown_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully retrieved selected option '{selected_option.strip()}' from dropdown '{dropdown_name}' on page '{page_name}'."
            )
            return selected_option.strip()
        except Exception as e:
            logger.error(
                f"Failed to retrieve selected option from dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to retrieve selected option from dropdown '{dropdown_name}' on page '{page_name}'. Error: {e}"
            )

    def assertSelectedDropdownText(
        self,
        page_name: str,
        element_name: str,
        expected_text: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Asserts that the selected option text of a dropdown matches the expected text.
        Supports locators that point to either the <select> element or option:checked.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            select_locator = locator
            if isinstance(locator, str):
                locator_lower = locator.lower()
                if "option:checked" in locator_lower:
                    select_locator = locator[
                        : locator_lower.index("option:checked")
                    ].strip()
                elif "option[selected]" in locator_lower:
                    select_locator = locator[
                        : locator_lower.index("option[selected]")
                    ].strip()

            dropdown = self.getElement(select_locator, timeout)
            dropdown.scroll_into_view_if_needed(timeout=timeout)
            dropdown.wait_for(state="visible", timeout=timeout)

            actual_text = dropdown.evaluate("""(element) => {
                        const selectedOption = element.querySelector('option:checked');
                        return selectedOption ? selectedOption.textContent : null;
                    }""")

            if actual_text is None:
                logger.error(
                    f"No selected option text found for '{element_name}' on page '{page_name}'."
                )
                return False

            expected_text_clean = " ".join(expected_text.split())
            actual_text_clean = " ".join(actual_text.split())

            if actual_text_clean == expected_text_clean:
                logger.info(
                    f"Asserted selected dropdown text successfully. Element '{element_name}' on page '{page_name}' has selected text: '{expected_text_clean}'."
                )
                return True

            logger.error(
                f"Assertion failed for selected dropdown text. Element '{element_name}' on page '{page_name}'. "
                f"Expected: '{expected_text_clean}', Actual: '{actual_text_clean}'."
            )
            return False
        except Exception as e:
            logger.error(
                f"Failed to assert selected dropdown text for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def selectComboboxOption(
        self,
        page_name: str,
        combobox_name: str,
        option_name: str,
        timeout: int = 60000,
    ) -> None:
        """
        Selects an option from a dropdown (combobox) based on its role and name.
        Args:
            page_name (str): The name of the page in the locators JSON.
            combobox_name (str): The name of the combobox element in the locators JSON.
            option_name (str): The name of the option to select.
            timeout (int): Timeout in milliseconds to wait for elements (default is 60000 ms).
        Raises:
            Exception: If any step in the dropdown selection fails.
        """
        try:
            # Locate the combobox
            combobox_locator = self.locator_manager.get_locator(
                page_name, combobox_name
            )
            combobox = self.getElement(combobox_locator, timeout)
            # Click the combobox to activate it
            combobox.click()
            logger.info(f"Clicked on combobox '{combobox_name}' on page '{page_name}'.")
            # Fill the combobox with the desired option name
            combobox.fill(option_name)
            logger.info(
                f"Filled combobox '{combobox_name}' with value '{option_name}' on page '{page_name}'."
            )
            combobox.press("Enter")  # Press Enter to trigger the dropdown options
            # Wait for the option to appear
            option_locator = self.getElement(
                {"role": "option", "name": option_name}, timeout
            )
            option_locator.wait_for(state="visible", timeout=timeout)
            logger.info(
                f"Option '{option_name}' is visible in combobox '{combobox_name}' on page '{page_name}'."
            )
            # Click the option to select it
            option_locator.click()
            logger.info(
                f"Selected option '{option_name}' in combobox '{combobox_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select option '{option_name}' in combobox '{combobox_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to select option '{option_name}' in combobox '{combobox_name}' on page '{page_name}'. Error: {e}"
            )

    def selectComboboxOptionAndWait(
        self,
        page_name: str,
        combobox_name: str,
        option_name: str,
        wait_time: int,
        timeout: int = 60000,
    ) -> bool:
        """
        Selects an option from a combobox (dropdown) based on its role and name, then waits for a specified amount of time.
        Args:
            page_name (str): The name of the page in the locators JSON.
            combobox_name (str): The name of the combobox element in the locators JSON.
            option_name (str): The name of the option to select.
            wait_time (int): Time in seconds to wait after selecting the option.
            timeout (int): Timeout in milliseconds to wait for elements (default is 60000 ms).
        Returns:
            bool: True if the option is selected and the wait is successful.
        Raises:
            Exception: If any step in the dropdown selection or waiting fails.
        """
        try:
            # Locate the combobox
            combobox_locator = self.locator_manager.get_locator(
                page_name, combobox_name
            )
            combobox = self.getElement(combobox_locator, timeout)
            # Click the combobox to activate it
            combobox.click()
            logger.info(f"Clicked on combobox '{combobox_name}' on page '{page_name}'.")
            # Fill the combobox with the desired option name
            combobox.fill(option_name)
            logger.info(
                f"Filled combobox '{combobox_name}' with value '{option_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            # Wait for the option to appear
            option_locator = self.getElement(
                {"role": "option", "name": option_name}, timeout
            )
            option_locator.wait_for(state="visible", timeout=timeout)
            logger.info(
                f"Option '{option_name}' is visible in combobox '{combobox_name}' on page '{page_name}'."
            )
            # Click the option to select it
            option_locator.click()
            logger.info(
                f"Selected option '{option_name}' in combobox '{combobox_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(f"Waited for {wait_time} seconds after selecting the option.")
            return True
        except Exception as e:
            logger.error(
                f"Failed to select option '{option_name}' in combobox '{combobox_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )
            raise Exception(
                f"Failed to select option '{option_name}' in combobox '{combobox_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def selectComboboxOptionByPosition(
        self,
        page_name: str,
        combobox_name: str,
        match_type: Literal["first", "last", "nth"],
        option_text: str,
        occurrence: int = 0,
        timeout: int = 60000,
    ) -> bool:
        """
        Selects an option from a combobox (dropdown) based on its position: first, last, or nth occurrence.
        Args:
            page_name (str): The name of the page in the locators JSON.
            combobox_name (str): The name of the combobox element in the locators JSON.
            match_type (Literal["first", "last", "nth"]): The type of match to perform: "first", "last", or "nth".
            option_text (str): The text of the option to select.
            occurrence (int): The occurrence index for "nth" match type (0-based index, must be provided explicitly).
            timeout (int): Timeout in milliseconds to wait for elements (default is 60000 ms).
        Returns:
            bool: True if the option is selected successfully.
        Raises:
            Exception: If any step in the dropdown selection fails.
        """
        try:
            # Locate the combobox
            combobox_locator = self.locator_manager.get_locator(
                page_name, combobox_name
            )
            combobox = self.getElement(combobox_locator, timeout)
            # Click the combobox to activate it
            combobox.click()
            logger.info(f"Clicked on combobox '{combobox_name}' on page '{page_name}'.")
            # Fill the combobox with the desired option text
            combobox.fill(option_text)
            logger.info(
                f"Filled combobox '{combobox_name}' with value '{option_text}' on page '{page_name}'."
            )
            # Determine the option to select based on the match type
            if match_type == "first":
                option_locator = self.page.locator("role=option").first
            elif match_type == "last":
                option_locator = self.page.locator("role=option").last
            elif match_type == "nth":
                option_locator = self.page.locator("role=option").nth(occurrence)
            else:
                raise ValueError(
                    f"Invalid match_type: {match_type}. Use 'first', 'last', or 'nth'."
                )
            # Wait for the option to appear
            option_locator.wait_for(state="visible", timeout=timeout)
            logger.info(
                f"Option '{match_type}' is visible in combobox '{combobox_name}' on page '{page_name}'."
            )
            # Click the option to select it
            option_locator.click()
            logger.info(
                f"Selected option '{match_type}' in combobox '{combobox_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to select option '{match_type}' in combobox '{combobox_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to select option '{match_type}' in combobox '{combobox_name}' on page '{page_name}'. Error: {e}"
            )

    def selectComboboxOptionByPositionAndWait(
        self,
        page_name: str,
        combobox_name: str,
        match_type: Literal["first", "last", "nth"],
        option_text: str,
        wait_time: int,
        occurrence: int = 0,
        timeout: int = 60000,
    ) -> bool:
        """
        Selects an option from a combobox (dropdown) based on its position: first, last, or nth occurrence,
        and waits for a specified amount of time after the selection.
        Args:
            page_name (str): The name of the page in the locators JSON.
            combobox_name (str): The name of the combobox element in the locators JSON.
            match_type (Literal["first", "last", "nth"]): The type of match to perform: "first", "last", or "nth".
            option_text (str): The text of the option to select.
            wait_time (int): Time in seconds to wait after selecting the option.
            occurrence (int): The occurrence index for "nth" match type (0-based index, must be provided explicitly).
            timeout (int): Timeout in milliseconds to wait for elements (default is 60000 ms).
        Returns:
            bool: True if the option is selected and the wait is successful.
        Raises:
            Exception: If any step in the dropdown selection or waiting fails.
        """
        try:
            # Locate the combobox
            combobox_locator = self.locator_manager.get_locator(
                page_name, combobox_name
            )
            combobox = self.getElement(combobox_locator, timeout)
            # Click the combobox to activate it
            combobox.click()
            logger.info(f"Clicked on combobox '{combobox_name}' on page '{page_name}'.")
            # Fill the combobox with the desired option text
            combobox.fill(option_text)
            logger.info(
                f"Filled combobox '{combobox_name}' with value '{option_text}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            # Determine the option to select based on the match type
            if match_type == "first":
                option_locator = self.page.locator("role=option").first
            elif match_type == "last":
                option_locator = self.page.locator("role=option").last
            elif match_type == "nth":
                option_locator = self.page.locator("role=option").nth(occurrence)
            else:
                raise ValueError(
                    f"Invalid match_type: {match_type}. Use 'first', 'last', or 'nth'."
                )
            # Wait for the option to appear
            option_locator.wait_for(state="visible", timeout=timeout)
            logger.info(
                f"Option '{match_type}' is visible in combobox '{combobox_name}' on page '{page_name}'."
            )
            # Click the option to select it
            option_locator.click()
            logger.info(
                f"Selected option '{match_type}' in combobox '{combobox_name}' on page '{page_name}'."
            )
            # Wait for the specified time
            time.sleep(wait_time)
            logger.info(f"Waited for {wait_time} seconds after selecting the option.")
            return True
        except Exception as e:
            logger.error(
                f"Failed to select option '{match_type}' in combobox '{combobox_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )
            raise Exception(
                f"Failed to select option '{match_type}' in combobox '{combobox_name}' on page '{page_name}' and wait for {wait_time} seconds. Error: {e}"
            )

    def checkCheckbox(self, page_name: str, element_name: str, timeout: int = 60000):
        """
        Checks a checkbox if it is not already checked.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the checkbox element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the checkbox (default is 60000).
        Raises:
            Exception: If the checkbox checking action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the checkbox element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Checkbox '{element_name}' not found on page '{page_name}'."
                )
            # Check the checkbox if it is not already checked
            if not element.is_checked():
                element.check()
            logger.info(
                f"Successfully checked checkbox '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to check checkbox '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to check checkbox '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def uncheckCheckbox(self, page_name: str, element_name: str, timeout: int = 60000):
        """
        Unchecks a checkbox if it is checked.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the checkbox element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the checkbox (default is 60000).
        Raises:
            Exception: If the checkbox unchecking action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the checkbox element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Checkbox '{element_name}' not found on page '{page_name}'."
                )
            # Uncheck the checkbox if it is checked
            if element.is_checked():
                element.uncheck()
            logger.info(
                f"Successfully unchecked checkbox '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to uncheck checkbox '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to uncheck checkbox '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def toggle(
        self, page_name: str, toggle_name: str, enable: bool, timeout: int = 60000
    ):
        """
        Toggles a switch element to the desired state (on/off).
        Args:
            page_name (str): The name of the page in the locators JSON.
            toggle_name (str): The name of the toggle element in the locators JSON.
            enable (bool): The desired state of the toggle (True for ON, False for OFF).
            timeout (int): Timeout in milliseconds to wait for the toggle (default is 60000).
        Raises:
            Exception: If the toggle action fails.
        """
        locator = self.locator_manager.get_locator(page_name, toggle_name)
        try:
            # Get the toggle element using the locator
            toggle_element = self.getElement(locator, timeout)
            if toggle_element is None:
                raise Exception(
                    f"Toggle '{toggle_name}' not found on page '{page_name}'."
                )
            # Scroll the toggle into view if it's not visible
            toggle_element.scroll_into_view_if_needed(timeout=timeout)
            # Check the current state of the toggle
            is_checked = toggle_element.is_checked()
            # Set the toggle to the desired state
            if enable and not is_checked:
                toggle_element.check()
                logger.info(
                    f"Successfully toggled '{toggle_name}' ON on page '{page_name}'."
                )
            elif not enable and is_checked:
                toggle_element.uncheck()
                logger.info(
                    f"Successfully toggled '{toggle_name}' OFF on page '{page_name}'."
                )
            else:
                logger.info(
                    f"Toggle '{toggle_name}' is already in the desired state on page '{page_name}'."
                )
        except Exception as e:
            logger.error(
                f"Failed to toggle '{toggle_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to toggle '{toggle_name}' on page '{page_name}'. Error: {e}"
            )

    def selectRadioButtonOption(
        self, page_name: str, element_name: str, timeout: int = 60000
    ):
        """
        Selects a radio button option.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the radio button element in the locators JSON.
            timeout (int): Timeout in milliseconds to wait for the radio button (default is 60000).
        Raises:
            Exception: If selecting the radio button option fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the radio button element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Radio button element '{element_name}' not found on page '{page_name}'."
                )
            # Select the radio button option
            element.click()
            logger.info(
                f"Successfully selected radio button '{element_name}' on page '{page_name}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to select radio button '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to select radio button '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def verifyRadioButtonOption(
        self, page_name: str, element_name: str, timeout: int = 60000
    ) -> bool:
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            if element is None:
                logger.error(
                    f"Radio button element '{element_name}' not found on page '{page_name}'."
                )
                return False
            is_selected = element.is_checked()
            if is_selected:
                logger.info(
                    f"Radio button '{element_name}' is selected on page '{page_name}'."
                )
                return True
            else:
                logger.warning(
                    f"Radio button '{element_name}' is NOT selected on page '{page_name}'."
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to verify radio button '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

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
                print(
                    f"\033[92m✅ Element '{element_name}' status is in expected state: {actual_status}\033[0m"
                )
                return True
            else:
                logger.warning(
                    f"Element '{element_name}' status is not in expected state. Current status: {actual_status}"
                )
                print(
                    f"\033[91m❌ Element '{element_name}' status is not in expected state. Current status: {actual_status}\033[0m"
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to verify status of element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def waitForElementState(
        self,
        page_name: str,
        element_name: str,
        state: Literal["attached", "detached", "hidden", "visible"],
        timeout: int = 60000,
    ) -> bool:
        """
        Waits for an element to reach a specific state.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to wait for.
            state (Literal['attached', 'detached', 'hidden', 'visible']): The desired state of the element.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element reaches the desired state, False otherwise.
        Raises:
            Exception: If the wait action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            element.wait_for(state=state, timeout=timeout)
            logger.info(
                f"Element '{element_name}' on page '{page_name}' reached state '{state}'."
            )
            return True
        except PlaywrightTimeoutError:
            logger.error(
                f"Timeout while waiting for element '{element_name}' on page '{page_name}' to reach state '{state}'."
            )
            raise Exception(
                f"Timeout while waiting for element '{element_name}' on page '{page_name}' to reach state '{state}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to wait for element '{element_name}' on page '{page_name}' to reach state '{state}'. Error: {e}"
            )
            raise Exception(
                f"Failed to wait for element '{element_name}' on page '{page_name}' to reach state '{state}'. Error: {e}"
            )

    def getElementAttribute(
        self,
        page_name: str,
        element_name: str,
        attribute_name: str,
        timeout: int = 60000,
    ) -> str:
        """
        Fetches the value of a specified attribute from a web element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to fetch the attribute from.
            attribute_name (str): The name of the attribute to retrieve.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            str: The value of the specified attribute.
        Raises:
            Exception: If the attribute cannot be fetched.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            attribute_value = element.get_attribute(attribute_name)
            if attribute_value is None:
                raise Exception(
                    f"Attribute '{attribute_name}' not found for element '{element_name}' on page '{page_name}'."
                )
            return attribute_value
        except Exception as e:
            logger.error(
                f"Failed to fetch attribute '{attribute_name}' from element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to fetch attribute '{attribute_name}' from element '{element_name}' on page '{page_name}'. Error: {e}"
            )

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
            logger.info(
                f"Timeout while waiting for the popup: {element_name} to be visible."
            )
        except Exception as e:
            logger.error(
                f"An error occurred while closing the popup: {element_name}. Error: {e}"
            )

    def handlePopUp(
        self,
        action: Literal["accept", "dismiss"] = "accept",
        text: str = "",
        timeout: int = 60000,
    ):
        """
        Handles JavaScript alerts, confirmation dialogs, and prompts.
        Args:
            action (Literal["accept", "dismiss"]): The action to perform on the alert. Can be "accept" or "dismiss". Default is "accept".
            text (str): The text to enter into the prompt, if applicable. Default is an empty string.
            timeout (int): Timeout in milliseconds to wait for the alert. Default is 60000 ms.
        Raises:
            Exception: If handling the alert fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to handle pop-ups.")
            # Use page.expect_event to handle the dialog
            with self.page.expect_event("dialog", timeout=timeout) as dialog_info:
                logger.info(
                    f"Waiting for alert to appear with a timeout of {timeout} ms."
                )
            dialog = dialog_info.value
            if action == "accept":
                dialog.accept(
                    prompt_text=text
                )  # Use the provided text or an empty string
            elif action == "dismiss":
                dialog.dismiss()
            else:
                raise ValueError("Invalid action. Use 'accept' or 'dismiss'.")
            logger.info(f"Alert handled with action: {action}")
        except Exception as e:
            logger.error(f"Failed to handle alert. Error: {e}")
            raise Exception(f"Failed to handle alert. Error: {e}")

    def acceptPopUp(self, timeout: int = 60000):
        """
        Accepts a JavaScript alert, confirmation dialog, or prompt.
        Args:
            timeout (int): Timeout in milliseconds to wait for the alert (default is 60000).
        Raises:
            Exception: If accepting the alert fails.
        """
        try:
            self.handlePopUp(action="accept", timeout=timeout)
            logger.info("Successfully accepted the pop-up.")
        except Exception as e:
            logger.error(f"Failed to accept the pop-up. Error: {e}")
            raise Exception(f"Failed to accept the pop-up. Error: {e}")

    def dismissPopUp(self, timeout: int = 60000):
        """
        Dismisses a JavaScript alert, confirmation dialog, or prompt.
        Args:
            timeout (int): Timeout in milliseconds to wait for the alert (default is 60000).
        Raises:
            Exception: If dismissing the alert fails.
        """
        try:
            self.handlePopUp(action="dismiss", timeout=timeout)
            logger.info("Successfully dismissed the pop-up.")
        except Exception as e:
            logger.error(f"Failed to dismiss the pop-up. Error: {e}")
            raise Exception(f"Failed to dismiss the pop-up. Error: {e}")

    def getPopUpText(self, timeout: int = 60000) -> str:
        """
        Retrieves the text of a JavaScript alert, confirmation dialog, or prompt.
        Args:
            timeout (int): Timeout in milliseconds to wait for the pop-up (default is 60000).
        Returns:
            str: The text of the pop-up.
        Raises:
            Exception: If retrieving the pop-up text fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to handle pop-ups.")
            # Use page.expect_event to wait for the dialog event
            with self.page.expect_event("dialog", timeout=timeout) as dialog_info:
                logger.info(
                    f"Waiting for pop-up to appear with a timeout of {timeout} ms."
                )
            # Retrieve the dialog object
            dialog = dialog_info.value
            pop_up_text = dialog.message  # Extract the message from the dialog
            dialog.dismiss()  # Dismiss the dialog after capturing its text
            # Check if pop-up text was captured
            if not pop_up_text:
                raise Exception("No pop-up appeared or no text was captured.")
            logger.info(f"Pop-up text retrieved successfully: {pop_up_text}")
            return pop_up_text
        except Exception as e:
            logger.error(f"Failed to retrieve pop-up text. Error: {e}")
            raise Exception(f"Failed to retrieve pop-up text. Error: {e}")

    def switchToFrame(self, frame_locator: str, timeout: int = 60000):
        """
        Switches the context to an iframe.
        Args:
            frame_locator (str): The locator for the iframe element.
            timeout (int): Timeout in milliseconds to wait for the iframe (default is 60000).
        Raises:
            Exception: If switching to the frame fails.
        """
        try:
            # Wait for the iframe element to be visible
            self.page.wait_for_selector(frame_locator, timeout=timeout)
            # Get the iframe element using the locator
            iframe_element = self.page.locator(frame_locator).element_handle()
            if iframe_element is None:
                raise Exception(
                    f"Failed to locate iframe with locator '{frame_locator}'."
                )
            # Get the frame object from the iframe element
            frame = iframe_element.content_frame()
            if frame is None:
                raise Exception(
                    f"Failed to retrieve the frame object for iframe with locator '{frame_locator}'."
                )
            # Switch the context to the iframe
            self.page = frame
            logger.info(
                f"Successfully switched to iframe with locator '{frame_locator}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to switch to iframe with locator '{frame_locator}'. Error: {e}"
            )
            raise Exception(
                f"Failed to switch to iframe with locator '{frame_locator}'. Error: {e}"
            )

    def switchToFrameByName(self, frame_name: str, timeout: int = 60000):
        """
        Switches to an iframe by its 'name' attribute.
        Args:
            frame_name (str): The 'name' attribute of the iframe to switch to.
            timeout (int): Timeout in milliseconds to wait for the iframe (default is 60000).
        Raises:
            Exception: If switching to the iframe fails.
        """
        try:
            # Wait for the iframe to appear (if needed)
            self.page.wait_for_selector(f"iframe[name='{frame_name}']", timeout=timeout)
            # Locate the frame by its name attribute
            frame = self.page.frame(name=frame_name)  # type: ignore
            if frame is None:
                raise Exception(f"Iframe with name '{frame_name}' not found.")
            # Store the frame in an instance variable for further interactions
            self.current_frame = frame
            logger.info(f"Successfully switched to iframe with name '{frame_name}'.")
        except Exception as e:
            logger.error(
                f"Failed to switch to iframe with name '{frame_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to switch to iframe with name '{frame_name}'. Error: {e}"
            )

    def switchToFrameByIndex(self, frame_index: int, timeout: int = 60000):
        """
        Switches to an iframe by its index on the page.
        Args:
            frame_index (int): The index of the iframe to switch to (0-based).
            timeout (int): Timeout in milliseconds to wait for the iframe (default is 60000).
        Raises:
            Exception: If the iframe cannot be found or switching fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to access frames.")
            # Get all frames on the page
            frames = self.page.frames
            if frame_index >= len(frames):
                raise Exception(
                    f"Iframe with index '{frame_index}' not found. Total frames available: {len(frames)}"
                )
            # Get the frame by index
            frame = frames[frame_index]
            if frame is None:
                raise Exception(f"Iframe with index '{frame_index}' is None.")
            # Store the frame in an instance variable for further interactions
            self.current_frame = frame
            logger.info(f"Successfully switched to iframe with index '{frame_index}'.")
        except Exception as e:
            logger.error(
                f"Failed to switch to iframe with index '{frame_index}'. Error: {e}"
            )
            raise Exception(
                f"Failed to switch to iframe with index '{frame_index}'. Error: {e}"
            )

    def switchToMainFrame(self):
        """
        Switches back to the main frame context.
        Raises:
            Exception: If switching back to the main frame fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError(
                    "self.page must be a Page object to access the main frame."
                )
            # Switch back to the main frame context
            main_page = self.page.context.pages[0]
            self.page = main_page
            # Clear the current_frame attribute
            self.current_frame = None
            logger.info("Successfully switched back to the main frame.")
        except Exception as e:
            logger.error(f"Failed to switch back to the main frame. Error: {e}")
            raise Exception(f"Failed to switch back to the main frame. Error: {e}")

    def switchToParentFrame(self):
        """
        Switches the context to the parent frame of the current frame.
        Raises:
            Exception: If switching to the parent frame fails.
        """
        try:
            # Ensure self.page is a Frame object
            if not isinstance(self.page, Frame):
                raise TypeError(
                    "self.page must be a Frame object to switch to the parent frame."
                )
            # Get the parent frame of the current frame
            parent_frame = self.page.parent_frame
            if parent_frame is None:
                raise Exception("The current frame has no parent frame.")
            # Switch the context to the parent frame
            self.page = parent_frame
            logger.info("Successfully switched to the parent frame.")
        except Exception as e:
            logger.error(f"Failed to switch to the parent frame. Error: {e}")
            raise Exception(f"Failed to switch to the parent frame. Error: {e}")

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

    def refreshPage(self, timeout: int = 60000) -> bool:
        """
        Refreshes the current page.
        Args:
            timeout (int): Timeout in milliseconds to wait for the page reload (default is 60000).
        Returns:
            bool: True if the page is refreshed successfully, False otherwise.
        Raises:
            RuntimeError: If refreshing the page fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to refresh the page.")
            # Perform the page reload
            self.page.reload(timeout=timeout)
            # Log success if the page reloads without issues
            logger.info("Page refreshed successfully.")
            return True
        except PlaywrightTimeoutError as e:
            # Log and raise a RuntimeError for timeout-specific errors
            error_message = (
                f"Timeout while refreshing the page within {timeout} ms. Error: {e}"
            )
            logger.error(error_message)
            raise RuntimeError(error_message)
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            # Log and raise a RuntimeError for unexpected errors
            error_message = (
                f"An unexpected error occurred while refreshing the page. Error: {e}"
            )
            logger.error(error_message)
            raise RuntimeError(error_message)

    def goBack(self, timeout: int = 60000) -> bool:
        """
        Navigates back to the previous page in the browser history.
        Args:
            timeout (int): Timeout in milliseconds to wait for the navigation (default is 60000).
        Returns:
            bool: True if the navigation is successful, False otherwise.
            Raises:
                Exception: If navigating back fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to navigate back.")
            response = self.page.go_back(timeout=timeout)
            if response:
                logger.info("Successfully navigated back to the previous page.")
                return True
            else:
                logger.warning("No previous page in the browser history.")
                return False
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to navigate back. Error: {e}")
            raise Exception(f"Failed to navigate back. Error: {e}")

    def goForward(self, timeout: int = 60000) -> bool:
        """
        Navigates forward to the next page in the browser history.
        Args:
            timeout (int): Timeout in milliseconds to wait for the navigation (default is 60000).
        Returns:
            bool: True if the navigation is successful, False otherwise.
        Raises:
            Exception: If navigating forward fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to navigate forward.")
            response = self.page.go_forward(timeout=timeout)
            if response:
                logger.info("Successfully navigated forward to the next page.")
                return True
            else:
                logger.warning("No next page in the browser history.")
                return False
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to navigate forward. Error: {e}")
            raise Exception(f"Failed to navigate forward. Error: {e}")

    def maximizeWindow(self) -> bool:
        """
        Maximizes the browser window to the maximum available screen size.
        Returns:
            bool: True if the window is maximized successfully.
            Raises:
                Exception: If maximizing the window fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError(
                    "self.page must be a Page object to maximize the window."
                )
            # Get the screen size of the system
            screen_width = self.page.evaluate("window.screen.availWidth")
            screen_height = self.page.evaluate("window.screen.availHeight")
            # Set the viewport size to the maximum screen size
            self.page.set_viewport_size(
                {"width": screen_width, "height": screen_height}
            )
            logger.info("Successfully maximized the browser window.")
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to maximize the browser window. Error: {e}")
            raise Exception(f"Failed to maximize the browser window. Error: {e}")

    def waitForPageLoad(
        self,
        timeout: int = 60000,
    ) -> bool:
        """
        Waits for the page to fully load.
        Args:
            timeout (int): Timeout in milliseconds to wait for the page to load (default is 60000).
        Returns:
            bool: True if the page loads successfully, False otherwise.
        """
        try:
            self.page.wait_for_load_state("load", timeout=timeout)
            logger.info("Page loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to load the page within {timeout} ms. Error: {e}")
            return False

    def waitForURLChange(self, expected_url: str, timeout: int = 60000) -> bool:
        try:
            self.page.wait_for_url(expected_url, timeout=timeout)
            return True
        except Exception as e:
            logger.error(
                f"Failed to wait for URL to change to '{expected_url}'. Error: {e}"
            )
            return False

    def getPageTitle(self, timeout: int = 60000) -> str:
        """
        Retrieves the title of the current page.
        Args:
            timeout (int): Timeout in milliseconds to wait for the page title (default is 60000).
        Returns:
            str: The title of the current page.
        Raises:
            Exception: If retrieving the page title fails.
        """
        try:
            # Wait for the page to be fully loaded
            self.page.wait_for_load_state("load", timeout=timeout)
            # Get the page title
            title = self.page.title()
            if not title:
                raise Exception("Failed to retrieve the page title.")
            logger.info(f"Successfully retrieved page title: {title}")
            return title
        except Exception as e:
            logger.error(f"Failed to retrieve page title. Error: {e}")
            raise Exception(f"Failed to retrieve page title. Error: {e}")

    def clearCookies(self) -> bool:
        """
        Clears all cookies in the browser context.
        Returns:
            bool: True if cookies are cleared successfully.
            Raises:
                Exception: If clearing cookies fails.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to clear cookies.")
            # Clear all cookies in the browser context
            self.page.context.clear_cookies()
            logger.info("Successfully cleared all cookies from the browser context.")
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to clear cookies. Error: {e}")
            raise Exception(f"Failed to clear cookies. Error: {e}")

    def captureTabCount(self, context: BrowserContext) -> int:
        """
        Captures the current number of tabs in the browser context.
        Args:
            context (BrowserContext): The browser context containing the tabs.
        Returns:
            int: The number of open tabs in the browser context.
        """
        try:
            # Get the list of pages (tabs) in the context
            pages = context.pages
            # Count the number of open tabs
            tab_count = len(pages)
            logger.info(f"Current number of tabs open: {tab_count}")
            return tab_count
        except Exception as e:
            logger.error(f"Failed to capture the tab count. Error: {e}")
            raise Exception(f"Failed to capture the tab count. Error: {e}")

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

    def switchToFirstTab(
        self,
        context: BrowserContext,
        timeout: int = 60000,
    ) -> Page:
        """
        Switches to the first tab in the browser context.
        Args:
            context (BrowserContext): The browser context containing the tabs.
            timeout (int): The maximum time to wait for the tab to be available (in milliseconds).
        Returns:
            Page: The page object of the first tab.
        Raises:
            Exception: If there are no tabs open or switching fails.
        """
        try:
            # Get the list of pages (tabs) in the context
            pages = context.pages
            current_tab_count = len(pages)
            # Validate that there are tabs open
            if current_tab_count == 0:
                raise Exception("No tabs are open in the browser context.")
            # Switch to the first tab (index 0)
            target_page = pages[0]
            target_page.bring_to_front()
            logger.info("Successfully switched to the first tab.")
            return target_page
        except Exception as e:
            logger.error(f"Failed to switch to the first tab. Error: {e}")
            raise Exception(f"Failed to switch to the first tab. Error: {e}")

    def switchToLastTab(
        self,
        context: BrowserContext,
        timeout: int = 60000,
    ) -> Page:
        """
        Switches to the last tab in the browser context.
        Args:
            context (BrowserContext): The browser context containing the tabs.
            timeout (int): The maximum time to wait for the tab to be available (in milliseconds).
        Returns:
            Page: The page object of the last tab.
        Raises:
            Exception: If there are no tabs open or switching fails.
        """
        try:
            # Get the list of pages (tabs) in the context
            pages = context.pages
            current_tab_count = len(pages)
            # Validate that there are tabs open
            if current_tab_count == 0:
                raise Exception("No tabs are open in the browser context.")
            # Get the index of the last tab
            last_tab_index = current_tab_count - 1
            # Switch to the last tab
            target_page = pages[last_tab_index]
            target_page.bring_to_front()
            logger.info(
                f"Successfully switched to the last tab at index {last_tab_index}."
            )
            return target_page
        except Exception as e:
            logger.error(f"Failed to switch to the last tab. Error: {e}")
            raise Exception(f"Failed to switch to the last tab. Error: {e}")

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

    def closeOtherTabs(
        self,
        context: BrowserContext,
        timeout: int = 60000,
    ) -> bool:
        """
        Closes all tabs except the currently active one.
        Args:
            context (BrowserContext): The browser context containing the tabs.
            timeout (int): Timeout in milliseconds to wait for the tabs (default is 60000 milliseconds).
        Returns:
            bool: True if other tabs are closed successfully, False otherwise.
        Raises:
            Exception: If closing other tabs fails.
        """
        try:
            # Get the currently active page (tab)
            active_page = self.page
            # Get the list of all pages (tabs) in the context
            pages = context.pages
            # Validate that there are tabs open
            if len(pages) <= 1:
                # If there's only one tab, nothing to close
                logger.info("No other tabs to close.")
                return True
            # Iterate through all pages and close tabs except the active one
            for page in pages:
                if page != active_page:
                    page.close()
                    logger.info(f"Closed tab with URL: {page.url}")
            logger.info("Successfully closed all other tabs.")
            return True
        except Exception as e:
            logger.error(f"Failed to close other tabs. Error: {e}")
            raise Exception(f"Failed to close other tabs. Error: {e}")

    def closeCurrentTabAndSwitchToPreviousTab(
        self, context: BrowserContext, timeout: int = 60000
    ) -> Page:
        """
        Closes the currently active tab and switches to the previous tab.
        Args:
            context (BrowserContext): The browser context containing the tabs.
            timeout (int): Timeout in milliseconds to wait for the tab switch (default is 60000).
        Returns:
            Page: The page object of the previous tab.
        Raises:
            Exception: If there is no previous tab or if the operation fails.
        """
        try:
            # Ensure self.page is a Page object
            if not isinstance(self.page, Page):
                raise TypeError(
                    "The current page (self.page) is not a valid Page object. It may be a Frame."
                )
            # Get the list of open tabs (pages) in the context
            pages = context.pages
            current_tab_count = len(pages)
            # Validate that there are at least two tabs to switch
            if current_tab_count < 2:
                raise Exception(
                    "Cannot switch to the previous tab. Only one tab is open."
                )
            # Get the index of the currently active tab
            current_tab_index = pages.index(self.page)
            # Close the currently active tab
            self.page.close()
            logger.info(f"Closed the current tab at index {current_tab_index}.")
            # Determine the index of the previous tab
            previous_tab_index = current_tab_index - 1
            # Ensure the previous tab index is valid
            if previous_tab_index < 0:
                raise Exception("No previous tab exists to switch to.")
            # Switch to the previous tab
            previous_tab = pages[previous_tab_index]
            previous_tab.bring_to_front()
            logger.info(f"Switched to the previous tab at index {previous_tab_index}.")
            # Update self.page to the previous tab
            self.page = previous_tab
            return previous_tab
        except Exception as e:
            logger.error(
                f"Failed to close the current tab and switch to the previous tab. Error: {e}"
            )
            raise Exception(
                f"Failed to close the current tab and switch to the previous tab. Error: {e}"
            )

    def captureWindowCount(self, context: BrowserContext) -> int:
        """
        Captures the current number of windows in the browser context.
        Args:
            context (BrowserContext): The browser context containing the windows.
        Returns:
            int: The number of open windows in the browser context.
        """
        try:
            # Get the list of pages (windows) in the context
            pages = context.pages
            # Count the number of open windows
            window_count = len(pages)
            logger.info(f"Current number of windows open: {window_count}")
            return window_count
        except Exception as e:
            logger.error(f"Failed to capture the window count. Error: {e}")
            raise Exception(f"Failed to capture the window count. Error: {e}")

    def switchToWindow(self, context: BrowserContext, window_index: int) -> Page:
        """
        Switches the context to a specific window based on its index.
        Args:
            context (BrowserContext): The browser context containing the windows.
            window_index (int): The index of the window to switch to.
        Returns:
            Page: The page object of the specified window.
        Raises:
            IndexError: If the window index is out of range.
        """
        pages = context.pages
        try:
            if window_index < len(pages):
                target_window = pages[window_index]
                target_window.bring_to_front()
                logger.info(f"Switched to window at index {window_index}.")
                return target_window
            else:
                logger.error(
                    f"Window index {window_index} out of range. There are only {len(pages)} windows open."
                )
                raise IndexError(
                    f"Window index {window_index} out of range. There are only {len(pages)} windows open."
                )
        except Exception as e:
            logger.error(
                f"Failed to switch to window at index {window_index}. Error: {e}"
            )
            raise Exception(
                f"Failed to switch to window at index {window_index}. Error: {e}"
            )

    def switchToOriginalWindow(
        self, context: BrowserContext, original_window_index: int = 0
    ) -> Page:
        """
        Switches back to the original window.
        Args:
            context (BrowserContext): The browser context containing the windows.
            original_window_index (int): The index of the original window (default is 0).
        Returns:
            Page: The page object of the original window.
        Raises:
            IndexError: If the window index is out of range.
        """
        pages = context.pages
        try:
            if original_window_index < len(pages):
                original_window = pages[original_window_index]
                original_window.bring_to_front()
                logger.info(
                    f"Switched back to the original window at index {original_window_index}."
                )
                return original_window
            else:
                logger.error(
                    f"Window index {original_window_index} out of range. There are only {len(pages)} windows open."
                )
                raise IndexError(
                    f"Window index {original_window_index} out of range. There are only {len(pages)} windows open."
                )
        except Exception as e:
            logger.error(f"Failed to switch back to the original window. Error: {e}")
            raise Exception(f"Failed to switch back to the original window. Error: {e}")

    def closeWindowByIndex(self, context: BrowserContext, window_index: int) -> bool:
        """
        Closes a specific browser window based on its index.
        Args:
            context (BrowserContext): The browser context containing the windows.
            window_index (int): The index of the window to close.
        Returns:
            bool: True if the window is closed successfully.
        Raises:
            IndexError: If the window index is out of range.
            Exception: If an error occurs while closing the window.
        """
        pages = context.pages
        if not pages:
            logger.error("No pages found in the browser context.")
            raise ValueError("No pages found in the browser context.")
        try:
            if window_index < len(pages):
                target_window = pages[window_index]
                target_window.close()
                logger.info(f"Closed window at index {window_index}.")
                return True
            else:
                logger.error(
                    f"Window index {window_index} out of range. There are only {len(pages)} windows open."
                )
                raise IndexError(
                    f"Window index {window_index} out of range. There are only {len(pages)} windows open."
                )
        except Exception as e:
            logger.error(f"Failed to close window at index {window_index}. Error: {e}")
            raise Exception(
                f"Failed to close window at index {window_index}. Error: {e}"
            )

    def assertTrue(self, condition, message):
        """
        Asserts that a condition is True. If False, appends the error message to the errors list.
        Args:
            condition (bool): The condition to assert.
            message (str): The error message to log and append if the assertion fails.
        """
        if not condition:
            self.errors.append(message)
            logger.error(f"Assertion failed: {message}")
        else:
            logger.info(f"Assertion passed: {message}")

    def assertAll(self):
        """
        Raises an AssertionError if there are any collected errors.
        """
        if self.errors:
            error_message = "\n".join(self.errors)
            logger.error(f"Assertions failed:\n{error_message}")
            raise AssertionError(f"Assertions failed:\n{error_message}")

    def isElementVisible(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is visible on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check visibility.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is visible, False otherwise.
        Raises:
            Exception: If there is an error during the visibility check.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_visible = element.is_visible()
            if is_visible:
                logger.info(
                    f"Element '{element_name}' is visible on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is not visible on page '{page_name}'."
                )
            return is_visible
        except Exception as e:
            logger.error(
                f"Failed to check visibility of element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementVisibleInSequence(
        self,
        page_name: str,
        element_names: list,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if multiple elements are visible in sequence.
        Args:
            page_name (str): The name of the page containing the elements.
            element_names (list): A list of element names to check visibility.
            timeout (int): Timeout in milliseconds to wait for each element (default is 60000).
        Returns:
            bool: True if all elements are visible in sequence, False otherwise.
        """
        try:
            for element_name in element_names:
                locator = self.locator_manager.get_locator(page_name, element_name)
                element = self.getElement(locator, timeout)
                if not element.is_visible():
                    logger.warning(
                        f"Element '{element_name}' is not visible on page '{page_name}'."
                    )
                    return False
                logger.info(
                    f"Element '{element_name}' is visible on page '{page_name}'."
                )
            return True
        except Exception as e:
            logger.error(
                f"Failed to check visibility of elements in sequence on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementNotVisible(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is visible on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check visibility.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is visible, False otherwise.
        Raises:
            Exception: If there is an error during the visibility check.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_visible = element.is_visible()
            if not is_visible:
                logger.info(
                    f"Element '{element_name}' is not visible on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is visible on page '{page_name}'."
                )
            return is_visible
        except Exception as e:
            logger.error(
                f"Failed to check visibility of element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementHidden(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is hidden on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is hidden, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_hidden = not element.is_visible()
            if is_hidden:
                logger.info(
                    f"Element '{element_name}' is hidden on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is visible on page '{page_name}'."
                )
            return is_hidden
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is hidden on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementEnabled(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is enabled on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_enabled = element.is_enabled()
            if is_enabled:
                logger.info(
                    f"Element '{element_name}' is enabled on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is not enabled on page '{page_name}'."
                )
            return is_enabled
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is enabled on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementDisabled(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is disabled on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is disabled, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_disabled = not element.is_enabled()
            if is_disabled:
                logger.info(
                    f"Element '{element_name}' is disabled on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is enabled on page '{page_name}'."
                )
            return is_disabled
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is disabled on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementEditable(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is editable on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is editable, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_editable = element.is_editable()
            if is_editable:
                logger.info(
                    f"Element '{element_name}' is editable on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is not editable on page '{page_name}'."
                )
            return is_editable
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is editable on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementChecked(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if a checkbox or radio button element is checked on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is checked, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            is_checked = element.is_checked()
            if is_checked:
                logger.info(
                    f"Element '{element_name}' is checked on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is not checked on page '{page_name}'."
                )
            return is_checked
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is checked on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementSelected(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element (e.g., dropdown option, radio button, or checkbox) is selected on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is selected, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            # Check if the element is a checkbox or radio button
            if element.get_attribute("type") in ["checkbox", "radio"]:
                is_selected = element.is_checked()
            else:
                # For other elements, check if they are selected
                is_selected = element.evaluate("el => el.selected")
            if is_selected:
                logger.info(
                    f"Element '{element_name}' is selected on page '{page_name}'."
                )
            else:
                logger.warning(
                    f"Element '{element_name}' is not selected on page '{page_name}'."
                )
            return is_selected
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is selected on page '{page_name}'. Error: {e}"
            )
            return False

    def isElementPresent(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Checks if an element is present in the DOM on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the element is present, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Try to locate the element within the given timeout
            self.page.wait_for_selector(locator, timeout=timeout)
            element = self.page.query_selector(locator)
            if element:
                logger.info(
                    f"Element '{element_name}' is present on page '{page_name}'."
                )
                return True
            else:
                logger.warning(
                    f"Element '{element_name}' is not present on page '{page_name}'."
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to check if element '{element_name}' is present on page '{page_name}'. Error: {e}"
            )
            return False

    def compareExpectedActualText(
        self,
        actual_text: str,
        expected_text: str,
    ) -> bool:  # Updated return type in the method signature
        """
        Compares actual text with expected text and returns the result.

        Args:
            actual_text (str): The actual text to compare.
            expected_text (str): The expected text to compare against.

        Returns:
            bool: True if the texts match, False otherwise.
        """
        try:
            if not expected_text:
                raise ValueError("Expected text is invalid or missing.")
            if not actual_text:
                raise ValueError("Actual text is invalid or missing.")
            # Remove leading and trailing spaces from both texts
            actual_text_cleaned = actual_text.strip()
            expected_text_cleaned = expected_text.strip()
            if expected_text_cleaned == actual_text_cleaned:
                logger.info(f"Expected text is displayed: {expected_text}")
                print(f"\033[92m✅ Expected text is displayed: {expected_text}\033[0m")
                return True
            else:
                logger.warning(
                    f"Expected text does not match. "
                    f"Expected: '{expected_text}', Actual: '{actual_text}'"
                )
                print(
                    f"\033[91m❌ Expected text does not match. "
                    f"Expected: '{expected_text}', Actual: '{actual_text}'\033[0m"
                )
                return False
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            return False
        except Exception as e:
            logger.error(f"An error occurred during text comparison: {e}")
            return False

    def checkExpectedTextInActual(
        self,
        actual_text: str,
        expected_text: str,
    ) -> bool:  # Updated return type in the method signature
        """
        Checks if the expected text is present in the actual text.

        Args:
            actual_text (str): The actual text to search within.
            expected_text (str): The expected text to search for.

        Returns:
            bool: True if the expected text is found in the actual text, False otherwise.
        """
        try:
            if not expected_text:
                raise ValueError("Expected text is invalid or missing.")
            if not actual_text:
                raise ValueError("Actual text is invalid or missing.")
            # Remove leading and trailing spaces from both texts
            actual_text_cleaned = actual_text.strip()
            expected_text_cleaned = expected_text.strip()
            if (
                expected_text_cleaned in actual_text_cleaned
            ):  # Check if expected text is a substring of actual text
                logger.info(f"Expected text is found in actual text: {expected_text}")
                print(
                    f"\033[92m✅ Expected text is found in actual text: {expected_text}\033[0m"
                )
                return True
            else:
                logger.warning(
                    f"Expected text is NOT found in actual text. "
                    f"Expected substring: '{expected_text}', Actual: '{actual_text}'"
                )
                print(
                    f"\033[91m❌ Expected text is NOT found in actual text. "
                    f"Expected substring: '{expected_text}', Actual: '{actual_text}'\033[0m"
                )
                return False
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            return False
        except Exception as e:
            logger.error(f"An error occurred during text comparison: {e}")
            return False

    def assertText(
        self,
        page_name: str,
        element_name: str,
        expected_text: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Asserts that the text of a specific element matches the expected text.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            expected_text (str): The expected text to match.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the text matches, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Get the actual text from the element
            actual_text = element.text_content()
            if actual_text is None:
                logger.error(f"Element '{element_name}' has no text content.")
                return False
            # Strip whitespace for comparison
            actual_text = actual_text.strip()
            expected_text = expected_text.strip()
            # Assert the text matches
            if actual_text == expected_text:
                logger.info(
                    f"Asserted text successfully. Element '{element_name}' on page '{page_name}' contains the expected text: '{expected_text}'."
                )
                return True
            else:
                logger.error(
                    f"Assertion failed. Element '{element_name}' on page '{page_name}' does not contain the expected text. "
                    f"Expected: '{expected_text}', Actual: '{actual_text}'."
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to assert text for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def assertContainsText(
        self,
        page_name: str,
        element_name: str,
        expected_text: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Asserts that the text of a specific element contains the expected text.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            expected_text (str): The expected text to be contained.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the text contains the expected text, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Get the actual text from the element
            actual_text = element.text_content()
            if actual_text is None:
                logger.error(f"Element '{element_name}' has no text content.")
                return False
            # Strip whitespace for comparison
            actual_text = actual_text.strip()
            expected_text = expected_text.strip()
            # Check if the actual text contains the expected text
            if expected_text in actual_text:
                logger.info(
                    f"Asserted text successfully. Element '{element_name}' on page '{page_name}' contains the expected text: '{expected_text}'."
                )
                return True
            else:
                logger.error(
                    f"Assertion failed. Element '{element_name}' on page '{page_name}' does not contain the expected text. "
                    f"Expected substring: '{expected_text}', Actual: '{actual_text}'."
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to assert contains text for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def assertExpectedActualText(
        self,
        actual_text: str,
        expected_text: str,
    ) -> bool:
        """
        Asserts that the actual text matches the expected text.
        Args:
            actual_text (str): The actual text to compare.
            expected_text (str): The expected text to compare against.
        Returns:
            bool: True if the texts match, False otherwise.
        """
        try:
            # Strip leading and trailing whitespace for comparison
            actual_text_cleaned = actual_text.strip()
            expected_text_cleaned = expected_text.strip()
            if actual_text_cleaned == expected_text_cleaned:
                logger.info(
                    f"Text matches. Expected: '{expected_text}', Actual: '{actual_text}'"
                )
                return True
            else:
                logger.warning(
                    f"Text does not match. Expected: '{expected_text}', Actual: '{actual_text}'"
                )
                return False
        except Exception as e:
            logger.error(f"Failed to assert expected and actual text. Error: {e}")
            return False

    def assertExpectedInActualText(
        self,
        actual_text: str,
        expected_text: str,
    ) -> bool:
        """
        Asserts that the expected text is present in the actual text.
        Args:
            actual_text (str): The actual text to search within.
            expected_text (str): The expected text to search for.
        Returns:
            bool: True if the expected text is found in the actual text, False otherwise.
        """
        try:
            # Strip leading and trailing whitespace for comparison
            actual_text_cleaned = actual_text.strip()
            expected_text_cleaned = expected_text.strip()
            if expected_text_cleaned in actual_text_cleaned:
                logger.info(
                    f"Expected text '{expected_text}' is found in actual text: '{actual_text}'"
                )
                return True
            else:
                logger.warning(
                    f"Expected text '{expected_text}' is NOT found in actual text: '{actual_text}'"
                )
                return False
        except Exception as e:
            logger.error(f"Failed to assert expected text in actual text. Error: {e}")
            return False

    def assertAttribute(
        self,
        page_name: str,
        element_name: str,
        attribute_name: str,
        expected_value: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Asserts that the value of a specified attribute of an element matches the expected value.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to check.
            attribute_name (str): The name of the attribute to check.
            expected_value (str): The expected value to match.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the attribute value matches the expected value, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Get the actual attribute value from the element
            actual_value = element.get_attribute(attribute_name)
            if actual_value is None:
                logger.error(
                    f"Element '{element_name}' has no attribute '{attribute_name}'."
                )
                return False
            # Strip whitespace for comparison
            actual_value = actual_value.strip()
            expected_value = expected_value.strip()
            # Assert the attribute value matches
            if actual_value == expected_value:
                logger.info(
                    f"Asserted attribute value successfully. Element '{element_name}' on page '{page_name}' has attribute '{attribute_name}' with expected value: '{expected_value}'."
                )
                return True
            else:
                logger.error(
                    f"Assertion failed. Element '{element_name}' on page '{page_name}' does not have attribute '{attribute_name}' with expected value. "
                    f"Expected: '{expected_value}', Actual: '{actual_value}'."
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to assert attribute value for element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def assertTitle(
        self,
        expected_title: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Asserts that the title of the current page matches the expected title.
        Args:
            expected_title (str): The expected title to match.
            timeout (int): Timeout in milliseconds to wait for the page title (default is 60000).
        Returns:
            bool: True if the title matches the expected title, False otherwise.
        """
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to get the title.")
            # Wait for the page to be fully loaded
            self.page.wait_for_load_state("load", timeout=timeout)
            # Get the actual title of the page
            actual_title = self.page.title()
            if not actual_title:
                logger.error("Failed to retrieve the page title.")
                return False
            # Strip whitespace for comparison
            actual_title = actual_title.strip()
            expected_title = expected_title.strip()
            # Assert the title matches
            if actual_title == expected_title:
                logger.info(
                    f"Asserted title successfully. The page title matches the expected title: '{expected_title}'."
                )
                return True
            else:
                logger.error(
                    f"Assertion failed. The page title does not match the expected title. "
                    f"Expected: '{expected_title}', Actual: '{actual_title}'."
                )
                return False
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to assert the page title. Error: {e}")
            return False

    def waitForStable(self, seconds: int = 3):
        logger.info(f"Waiting for {seconds} seconds to ensure application stability...")
        sleep(seconds)

    def uploadFile(
        self, page_name: str, element_name: str, file_path: str, timeout: int = 60000
    ) -> bool:
        """
        Uploads a file to a specified element on a page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to upload the file to.
            file_path (str): The path of the file to upload.
            timeout (int): Timeout for locating the element (default is 60000 ms).
        Returns:
            bool: True if the file is uploaded successfully.
        Raises:
            Exception: If the file upload fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            element = self.getElement(locator, timeout)
            element.set_input_files(file_path)
            logger.info(
                f"Successfully uploaded file '{file_path}' to element '{element_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to upload file '{file_path}' to element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to upload file '{file_path}' to element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def uploadMultipleFiles(
        self,
        page_name: str,
        element_name: str,
        file_paths: list,
        timeout: int = 60000,
    ) -> None:
        """
        Uploads multiple files to a specified file input element.
        Args:
            page_name (str): The name of the page containing the file input element.
            element_name (str): The name of the file input element.
            file_paths (list): A list of file paths to upload.
            timeout (int): Timeout in milliseconds to wait for the file input element (default is 60000).
        Raises:
            Exception: If the file upload fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Validate file paths
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")
            # Locate the file input element
            element = self.getElement(locator, timeout)
            # Upload the files
            element.set_input_files(file_paths)
            logger.info(
                f"Successfully uploaded files '{file_paths}' to element '{element_name}' on page '{page_name}'."
            )
        except FileNotFoundError as e:
            logger.error(f"File not found during upload. Error: {e}")
            raise Exception(f"File not found during upload. Error: {e}")
        except Exception as e:
            logger.error(
                f"Failed to upload files '{file_paths}' to element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to upload files '{file_paths}' to element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def downloadFile(
        self, page_name: str, element_name: str, timeout: int = 60000
    ) -> str:
        """
        Downloads a file by clicking an element, saves it to the 'downloads' folder, and returns the file name.
        Args:
            page_name (str): The name of the page in the locators JSON.
            element_name (str): The name of the element in the locators JSON that triggers the download.
            timeout (int): Timeout in milliseconds to wait for the download (default is 60000).
        Returns:
            str: The name of the downloaded file if successful.
        Raises:
            Exception: If the file download fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        downloads_folder = os.path.join(
            os.path.dirname(__file__), "..", "downloads"
        )  # Relative path to 'downloads' folder
        try:
            # Ensure the downloads folder exists
            if not os.path.exists(downloads_folder):
                os.makedirs(downloads_folder)
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to handle downloads.")
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                logger.error(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Set up the download event handler
            with self.page.expect_download() as download_info:
                # Click the element to trigger the download
                element.click()
            # Wait for the download to complete
            download = download_info.value
            # Get the file name from the download object
            downloaded_file_name = download.suggested_filename
            # Save the file to the 'downloads' folder
            download_path = os.path.join(downloads_folder, downloaded_file_name)
            download.save_as(download_path)
            logger.info(
                f"Successfully downloaded file '{downloaded_file_name}' to '{download_path}' from element '{element_name}' on page '{page_name}'."
            )
            return downloaded_file_name
        except TypeError as te:
            logger.error(f"Type error: {te}")
            raise Exception(f"Type error: {te}")
        except Exception as e:
            logger.error(
                f"Failed to download file from element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to download file from element '{element_name}' on page '{page_name}'. Error: {e}"
            )

    def dragAndDrop(
        self,
        page_name: str,
        source_element_name: str,
        target_element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Drags an element from a source location and drops it onto a target location.
        Args:
            page_name (str): The name of the page containing the elements.
            source_element_name (str): The name of the source element to drag.
            target_element_name (str): The name of the target element to drop onto.
            timeout (int): Timeout in milliseconds to wait for the elements (default is 60000).
        Returns:
            bool: True if the drag-and-drop action is successful.
        Raises:
            Exception: If the drag-and-drop action fails.
        """
        source_locator = self.locator_manager.get_locator(
            page_name, source_element_name
        )
        target_locator = self.locator_manager.get_locator(
            page_name, target_element_name
        )
        try:
            source_element = self.getElement(source_locator, timeout)
            target_element = self.getElement(target_locator, timeout)
            source_element.drag_to(target_element)
            logger.info(
                f"Successfully dragged element '{source_element_name}' and dropped it onto '{target_element_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to drag element '{source_element_name}' and drop it onto '{target_element_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to drag element '{source_element_name}' and drop it onto '{target_element_name}' on page '{page_name}'. Error: {e}"
            )

    def takeScreenshot(self, file_path: str, full_page: bool = True) -> bool:
        try:
            if not isinstance(self.page, Page):
                raise TypeError("self.page must be a Page object to take a screenshot.")
            self.page.screenshot(path=file_path, full_page=full_page)
            logger.info(f"Screenshot saved at: {file_path}")
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(f"Failed to take screenshot. Error: {e}")
            return False

    def takeElementScreenshot(
        self, page_name: str, element_name: str, file_path: str, timeout: int = 60000
    ) -> bool:
        """
        Captures a screenshot of a specific element on the page.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to capture the screenshot of.
            file_path (str): The file path where the screenshot will be saved.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the screenshot is captured successfully.
        Raises:
            Exception: If capturing the screenshot fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            if element is None:
                raise Exception(
                    f"Element '{element_name}' not found on page '{page_name}'."
                )
            # Scroll the element into view if it's not visible
            element.scroll_into_view_if_needed(timeout=timeout)
            # Capture the screenshot of the element
            element.screenshot(path=file_path)
            logger.info(f"Element screenshot saved at: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to take element screenshot. Error: {e}")
            raise Exception(f"Failed to take element screenshot. Error: {e}")

    def getTableRowCount(
        self, page_name: str, table_name: str, timeout: int = 60000
    ) -> int:
        """
        Retrieves the row count of a specified table on the page.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to get the row count from.
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            int: The number of rows in the table.
        Raises:
            Exception: If retrieving the row count fails.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Get the row count by counting the number of <tr> elements within the table
            row_count = table.locator("tr").count()
            logger.info(
                f"Row count for table '{table_name}' on page '{page_name}': {row_count}"
            )
            return row_count
        except Exception as e:
            logger.error(
                f"Failed to get row count for table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to get row count for table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def getTableColumnCount(
        self, page_name: str, table_name: str, timeout: int = 60000
    ) -> int:
        """
        Retrieves the column count of a specified table on the page.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to get the column count from.
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            int: The number of columns in the table.
        Raises:
            Exception: If retrieving the column count fails.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Get the first row of the table to determine the column count
            first_row = table.locator("tr").first
            if first_row is None:
                raise Exception(
                    f"Failed to retrieve the first row of table '{table_name}' on page '{page_name}'."
                )
            # Count the number of <td> or <th> elements in the first row
            column_count = first_row.locator("th, td").count()
            logger.info(
                f"Column count for table '{table_name}' on page '{page_name}': {column_count}"
            )
            return column_count
        except Exception as e:
            logger.error(
                f"Failed to get column count for table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to get column count for table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def getTableCellValue(
        self,
        page_name: str,
        table_name: str,
        row_index: int,
        column_index: int,
        timeout: int = 60000,
    ) -> str:
        """
        Retrieves the value of a specific cell in a table.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to retrieve the cell value from.
            row_index (int): The 0-based index of the row.
            column_index (int): The 0-based index of the column.
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            str: The value of the specified cell.
        Raises:
            Exception: If retrieving the cell value fails.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Locate the specific row
            rows = table.locator("tr")
            if row_index >= rows.count():
                raise Exception(
                    f"Row index {row_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total rows: {rows.count()}."
                )
            row = rows.nth(row_index)
            # Locate the specific cell in the row
            cells = row.locator("th, td")
            if column_index >= cells.count():
                raise Exception(
                    f"Column index {column_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total columns: {cells.count()}."
                )
            cell = cells.nth(column_index)
            # Get the text content of the cell
            cell_value = cell.text_content()
            if cell_value is None:
                raise Exception(
                    f"Failed to retrieve the value of cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'."
                )
            logger.info(
                f"Successfully retrieved cell value: '{cell_value.strip()}' from row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'."
            )
            return cell_value.strip()
        except Exception as e:
            logger.error(
                f"Failed to retrieve cell value from row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to retrieve cell value from row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def clickTableCell(
        self,
        page_name: str,
        table_name: str,
        row_index: int,
        column_index: int,
        timeout: int = 60000,
    ) -> bool:
        """
        Clicks a specific cell in a table.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to click the cell in.
            row_index (int): The 0-based index of the row.
            column_index (int): The 0-based index of the column.
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            bool: True if the cell is clicked successfully.
        Raises:
            Exception: If clicking the cell fails.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Locate the specific row
            rows = table.locator("tr")
            if row_index >= rows.count():
                raise Exception(
                    f"Row index {row_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total rows: {rows.count()}."
                )
            row = rows.nth(row_index)
            # Locate the specific cell in the row
            cells = row.locator("th, td")
            if column_index >= cells.count():
                raise Exception(
                    f"Column index {column_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total columns: {cells.count()}."
                )
            cell = cells.nth(column_index)
            # Scroll the cell into view if it's not visible
            cell.scroll_into_view_if_needed(timeout=timeout)
            # Click the cell
            cell.click()
            logger.info(
                f"Successfully clicked cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to click cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to click cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def doubleClickTableCell(
        self,
        page_name: str,
        table_name: str,
        row_index: int,
        column_index: int,
        timeout: int = 60000,
    ) -> bool:
        """
        Double-clicks a specific cell in a table.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to double-click the cell in.
            row_index (int): The 0-based index of the row.
            column_index (int): The 0-based index of the column.
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            bool: True if the cell is double-clicked successfully.
        Raises:
            Exception: If double-clicking the cell fails.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Locate the specific row
            rows = table.locator("tr")
            if row_index >= rows.count():
                raise Exception(
                    f"Row index {row_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total rows: {rows.count()}."
                )
            row = rows.nth(row_index)
            # Locate the specific cell in the row
            cells = row.locator("th, td")
            if column_index >= cells.count():
                raise Exception(
                    f"Column index {column_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total columns: {cells.count()}."
                )
            cell = cells.nth(column_index)
            # Scroll the cell into view if it's not visible
            cell.scroll_into_view_if_needed(timeout=timeout)
            # Double-click the cell
            cell.dblclick()
            logger.info(
                f"Successfully double-clicked cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to double-click cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to double-click cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def enterTextInTableCell(
        self,
        page_name: str,
        table_name: str,
        row_index: int,
        column_index: int,
        text: str,
        clear_first: bool = True,
        timeout: int = 60000,
    ) -> bool:
        """
        Enters text into a specific table cell.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to enter text into.
            row_index (int): The 0-based index of the row.
            column_index (int): The 0-based index of the column.
            text (str): The text to enter into the cell.
            clear_first (bool): Whether to clear existing text before entering new text (default is True).
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            bool: True if the text is entered successfully, False otherwise.
        Raises:
            Exception: If entering text into the table cell fails, stopping script execution.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Locate the specific row
            rows = table.locator("tr")
            if row_index >= rows.count():
                raise Exception(
                    f"Row index {row_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total rows: {rows.count()}."
                )
            row = rows.nth(row_index)
            # Locate the specific cell in the row
            cells = row.locator("th, td")
            if column_index >= cells.count():
                raise Exception(
                    f"Column index {column_index} is out of bounds for table '{table_name}' on page '{page_name}'. Total columns: {cells.count()}."
                )
            cell = cells.nth(column_index)
            # Scroll the cell into view if it's not visible
            cell.scroll_into_view_if_needed(timeout=timeout)
            # Clear the cell text if required
            if clear_first:
                cell.fill("")
            # Enter the new text
            cell.fill(text)
            logger.info(
                f"Successfully entered text '{text}' in cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'."
            )
            return True
        except Exception as e:
            # Log the error and raise the exception to stop the script
            logger.error(
                f"Failed to enter text '{text}' in cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to enter text '{text}' in cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def searchTextInTable(
        self,
        page_name: str,
        table_name: str,
        search_text: str,
        timeout: int = 60000,
    ) -> tuple:
        """
        Searches for a specific text within a table.
        Args:
            page_name (str): The name of the page containing the table.
            table_name (str): The name of the table to search.
            search_text (str): The text to search for within the table.
            timeout (int): Timeout in milliseconds to wait for the table (default is 60000).
        Returns:
            tuple: A tuple (found: bool, row_index: int, column_index: int) indicating if the text was found and its position.
        Raises:
            Exception: If there is an error during the search process.
        """
        locator = self.locator_manager.get_locator(page_name, table_name)
        try:
            # Get the table element using the locator
            table = self.getElement(locator, timeout)
            if table is None:
                raise Exception(
                    f"Table '{table_name}' not found on page '{page_name}'."
                )
            # Get all rows in the table
            rows = table.locator("tr")
            for row_index in range(rows.count()):
                row = rows.nth(row_index)
                # Get all cells in the row
                cells = row.locator("th, td")
                for column_index in range(cells.count()):
                    cell = cells.nth(column_index)
                    cell_text = cell.text_content()
                    if cell_text is not None and search_text in cell_text.strip():
                        logger.info(
                            f"Found text '{search_text}' in cell at row {row_index}, column {column_index} in table '{table_name}' on page '{page_name}'."
                        )
                        return (True, row_index, column_index)
            # If text not found, return False
            logger.warning(
                f"Text '{search_text}' not found in table '{table_name}' on page '{page_name}'."
            )
            return (False, -1, -1)
        except Exception as e:
            logger.error(
                f"Failed to search text '{search_text}' in table '{table_name}' on page '{page_name}'. Error: {e}"
            )
            raise Exception(
                f"Failed to search text '{search_text}' in table '{table_name}' on page '{page_name}'. Error: {e}"
            )

    def generateRandomString(
        self,
        length: int = 8,
    ) -> str:
        """
        Generates a random string containing only letters (uppercase and lowercase).
        Args:
            length (int): The length of the random string to generate. Default is 8.
        Returns:
            str: The generated random string.
        Raises:
            ValueError: If the provided length is less than or equal to 0.
        """
        try:
            if length <= 0:
                raise ValueError("Length must be greater than 0.")
            # Generate a random string of the specified length
            random_string = "".join(random.choices(string.ascii_letters, k=length))
            logger.info(f"Generated random string: {random_string}")
            return random_string
        except Exception as e:
            logger.error(f"Failed to generate random string. Error: {e}")
            raise Exception(f"Failed to generate random string. Error: {e}")

    def generateRandomNumber(
        self,
        min_value: int = 0,
        max_value: int = 100,
    ) -> int:
        """
        Generates a random integer within the specified range.
        Args:
            min_value (int): The minimum value for the random number (inclusive). Default is 0.
            max_value (int): The maximum value for the random number (inclusive). Default is 100.
        Returns:
            int: The generated random number.
        Raises:
            ValueError: If min_value is greater than max_value.
        """
        try:
            if min_value > max_value:
                raise ValueError("min_value must not be greater than max_value.")
            # Generate a random number between min_value and max_value
            random_number = random.randint(min_value, max_value)
            logger.info(f"Generated random number: {random_number}")
            return random_number
        except Exception as e:
            logger.error(f"Failed to generate random number. Error: {e}")
            raise Exception(f"Failed to generate random number. Error: {e}")

    def generateRandomEmail(
        self,
        domain: str = "example.com",
        length: int = 8,
    ) -> str:
        """
        Generates a random email address.
        Args:
            domain (str): The domain for the email address (e.g., "example.com"). Default is "example.com".
            length (int): The length of the random string used for the email username. Default is 8.
        Returns:
            str: The generated random email address.
        Raises:
            ValueError: If the length is less than or equal to 0.
        """
        try:
            if length <= 0:
                raise ValueError("Length must be greater than 0.")

            # Generate a random string for the email username
            username = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            email = f"{username}@{domain}"
            logger.info(f"Generated random email: {email}")
            return email
        except Exception as e:
            logger.error(f"Failed to generate random email. Error: {e}")
            raise Exception(f"Failed to generate random email. Error: {e}")

    def generateRandomAlphanumeric(
        self,
        length: int = 8,
    ) -> str:
        """
        Generates a random alphanumeric string.
        Args:
            length (int): The length of the random alphanumeric string to generate. Default is 8.
        Returns:
            str: The generated random alphanumeric string.
        Raises:
            ValueError: If the provided length is less than or equal to 0.
        """
        try:
            if length <= 0:
                raise ValueError("Length must be greater than 0.")
            # Generate a random alphanumeric string of the specified length
            random_alphanumeric = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            logger.info(f"Generated random alphanumeric string: {random_alphanumeric}")
            return random_alphanumeric
        except Exception as e:
            logger.error(f"Failed to generate random alphanumeric string. Error: {e}")
            raise Exception(
                f"Failed to generate random alphanumeric string. Error: {e}"
            )

    def generateDate(
        self,
        format: str = "dd/mm/yyyy",
    ) -> str:
        """
        Generates the current date in one of the supported formats.
        Args:
            format (str): The format of the date. Supported formats:
                        - "dd/mm/yyyy" -> Example: "11/08/2026"
                        - "mm/dd/yyyy" -> Example: "08/11/2026"
                        - "dd-mm-yyyy" -> Example: "11-08-2026"
                        - "mm-dd-yyyy" -> Example: "08-11-2026"
        Returns:
            str: The generated date.
        Raises:
            ValueError: If the provided format is unsupported.
        """
        try:
            # Map supported formats to their corresponding strftime format
            supported_formats = {
                "dd/mm/yyyy": "%d/%m/%Y",
                "mm/dd/yyyy": "%m/%d/%Y",
                "dd-mm-yyyy": "%d-%m-%Y",
                "mm-dd-yyyy": "%m-%d-%Y",
            }
            # Check if the format is supported
            if format not in supported_formats:
                raise ValueError(
                    f"Unsupported format '{format}'. Supported formats are: {', '.join(supported_formats.keys())}"
                )
            # Generate the current date in the specified format
            current_date = datetime.now().strftime(supported_formats[format])
            logger.info(f"Generated date in format '{format}': {current_date}")
            return current_date
        except Exception as e:
            logger.error(f"Failed to generate date in format '{format}'. Error: {e}")
            raise Exception(f"Failed to generate date in format '{format}'. Error: {e}")

    def generateTimestamp(
        self,
        format: str = "%Y-%m-%d_%H-%M-%S",
    ) -> str:
        """
        Generates a current timestamp in the specified format.
        Args:
            format (str): The format of the timestamp. Default is "%Y-%m-%d_%H-%M-%S".
                        Example formats:
                        - "%Y-%m-%d_%H-%M-%S" -> "2026-08-11_14-30-45"
                        - "%d/%m/%Y %H:%M:%S" -> "11/08/2026 14:30:45"
                        - "%Y%m%d%H%M%S" -> "20260811143045"
        Returns:
            str: The generated timestamp.
        Raises:
            ValueError: If the provided format is invalid.
        """
        try:
            # Generate the current timestamp
            timestamp = datetime.now().strftime(format)
            logger.info(f"Generated timestamp: {timestamp}")
            return timestamp
        except Exception as e:
            logger.error(f"Failed to generate timestamp. Error: {e}")
            raise Exception(f"Failed to generate timestamp. Error: {e}")

    def moveMouse(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Moves the mouse to a specified element.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to move the mouse to.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the mouse move action is successful, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError(
                    "self.page must be a Page object to perform mouse operations."
                )
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Get the bounding box of the element
            bounding_box = element.bounding_box()
            if bounding_box is None:
                logger.error(
                    f"Failed to get bounding box for element '{element_name}' on page '{page_name}'."
                )
                return False
            # Move the mouse to the center of the element
            x = bounding_box["x"] + bounding_box["width"] / 2
            y = bounding_box["y"] + bounding_box["height"] / 2
            self.page.mouse.move(x, y)
            logger.info(
                f"Successfully moved the mouse to element '{element_name}' on page '{page_name}'."
            )
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(
                f"Failed to move the mouse to element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def mouseClick(
        self,
        page_name: str,
        element_name: str,
        timeout: int = 60000,
    ) -> bool:
        """
        Moves the mouse to a specified element and performs a click action.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to move the mouse to and click.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
        Returns:
            bool: True if the mouse click action is successful, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Ensure self.page is a Page object, not a Frame
            if not isinstance(self.page, Page):
                raise TypeError(
                    "self.page must be a Page object to perform mouse actions."
                )
            # Get the element using the locator
            element = self.getElement(locator, timeout)
            # Scroll the element into view
            element.scroll_into_view_if_needed(timeout=timeout)
            # Wait for the element to be visible
            element.wait_for(state="visible", timeout=timeout)
            # Get the bounding box of the element
            bounding_box = element.bounding_box()
            if bounding_box is None:
                logger.error(
                    f"Failed to get bounding box for element '{element_name}' on page '{page_name}'."
                )
                return False
            # Move the mouse to the center of the element
            x = bounding_box["x"] + bounding_box["width"] / 2
            y = bounding_box["y"] + bounding_box["height"] / 2
            self.page.mouse.move(x, y)
            # Perform the click action
            self.page.mouse.click(x, y)
            logger.info(
                f"Successfully clicked on element '{element_name}' on page '{page_name}'."
            )
            return True
        except TypeError as te:
            logger.error(f"Type error: {te}")
            return False
        except Exception as e:
            logger.error(
                f"Failed to click on element '{element_name}' on page '{page_name}'. Error: {e}"
            )
            return False

    def mouseWheel(
        self,
        page_name: str,
        scroll_amount: int,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page using mouse wheel with multiple attempts.
        Args:
            page_name (str): The name of the page to scroll.
            scroll_amount (int): Amount to scroll each time.
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll action is successful, False otherwise.
        """
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} on page '{page_name}'."
                )
                page.mouse.wheel(0, scroll_amount)  # Use the main Page object to scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll
            logger.info(f"Successfully scrolled on page '{page_name}'.")
            return True
        except Exception as e:
            logger.error(
                f"Failed to scroll on page '{page_name}' using mouse wheel. Error: {e}"
            )
            return False

    def mouseWheelToElement(
        self,
        page_name: str,
        element_name: str,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page to a specific element using mouse wheel with multiple attempts.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to scroll to.
            scroll_amount (int): Amount to scroll each time.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll action is successful, False otherwise.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            # Check if the element is already visible
            element = self.getElement(locator, timeout)
            if element and element.is_visible():
                logger.info(
                    f"Element '{element_name}' is already visible on page '{page_name}'. No need to scroll."
                )
                return True
            # If the element is not visible, scroll to find it
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to locate the element."
                )
                page.mouse.wheel(0, scroll_amount)  # Use the main Page object to scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll
                # Check if the element is visible after scrolling
                element = self.getElement(locator, timeout)
                if element and element.is_visible():
                    logger.info(
                        f"Element '{element_name}' found on page '{page_name}' after {attempt + 1} scroll attempts."
                    )
                    return True
            # If the loop completes and the element is still not visible
            logger.warning(
                f"Failed to locate element '{element_name}' on page '{page_name}' after {scrolls} scroll attempts."
            )
            return False
        except Exception as e:
            logger.error(
                f"Failed to scroll to element '{element_name}' on page '{page_name}' using mouse wheel. Error: {e}"
            )
            return False

    def mouseWheelAndClickElement(
        self,
        page_name: str,
        element_name: str,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page to a specific element using mouse wheel with multiple attempts and clicks the element once visible.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to scroll to and click.
            scroll_amount (int): Amount to scroll each time.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll and click action are successful.
            Raises:
                Exception: If the element is not found or the click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            # Check if the element is already visible
            element = self.getElement(locator, timeout)
            if element and element.is_visible():
                logger.info(
                    f"Element '{element_name}' is already visible on page '{page_name}'. Clicking the element."
                )
                element.click()
                return True
            # If the element is not visible, scroll to find it
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to locate the element."
                )
                page.mouse.wheel(0, scroll_amount)  # Use the main Page object to scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll
                # Check if the element is visible after scrolling
                element = self.getElement(locator, timeout)
                if element and element.is_visible():
                    logger.info(
                        f"Element '{element_name}' found on page '{page_name}' after {attempt + 1} scroll attempts. Clicking the element."
                    )
                    element.click()
                    return True
            # If the loop completes and the element is still not visible
            error_message = f"Failed to locate and click element '{element_name}' on page '{page_name}' after {scrolls} scroll attempts."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to scroll to and click element '{element_name}' on page '{page_name}' using mouse wheel. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def mouseWheelAndDoubleClickElement(
        self,
        page_name: str,
        element_name: str,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page to a specific element using mouse wheel with multiple attempts and double-clicks the element once visible.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to scroll to and double-click.
            scroll_amount (int): Amount to scroll each time.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll and double-click action are successful.
            Raises:
                Exception: If the element is not found or the double-click action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            # Check if the element is already visible
            element = self.getElement(locator, timeout)
            if element and element.is_visible():
                logger.info(
                    f"Element '{element_name}' is already visible on page '{page_name}'. Double-clicking the element."
                )
                element.dblclick()
                return True
            # If the element is not visible, scroll to find it
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to locate the element."
                )
                page.mouse.wheel(0, scroll_amount)  # Use the main Page object to scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll

                # Check if the element is visible after scrolling
                element = self.getElement(locator, timeout)
                if element and element.is_visible():
                    logger.info(
                        f"Element '{element_name}' found on page '{page_name}' after {attempt + 1} scroll attempts. Double-clicking the element."
                    )
                    element.dblclick()
                    return True
            # If the loop completes and the element is still not visible
            error_message = f"Failed to locate and double-click element '{element_name}' on page '{page_name}' after {scrolls} scroll attempts."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to scroll to and double-click element '{element_name}' on page '{page_name}' using mouse wheel. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def mouseWheelAndClickByText(
        self,
        text: str,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page using mouse wheel with multiple attempts and clicks on an element containing the specified text.
        Args:
            text (str): The text to locate the element by.
            scroll_amount (int): Amount to scroll each time.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll and click action are successful.
            Raises:
                Exception: If the element containing the text is not found or the click action fails.
        """
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to locate the element containing text: '{text}'."
                )
                page.mouse.wheel(
                    0, scroll_amount
                )  # Scroll downward using the main Page object
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll
                # Locate the element containing the specified text
                element = page.get_by_text(text, exact=True)
                if element.is_visible():
                    logger.info(
                        f"Element containing text '{text}' found after {attempt + 1} scroll attempts. Clicking the element."
                    )
                    element.click()
                    return True
            # If the loop completes and the element is still not visible
            error_message = f"Failed to locate and click the element containing text '{text}' after {scrolls} scroll attempts."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to scroll to and click the element containing text '{text}' using mouse wheel. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def mouseWheelAndEnterText(
        self,
        page_name: str,
        element_name: str,
        text: str,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
        clear_first: bool = True,
    ) -> bool:
        """
        Scrolls the page to a specific element using mouse wheel with multiple attempts and enters text into the element once visible.
        Args:
            page_name (str): The name of the page containing the element.
            element_name (str): The name of the element to scroll to and enter text into.
            text (str): The text to enter into the element.
            scroll_amount (int): Amount to scroll each time.
            timeout (int): Timeout in milliseconds to wait for the element (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
            clear_first (bool): Whether to clear the existing text before entering new text (default is True).
        Returns:
            bool: True if the scroll and text entry action are successful.
            Raises:
                Exception: If the element is not found or the text entry action fails.
        """
        locator = self.locator_manager.get_locator(page_name, element_name)
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            # Check if the element is already visible
            element = self.getElement(locator, timeout)
            if element and element.is_visible():
                logger.info(
                    f"Element '{element_name}' is already visible on page '{page_name}'. Entering text into the element."
                )
                if clear_first:
                    element.fill("")  # Clear existing text
                element.fill(text)
                return True
            # If the element is not visible, scroll to find it
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to locate the element."
                )
                page.mouse.wheel(0, scroll_amount)  # Use the main Page object to scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll

                # Check if the element is visible after scrolling
                element = self.getElement(locator, timeout)
                if element and element.is_visible():
                    logger.info(
                        f"Element '{element_name}' found on page '{page_name}' after {attempt + 1} scroll attempts. Entering text into the element."
                    )
                    if clear_first:
                        element.fill("")  # Clear existing text
                    element.fill(text)
                    return True
            # If the loop completes and the element is still not visible
            error_message = f"Failed to locate and enter text into element '{element_name}' on page '{page_name}' after {scrolls} scroll attempts."
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Failed to scroll to and enter text into element '{element_name}' on page '{page_name}' using mouse wheel. Error: {e}"
            logger.error(error_message)
            raise Exception(error_message)

    def mouseWheelToTop(
        self,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page to the top using mouse wheel with multiple attempts.
        Args:
            scroll_amount (int): Amount to scroll each time (negative value for upward scroll).
            timeout (int): Timeout in milliseconds to wait for the page stabilization (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll action is successful, False otherwise.
        """
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to move to the top of the page."
                )
                page.mouse.wheel(0, -scroll_amount)  # Negative value for upward scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll

                # Check if the page has reached the top
                current_scroll_position = page.evaluate("window.scrollY")
                if current_scroll_position == 0:
                    logger.info(
                        f"Successfully scrolled to the top of the page after {attempt + 1} scroll attempts."
                    )
                    return True
            # If the loop completes and the page is still not at the top
            logger.warning(
                f"Failed to scroll to the top of the page after {scrolls} scroll attempts."
            )
            return False
        except Exception as e:
            logger.error(
                f"Failed to scroll to the top of the page using mouse wheel. Error: {e}"
            )
            return False

    def mouseWheelToBottom(
        self,
        scroll_amount: int,
        timeout: int = 60000,
        scrolls: int = 10,
        wait_time: int = 3,
    ) -> bool:
        """
        Scrolls the page to the bottom using mouse wheel with multiple attempts.
        Args:
            scroll_amount (int): Amount to scroll each time.
            timeout (int): Timeout in milliseconds to wait for the page stabilization (default is 60000).
            scrolls (int): Number of times to scroll the page (default is 10).
            wait_time (int): Time to wait after each scroll (default is 3 seconds).
        Returns:
            bool: True if the scroll action is successful, False otherwise.
        """
        try:
            # Ensure self.page is a Page object
            page = (
                self.page if isinstance(self.page, Page) else self.page.page
            )  # Get the main Page object if self.page is a Frame
            for attempt in range(scrolls):
                logger.info(
                    f"Scrolling attempt {attempt + 1}/{scrolls} to move to the bottom of the page."
                )
                page.mouse.wheel(0, scroll_amount)  # Positive value for downward scroll
                time.sleep(
                    wait_time
                )  # Wait for the page to stabilize after each scroll
                # Check if the page has reached the bottom
                current_scroll_position = page.evaluate("window.scrollY")
                total_height = page.evaluate("document.body.scrollHeight")
                viewport_height = (
                    page.viewport_size["height"] if page.viewport_size else 0
                )
                if current_scroll_position + viewport_height >= total_height:
                    logger.info(
                        f"Successfully scrolled to the bottom of the page after {attempt + 1} scroll attempts."
                    )
                    return True
            # If the loop completes and the page is still not at the bottom
            logger.warning(
                f"Failed to scroll to the bottom of the page after {scrolls} scroll attempts."
            )
            return False
        except Exception as e:
            logger.error(
                f"Failed to scroll to the bottom of the page using mouse wheel. Error: {e}"
            )
            return False

    def convertStringToInt(self, string_value: str) -> int:
        """
        Converts a string to an integer.
        Args:
            string_value (str): The string value to convert.
        Returns:
            int: The converted integer value.
        Raises:
            Exception: If the conversion fails.
        """
        try:
            # Attempt to convert the string to an integer
            int_value = int(string_value)
            logger.info(
                f"Successfully converted string '{string_value}' to integer: {int_value}"
            )
            return int_value
        except ValueError as ve:
            logger.error(
                f"Failed to convert string '{string_value}' to integer. Error: {ve}"
            )
            raise Exception(
                f"Failed to convert string '{string_value}' to integer. Error: {ve}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while converting string '{string_value}' to integer. Error: {e}"
            )
            raise Exception(
                f"An unexpected error occurred while converting string '{string_value}' to integer. Error: {e}"
            )

    def convertStringToDouble(self, string_value: str) -> float:
        """
        Converts a string to a double (floating-point number).
        Args:
            string_value (str): The string value to convert.
        Returns:
            float: The converted double value.
        Raises:
            Exception: If the conversion fails.
        """
        try:
            # Attempt to convert the string to a double (float)
            double_value = float(string_value)
            logger.info(
                f"Successfully converted string '{string_value}' to double: {double_value}"
            )
            return double_value
        except ValueError as ve:
            logger.error(
                f"Failed to convert string '{string_value}' to double. Error: {ve}"
            )
            raise Exception(
                f"Failed to convert string '{string_value}' to double. Error: {ve}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while converting string '{string_value}' to double. Error: {e}"
            )
            raise Exception(
                f"An unexpected error occurred while converting string '{string_value}' to double. Error: {e}"
            )

    def convertIntToString(self, int_value: int) -> str:
        """
        Converts an integer to a string.
        Args:
            int_value (int): The integer value to convert.
        Returns:
            str: The converted string value.
        Raises:
            Exception: If the conversion fails.
        """
        try:
            # Attempt to convert the integer to a string
            string_value = str(int_value)
            logger.info(
                f"Successfully converted integer '{int_value}' to string: '{string_value}'"
            )
            return string_value
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while converting integer '{int_value}' to string. Error: {e}"
            )
            raise Exception(
                f"An unexpected error occurred while converting integer '{int_value}' to string. Error: {e}"
            )

    def convertDoubleToString(self, double_value: float) -> str:
        """
        Converts a double (floating-point number) to a string.
        Args:
            double_value (float): The double value to convert.
        Returns:
            str: The converted string value.
        Raises:
            Exception: If the conversion fails.
        """
        try:
            # Attempt to convert the double to a string
            string_value = str(double_value)
            logger.info(
                f"Successfully converted double '{double_value}' to string: '{string_value}'"
            )
            return string_value
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while converting double '{double_value}' to string. Error: {e}"
            )
            raise Exception(
                f"An unexpected error occurred while converting double '{double_value}' to string. Error: {e}"
            )

    def convertDoubleToInt(self, double_value: float) -> int:
        """
        Converts a double (floating-point number) to an integer.
        Args:
            double_value (float): The double value to convert.
        Returns:
            int: The converted integer value.
        Raises:
            Exception: If the conversion fails.
        """
        try:
            # Attempt to convert the double to an integer
            int_value = int(double_value)
            logger.info(
                f"Successfully converted double '{double_value}' to integer: {int_value}"
            )
            return int_value
        except ValueError as ve:
            logger.error(
                f"Failed to convert double '{double_value}' to integer. Error: {ve}"
            )
            raise Exception(
                f"Failed to convert double '{double_value}' to integer. Error: {ve}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while converting double '{double_value}' to integer. Error: {e}"
            )
            raise Exception(
                f"An unexpected error occurred while converting double '{double_value}' to integer. Error: {e}"
            )

    def roundOff(self, number: float, decimal_places: int = 2) -> float:
        """
        Rounds off a floating-point number to the specified number of decimal places.

        Args:
            number (float): The number to round off.
            decimal_places (int): The number of decimal places to round to (default is 2).

        Returns:
            float: The rounded-off number.

        Raises:
            ValueError: If the `decimal_places` is less than 0.
        """
        try:
            if decimal_places < 0:
                raise ValueError("The number of decimal places must be 0 or greater.")
            # Round off the number
            rounded_number = round(number, decimal_places)
            logger.info(
                f"Successfully rounded off {number} to {decimal_places} decimal places: {rounded_number}"
            )
            return rounded_number
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            raise Exception(f"Validation error: {ve}")
        except Exception as e:
            logger.error(f"An error occurred while rounding off the number. Error: {e}")
            raise Exception(
                f"An error occurred while rounding off the number. Error: {e}"
            )

    def replaceStringValue(
        self, original_string: str, old_value: str, new_value: str
    ) -> str:
        """
        Replaces occurrences of a specified substring within a string with a new substring.

        Args:
            original_string (str): The original string to perform the replacement on.
            old_value (str): The substring to be replaced.
            new_value (str): The substring to replace with.

        Returns:
            str: The string with the replaced values.

        Raises:
            ValueError: If the `old_value` is an empty string.
        """
        try:
            if old_value == "":
                raise ValueError(
                    "The substring to be replaced cannot be an empty string."
                )
            # Replace the old_value with new_value in the original_string
            replaced_string = original_string.replace(old_value, new_value)
            logger.info(
                f"Successfully replaced '{old_value}' with '{new_value}' in the string. Result: {replaced_string}"
            )
            return replaced_string
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            raise Exception(f"Validation error: {ve}")
        except Exception as e:
            logger.error(f"An error occurred while replacing string values. Error: {e}")
            raise Exception(
                f"An error occurred while replacing string values. Error: {e}"
            )

    def stringAppend(self, original_string: str, append_value: str) -> str:
        """
        Appends a specified substring to the end of an original string.

        Args:
            original_string (str): The original string to append to.
            append_value (str): The substring to append to the original string.

        Returns:
            str: The updated string with the appended value.
        """
        try:
            # Append the new value to the original string
            updated_string = original_string + append_value
            logger.info(
                f"Successfully appended '{append_value}' to the original string. Result: {updated_string}"
            )
            return updated_string
        except Exception as e:
            logger.error(f"An error occurred while appending string values. Error: {e}")
            raise Exception(
                f"An error occurred while appending string values. Error: {e}"
            )

    def numberAppend(
        self, original_value: Union[str, float, int], number: float
    ) -> str:
        """
        Appends a specified number to the end of an original string or number.

        Args:
            original_value (Union[str, float, int]): The original value (can be a string or a number).
            number (float): The number to append to the original value.

        Returns:
            str: The updated string with the appended number.
        """
        try:
            # Convert original_value to a string if it's a number
            if isinstance(original_value, (int, float)):
                original_value = str(original_value)

            # Convert the number to a string
            number_string = str(number)

            # Append the number string to the original string
            updated_string = original_value + number_string
            logger.info(
                f"Successfully appended number '{number}' to the original value. Result: {updated_string}"
            )
            return updated_string
        except Exception as e:
            logger.error(
                f"An error occurred while appending number to value. Error: {e}"
            )
            raise Exception(
                f"An error occurred while appending number to value. Error: {e}"
            )

    def cleanCurrencyValue(
        self, currency_string: str, currency_symbol: str = "USD"
    ) -> float:
        """
        Cleans up a currency string by removing commas and the specified currency symbol, returning the numerical value.
        Args:
            currency_string (str): The currency string to clean up.
            currency_symbol (str): The currency symbol to remove (default is "USD").
        Returns:
            float: The cleaned numerical value.
        Raises:
            ValueError: If the cleaned string cannot be converted to a float.
        """
        try:
            # Remove commas from the string
            cleaned_string = currency_string.replace(",", "")
            # Remove the currency symbol from the string
            cleaned_string = cleaned_string.replace(currency_symbol, "").strip()
            # Convert the cleaned string to a float
            numerical_value = float(cleaned_string)
            logger.info(
                f"Successfully cleaned currency string '{currency_string}'. Result: {numerical_value}"
            )
            return numerical_value
        except ValueError as ve:
            logger.error(f"Failed to convert cleaned string to float. Error: {ve}")
            raise Exception(f"Failed to convert cleaned string to float. Error: {ve}")
        except Exception as e:
            logger.error(
                f"An error occurred while cleaning currency string. Error: {e}"
            )
            raise Exception(
                f"An error occurred while cleaning currency string. Error: {e}"
            )

    def cleanAndExtractNumber(self, value: str) -> Union[int, float]:
        """
        Cleans up a string by removing %, $, spaces, and commas, and returns the numerical value.
        If the cleaned value is an integer, it returns an integer. If it's a float, it returns a float.
        Args:
            value (str): The string to clean up.
        Returns:
            Union[int, float]: The cleaned numerical value as an integer or float.
        Raises:
            ValueError: If the cleaned string cannot be converted to a number.
        """
        try:
            # Remove % and $ symbols, spaces, and commas from the string
            cleaned_value = (
                value.replace("%", "")
                .replace("$", "")
                .replace(",", "")
                .replace(" ", "")
            )
            # Convert the cleaned string to a float
            numerical_value = float(cleaned_value)
            # Check if the number is an integer (e.g., 100 instead of 100.0)
            if numerical_value.is_integer():
                numerical_value = int(numerical_value)
            logger.info(
                f"Successfully cleaned value '{value}'. Result: {numerical_value}"
            )
            return numerical_value
        except ValueError as ve:
            logger.error(f"Failed to convert cleaned value to a number. Error: {ve}")
            raise ValueError(
                f"Failed to convert cleaned value to a number. Error: {ve}"
            )
        except Exception as e:
            logger.error(
                f"An error occurred while cleaning and extracting number. Error: {e}"
            )
            raise Exception(
                f"An error occurred while cleaning and extracting number. Error: {e}"
            )
