"""
Encryption utility module providing functions for data encryption and decryption.
This module handles secure data encryption using Fernet symmetric encryption.
"""

from cryptography.fernet import Fernet
from typing import Union, Optional
import base64
import os
from pathlib import Path

class Encryption:
    """Encryption utility class."""
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize the encryption utility.
        
        Args:
            key: Optional encryption key. If not provided, a new key will be generated.
        """
        self.key = key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a new encryption key.
        
        Returns:
            bytes: The generated key
        """
        return Fernet.generate_key()

    def encrypt(self, data: Union[str, bytes]) -> bytes:
        """
        Encrypt data.
        
        Args:
            data: Data to encrypt (string or bytes)
            
        Returns:
            bytes: Encrypted data
        """
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data.
        
        Args:
            encrypted_data: Data to decrypt
            
        Returns:
            bytes: Decrypted data
        """
        return self.cipher_suite.decrypt(encrypted_data)

    def encrypt_file(self, file_path: Union[str, Path]) -> bytes:
        """
        Encrypt a file.
        
        Args:
            file_path: Path to the file to encrypt
            
        Returns:
            bytes: Encrypted file data
        """
        with open(file_path, 'rb') as file:
            file_data = file.read()
        return self.encrypt(file_data)

    def decrypt_file(self, encrypted_data: bytes, output_path: Union[str, Path]) -> None:
        """
        Decrypt data and save to a file.
        
        Args:
            encrypted_data: Encrypted data to decrypt
            output_path: Path where to save the decrypted file
        """
        decrypted_data = self.decrypt(encrypted_data)
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)

    def save_key(self, key_path: Union[str, Path]) -> None:
        """
        Save the encryption key to a file.
        
        Args:
            key_path: Path where to save the key
        """
        with open(key_path, 'wb') as key_file:
            key_file.write(self.key)

    @classmethod
    def load_key(cls, key_path: Union[str, Path]) -> 'Encryption':
        """
        Load an encryption key from a file.
        
        Args:
            key_path: Path to the key file
            
        Returns:
            Encryption: New encryption instance with loaded key
        """
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        return cls(key) 