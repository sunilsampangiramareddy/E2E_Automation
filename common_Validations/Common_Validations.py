import logging
import time
from playwright.sync_api import Page

logger = logging.getLogger("playwright_pytest")


class CommonValidations:
    def __init__(self, page: Page):
        self.page = page
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")

    def collect_table_data(self, xpath: str, column_name: str):
        collected_data = []
        print(f"Collecting {column_name}...")
        logger.info(f"Collecting {column_name}...")
        count = self.page.locator(xpath).count()
        if count == 0:
            logger.warning(f"No elements found for {column_name} with XPath: {xpath}")
            return collected_data
        for node in range(count):
            data = self.page.locator(xpath).nth(node).text_content().strip()
            if data:
                collected_data.append(data)
                print(f"Found {column_name}: {data}")
                logger.info(f"Found {column_name}: {data}")
        print(f"The collected elements in the {column_name} list are:")
        print(collected_data)
        logger.info(
            f"The collected elements in the {column_name} list are: {collected_data}"
        )
        return collected_data

    def readBOMTable_SaveToList(self, column_name):
        xpath_mapping = {
            "Part Number": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_0']",
            "Quantity": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_1']",
            "Description": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_2']",
        }
        xpath = xpath_mapping.get(column_name)
        if not xpath:
            logger.error(f"Invalid column name: {column_name}")
            return []
        return self.collect_table_data(xpath, column_name)

    def readProductTable_SaveToList(self, column_name):
        xpath_mapping = {
            "Product": "//div[contains(@class, 'oj-fa-cx-cpq-fragmentsUI-lineItems-rowHeader oj-sm-align-self-center cx-cpq-line-item-row')]",
            "Qty": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-unitQuantity_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
            "Part Description": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-partDescription_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
        }
        xpath = xpath_mapping.get(column_name)
        if not xpath:
            logger.error(f"Invalid column name: {column_name}")
            return []
        return self.collect_table_data(xpath, column_name)

    def compare_lists(self, list1, list2):
        errors = []
        # Log the lists being compared
        logger.info(f"Comparing lists:\nList1: {list1}\nList2: {list2}")
        if len(list1) != len(list2):
            logger.error("List lengths do not match!")
            errors.append(
                f"Lengths differ: List1 ({len(list1)}) vs List2 ({len(list2)})"
            )
        for i in range(min(len(list1), len(list2))):
            if list1[i] != list2[i]:
                logger.error(f"Mismatch at index {i}: {list1[i]} != {list2[i]}")
                errors.append(f"Mismatch at index {i}: {list1[i]} != {list2[i]}")
        if not errors:
            logger.info("Lists match successfully!")
        return errors

    def is_value_present_in_list(
        self, value_to_check: str, data_list: list, column_name: str
    ) -> bool:
        """
        Checks if a specific text value is present in the given list.

        Args:
            value_to_check (str): The value to search for in the list.
            data_list (list): The list to search within.
            column_name (str): The name of the column (for logging purposes).

        Returns:
            bool: True if the value is found, False otherwise.
        """
        logger.info(
            f"Checking if '{value_to_check}' is present in the {column_name} list..."
        )
        logger.info(f"The {column_name} list contains: {data_list}")
        if value_to_check in data_list:
            logger.info(f"'{value_to_check}' is present in the {column_name} list.")
            return True
        else:
            logger.warning(
                f"'{value_to_check}' is NOT present in the {column_name} list."
            )
            return False
