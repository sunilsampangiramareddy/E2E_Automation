import os
import shutil
import logging

class ArtifactPurge:
    def __init__(self, base_directory):
        """
        Initialize ArtifactPurge with the base directory and folders to clean.

        :param base_directory: The base directory where the folders are located.
        """
        self.base_directory = base_directory
        self.folders_to_clean = [
            'reports',
            'screenshots',
            'downloads',
            'excel_test_results',
            'generated_test_data'
        ]

    def clean_folders(self):
        """
        Clean the specified folders by deleting their contents.
        """
        for folder in self.folders_to_clean:
            folder_path = os.path.join(self.base_directory, folder)
            logging.info(f"Checking folder: {folder_path}")
            if os.path.exists(folder_path):
                try:
                    self._delete_contents(folder_path)
                    logging.info(f"Contents of folder {folder_path} cleaned.")
                except Exception as e:
                    logging.error(f"Error cleaning contents of folder {folder_path}: {e}")
            else:
                logging.warning(f"Folder {folder_path} does not exist. Skipping.")

    def _delete_contents(self, folder_path):
        """
        Delete the contents of the specified folder but keep the folder itself.

        :param folder_path: The path of the folder to clean.
        """
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    logging.info(f"Deleted folder: {item_path}")
                else:
                    os.remove(item_path)
                    logging.info(f"Deleted file: {item_path}")
            except Exception as e:
                logging.error(f"Error deleting {item_path}: {e}")

# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Configure logging
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Relative path to the parent directory
    cleaner = ArtifactPurge(base_directory)
    cleaner.clean_folders()
