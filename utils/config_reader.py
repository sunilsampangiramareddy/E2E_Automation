import json
import os

class ConfigReader:
    def __init__(self, config_path='C:\Automation_Project\E2E_Automation\config.json'):
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)

    def get_username(self):
            return self.config_data.get('username')
    
    def get_encodedString(self):
            return self.config_data.get('encodedString')
