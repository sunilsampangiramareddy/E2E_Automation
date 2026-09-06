import os
import logging
import time
import pandas as pd
from playwright.sync_api import Page

logger = logging.getLogger("playwright_pytest")


class CommonValidations:
    nw = 3
    sw = 5
    mw = 10

    def __init__(self, page: Page):
        self.page = page
        self.addToQuote = self.page.get_by_role("button", name="Add to Quote")
        self.cached_file_path = None  # Cache for the downloaded file path

    def collect_table_data(self, xpath: str, column_name: str):
        collected_data = []
        # print(f"Collecting {column_name}...")
        logger.info(f"Collecting {column_name}...")
        count = self.page.locator(xpath).count()
        if count == 0:
            logger.warning(f"No elements found for {column_name} with XPath: {xpath}")
            return collected_data
        for node in range(count):
            data = self.page.locator(xpath).nth(node).text_content()
            if data is None or data.strip() == "":  # Handle empty or blank cells
                collected_data.append("")  # Add empty string for empty or blank cells
                # print(f"Found {column_name}: Empty cell")
                logger.info(f"Found {column_name}: Empty cell")
            else:
                collected_data.append(data.strip())  # Add non-empty cells
                # print(f"Found {column_name}: {data.strip()}")
                logger.info(f"Found {column_name}: {data.strip()}")
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

    def compareLists(self, list1, list2):
        errors = []
        # Log the lists being compared
        logger.info(f"Comparing lists:\nList1: {list1}\nList2: {list2}")
        print(f"Comparing lists:\nList1: {list1}\nList2: {list2}")
        if len(list1) != len(list2):
            logger.error("List lengths do not match!")
            print(f"\033[91m❌ List lengths do not match!\033[0m")
            errors.append(
                f"Lengths differ: List1 ({len(list1)}) vs List2 ({len(list2)})"
            )
        for i in range(min(len(list1), len(list2))):
            # Normalize values in both lists
            value1 = list1[i] if pd.notna(list1[i]) else ""
            value2 = list2[i] if pd.notna(list2[i]) else ""

            # Convert numeric strings to integers or floats for comparison
            try:
                if isinstance(value1, str) and "," in value1:
                    value1 = float(value1.replace(",", ""))
                elif isinstance(value1, str) and value1.isdigit():
                    value1 = int(value1)
                if isinstance(value2, str) and "," in value2:
                    value2 = float(value2.replace(",", ""))
                elif isinstance(value2, str) and value2.isdigit():
                    value2 = int(value2)
            except ValueError:
                pass  # If conversion fails, leave the values as-is

            if value1 != value2:
                logger.error(f"Mismatch at index {i}: {value1} != {value2}")
                print(f"\033[91m❌ Mismatch at index {i}: {value1} != {value2}\033[0m")
                errors.append(f"Mismatch at index {i}: {value1} != {value2}")
        if not errors:
            logger.info("Lists match successfully!")
            # print(f"\033[92m✅ Lists match successfully!\033[0m")
        return errors

    def isValuePresentInList(
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
        # print(f"Checking if '{value_to_check}' is present in the {column_name} list...")
        logger.info(f"The {column_name} list contains: {data_list}")
        print(f"The {column_name} list contains: {data_list}")
        if value_to_check in data_list:
            logger.info(f"'{value_to_check}' is present in the {column_name} list.")
            print(
                f"\033[92m✅ '{value_to_check}' is present in the {column_name} list.\033[0m"
            )
            return True
        else:
            logger.warning(
                f"'{value_to_check}' is NOT present in the {column_name} list."
            )
            print(
                f"\033[91m❌ '{value_to_check}' is NOT present in the {column_name} list.\033[0m"
            )
            return False

    def validateZeroNetPrice(self, value: str) -> bool:
        try:
            # Convert the value to a float first to handle decimal values like "0.00"
            numeric_value = float(value)
            # Convert the float to an integer
            int_value = int(numeric_value)
        except ValueError:
            # Log a warning if the value is not numeric
            logger.warning(f"Value '{value}' is not numeric and cannot be validated.")
            print(
                f"\033[91m❌ Value '{value}' is not numeric and cannot be validated.\033[0m"
            )
            return False
        if int_value == 0:
            # Log success if the value represents 0
            logger.info(
                "Net Price is correctly set to 0 (or equivalent value like 0.00)."
            )
            print(
                f"\033[92m✅ Net Price is correctly set to 0 (or equivalent value like 0.00).\033[0m"
            )
            return True
        else:
            # Log a warning if the value does not represent 0
            logger.warning(
                f"Unexpected Net Price value: {value} (converted to {int_value})."
            )
            print(
                f"\033[91m❌ Unexpected Net Price value: {value} (converted to {int_value}).\033[0m"
            )
            return False

    def readProductTableAndValidateZeroNetPrice(self, page, column_name):
        logger.info(f"Reading product table for column: {column_name}")
        # Define a dictionary for column XPaths
        column_xpaths = {
            "Net Price": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-netPrice_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
        }
        # Get the XPath for the requested column
        xpath = column_xpaths.get(column_name)
        if not xpath:
            logger.error(f"Invalid column name provided: {column_name}")
            return []
        # Locate elements using the XPath
        locator = page.locator(xpath)
        count = locator.count()
        logger.info(
            f"Found {count} elements with the specified XPath for column: {column_name}"
        )
        print(
            f"Found {count} elements with the specified XPath for column: {column_name}"
        )
        # Initialize a list to store validation results
        validation_results = []
        # Extract and validate text for each element
        for i in range(count):
            element = locator.nth(i)
            text = element.inner_text().strip()
            # Skip rows with empty or blank values
            if not text:
                logger.info(
                    f"Row {i + 1}: Empty or blank value found. Skipping this row."
                )
                print(f"Row {i + 1}: Empty or blank value found. Skipping this row.")
                continue
            logger.info(f"Row {i + 1}: Extracted text: {text}")
            print(f"Row {i + 1}: Extracted text: {text}")
            try:
                # Convert the text to a float and then to an integer for validation
                numeric_value = float(text)
                int_value = int(numeric_value)
                if int_value == 0:
                    logger.info(f"Row {i + 1}: Net Price is correctly set to 0.")
                    print(
                        f"\033[92m✅ Row {i + 1}: Net Price is correctly set to 0.\033[0m"
                    )
                    validation_results.append(True)
                else:
                    logger.warning(
                        f"Row {i + 1}: Unexpected Net Price value: {text} (converted to {int_value})."
                    )
                    print(
                        f"\033[91m❌ Row {i + 1}: Unexpected Net Price value: {text} (converted to {int_value}).\033[0m"
                    )
                    validation_results.append(False)
            except ValueError:
                logger.error(
                    f"Row {i + 1}: Invalid Net Price value: {text}. Cannot convert to number."
                )
                print(
                    f"\033[91m❌ Row {i + 1}: Invalid Net Price value: {text}. Cannot convert to number.\033[0m"
                )
                validation_results.append(False)
        # Log the overall validation results
        logger.info(
            f"Validation results for column '{column_name}': {validation_results}"
        )
        print(f"Validation results for column '{column_name}': {validation_results}")
        return validation_results

    def validateBOMTable_Config(self, part_number, quantity):
        """
        Validates the BOM table by comparing the part number and quantity values.
        Args:
            part_number (str): The part number to compare against.
            quantity (str or int or float): The quantity to compare against (from an Excel sheet).
        Returns:
            bool: True if validation is successful, False otherwise.
        """
        xpath_mapping = {
            "Part Number": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_0']",
            "Quantity": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_1']",
        }
        # Get XPaths for Part Number and Quantity columns
        part_number_xpath = xpath_mapping.get("Part Number")
        quantity_xpath = xpath_mapping.get("Quantity")

        if not part_number_xpath or not quantity_xpath:
            logger.error("Invalid column name for Part Number or Quantity.")
            print("\033[91m❌ Invalid column name for Part Number or Quantity.\033[0m")
            return False

        # Locate Part Number elements
        part_number_elements = self.page.locator(part_number_xpath)
        quantity_elements = self.page.locator(quantity_xpath)

        # Get the count of rows in the table
        row_count = part_number_elements.count()
        logger.info(f"Found {row_count} rows in the BOM table.")
        # print(f"Found {row_count} rows in the BOM table.")

        # Convert the provided quantity parameter to float for comparison
        try:
            parameter_quantity = float(str(quantity).replace(",", ""))
        except ValueError:
            logger.error(
                f"Invalid quantity parameter: {quantity}. Cannot convert to float."
            )
            print(
                f"\033[91m❌ Invalid quantity parameter: {quantity}. Cannot convert to float.\033[0m"
            )
            return False

        # Loop through each row in the table
        validation_passed = False  # Flag to track if any match is found
        for i in range(row_count):
            # Read Part Number value
            part_number_value = part_number_elements.nth(i).text_content().strip()
            if not part_number_value:
                logger.info(
                    f"Row {i + 1}: Empty or blank Part Number value. Skipping this row."
                )
                print(
                    f"Row {i + 1}: Empty or blank Part Number value. Skipping this row."
                )
                continue

            logger.info(f"Row {i + 1}: Found Part Number: {part_number_value}")
            # print(f"Row {i + 1}: Found Part Number: {part_number_value}")

            # Compare Part Number value with the parameterized part number
            if part_number_value == part_number:
                logger.info(f"Row {i + 1}: Part Number matches: {part_number_value}")
                print(
                    f"\033[92m✅ Row {i + 1}: Part Number matches correctly with expected: '{part_number}' and actual: '{part_number_value}'.\033[0m"
                )

                # Read Quantity value for the matching Part Number
                quantity_value = quantity_elements.nth(i).text_content().strip()
                if not quantity_value:
                    logger.info(
                        f"Row {i + 1}: Empty or blank Quantity value. Skipping this row."
                    )
                    print(
                        f"Row {i + 1}: Empty or blank Quantity value. Skipping this row."
                    )
                    continue

                logger.info(f"Row {i + 1}: Found Quantity: {quantity_value}")
                # print(f"Row {i + 1}: Found Quantity: {quantity_value}")

                # Convert the Quantity value to float for comparison
                try:
                    table_quantity = float(quantity_value.replace(",", ""))
                except ValueError:
                    logger.error(
                        f"Row {i + 1}: Invalid Quantity value: {quantity_value}. Cannot convert to float."
                    )
                    print(
                        f"\033[91m❌ Row {i + 1}: Invalid Quantity value: {quantity_value}. Cannot convert to float.\033[0m"
                    )
                    continue

                # Compare table quantity with parameterized quantity
                if table_quantity == parameter_quantity:
                    logger.info(
                        f"Row {i + 1}: Quantity matches correctly: {table_quantity}"
                    )
                    # print(f"\033[92m✅ Row {i + 1}: Quantity matches correctly: {table_quantity}\033[0m")
                    print(
                        f"\033[92m✅ Row {i + 1}: Quantity matches correctly with expected: '{parameter_quantity}' and actual: '{table_quantity}'.\033[0m"
                    )
                    validation_passed = True
                else:
                    logger.warning(
                        f"Row {i + 1}: Quantity mismatch: Table ({table_quantity}) vs Parameter ({parameter_quantity})"
                    )
                    print(
                        f"\033[91m❌ Row {i + 1}: Quantity mismatch with expected: '{parameter_quantity}' and actual: '{table_quantity}'.\033[0m"
                    )

        # If no match is found
        if validation_passed:
            logger.info(f"Validation passed for Part Number: {part_number}")
        else:
            logger.warning(f"No matching Part Number found for: {part_number}")
            print(
                f"\033[91m❌ Expected Part Number: '{part_number}', but no matching Part Number was found in the BOM table.\033[0m"
            )
        return validation_passed

    def validateProductTable_Config(self, product_name, quantity):
        """
        Validates the product table by comparing the product name and quantity values.

        Args:
            product_name (str): The product name to compare against.
            quantity (str or int or float): The quantity to compare against (from an Excel sheet).

        Returns:
            bool: True if validation is successful, False otherwise.
        """
        # Define a dictionary for column XPaths
        column_xpaths = {
            "Product": "//div[contains(@class, 'oj-fa-cx-cpq-fragmentsUI-lineItems-rowHeader oj-sm-align-self-center cx-cpq-line-item-row')]",
            "Qty": "//div[contains(@class, 'oj-flex oj-fa-cx-cpq-field-unitQuantity_l_c oracle-cx-cpq-fragmentsUI-cx-cpq-fragment-dataGridColumnTruncate')]",
        }

        # Get XPaths for Product Name and Quantity columns
        product_xpath = column_xpaths.get("Product")
        quantity_xpath = column_xpaths.get("Qty")

        if not product_xpath or not quantity_xpath:
            logger.error("Invalid column name for Product or Quantity.")
            print("\033[91m❌ Invalid column name for Product or Quantity.\033[0m")
            return False

        # Locate Product elements
        product_elements = self.page.locator(product_xpath)
        quantity_elements = self.page.locator(quantity_xpath)

        # Get the count of rows in the table
        row_count = product_elements.count()
        logger.info(f"Found {row_count} rows in the product table.")
        print(f"Found {row_count} rows in the product table.")

        # Convert the provided quantity parameter to float for comparison
        try:
            parameter_quantity = float(str(quantity).replace(",", ""))
        except ValueError:
            logger.error(
                f"Invalid quantity parameter: {quantity}. Cannot convert to float."
            )
            print(
                f"\033[91m❌ Invalid quantity parameter: {quantity}. Cannot convert to float.\033[0m"
            )
            return False

        # Loop through each row in the table
        validation_passed = False  # Flag to track if any match is found
        for i in range(row_count):
            # Read Product Name value
            product_name_value = product_elements.nth(i).text_content().strip()
            if not product_name_value:
                logger.info(
                    f"Row {i + 1}: Empty or blank Product Name value. Skipping this row."
                )
                print(
                    f"Row {i + 1}: Empty or blank Product Name value. Skipping this row."
                )
                continue

            logger.info(f"Row {i + 1}: Found Product Name: {product_name_value}")
            print(f"Row {i + 1}: Found Product Name: {product_name_value}")

            # Compare Product Name value with the parameterized product name
            if product_name_value == product_name:
                logger.info(f"Row {i + 1}: Product Name matches: {product_name_value}")
                print(
                    f"\033[92m✅ Row {i + 1}: Product Name matches: {product_name_value}\033[0m"
                )

                # Read Quantity value for the matching Product Name
                quantity_value = quantity_elements.nth(i).text_content().strip()
                if not quantity_value:
                    logger.info(
                        f"Row {i + 1}: Empty or blank Quantity value. Skipping this row."
                    )
                    print(
                        f"Row {i + 1}: Empty or blank Quantity value. Skipping this row."
                    )
                    continue

                logger.info(f"Row {i + 1}: Found Quantity: {quantity_value}")
                print(f"Row {i + 1}: Found Quantity: {quantity_value}")

                # Convert the Quantity value to float for comparison
                try:
                    table_quantity = float(quantity_value.replace(",", ""))
                except ValueError:
                    logger.error(
                        f"Row {i + 1}: Invalid Quantity value: {quantity_value}. Cannot convert to float."
                    )
                    print(
                        f"\033[91m❌ Row {i + 1}: Invalid Quantity value: {quantity_value}. Cannot convert to float.\033[0m"
                    )
                    continue

                # Compare table quantity with parameterized quantity
                if table_quantity == parameter_quantity:
                    logger.info(
                        f"Row {i + 1}: Quantity matches correctly: {table_quantity}"
                    )
                    print(
                        f"\033[92m✅ Row {i + 1}: Quantity matches correctly: {table_quantity}\033[0m"
                    )
                    validation_passed = True
                else:
                    logger.warning(
                        f"Row {i + 1}: Quantity mismatch: Table ({table_quantity}) vs Parameter ({parameter_quantity})"
                    )
                    print(
                        f"\033[91m❌ Row {i + 1}: Quantity mismatch: Table ({table_quantity}) vs Parameter ({parameter_quantity})\033[0m"
                    )

        # If no match is found
        if validation_passed:
            logger.info(f"Validation passed for Product Name: {product_name}")
        else:
            logger.warning(f"No matching Product Name found for: {product_name}")
            print(
                f"\033[91m❌ No matching Product Name found for: {product_name}\033[0m"
            )
        return validation_passed

    def readBOMTable(self, column_name):
        logger.info(f"Reading BOM table for column: {column_name}")
        # Define a dictionary for column XPaths
        xpath_mapping = {
            "Part Number": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_0']",
            "Quantity": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_1']",
            "Description": "//td[starts-with(@id, 'bom-table:') and substring(@id, string-length(@id) - string-length('_0') + 1) = '_2']",
        }
        # Validate the column name
        xpath = xpath_mapping.get(column_name)
        if not xpath:
            logger.error(f"Invalid column name provided: {column_name}")
            return []
        # Locate elements using the XPath
        locator = self.page.locator(xpath)
        count = locator.count()
        if count == 0:
            logger.info(f"No elements found for column: {column_name}")
            return []
        logger.info(f"Found {count} elements for column: {column_name}")
        # Extract text from elements
        extracted_texts = []
        for i in range(count):
            try:
                text = locator.nth(i).inner_text().strip()
                if text:
                    extracted_texts.append(text)
                else:
                    logger.info(
                        f"Empty text found for element index {i} in column: {column_name}"
                    )
            except Exception as e:
                logger.error(f"Error extracting text for element index {i}: {e}")
                logger.warning(f"Skipping element index {i} due to error.")
        # Print the extracted texts in a single row separated by spaces, including the column name
        if extracted_texts:
            # print(
            # f"Extracted texts for column '{column_name}': {' '.join(extracted_texts)}"
            # )
            logger.info(
                f"Extracted texts for {column_name}: {' '.join(extracted_texts)}"
            )
        else:
            logger.info(f"No valid data extracted from the column: {column_name}")
        return extracted_texts

    def download_excel_file(self) -> str:
        """
        Handles the download of an Excel file from the web page and returns the file path.
        Uses the unique name provided by the application for the downloaded file.
        """
        try:
            # Define the shared downloads folder
            download_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(
                download_dir, exist_ok=True
            )  # Create the 'downloads' folder if it doesn't exist

            # Step 1: Click the "More Actions" button
            self.page.locator(
                "(//div[contains(@class, 'oj-button-label')]//span[contains(@class, 'oj-button-text')])[9]"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator(
                "(//div[contains(@class, 'oj-button-label')]//span[contains(@class, 'oj-button-text')])[9]"
            ).click()
            logger.info("Clicked the 'More Actions' button.")
            time.sleep(self.nw)

            # Step 2: Click the "Export Lines" button
            self.page.locator(
                "//span[normalize-space(text())='Export Lines']"
            ).wait_for(state="visible", timeout=60000)
            self.page.locator("//span[normalize-space(text())='Export Lines']").click()
            logger.info("Clicked the 'Export Lines' button.")
            time.sleep(self.sw)

            # Step 3: Handle the downloaded Excel file
            # Wait for the file to download and save it directly to the shared directory
            with self.page.expect_download() as download_info:
                pass
            download = download_info.value

            # Save the file using the unique name provided by the application
            file_path = os.path.join(download_dir, download.suggested_filename)
            download.save_as(file_path)
            logger.info(
                f"Downloaded LIG Table excel file name: {download.suggested_filename}"
            )
            print(
                f"\033[94mℹ️ Downloaded LIG Table excel file name: {download.suggested_filename}\033[0m"
            )
            logger.info(f"Downloaded to the location: {file_path}")
            print(f"\033[94mℹ️ Downloaded to: {file_path}\033[0m")

            return file_path
        except Exception as e:
            logger.error(f"An unexpected error occurred during file download: {e}")
            print(
                f"\033[91m❌ An unexpected error occurred during file download: {e}\033[0m"
            )
            return ""

    def read_excel_file(self, file_path: str, column_name: str) -> list:
        """
        Reads data from a specific column in an Excel file, skipping rows with empty or blank cells.

        Parameters:
            file_path (str): The file path of the Excel file.
            column_name (str): The name of the column to read data from.

        Returns:
            list: A list containing the data from the specified column, excluding empty or blank cells.
        """
        try:
            # Use pandas to read the Excel file
            excel_data = pd.read_excel(file_path)

            # Check if the specified column exists
            if column_name not in excel_data.columns:
                logger.warning(
                    f"The column '{column_name}' does not exist in the Excel file. Skipping column extraction."
                )
                print(
                    f"The column '{column_name}' does not exist in the Excel file. Skipping column extraction."
                )
                return []

            # Extract column data and log messages for empty or blank cells
            column_data = []
            for index, value in excel_data[column_name].items():
                if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
                    logger.info(
                        f"Row {index + 1}: Empty or blank value in column '{column_name}'. Skipping this row."
                    )
                    print(
                        f"Row {index + 1}: Empty or blank value in column '{column_name}'. Skipping this row."
                    )
                    continue
                column_data.append(value)

            logger.info(f"Data from column '{column_name}': {column_data}")
            print(
                f"Data from column '{column_name}': {' | '.join(map(str, column_data))}"
            )
            return column_data

        except Exception as e:
            logger.error(f"Failed to read Excel file: {e}")
            print(f"Failed to read Excel file: {e}")
            return []

    def read_excel_file_including_empty(self, file_path: str, column_name: str) -> list:
        """
        Reads data from a specific column in an Excel file, including empty or blank cells.

        Parameters:
            file_path (str): The file path of the Excel file.
            column_name (str): The name of the column to read data from.

        Returns:
            list: A list containing the data from the specified column, including empty or blank cells.
        """
        try:
            # Use pandas to read the Excel file
            excel_data = pd.read_excel(file_path)

            # Check if the specified column exists
            if column_name not in excel_data.columns:
                logger.warning(
                    f"The column '{column_name}' does not exist in the Excel file. Skipping column extraction."
                )
                print(
                    f"The column '{column_name}' does not exist in the Excel file. Skipping column extraction."
                )
                return []

            # Extract column data, including empty or blank cells
            column_data = excel_data[column_name].tolist()

            logger.info(f"Data from column '{column_name}': {column_data}")
            print(
                f"Data from column '{column_name}': {' | '.join(map(str, column_data))}"
            )
            return column_data

        except Exception as e:
            logger.error(f"Failed to read Excel file: {e}")
            print(f"Failed to read Excel file: {e}")
            return []

    def validateProductTable_Excel_Config(self, file_path: str, product_name, quantity):
        """
        Validates the product table by comparing the product name and quantity values.

        Args:
            file_path (str): The path of the downloaded Excel file.
            product_name (str): The product name to compare against.
            quantity (str or int or float): The quantity to compare against (from an Excel sheet).

        Returns:
            None
        """
        try:
            if not file_path or not os.path.exists(file_path):
                logger.error("Invalid file path or file does not exist.")
                return False

            # Read the Excel file and validate rows
            excel_data = pd.read_excel(file_path)

            # Check if the required columns exist
            if "Product" not in excel_data.columns or "Qty." not in excel_data.columns:
                raise ValueError(
                    "Required columns ('Product', 'Qty.') not found in the Excel file."
                )

            # Iterate through rows and validate
            for index, row in excel_data.iterrows():
                product_value = row["Product"]
                quantity_value = row["Qty."]

                if product_value == product_name:
                    print(
                        f"\033[92m✅ Row {index + 1}: Product name matches correctly with expected: '{product_name}' and actual: '{product_value}'.\033[0m"
                    )

                    if quantity_value == quantity:
                        print(
                            f"\033[92m✅ Row {index + 1}: Quantity matches correctly with expected: '{quantity}' and actual: '{quantity_value}'.\033[0m"
                        )
                        return True
                    else:
                        print(
                            f"\033[91m❌ Row {index + 1}: Quantity mismatch with expected: '{quantity}' and actual: '{quantity_value}'.\033[0m"
                        )
                        return False
            # If no matching product is found
            print(
                f"\033[91m❌ Expected Product: '{product_name}', but no matching product was found in the LIG table.\033[0m"
            )
            return False
        except Exception as e:
            logger.error(f"An error occurred while validating the product table: {e}")
            print(f"An error occurred while validating the product table: {e}")
            raise

    def readProductTable_Excel(self, file_path: str, column_name: str) -> list:
        """
        Reads data from a specific column in an Excel file, skipping rows with empty or blank cells.

        Parameters:
            file_path (str): The path of the downloaded Excel file.
            column_name (str): The name of the column to read data from.

        Returns:
            list: A list containing the data from the specified column, excluding empty or blank cells.
        """
        try:
            if not file_path or not os.path.exists(file_path):
                logger.error("Invalid file path or file does not exist.")
                print("❌ Invalid file path or file does not exist.")
                return []

            # Use pandas to read the Excel file
            excel_data = pd.read_excel(file_path)

            # Check if the specified column exists
            if column_name not in excel_data.columns:
                logger.warning(
                    f"The column '{column_name}' does not exist in the Excel file. Skipping column extraction."
                )
                print(
                    f"❌ The column '{column_name}' does not exist in the Excel file. Skipping column extraction."
                )
                return []

            # Extract column data, skipping empty or blank cells
            column_data = []
            for index, value in excel_data[column_name].items():
                if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
                    logger.info(
                        f"Row {index + 1}: Empty or blank value in column '{column_name}'. Skipping this row."
                    )
                    continue
                column_data.append(value)

            logger.info(f"Data from column '{column_name}': {column_data}")
            print(f"Data from column '{column_name}': {column_data}")
            return column_data

        except Exception as e:
            logger.error(f"Failed to read column '{column_name}' from Excel file: {e}")
            print(f"❌ Failed to read column '{column_name}' from Excel file: {e}")
            return []

    def readProductTable_Excel_SaveToList(
        self, file_path: str, column_name: str
    ) -> list:
        """
        Reads a specific column from the Product table in a downloaded Excel file and saves it to a list, including empty or blank cells.

        Args:
            file_path (str): The path of the downloaded Excel file.
            column_name (str): The name of the column to read (e.g., "Product", "Qty.", "Part Description").

        Returns:
            list: A list containing the data from the specified column, including empty or blank cells.
        """
        try:
            if not file_path or not os.path.exists(file_path):
                logger.error("Invalid file path or file does not exist.")
                return []

            # Step 1: Read the specified column from the Excel file
            logger.info(
                f"Reading column '{column_name}' from Product table in Excel file: {file_path}"
            )
            column_data = self.read_excel_file_including_empty(file_path, column_name)

            # Log the extracted data
            logger.info(f"Extracted data for column '{column_name}': {column_data}")

            # Return the extracted list
            return column_data

        except Exception as e:
            logger.error(
                f"An error occurred while reading column '{column_name}' from the Product table: {e}"
            )
            print(
                f"An error occurred while reading column '{column_name}' from the Product table: {e}"
            )
            return []

    def compareBomAndProduct_Tables(
        self,
        bom_part_numbers,
        bom_quantities,
        bom_descriptions,
        product_part_numbers,
        product_quantities,
        product_descriptions,
    ):
        """
        Compares BOM table data with Product table data for part numbers, quantities, and descriptions.

        Args:
            bom_part_numbers (list): List of part numbers from BOM table.
            bom_quantities (list): List of quantities from BOM table.
            bom_descriptions (list): List of descriptions from BOM table.
            product_part_numbers (list): List of part numbers from Product table.
            product_quantities (list): List of quantities from Product table.
            product_descriptions (list): List of descriptions from Product table.

        Returns:
            bool: True if all comparisons pass, False otherwise.
        """
        errors = []
        print(f"\033[94mℹ️ Comparing BOM and LIG Table Details for Part Number\033[0m")
        # Compare Part Numbers
        errors += self.compareLists(bom_part_numbers, product_part_numbers)
        if errors:
            logger.warning(
                "Mismatch found during Part Number comparison:\n" + "\n".join(errors)
            )
            print(f"\033[91m❌ Part Number comparison failed!\033[0m")
        else:
            logger.info("Part Number comparison passed successfully!")
            print(f"\033[92m✅ Part Number comparison passed successfully!\033[0m")

        print(f"\n\033[94mℹ️ Comparing BOM and LIG Table Details for Quantity\033[0m")
        # Compare Quantities
        errors += self.compareLists(bom_quantities, product_quantities)
        if errors:
            logger.warning(
                "Mismatch found during Quantity comparison:\n" + "\n".join(errors)
            )
            print(f"\033[91m❌ Quantity comparison failed!\033[0m")
        else:
            logger.info("Quantity comparison passed successfully!")
            print(f"\033[92m✅ Quantity comparison passed successfully!\033[0m")

        print(
            f"\n\033[94mℹ️ Comparing BOM and LIG Table Details for Description\033[0m"
        )
        # Compare Descriptions
        errors += self.compareLists(bom_descriptions, product_descriptions)
        if errors:
            logger.warning(
                "Mismatch found during Description comparison:\n" + "\n".join(errors)
            )
            print(f"\033[91m❌ Description comparison failed!\033[0m")
        else:
            logger.info("Description comparison passed successfully!")
            print(f"\033[92m✅ Description comparison passed successfully!\033[0m")

        # Final result
        if errors:
            logger.warning("The following mismatches were found:\n" + "\n".join(errors))
            return False
        else:
            logger.info(
                "BOM table and Product table values have been verified successfully!"
            )
            # print(f"\033[92m✅ BOM table and Product table values have been verified successfully!\033[0m")
            return True
