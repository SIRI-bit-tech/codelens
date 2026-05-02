"""Secure API key storage using keyring"""

import keyring
from typing import Optional
from app.config.constants import (
    KEYRING_SERVICE_NAME,
    KEYRING_GEMINI_API_KEY,
    KEYRING_OPENAI_API_KEY,
    KEYRING_CLAUDE_API_KEY
)


class KeyringHelper:
    """Manages secure storage of API keys using system keyring"""

    @staticmethod
    def set_api_key(provider: str, api_key: str):
        """Store API key securely in system keyring for specific provider"""
        key_name = KeyringHelper._get_key_name(provider)
        keyring.set_password(KEYRING_SERVICE_NAME, key_name, api_key)

    @staticmethod
    def get_api_key(provider: str) -> Optional[str]:
        """Retrieve API key from system keyring for specific provider"""
        key_name = KeyringHelper._get_key_name(provider)
        return keyring.get_password(KEYRING_SERVICE_NAME, key_name)

    @staticmethod
    def delete_api_key(provider: str):
        """Delete API key from system keyring for specific provider"""
        try:
            key_name = KeyringHelper._get_key_name(provider)
            keyring.delete_password(KEYRING_SERVICE_NAME, key_name)
        except keyring.errors.PasswordDeleteError:
            pass

    @staticmethod
    def has_api_key(provider: str) -> bool:
        """Check if API key exists in keyring for specific provider"""
        return KeyringHelper.get_api_key(provider) is not None

    @staticmethod
    def _get_key_name(provider: str) -> str:
        """Get the keyring key name for a provider"""
        key_map = {
            "gemini": KEYRING_GEMINI_API_KEY,
            "openai": KEYRING_OPENAI_API_KEY,
            "claude": KEYRING_CLAUDE_API_KEY
        }
        return key_map.get(provider, KEYRING_GEMINI_API_KEY)
