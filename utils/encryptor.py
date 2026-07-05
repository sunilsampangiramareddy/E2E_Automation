from cryptography.fernet import Fernet
import os
import json


class Encryptor:
    def __init__(self, key: bytes = None):
        """
        Initialize the Encryptor with an encryption key.
        If no key is provided, a new key will be generated.
        """
        if key is None:
            self.key = Fernet.generate_key()  # Generate a new encryption key
        else:
            self.key = key

        self.cipher_suite = Fernet(self.key)

    def encrypt_password(self, password: str) -> str:
        """
        Encrypts a password using the provided or generated key.
        :param password: The plain text password to encrypt.
        :return: The encrypted password as a string.
        """
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return encrypted_password.decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        """
        Decrypts an encrypted password using the provided or generated key.
        :param encrypted_password: The encrypted password to decrypt.
        :return: The plain text password as a string.
        """
        decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_password.decode()

    @staticmethod
    def generate_key() -> bytes:
        """
        Generates a new encryption key.
        :return: The generated encryption key as bytes.
        """
        return Fernet.generate_key()

    @staticmethod
    def save_key_to_file(file_path: str, key: bytes):
        """
        Saves the encryption key to a file.
        :param file_path: Path to the file where the key will be saved.
        :param key: The encryption key as bytes.
        """
        with open(file_path, "wb") as key_file:
            key_file.write(key)
        print(f"Encryption key saved to: {file_path}")

    @staticmethod
    def load_key_from_file(file_path: str) -> bytes:
        """
        Loads the encryption key from a file.
        :param file_path: Path to the file where the key is stored.
        :return: The encryption key as bytes.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Encryption key file not found: {file_path}")
        with open(file_path, "rb") as key_file:
            return key_file.read()


# Example usage
if __name__ == "__main__":
    # Step 1: Generate and save the encryption key
    key_file_path = "key.key"
    key = Encryptor.generate_key()
    Encryptor.save_key_to_file(key_file_path, key)

    # Step 2: Load the encryption key from the file
    loaded_key = Encryptor.load_key_from_file(key_file_path)

    # Step 3: Initialize the Encryptor with the loaded key
    encryptor = Encryptor(loaded_key)

    # =========Step 4: Enter multiple passwords below to encrypt and save to config.json========================================
    password1 = "pwd1"  # Replace with your actual password for apptestmbob4 user
    password2 = "pwd2"  # Replace with your actual password for netAppApiTestUser user
    # ==========================================================================================================================

    encrypted_password1 = encryptor.encrypt_password(password1)
    encrypted_password2 = encryptor.encrypt_password(password2)

    print(f"Encrypted Password 1: {encrypted_password1}")
    print(f"Encrypted Password 2: {encrypted_password2}")

    # Step 5: Save the encrypted passwords to config.json
    config_data = {
        "username": "apptestmbob4@netapp.com",
        "encodedString": encrypted_password1,
        "usernameAPI": "netAppApiTestUser",
        "encodedStringAPI": encrypted_password2,
    }

    with open("config.json", "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    print("Updated config.json with encrypted passwords.")

    # Step 6: Decrypt the encrypted passwords to verify
    decrypted_password1 = encryptor.decrypt_password(encrypted_password1)
    decrypted_password2 = encryptor.decrypt_password(encrypted_password2)

    print(f"Decrypted Password 1: {decrypted_password1}")
    print(f"Decrypted Password 2: {decrypted_password2}")

    # Step 7: Verify that the decrypted passwords match the originals
    assert decrypted_password1 == password1, "Decryption of password 1 failed!"
    assert decrypted_password2 == password2, "Decryption of password 2 failed!"
    print("Encryption and decryption successful!")
