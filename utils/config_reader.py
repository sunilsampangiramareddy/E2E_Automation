import json
import os
from utils.encryptor import Encryptor


class ConfigReader:
    def __init__(self, config_path=None, key_path="key.key"):
        if config_path is None:
            # Use environment variable or default to a relative path
            config_path = os.getenv(
                "CONFIG_PATH", os.path.join(os.getcwd(), "config.json")
            )
        self.config_path = config_path
        self.key_path = key_path
        self.config_data = self._load_config()
        self.encryptor = Encryptor(Encryptor.load_key_from_file(self.key_path))

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, "r") as config_file:
            return json.load(config_file)

    def _load_key(self):
        """
        Load the encryption key from the key file (key.key).
        """
        if not os.path.exists(self.key_path):
            raise FileNotFoundError(f"Encryption key file not found: {self.key_path}")
        with open(self.key_path, "rb") as key_file:
            return key_file.read()

    def get_username(self):
        return self.config_data.get("username")

    def get_encodedString(self):
        """
        Retrieve and decrypt the password from the configuration file.
        """
        encrypted_password = self.config_data.get("encodedString")
        return self.encryptor.decrypt_password(encrypted_password)

    def get_usernameAPI(self):
        return self.config_data.get("usernameAPI")

    def get_encodedStringAPI(self):
        encrypted_password_api = self.config_data.get("encodedStringAPI")
        return self.encryptor.decrypt_password(encrypted_password_api)
