from tracemalloc import start

from numpy import rint
from playwright.sync_api import Page, expect
import time
import logging

from conftest import page
from utils.utils import wait_for_element

logger = logging.getLogger("playwright_pytest")


class HomePageFAS_AFF_ASA_AFX:
    nw = 3
    sw = 5
    mw = 10
    lw = 20
    bw = 50

    def __init__(self, page: Page):
        self.page = page
        self._initialize_locators()

    def _initialize_locators(self):
        self.productName = self.page.locator("#im-selectTemplateType").get_by_text(
            "FAS/AFF/ASA/AFX"
        )
        self.addHaPair = self.page.get_by_role("button", name="Add HA Pair")
        self.configureButton = self.page.get_by_role("button", name="Configure")
        self.storageTab = self.page.get_by_role("tab", name="Storage")
        self.tabNICsandAdapters = self.page.get_by_role("tab", name="NICs and Adapters")
        self.backToClusterManager = self.page.get_by_role(
            "button", name="Back To Cluster Manager"
        )
        self.servicesTab = self.page.get_by_role("tab", name="Services")
        self.switchesTab = self.page.get_by_role("tab", name="Switches")
        self.IsThisATechRefresh = self.page.get_by_role(
            "group", name="Is this a tech refresh?"
        ).get_by_label("No", exact=True)
        self.doesYourCustomerRequireBlueXP = self.page.get_by_role(
            "group", name="Does your Customer require"
        ).get_by_label("No", exact=True)
        self.doesYourCustomerNeedPSONTAP = self.page.get_by_role(
            "group", name="Does your Customer need PS to"
        ).get_by_label("No", exact=True)
        self.doYouWantToAddRansomwareRecoveryAssurance = self.page.get_by_role(
            "group", name="Do you want to add the"
        ).get_by_label("No", exact=True)
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")
        self.saveButton = self.page.get_by_role("button", name="Save")
        self.productsTab = self.page.get_by_role("tab", name=" Products")

    def clickProductName(self, product_name):
        if product_name == "FAS/AFF/ASA/AFX":
            wait_for_element(self.productName)
            self.productName.click()
            time.sleep(self.nw)
        else:
            raise ValueError(f"Invalid product name: {product_name}")

    def selectSubProduct(self, sub_Product):
        if sub_Product == "FAS/AFF Advanced Configure Flow":
            self.page.get_by_role("option", name="FAS/AFF/ASA/AFX").wait_for(
                state="visible", timeout=60000
            )
            self.page.get_by_role("option", name="FAS/AFF/ASA/AFX").click()
            self.page.get_by_role("row", name="FAS/AFF Advanced Configure").get_by_role(
                "link"
            ).click()
            time.sleep(self.nw)
        else:
            raise ValueError(f"Invalid sub product name: {sub_Product}")

    def configureCluster(self, cluster):
        # Parameterized XPath
        xpath = f"//div[@class='selectorTile' and text()='{cluster}']"
        self.page.locator(xpath).wait_for(state="visible", timeout=60000)
        self.page.locator(xpath).click()
        self.page.get_by_role("button", name="Next").click()
        time.sleep(self.lw)

    def access_SelectAll(self):
        self.page.get_by_role("tab", name="Access").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("tab", name="Access").click()
        self.page.get_by_role("checkbox", name="Select All").check()
        time.sleep(self.nw)
        self.page.get_by_role("tab", name="Cluster Manager").click()
        time.sleep(self.nw)

    def selectSystemModel(self, model: str):
        self.page.get_by_role("combobox", name="Model", exact=True).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Model", exact=True).click()
        self.page.get_by_role("combobox", name="Model", exact=True).fill(model)
        self.page.get_by_text(model).click()
        time.sleep(self.nw)

    def clickAddHaPair(self):
        wait_for_element(self.addHaPair)
        self.addHaPair.click()
        time.sleep(self.nw)

    def clickConfigureButton(self):
        wait_for_element(self.configureButton)
        self.configureButton.click()
        time.sleep(self.lw)

    def clickStorageTab(self):
        wait_for_element(self.storageTab)
        self.storageTab.click()
        time.sleep(self.sw)

    def selectDriveType_BaseStorage(self, driveType: str):
        self.page.get_by_role("combobox", name="Drive Type").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Drive Type").click()
        self.page.get_by_role("combobox", name="Drive Type").fill(driveType)
        self.page.get_by_text(driveType).click()
        time.sleep(self.sw)

    def enterDrivePackQty_BaseStorage(self, qty: int):
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").click()
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").fill(str(qty))
        self.page.get_by_role("spinbutton", name="Drive Pack Qty").press("Tab")
        time.sleep(self.sw)

    def clickTabNICsandAdapters(self):
        wait_for_element(self.tabNICsandAdapters)
        self.tabNICsandAdapters.click()
        time.sleep(self.nw)

    def selectCableType_Adapters(self, cable: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableType"
        ).first.wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableType"
        ).first.dblclick()
        # self.page.locator("[id=\"networkAdapterCableType|input\"]").dblclick()
        self.page.locator(
            '[id="oj-searchselect-filter-networkAdapterCableType|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-networkAdapterCableType|input"]'
        ).fill(cable)
        self.page.get_by_text(cable, exact=True).click()
        time.sleep(self.sw)

    def selectCableLength_Adapters(self, cableLength: str):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableLength"
        ).first.wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableLength"
        ).first.click()
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-networkAdapterCableLength"
        ).first.dblclick()
        # self.page.locator("[id=\"networkAdapterCableLength|input\"]").dblclick()
        self.page.locator(
            '[id="oj-searchselect-filter-networkAdapterCableLength|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-networkAdapterCableLength|input"]'
        ).fill(cableLength)
        self.page.get_by_text(cableLength).click()
        time.sleep(self.sw)

    def selectCableType_BaseConnectivity(self, cableType_BaseConnectivity: str):
        self.page.wait_for_selector(
            '[id="baseConnectivityCableType|input"]',
            state="visible",
            timeout=60000,
        )
        self.page.locator('[id="baseConnectivityCableType|input"]').click()
        time.sleep(self.nw)
        self.page.locator(
            '[id="oj-searchselect-filter-baseConnectivityCableType|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-baseConnectivityCableType|input"]'
        ).fill(cableType_BaseConnectivity)
        self.page.get_by_text(cableType_BaseConnectivity, exact=True).click()
        time.sleep(self.sw)

    def selectMode_BaseConnectivity(self, mode_BaseConnectivity: str):
        self.page.get_by_role("combobox", name="Mode", exact=True).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Mode", exact=True).click()
        time.sleep(self.nw)
        self.page.get_by_role("combobox", name="Mode", exact=True).click()
        self.page.get_by_role("combobox", name="Mode", exact=True).fill(
            mode_BaseConnectivity
        )
        self.page.get_by_text(mode_BaseConnectivity).click()
        time.sleep(self.sw)

    def selectCableLength_BaseConnectivity(self, cableLength_BaseConnectivity: str):
        self.page.locator('[id="baseConnectivityCableLength|input"]').wait_for(
            state="visible", timeout=60000
        )
        self.page.locator('[id="baseConnectivityCableLength|input"]').click()
        time.sleep(self.nw)
        self.page.locator(
            '[id="oj-searchselect-filter-baseConnectivityCableLength|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-baseConnectivityCableLength|input"]'
        ).fill(cableLength_BaseConnectivity)
        self.page.get_by_text(cableLength_BaseConnectivity).click()
        time.sleep(self.sw)

    def selectType_InterconnectivityCable(self, type_InterconnectivityCable: str):
        self.page.get_by_role("combobox", name="Type", exact=True).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Type", exact=True).click()
        time.sleep(self.nw)
        self.page.get_by_role("combobox", name="Type", exact=True).click()
        self.page.get_by_role("combobox", name="Type", exact=True).fill(
            type_InterconnectivityCable
        )
        self.page.get_by_text(type_InterconnectivityCable, exact=True).click()
        time.sleep(self.sw)

    def selectLength_InterconnectivityCable(self, length_InterconnectivityCable: str):
        self.page.get_by_role("combobox", name="Length", exact=True).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Length", exact=True).click()
        time.sleep(self.nw)
        self.page.get_by_role("combobox", name="Length", exact=True).click()
        self.page.get_by_role("combobox", name="Length", exact=True).fill(
            length_InterconnectivityCable
        )
        self.page.get_by_text(length_InterconnectivityCable).click()
        time.sleep(self.sw)

    def selectShelfType_StorageShelves(self, shelfType_StorageShelves: str):
        self.page.get_by_role("gridcell").nth(1).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(1).click()
        time.sleep(self.nw)
        self.page.locator('[id="shelfType|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-shelfType|input"]').click()
        self.page.locator('[id="oj-searchselect-filter-shelfType|input"]').fill(
            shelfType_StorageShelves
        )
        self.page.get_by_text(shelfType_StorageShelves).click()
        time.sleep(self.sw)

    def enterShelfQty_StorageShelves(self, shelfQty_StorageShelves: int):
        self.page.get_by_role("gridcell", name="0").first.wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell", name="0").first.click()
        time.sleep(self.nw)
        self.page.locator('[id="shelfQuantity|input"]').click()
        self.page.locator('[id="shelfQuantity|input"]').fill(
            str(shelfQty_StorageShelves)
        )
        self.page.locator('[id="shelfQuantity|input"]').press("Tab")
        time.sleep(self.sw)

    def selectDriveType_StorageShelves(self, driveType_StorageShelves: str):
        self.page.locator('[id="extDrivePackType|input"]').wait_for(
            state="visible", timeout=60000
        )
        self.page.locator('[id="extDrivePackType|input"]').click()
        time.sleep(self.nw)
        self.page.locator(
            '[id="oj-searchselect-filter-extDrivePackType|input"]'
        ).dblclick()
        self.page.locator('[id="oj-searchselect-filter-extDrivePackType|input"]').fill(
            driveType_StorageShelves
        )
        self.page.get_by_text(driveType_StorageShelves).click()
        time.sleep(self.sw)

    def enterDrivePackQty_StorageShelves(self, drivePackQty_StorageShelves: int):
        self.page.locator(
            "(//div[contains(@class, 'cpq-table-data-cell') and contains(@class, 'type-number') and contains(@class, 'oj-selected')])[2]"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            "(//div[contains(@class, 'cpq-table-data-cell') and contains(@class, 'type-number') and contains(@class, 'oj-selected')])[2]"
        ).click()
        time.sleep(self.nw)
        self.page.locator('[id="extDrivePackTypeQty|input"]').click()
        self.page.locator('[id="extDrivePackTypeQty|input"]').fill(
            str(drivePackQty_StorageShelves)
        )
        self.page.locator('[id="extDrivePackTypeQty|input"]').press("Tab")
        time.sleep(self.sw)

    def enterControllerToStorageCableLenth_StorageCables(
        self, controllerToStorageCableLenth_StorageCables: str
    ):
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-storageCableLength"
        ).wait_for(state="visible", timeout=60000)
        self.page.locator(
            ".cpq-table-data-cell.oj-table-data-cell.oj-form-control-inherit.col-storageCableLength"
        ).click()
        time.sleep(self.nw)
        self.page.locator('[id="storageCableLength|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-storageCableLength|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-storageCableLength|input"]'
        ).fill(controllerToStorageCableLenth_StorageCables)
        self.page.get_by_text(controllerToStorageCableLenth_StorageCables).click()
        time.sleep(self.sw)

    def clickBackToClusterManager(self):
        wait_for_element(self.backToClusterManager)
        self.backToClusterManager.click()
        time.sleep(self.lw)

    def clickServicesTab(self):
        wait_for_element(self.servicesTab)
        self.servicesTab.click()
        time.sleep(self.nw)

    def clickSwitchesTab(self):
        wait_for_element(self.switchesTab)
        self.switchesTab.click()
        time.sleep(self.nw)

    def clickIsThisATechRefresh(self):
        wait_for_element(self.IsThisATechRefresh)
        self.IsThisATechRefresh.click()
        time.sleep(self.nw)

    def clickDoesYourCustomerRequireBlueXP(self):
        wait_for_element(self.doesYourCustomerRequireBlueXP)
        self.doesYourCustomerRequireBlueXP.click()
        time.sleep(self.nw)

    def clickDoesYourCustomerNeedPSONTAP(self):
        wait_for_element(self.doesYourCustomerNeedPSONTAP)
        self.doesYourCustomerNeedPSONTAP.click()
        time.sleep(self.nw)

    def clickDoYouWantToAddRansomwareRecoveryAssurance(self):
        wait_for_element(self.doYouWantToAddRansomwareRecoveryAssurance)
        self.doYouWantToAddRansomwareRecoveryAssurance.click()
        time.sleep(self.nw)

    def selectIncludeSwitch_Yes(self):
        self.page.locator("#includeAClusterSwitch-yes").wait_for(
            state="visible", timeout=60000
        )
        self.page.locator("#includeAClusterSwitch-yes").click()
        time.sleep(self.nw)

    def selectType_Cluster_BackendSwitch(self, type_Cluster_BackendSwitch: str):
        self.page.locator('[id="clusterSwitchType|input"]').wait_for(
            state="visible", timeout=60000
        )
        self.page.locator('[id="clusterSwitchType|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitchType|input"]'
        ).click()
        self.page.locator('[id="oj-searchselect-filter-clusterSwitchType|input"]').fill(
            type_Cluster_BackendSwitch
        )
        self.page.get_by_text(type_Cluster_BackendSwitch, exact=True).click()
        time.sleep(self.nw)

    def selectPortCount_Cluster_BackendSwitch(
        self, portCount_Cluster_BackendSwitch: str
    ):
        self.page.get_by_role("combobox", name="Port Count").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Port Count").click()
        self.page.get_by_role("combobox", name="Port Count").fill(
            str(portCount_Cluster_BackendSwitch)
        )
        self.page.get_by_text(str(portCount_Cluster_BackendSwitch), exact=True).click()
        time.sleep(self.nw)

    def selectSpeed_Cluster_BackendSwitch(self, speed_Cluster_BackendSwitch: str):
        self.page.get_by_role("combobox", name="Speed (Gbps)").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Speed (Gbps)").click()
        self.page.get_by_role("combobox", name="Speed (Gbps)").click()
        self.page.get_by_role("combobox", name="Speed (Gbps)").fill(
            str(speed_Cluster_BackendSwitch)
        )
        self.page.get_by_text(str(speed_Cluster_BackendSwitch), exact=True).click()
        time.sleep(self.nw)

    def selectClusterInterconnectCable_Switch(
        self, clusterInterconnectCable_Switch: str
    ):
        self.page.get_by_role("gridcell").nth(1).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(1).dblclick()
        # self.page.locator('[id="clusterSwitchInterconnectCable|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitchInterconnectCable|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitchInterconnectCable|input"]'
        ).fill(clusterInterconnectCable_Switch)
        self.page.get_by_text(clusterInterconnectCable_Switch, exact=True).click()
        time.sleep(self.nw)

    def selectType_ClusterInterconnectCable_Switch(
        self, type_ClusterInterconnectCable_Switch: str
    ):
        self.page.get_by_role("gridcell").nth(3).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(3).click()
        self.page.locator('[id="clusterSwitch10GbeCableType|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitch10GbeCableType|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitch10GbeCableType|input"]'
        ).fill(type_ClusterInterconnectCable_Switch)
        self.page.get_by_text(type_ClusterInterconnectCable_Switch, exact=True).click()
        time.sleep(self.nw)

    def selectLength_ClusterInterconnectCable_Switch(
        self, length_ClusterInterconnectCable_Switch: str
    ):
        self.page.get_by_role("gridcell").nth(4).wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell").nth(4).click()
        self.page.locator('[id="clusterSwitch10GbeCableLength|input"]').click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitch10GbeCableLength|input"]'
        ).click()
        self.page.locator(
            '[id="oj-searchselect-filter-clusterSwitch10GbeCableLength|input"]'
        ).fill(length_ClusterInterconnectCable_Switch)
        self.page.get_by_text(
            length_ClusterInterconnectCable_Switch, exact=True
        ).click()
        time.sleep(self.nw)

    def enterQty_ClusterInterconnectCable_Switch(
        self, qty_ClusterInterconnectCable_Switch: int
    ):
        self.page.get_by_role("gridcell", name="0").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("gridcell", name="0").click()
        self.page.locator('[id="clusterSwitch10GbeCableQty|input"]').click()
        self.page.locator('[id="clusterSwitch10GbeCableQty|input"]').click()
        self.page.locator('[id="clusterSwitch10GbeCableQty|input"]').fill(
            str(qty_ClusterInterconnectCable_Switch)
        )
        self.page.locator('[id="clusterSwitch10GbeCableQty|input"]').press("Tab")
        time.sleep(self.nw)

    def selectWhatCableLengthDoYouWant_Switch(
        self, whatCableLengthDoYouWant_Switch: str
    ):
        self.page.get_by_role(
            "combobox", name="What cable length do you want?"
        ).wait_for(state="visible", timeout=60000)
        self.page.get_by_role("combobox", name="What cable length do you want?").click()
        self.page.get_by_role("combobox", name="What cable length do you want?").click()
        self.page.get_by_role("combobox", name="What cable length do you want?").fill(
            whatCableLengthDoYouWant_Switch
        )
        self.page.get_by_text(whatCableLengthDoYouWant_Switch).click()
        time.sleep(self.nw)

    def selectResponseTime_ClusterBackendInterconnectSwitchServices(
        self, responseTime_ClusterBackendInterconnectSwitchServices: str
    ):
        self.page.get_by_role("combobox", name="Response Time").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Response Time").click()
        self.page.get_by_role("combobox", name="Response Time").click()
        self.page.get_by_role("combobox", name="Response Time").fill(
            responseTime_ClusterBackendInterconnectSwitchServices
        )
        self.page.get_by_text(
            responseTime_ClusterBackendInterconnectSwitchServices
        ).click()
        time.sleep(self.nw)

    def selectServiceLevel_ClusterBackendInterconnectSwitchServices(
        self, serviceLevel_ClusterBackendInterconnectSwitchServices: str
    ):
        self.page.get_by_role("combobox", name="Service Level").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Service Level").click()
        self.page.get_by_role("combobox", name="Service Level").click()
        self.page.get_by_role("combobox", name="Service Level").fill(
            serviceLevel_ClusterBackendInterconnectSwitchServices
        )
        self.page.get_by_text(
            serviceLevel_ClusterBackendInterconnectSwitchServices
        ).click()
        time.sleep(self.nw)

    def selectTerm_ClusterBackendInterconnectSwitchServices(
        self, term_ClusterBackendInterconnectSwitchServices: str
    ):
        self.page.get_by_role("combobox", name="Term").wait_for(
            state="visible", timeout=60000
        )
        self.page.get_by_role("combobox", name="Term").click()
        self.page.get_by_role("combobox", name="Term").click()
        self.page.get_by_role("combobox", name="Term").fill(
            str(term_ClusterBackendInterconnectSwitchServices)
        )
        self.page.get_by_text(
            str(term_ClusterBackendInterconnectSwitchServices), exact=True
        ).click()
        time.sleep(self.nw)

    def clickAddToQuote(self):
        wait_for_element(self.addToQuote)
        self.addToQuote.click()
        time.sleep(self.lw)

    def get_AddToQuote_NavigationTime(self):
        self.addToQuote.wait_for(state="visible", timeout=60000)
        print("[STEP] Measuring navigation time from Add To Quote → Product Page")
        start = time.perf_counter()
        print(f"[INFO] Start time: {start:.4f}")
        self.addToQuote.click()
        print("[ACTION] Clicked Add To Quote button")
        print("[WAIT] Waiting for Product Page element.......")
        self.productsTab.wait_for(state="visible", timeout=90000)
        end = time.perf_counter()
        print(f"[INFO] End time: {end:.4f}")
        elapsed = round(end - start, 2)
        print(
            f"[RESULT] AddToQuote to Products Page Navigation completed in {elapsed} seconds"
        )
        return elapsed

    def clickSaveButton(self):
        wait_for_element(self.saveButton)
        self.saveButton.click()
        time.sleep(self.mw)
