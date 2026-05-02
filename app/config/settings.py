"""Application settings management using QSettings"""

from PyQt6.QtCore import QSettings
from typing import Any


class Settings:
    """Manages application settings using platform-native storage"""

    DEFAULTS = {
        "theme": "system",
        "font_size": 13,
        "default_mode": "overview",
        "stream_responses": True,
        "auto_detect_language": True,
        "save_history": True,
        "max_history_items": 20,
    }

    def __init__(self):
        self.settings = QSettings("CodeLens", "CodeLens")
        self._ensure_defaults()

    def _ensure_defaults(self):
        """Ensure all default settings exist"""
        for key, value in self.DEFAULTS.items():
            if not self.settings.contains(key):
                self.settings.setValue(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        if default is None and key in self.DEFAULTS:
            default = self.DEFAULTS[key]
        return self.settings.value(key, default)

    def set(self, key: str, value: Any):
        """Set a setting value"""
        self.settings.setValue(key, value)

    def get_theme(self) -> str:
        """Get current theme"""
        return self.get("theme", "system")

    def set_theme(self, theme: str):
        """Set theme (light, dark, system)"""
        if theme in ["light", "dark", "system"]:
            self.set("theme", theme)

    def get_font_size(self) -> int:
        """Get font size"""
        size = self.get("font_size", 13)
        return int(size) if isinstance(size, str) else size

    def set_font_size(self, size: int):
        """Set font size"""
        if 10 <= size <= 22:
            self.set("font_size", size)

    def get_default_mode(self) -> str:
        """Get default explanation mode"""
        return self.get("default_mode", "overview")

    def set_default_mode(self, mode: str):
        """Set default explanation mode"""
        self.set("default_mode", mode)

    def get_stream_responses(self) -> bool:
        """Get stream responses setting"""
        value = self.get("stream_responses", True)
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    def set_stream_responses(self, enabled: bool):
        """Set stream responses"""
        self.set("stream_responses", enabled)

    def get_auto_detect_language(self) -> bool:
        """Get auto detect language setting"""
        value = self.get("auto_detect_language", True)
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    def set_auto_detect_language(self, enabled: bool):
        """Set auto detect language"""
        self.set("auto_detect_language", enabled)

    def get_save_history(self) -> bool:
        """Get save history setting"""
        value = self.get("save_history", True)
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    def set_save_history(self, enabled: bool):
        """Set save history"""
        self.set("save_history", enabled)

    def get_max_history_items(self) -> int:
        """Get max history items"""
        value = self.get("max_history_items", 20)
        return int(value) if isinstance(value, str) else value

    def set_max_history_items(self, count: int):
        """Set max history items"""
        if count > 0:
            self.set("max_history_items", count)
