from locale import currency
from unicodedata import name
from playwright.sync_api import Page, expect
import time
import random
import logging
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class CreateOpportunity:
    nw = 3

    def __init__(self, page: Page):
        self.page = page
        self.searchAccount = page.get_by_role("combobox", name="Account")
        self.nextButton = page.get_by_role("button", name="Next")
        self.opportunityType = page.locator(
            "//select[@class='slds-select' and @name='Opportunity_Type']"
        )
        self.opportunityName = page.locator(
            "//input[@class='slds-input' and @name='Opportunity_Name']"
        )
        self.opportunityName_1p = page.locator(
            "//input[@class='slds-input' and @name='X1P_Opportunity_Name']"
        )
        self.primaryContact = page.locator(
            "//select[@class='slds-select' and @name='Primary_Contact']"
        )
        self.primaryContact_1p = page.locator(
            "//input[@placeholder='Search Primary Contact']"
        )
        self.salesPlay = page.locator(
            "//select[@class='slds-select' and (@name='Sales_Play_NON_Enterprise' or @name='Sales_Play_Enterprise')]"
        )
        self.channel = page.locator(
            "//select[@class='slds-select' and @name='Channel']"
        )
        self.reseller = page.locator(
            "//input[@class='slds-combobox__input slds-input' and @placeholder='Search Accounts...' and @aria-label='Reseller']"
        )
        self.salesType = page.locator(
            "//select[@class='slds-select' and @name='Sales_Motion']"
        )
        self.salesType_1p = page.locator(
            "//select[@name='Sales_Type' and contains(@class, 'slds-select')]"
        )
        self.installedBaseType = page.locator(
            "//select[@class='slds-select' and @name='Installed_Base_Type']"
        )
        self.currency = page.locator(
            "//select[@class='slds-select' and @name='Currency']"
        )
        self.endCustomerUsage = page.locator("//select")
        # self.pathway = page.locator("//select[@class='slds-select' and @name='Pathway']")
        self.pathway = page.locator(
            "//select[@class='slds-select' and (@name='Pathway' or @name='Pathway1' or @name='Pathway0')]"
        )
        self.partnerSalesModel = page.locator(
            "//select[@class='slds-select' and @name='Partner_Sales_Model']"
        )
        self.resellerSalesRep = page.locator(
            "//select[@class='slds-select' and @name='Final_Reseller_Sales_Rep']"
        )
        self.resellerSE = page.locator(
            "//select[@class='slds-select' and @name='FInal_Reseller_SE']"
        )
        self.distributor = page.locator(
            "//select[@class='slds-select' and @name='Distributor_R']"
        )

        self.hyperscaler = page.locator(
            "//select[@name='X1PHyperscaler' and contains(@class, 'slds-select')]"
        )
        self.opportunityNumber = page.locator(
            "//records-highlights-details-item[2]/div/p[2]/slot/lightning-formatted-text"
        )
        self.opptyName = page.locator("//h1/slot/lightning-formatted-text")

    def enterAccount(self, account: str):
        wait_for_element(self.searchAccount)
        self.searchAccount.click()
        self.searchAccount.click()
        time.sleep(self.nw)
        self.searchAccount.fill(str(account))
        time.sleep(self.nw)
        self.page.get_by_role("option", name="Search Show more results for").locator(
            "svg"
        ).click()
        self.page.locator(
            "//tr[1]/td[1]/lightning-primitive-cell-checkbox/span/label/span[1]"
        ).click()
        self.page.get_by_role("button", name="Select").click()

    def clickNextButton(self):
        wait_for_element(self.nextButton)
        self.nextButton.click()

    def clickNextButton_2(self):
        wait_for_element(self.nextButton)
        self.nextButton.click()

    def selectOpportunityType(self, oppotunityType):
        # Wait for the opportunityType dropdown to be visible
        wait_for_element(self.opportunityType)
        # Select the option by value
        self.opportunityType.select_option(oppotunityType)

    def enterOpportunityName(self, opportunity_Name: str):
        random_number = random.randint(10000, 99999)
        full_opportunity_name = f"{opportunity_Name} {random_number}"
        wait_for_element(self.opportunityName)
        self.opportunityName.click()
        self.opportunityName.fill(full_opportunity_name)
        logger.info(f"Entered opportunity name: {full_opportunity_name}")

    def enterOpportunityName_1p(self, opportunity_Name: str):
        random_number = random.randint(10000, 99999)
        full_opportunity_name = f"{opportunity_Name} {random_number}"
        wait_for_element(self.opportunityName_1p)
        self.opportunityName_1p.click()
        self.opportunityName_1p.fill(full_opportunity_name)
        logger.info(f"Entered 1P opportunity name: {full_opportunity_name}")

    def selectPrimaryContact(self, primary_Contact):
        # Wait for the primaryContact dropdown to be visible
        wait_for_element(self.primaryContact)
        # Select the option by value
        self.primaryContact.select_option(primary_Contact)

    def selectPrimaryContact_1p(self, primary_Contact):
        wait_for_element(self.primaryContact_1p)
        self.primaryContact_1p.click()
        self.primaryContact_1p.fill(primary_Contact)
        # Parameterize the XPath with the function argument
        xpath = f"//span[text()='{primary_Contact}']"
        self.page.locator(xpath).click()

    def selectSalesPlay(self, sales_Play):
        # Wait for the salesPlay dropdown to be visible
        wait_for_element(self.salesPlay)
        # Select the option by value
        self.salesPlay.select_option(sales_Play)

    def selectChannel(self, channelOption):
        # Wait for the channel dropdown to be visible
        wait_for_element(self.channel)
        # Select the option by value
        self.channel.select_option(channelOption)

    def selectReseller(self, reseller_Account):
        wait_for_element(self.reseller)
        self.reseller.click()
        self.reseller.fill(str(reseller_Account))
        time.sleep(self.nw)
        self.page.locator(
            "//span[starts-with(@title, 'Show more results for')]"
        ).click()
        self.page.locator(
            "//tr[1]/td[1]/lightning-primitive-cell-checkbox/span/label/span[1]"
        ).click()
        self.page.get_by_role("button", name="Select").click()

    def selectSalesType(self, sales_Type):
        # Wait for the salesType dropdown to be visible
        wait_for_element(self.salesType)
        # Select the option by value
        self.salesType.select_option(sales_Type)

    def selectSalesType_1p(self, sales_Type):
        # Wait for the salestype1p dropdown to be visible
        wait_for_element(self.salesType_1p)
        # Select the option by value
        self.salesType_1p.select_option(sales_Type)

    def selectInstalledBaseType(self, installedBase_Type):
        # Wait for the installedBaseType dropdown to be visible
        wait_for_element(self.installedBaseType)
        # Select the option by value
        self.installedBaseType.select_option(installedBase_Type)

    def selectCurrency(self, currencyType):
        # Wait for the currency dropdown to be visible
        wait_for_element(self.currency)
        # Select the option by value
        self.currency.select_option(currencyType)
        time.sleep(self.nw)

    def selectEndCustomerUsage_option(self, option_value):
        # Wait for the endCustomerUsage dropdown to be visible
        wait_for_element(self.endCustomerUsage)
        # Select the option by value
        self.endCustomerUsage.select_option(option_value)

    def selectPathway(self, pathwayOption):
        # Wait for the pathway dropdown to be visible
        wait_for_element(self.pathway)
        # Select the option by value
        self.pathway.select_option(pathwayOption)

    def selectPartnerSalesModel(self, partnerSalesModelOption):
        # Wait for the partnerSalesModel dropdown to be visible
        wait_for_element(self.partnerSalesModel)
        # Select the option by value
        self.partnerSalesModel.select_option(partnerSalesModelOption)

    def selectResellerSalesRep(self, resellerSalesRepOption):
        # Wait for the resellerSalesRep dropdown to be visible
        wait_for_element(self.resellerSalesRep)
        # Select the option by value
        self.resellerSalesRep.select_option(resellerSalesRepOption)
        time.sleep(self.nw)

    def selectResellerSE(self, resellerSEOption):
        # Wait for the resellerSE dropdown to be visible
        wait_for_element(self.resellerSE)
        # Select the option by value
        self.resellerSE.select_option(resellerSEOption)

    def selectDistributor(self, distributorOption):
        # Wait for the distributor dropdown to be visible
        wait_for_element(self.distributor)
        # Select the option by value
        self.distributor.select_option(distributorOption)

    def selectHyperscaler(self, hyperscalerOption):
        # Wait for the hyperscaler dropdown to be visible
        wait_for_element(self.hyperscaler)
        # Select the option by value
        self.hyperscaler.select_option(hyperscalerOption)

    def captureOpportunityNumber(self):
        wait_for_element(self.opportunityNumber)
        opp_number = self.opportunityNumber.inner_text()
        return opp_number

    def captureOpportunityName(self):
        wait_for_element(self.opptyName)
        opp_name = self.opptyName.inner_text()
        return opp_name
