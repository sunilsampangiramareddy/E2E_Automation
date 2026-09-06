import time
import logging
from decimal import Decimal
from datetime import date
from playwright.sync_api import Page
from utils.utils import wait_for_element


logger = logging.getLogger("playwright_pytest")


class DeveloperConsole:
    nw = 2
    sw = 5
    mw = 10
    lw = 20

    def __init__(self, page: Page):
        self.page = page
        self.query_editor_textarea = page.locator("textarea#queryEditorText-inputEl")
        # Execute button ID is stable - lives in the Query Editor sub-tab
        self.execute_button = page.locator("button#queryExecuteButton-btnEl")

    def enter_query(self, query: str):
        wait_for_element(self.query_editor_textarea)
        self.query_editor_textarea.click()
        self.query_editor_textarea.fill(query)
        time.sleep(self.nw)

    def execute_query(self):
        wait_for_element(self.execute_button)
        self.execute_button.click()
        time.sleep(self.sw)

    def _active_results_grid(self):
        """Locate the SOQL query results grid specifically (not the Logs traceGrid
        or the History executehistory grid, which also carry the x-grid class).
        Older result tabs remain in the DOM with display:none after each new query,
        so we must filter to the currently visible header, not just match by text."""
        header = self.page.locator("span.x-panel-header-text:visible").filter(
            has_text="Query Results"
        )
        wait_for_element(header)
        header.wait_for(state="visible")
        if header.count() > 1:
            header = header.last
        grid = header.locator("xpath=ancestor::div[contains(@class,'x-grid')][1]")
        return grid

    def _edit_cell(self, row_locator, column_id: str, field_name: str, new_value: str):
        """Double-click a cell to spawn its inline editor, then set the value.
        Uses Enter (not Tab) to commit, since Tab in ExtJS grid editors often
        auto-advances the floating editor to the next cell instead of closing it,
        which then blocks subsequent dblclicks with an intercepting overlay."""
        cell = row_locator.locator(f"td.x-grid-cell-{column_id} .x-grid-cell-inner")
        cell.dblclick()
        time.sleep(self.nw)
        editor_input = self.page.locator(f'input[name="{field_name}"]:visible')
        wait_for_element(editor_input)
        editor_input.fill(new_value)
        editor_input.press("Enter")
        time.sleep(self.nw)
        # Explicitly close any lingering editor overlay before moving to the next cell
        self.page.keyboard.press("Escape")
        time.sleep(self.nw / 2)

    def click_save_rows(self):
        grid = self._active_results_grid()
        save_button = grid.get_by_role("button", name="Save Rows")
        wait_for_element(save_button)
        save_button.click()

    def markQuoteAsBooked(
        self,
        quote_name: str,
        quote_status: str,
        order_status: str,
        booked_date: str = None,
    ):
        """Mark a quote as booked, setting Booked_Date__c, Order_Status__c, and Status.
        booked_date defaults to today's date in YYYY-MM-DD format, matching the
        format Salesforce displays for this field (e.g. '2026-07-09')."""
        if booked_date is None:
            booked_date = date.today().isoformat()  # e.g. "2026-07-14"

        query = (
            f"SELECT Id,Booked_Date__c,Order_Status__c,Status FROM Quote "
            f"WHERE Name = '{quote_name}'"
        )
        self.enter_query(query)
        self.execute_query()

        grid = self._active_results_grid()
        row = grid.locator("tr.x-grid-row").first
        wait_for_element(row)

        # gridcolumn IDs are also dynamic - find the right column by header text instead
        self._edit_cell(
            row, self._column_id(grid, "Booked_Date__c"), "Booked_Date__c", booked_date
        )
        self._edit_cell(
            row,
            self._column_id(grid, "Order_Status__c"),
            "Order_Status__c",
            order_status,
        )
        self._edit_cell(row, self._column_id(grid, "Status"), "Status", quote_status)

        self.click_save_rows()

    def _column_id(self, grid, header_text: str) -> str:
        """Resolve the dynamic gridcolumn-N id from its header text.
        Note: the header text lives in a <span class="x-column-header-text">,
        not a <div> - the surrounding <div class="x-column-header-inner"> also
        contains 'x-column-header' as a substring, so the ancestor xpath must
        explicitly exclude it to land on the correct gridcolumn-N container."""
        header = grid.locator(f"span.x-column-header-text:text-is('{header_text}')")
        wait_for_element(header)
        col_id = header.locator(
            "xpath=ancestor::div[contains(@class,'x-column-header') "
            "and not(contains(@class,'x-column-header-inner'))][1]"
        ).get_attribute("id")
        return col_id

    def get_DealScore_value(self, query: str, column_name: str) -> str:
        """Run the provided SOQL query and return the first-row value of the requested column."""
        query_text = str(query).strip()
        field_name = str(column_name).strip()

        if not query_text:
            raise ValueError("Query cannot be empty")
        if not field_name:
            raise ValueError("Column name cannot be empty")

        self.enter_query(query_text)
        self.execute_query()

        grid = self._active_results_grid()
        row = grid.locator("tr.x-grid-row").first
        wait_for_element(row)

        col_id = self._column_id(grid, field_name)
        cell = row.locator(f"td.x-grid-cell-{col_id} .x-grid-cell-inner").first
        wait_for_element(cell)

        value = cell.inner_text().strip()
        logger.info(f"Fetched value for column={field_name}: {value}")
        return value

    def get_cumulative_deal_score_values(
        self,
        quote_numbers: list,
        column_name_1: str,
        column_name_2: str,
        column_name_3: str,
        column_name_4: str,
    ) -> dict:
        """Aggregate DDS Deal Score values across the provided quote numbers."""
        cumulative_Deal_Score_To_2 = Decimal("0.00")
        cumulative_Deal_Score_To_3 = Decimal("0.00")
        cumulative_Deal_Score_To_4 = Decimal("0.00")
        cumulative_Deal_Score_To_5 = Decimal("0.00")

        for quote_number in quote_numbers:
            query = (
                "SELECT ID, Quote_Number_CPQ__c,Deal_Score_To_2_Net_USD__c,"
                "Deal_Score_To_3_Net_USD__c,Deal_Score_To_4_Net_USD__c,"
                "Deal_Score_To_5_Net_USD__c "
                f"FROM Quote WHERE Quote_Number_CPQ__c = '{quote_number}'"
            )

            Deal_Score_To_2 = self.get_DealScore_value(query, column_name_1)
            logger.info(f"Fetched value for Deal_Score_To_2 ({quote_number}): {Deal_Score_To_2}")
            print(f"ℹ️ Developer console fetched value for Deal_Score_To_2 ({quote_number}): {Deal_Score_To_2}")

            Deal_Score_To_3 = self.get_DealScore_value(query, column_name_2)
            logger.info(f"Fetched value for Deal_Score_To_3 ({quote_number}): {Deal_Score_To_3}")
            print(f"ℹ️ Developer console fetched value for Deal_Score_To_3 ({quote_number}): {Deal_Score_To_3}")

            Deal_Score_To_4 = self.get_DealScore_value(query, column_name_3)
            logger.info(f"Fetched value for Deal_Score_To_4 ({quote_number}): {Deal_Score_To_4}")
            print(f"ℹ️ Developer console fetched value for Deal_Score_To_4 ({quote_number}): {Deal_Score_To_4}")

            Deal_Score_To_5 = self.get_DealScore_value(query, column_name_4)
            logger.info(f"Fetched value for Deal_Score_To_5 ({quote_number}): {Deal_Score_To_5}")
            print(f"ℹ️ Developer console fetched value for Deal_Score_To_5 ({quote_number}): {Deal_Score_To_5}")

            cumulative_Deal_Score_To_2 += Decimal(str(Deal_Score_To_2).replace(",", "").strip())
            cumulative_Deal_Score_To_3 += Decimal(str(Deal_Score_To_3).replace(",", "").strip())
            cumulative_Deal_Score_To_4 += Decimal(str(Deal_Score_To_4).replace(",", "").strip())
            cumulative_Deal_Score_To_5 += Decimal(str(Deal_Score_To_5).replace(",", "").strip())

        return {
            "Deal_Score_To_2": cumulative_Deal_Score_To_2,
            "Deal_Score_To_3": cumulative_Deal_Score_To_3,
            "Deal_Score_To_4": cumulative_Deal_Score_To_4,
            "Deal_Score_To_5": cumulative_Deal_Score_To_5,
        }
                    