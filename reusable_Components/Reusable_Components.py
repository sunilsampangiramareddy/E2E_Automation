import logging
from utils.config_reader import ConfigReader
import os
from socket import timeout
import time
from time import sleep
from typing import Literal
import random
import string
from datetime import datetime
from common_Methods.Common_Methods import CommonMethods
from pages_SFDC.Create_Opportunity import CreateOpportunity
from pages_SFDC.Home_Page import HomePage
from utils.screenshot_util import ScreenshotUtil
from playwright.sync_api import (  # type: ignore
    Page,
    Frame,
    BrowserContext,
    TimeoutError as PlaywrightTimeoutError,
)
from utils.locator_manager import LocatorManager
from utils.data_validation import is_valid_data

logger = logging.getLogger("playwright_pytest")


class ReusableComponents:
    nw = 3

    def __init__(self, page: Page, locator_manager: LocatorManager):
        self.page = page
        self.locator_manager = locator_manager
        self.cm = CommonMethods(page, locator_manager)
        self.co = CreateOpportunity(page)
        self.hp = HomePage(page)
        self.ss = ScreenshotUtil(page)

    def loginToSFDC(self, config, test_case: dict, timeout: int = 60000) -> str:
        """
        Logs into the application using the provided credentials.
        Args:
            username (str): The username for login.
            password (str): The password for login.
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            bool: True if login is successful, False otherwise.
        """
        try:
            # Enter the username
            if is_valid_data(test_case["User Name"]):
                self.cm.enterText(
                    "LoginPage",
                    "username_Input",
                    test_case["User Name"],
                    timeout=timeout,
                )
                logger.info(f"Username entered: {test_case["User Name"]}")
            # Click the next button
            self.cm.clickElement("LoginPage", "next_Button", timeout=timeout)
            logger.info("Clicked on the next button")
            # Enter the password
            self.cm.enterText(
                "LoginPage",
                "password_Input",
                config.get_encodedString(),
                timeout=timeout,
            )
            logger.info("Entered password")
            # Click the sign-in button
            self.cm.clickElement("LoginPage", "signin_Button", timeout=timeout)
            logger.info("Clicked on the sign-in button")
            self.cm.clickElement("LoginPage", "yes_Button", timeout=timeout)
            logger.info("Clicked on the 'Yes' button to stay signed in")
            is_visible = self.cm.isElementVisible("HomePage", "opportunities_Label")
            self.cm.assertTrue(
                is_visible, "Opportunities label is visible on the homepage"
            )
            home_page_url = self.cm.getCurrentURL()
            logger.info(f"Login successful, captured homepage URL: {home_page_url}")
            return home_page_url
        except Exception as e:
            logger.error(f"Login failed due to an error: {e}")
            raise e

    def createDirectOpportunity(self, test_case: dict, timeout: int = 60000) -> dict:
        """
        Creates an opportunity using the provided test case details.
        Args:
            test_case (dict): Dictionary containing test case details.
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            dict: Dictionary containing opportunity details (number, name, and URL).
        """
        try:
            # Click on opportunities tab
            self.cm.clickElement("HomePage", "opportunities_Tab", timeout=timeout)
            logger.info("Clicked on opportunities tab")
            # Click on new opportunity button
            self.cm.clickElement("HomePage", "new_Opportunity_Button", timeout=timeout)
            logger.info("Clicked on new opportunity button")
            # Enter account name
            if is_valid_data(test_case["Account Name"]):
                self.co.enterAccount(test_case["Account Name"])
                logger.info(
                    f"Entered and selected account: {test_case['Account Name']}"
                )
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info("Clicked on next button")
            # Select opportunity type
            if is_valid_data(test_case["Opportunity Type"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "opportunity_Type",
                    test_case["Opportunity Type"],
                    timeout=timeout,
                )
                logger.info(
                    f"Selected opportunity type: {test_case['Opportunity Type']}"
                )
            # Enter opportunity name
            if is_valid_data(test_case["Opportunity Name"]):
                self.co.enterOpportunityName(test_case["Opportunity Name"])
                logger.info(f"Entered opportunity name")
            # Select primary contact
            if is_valid_data(test_case["Primary Contact"]):
                self.co.select_PrimaryContact(test_case["Primary Contact"])
                logger.info(f"Selected primary contact: {test_case['Primary Contact']}")
            if is_valid_data(test_case["Sales Type"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "sales_Type",
                    test_case["Sales Type"],
                )
                logger.info(f"Selected sales type: {test_case['Sales Type']}")
            # Select sales play
            if is_valid_data(test_case["Sales Play"]):
                self.cm.clickElement(
                    "CreateOpportunity", "sales_Play_Combobox", timeout=timeout
                )
                self.cm.clickByText(
                    test_case["Sales Play"],
                    timeout=timeout,
                )
                logger.info(f"Selected sales play: {test_case['Sales Play']}")
            # Select channel
            if is_valid_data(test_case["Channel"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "channel",
                    test_case["Channel"],
                    timeout=timeout,
                )
                logger.info(f"Selected channel: {test_case['Channel']}")
            # Select currency
            if is_valid_data(test_case["Currency"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "currency",
                    test_case["Currency"],
                    timeout=timeout,
                )
                logger.info(f"Selected currency: {test_case['Currency']}")
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info("Clicked on next button")
            # Read opportunity number
            oppty_number = self.cm.readText(
                "CreateOpportunity", "opportunity_Number", timeout=timeout
            )
            logger.info(f"Opportunity Number: {oppty_number}")
            # Read opportunity name
            oppty_name = self.cm.readText(
                "CreateOpportunity", "opportunity_Name", timeout=timeout
            )
            logger.info(f"Opportunity Name: {oppty_name}")
            # Get current URL
            oppty_url = self.cm.getCurrentURL()
            logger.info(f"Captured Spark URL: {oppty_url}")
            return {
                "opportunity_number": oppty_number,
                "opportunity_name": oppty_name,
                "opportunity_url": oppty_url,
            }
        except Exception as e:
            logger.error(f"Failed to create opportunity due to an error: {e}")
            raise e

    def createIndirectOpportunity(self, test_case: dict, timeout: int = 60000) -> dict:
        """
        Creates an indirect opportunity using the provided test case details.
        Args:
            test_case (dict): Dictionary containing test case details.
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            dict: Dictionary containing opportunity details (number, name, and URL).
        """
        try:
            # Click on opportunities tab
            self.cm.clickElement("HomePage", "opportunities_Tab", timeout=timeout)
            logger.info(f"Clicked on opportunities tab")
            # Click on new opportunity button
            self.cm.clickElement("HomePage", "new_Opportunity_Button", timeout=timeout)
            logger.info(f"Clicked on new opportunity button")
            # Enter account name
            if is_valid_data(test_case["Account Name"]):
                self.co.enterAccount(test_case["Account Name"])
                logger.info(
                    f"Entered and selected account: {test_case['Account Name']}"
                )
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Select opportunity type
            if is_valid_data(test_case["Opportunity Type"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "opportunity_Type",
                    test_case["Opportunity Type"],
                    timeout=timeout,
                )
                logger.info(
                    f"Selected opportunity type: {test_case['Opportunity Type']}"
                )
            # Enter opportunity name
            if is_valid_data(test_case["Opportunity Name"]):
                self.co.enterOpportunityName(test_case["Opportunity Name"])
                logger.info(f"Entered opportunity name")
            # Select primary contact
            if is_valid_data(test_case["Primary Contact"]):
                self.co.select_PrimaryContact(test_case["Primary Contact"])
                logger.info(f"Selected primary contact: {test_case['Primary Contact']}")
            # Select sales play
            if is_valid_data(test_case["Sales Play"]):
                self.cm.clickElement(
                    "CreateOpportunity", "sales_Play_Combobox", timeout=timeout
                )
                self.cm.clickByText(test_case["Sales Play"], timeout=timeout)
                logger.info(f"Selected sales play: {test_case['Sales Play']}")
            # Select channel
            if is_valid_data(test_case["Channel"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "channel",
                    test_case["Channel"],
                    timeout=timeout,
                )
                logger.info(f"Selected channel: {test_case['Channel']}")
            # Select reseller account
            if is_valid_data(test_case["Reseller Account"]):
                self.co.selectReseller(test_case["Reseller Account"])
                logger.info(
                    f"Entered reseller account: {test_case['Reseller Account']}"
                )
            # Select sales type
            if is_valid_data(test_case["Sales Type"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "sales_Type",
                    test_case["Sales Type"],
                    timeout=timeout,
                )
                logger.info(f"Selected sales type: {test_case['Sales Type']}")
            # Select installed base type
            if is_valid_data(test_case["Installed Base Type"]):
                self.co.selectInstalledBaseType(test_case["Installed Base Type"])
                logger.info(
                    f"Selected installed base type: {test_case['Installed Base Type']}"
                )
            # Select currency
            if is_valid_data(test_case["Currency"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "currency",
                    test_case["Currency"],
                    timeout=timeout,
                )
                logger.info(f"Selected currency: {test_case['Currency']}")
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Select pathway
            if is_valid_data(test_case["Pathway"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "pathway",
                    test_case["Pathway"],
                    timeout=timeout,
                )
                logger.info(f"Selected pathway: {test_case['Pathway']}")
            # Select partner sales model
            if is_valid_data(test_case["Partner Sales Model"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "partner_Sales_Model",
                    test_case["Partner Sales Model"],
                    timeout=timeout,
                )
                logger.info(
                    f"Selected partner sales model: {test_case['Partner Sales Model']}"
                )
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Handle end customer usage
            if self.cm.isElementVisible(
                "CreateOpportunity", "end_Customer_Label", timeout=10000
            ):
                if is_valid_data(test_case["End Customer Usage"]):
                    self.cm.selectOptionInListbox(
                        "CreateOpportunity",
                        "end_Customer_Usage",
                        test_case["End Customer Usage"],
                        timeout=timeout,
                    )
                    logger.info(
                        f"Selected end customer usage: {test_case['End Customer Usage']}"
                    )
                    self.cm.clickElement(
                        "CreateOpportunity", "next_Button", timeout=timeout
                    )
                    logger.info(f"Clicked on next button")
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Select reseller sales rep
            if is_valid_data(test_case["Reseller Sales Rep"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "reseller_Sales_Rep",
                    test_case["Reseller Sales Rep"],
                    timeout=timeout,
                )
                logger.info(
                    f"Selected reseller sales rep: {test_case['Reseller Sales Rep']}"
                )
            # Select reseller SE
            if is_valid_data(test_case["Reseller SE"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "reseller_SE",
                    test_case["Reseller SE"],
                    timeout=timeout,
                )
                logger.info(f"Selected reseller SE: {test_case['Reseller SE']}")
            # Select distributor
            if is_valid_data(test_case["Distributor"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "distributor",
                    test_case["Distributor"],
                    timeout=timeout,
                )
                logger.info(f"Selected distributor: {test_case['Distributor']}")
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Read opportunity details
            oppty_number = self.cm.readText(
                "CreateOpportunity", "opportunity_Number", timeout=timeout
            )
            logger.info(f"Opportunity Number: {oppty_number}")
            oppty_name = self.cm.readText(
                "CreateOpportunity", "opportunity_Name", timeout=timeout
            )
            logger.info(f"Opportunity Name: {oppty_name}")
            spark_url = self.cm.getCurrentURL()
            logger.info(f"Captured Spark URL: {spark_url}")
            # Return opportunity details
            return {
                "opportunity_number": oppty_number,
                "opportunity_name": oppty_name,
                "opportunity_url": spark_url,
            }
        except Exception as e:
            logger.error(f"Failed to create indirect opportunity due to an error: {e}")
            raise e

    def create1POpportunity(self, test_case: dict, timeout: int = 60000) -> dict:
        """
        Creates a 1P opportunity using the provided test case details.
        Args:
            test_case (dict): Dictionary containing test case details.
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            dict: Dictionary containing opportunity details (number, name, and URL).
        """
        try:
            # Click on opportunities tab
            self.cm.clickElement("HomePage", "opportunities_Tab", timeout=timeout)
            logger.info(f"Clicked on opportunities tab")
            # Click on new opportunity button
            self.cm.clickElement("HomePage", "new_Opportunity_Button", timeout=timeout)
            logger.info(f"Clicked on new opportunity button")
            # Enter account name
            if is_valid_data(test_case["Account Name"]):
                self.co.enterAccount(test_case["Account Name"])
                logger.info(
                    f"Entered and selected account: {test_case['Account Name']}"
                )
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Select opportunity type
            if is_valid_data(test_case["Opportunity Type"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "opportunity_Type",
                    test_case["Opportunity Type"],
                    timeout=timeout,
                )
                logger.info(
                    f"Selected opportunity type: {test_case['Opportunity Type']}"
                )
            # Enter opportunity name
            if is_valid_data(test_case["Opportunity Name"]):
                self.co.enterOpportunityName_1p(test_case["Opportunity Name"])
                logger.info(f"Entered opportunity name")
            # Select 1P sales type
            if is_valid_data(test_case["Sales Type"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "sales_Type_1P",
                    test_case["Sales Type"],
                    timeout=timeout,
                )
                logger.info(f"Selected 1P sales type: {test_case['Sales Type']}")
            # Select 1P primary contact
            if is_valid_data(test_case["Primary Contact"]):
                self.co.select_PrimaryContact(test_case["Primary Contact"])
                logger.info(
                    f"Selected 1P primary contact: {test_case['Primary Contact']}"
                )
            # Select hyperscaler
            if is_valid_data(test_case["Hyperscaler"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "hyperscaler",
                    test_case["Hyperscaler"],
                    timeout=timeout,
                )
                logger.info(f"Selected hyperscaler: {test_case['Hyperscaler']}")
            # Select confidential
            if is_valid_data(test_case["Confidential"]):
                self.cm.selectOptionInListbox(
                    "CreateOpportunity",
                    "confidential",
                    test_case["Confidential"],
                    timeout=timeout,
                )
                logger.info(f"Selected confidential: {test_case['Confidential']}")
            # Click next button
            self.cm.clickElement("CreateOpportunity", "next_Button", timeout=timeout)
            logger.info(f"Clicked on next button")
            # Read opportunity number
            oppty_number = self.cm.readText(
                "CreateOpportunity", "opportunity_Number", timeout=timeout
            )
            logger.info(f"Opportunity Number: {oppty_number}")
            # Read opportunity name
            oppty_name = self.cm.readText(
                "CreateOpportunity", "opportunity_Name", timeout=timeout
            )
            logger.info(f"Opportunity Name: {oppty_name}")
            # Get current URL
            spark_url = self.cm.getCurrentURL()
            logger.info(f"Captured Spark URL: {spark_url}")
            # Return opportunity details
            return {
                "opportunity_number": oppty_number,
                "opportunity_name": oppty_name,
                "opportunity_url": spark_url,
            }
        except Exception as e:
            logger.error(f"Failed to create 1P opportunity due to an error: {e}")
            raise e

    def addProductsInSFDC(self, test_case: dict, timeout: int = 60000) -> bool:
        """
        Adds products to an opportunity using the provided test case details.
        Args:
            test_case (dict): Dictionary containing test case details.
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            bool: True if products are added successfully, False otherwise.
        """
        try:
            # Capture the current URL
            spark_url = self.cm.getCurrentURL()
            logger.info(f"Captured Spark URL: {spark_url}")
            # Select product
            if is_valid_data(test_case["Product Name"]):
                self.hp.selectProduct(test_case["Product Name"])
                logger.info(f"Selected product: {test_case['Product Name']}")
            # Enter product price
            if is_valid_data(test_case["Product Price"]):
                self.hp.enterProductPrice(test_case["Product Price"])
                logger.info(f"Entered product price: {test_case['Product Price']}")
            # Navigate back to the captured URL
            self.cm.navigateToUrl(spark_url)
            logger.info(f"Navigated back to Spark URL: {spark_url}")
            # Capture screenshot
            self.ss.capture_screenshot("Captured Opportunity details")
            logger.info("Captured Opportunity details screenshot")
            return True
        except Exception as e:
            logger.error(f"Failed to add products due to an error: {e}")
            raise e  # Raise the exception to fail the script

    def captureOpportunityDetails(self, timeout: int = 60000) -> dict:
        """
        Captures opportunity details such as opportunity number, name, and URL.
        Args:
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            dict: Dictionary containing opportunity details (number, name, and URL).
        """
        try:
            # Read opportunity number
            oppty_number = self.cm.readText(
                "CreateOpportunity", "opportunity_Number", timeout=timeout
            )
            logger.info(f"Opportunity Number: {oppty_number}")
            # Read opportunity name
            oppty_name = self.cm.readText(
                "CreateOpportunity", "opportunity_Name", timeout=timeout
            )
            logger.info(f"Opportunity Name: {oppty_name}")
            # Get current URL
            spark_url = self.cm.getCurrentURL()
            logger.info(f"Captured Spark URL: {spark_url}")
            # Return opportunity details
            return {
                "opportunity_number": oppty_number,
                "opportunity_name": oppty_name,
                "opportunity_url": spark_url,
            }
        except Exception as e:
            logger.error(f"Failed to capture opportunity details due to an error: {e}")
            raise e

    def captureQuoteDetails(self, timeout: int = 60000) -> dict:
        """
        Captures quote details such as quote number, quote name, and CPQ URL.
        Args:
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            dict: Dictionary containing quote details (number, name, and URL).
        """
        try:
            # Read quote number
            quote_number = self.cm.readText(
                "HomePage_CPQ", "quote_Number", timeout=timeout
            )
            logger.info(f"Quote Number: {quote_number}")
            # Read quote name
            quote_name = self.cm.readText("HomePage_CPQ", "quote_Name", timeout=timeout)
            logger.info(f"Quote Name: {quote_name}")
            # Get current CPQ URL
            cpq_url = self.cm.getCurrentURL()
            logger.info(f"Keystone CPQ URL: {cpq_url}")
            # Return quote details
            return {
                "quote_number": quote_number,
                "quote_name": quote_name,
                "cpq_url": cpq_url,
            }
        except Exception as e:
            logger.error(f"Failed to capture quote details due to an error: {e}")
            raise e  # Raise the exception to fail the script

    def personaLogin(self, test_case: dict, timeout: int = 60000) -> bool:
        """
        Logs in as a specific user persona using the provided test case details.
        Args:
            test_case (dict): Dictionary containing test case details (e.g., "User Persona_1").
            timeout (int): Timeout in milliseconds for each action (default is 60000).
        Returns:
            bool: True if persona login is successful, False otherwise.
        """
        try:
            # Click on Setup icon and menu item
            self.cm.clickElement("HomePage", "setup_Icon", timeout=timeout)
            self.cm.clickElement("HomePage", "setup_menu_item", timeout=timeout)
            logger.info("Clicked on Setup icon and menu item")
            # Switch to the second tab
            secondTab = self.cm.switchToTab(
                self.page.context, tab_index=1, expected_tab_count=2
            )
            self.cm.waitForPageLoad(secondTab, timeout=timeout)
            logger.info("Switched to the Setup tab")
            # Update the CommonMethods instance to use the second tab
            self.cm = CommonMethods(secondTab, self.locator_manager)
            # Search for the user persona in Setup
            self.cm.clickElement("GeneralSetup", "search_Setup_Input", timeout=timeout)
            self.cm.enterText(
                "GeneralSetup",
                "search_Setup_Input",
                test_case["User Persona"],
                timeout=timeout,
            )
            self.cm.clickByLinkText(
                test_case["User Persona"],
                partial_match=True,
                occurrence=1,
                timeout=timeout,
            )
            logger.info(f"Searched for user persona: {test_case['User Persona']}")
            # Switch to the frame in Setup
            frame_locator_setup = self.locator_manager.get_locator(
                "HomePage", "frame_Locator"
            )
            self.cm.switchToFrame(frame_locator_setup)
            logger.info("Switched to Setup frame")
            # Click the login button from the Setup frame
            self.cm.page.get_by_role("button", name="Login", exact=True).nth(1).click()
            logger.info("Clicked Login button from Setup frame")
            return True
        except Exception as e:
            logger.error(f"Failed to log in as persona due to an error: {e}")
            raise e  # Raise the exception to fail the script
