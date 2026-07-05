import json
import os


class LocatorManager:
    def __init__(self, file_path):
        self.locators = self.load_locators(file_path)

    def load_locators(self, file_path):
        """
        Load locators from a JSON file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Locator file not found: {file_path}")
        with open(file_path, "r") as file:
            return json.load(file)

    def get_locator(self, page_name, element_name):
        """
        Retrieve a locator for a specific page and element.

        :param page_name: The name of the page in the JSON file.
        :param element_name: The name of the element in the JSON file.
        :return: Locator (string or dictionary).
        """
        try:
            return self.locators[page_name][element_name]
        except KeyError:
            raise Exception(
                f"Locator for '{element_name}' on page '{page_name}' not found."
            )
