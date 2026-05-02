"""Secure API key storage using keyring"""

import keyring
from typing import Optional
from app.config.constants import KEYRING_SERVICE_NAME, KEYRING_API_KEY_NAME


class KeyringHelper:
    """Manages secure storage of API keys using system keyring"""

    @staticmethod
    def set_api_key(api_key: str):
        """Store API key securely in system keyring"""
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_API_KEY_NAME, api_key)

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Retrieve API key from system keyring"""
        return keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_API_KEY_NAME)

    @staticmethod
    def delete_api_key():
        """Delete API key from system keyring"""
        try:
            keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_API_KEY_NAME)
        except keyring.errors.PasswordDeleteError:
            pass

    @staticmethod
    def has_api_key() -> bool:
        """Check if API key exists in keyring"""
        return KeyringHelper.get_api_key() is not None
