"""Custom status bar widget"""

from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from datetime import datetime


class CustomStatusBar(QStatusBar):
    """Custom status bar showing language, tokens, connection status, and timestamp"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language_label = QLabel("Language: Auto")
        self.token_label = QLabel("Tokens: 0")
        self.connection_label = QLabel("● Disconnected")
        self.timestamp_label = QLabel("")

        self.addWidget(self.language_label)
        self.addWidget(self.token_label)
        self.addPermanentWidget(self.connection_label)
        self.addPermanentWidget(self.timestamp_label)

        self.set_connection_status(False)

    def set_language(self, language: str):
        """Update language display"""
        self.language_label.setText(f"Language: {language.title()}")

    def set_token_count(self, count: int):
        """Update token count display"""
        self.token_label.setText(f"Tokens: ~{count}")

    def set_connection_status(self, connected: bool):
        """Update connection status indicator"""
        if connected:
            self.connection_label.setText("● Connected")
            self.connection_label.setStyleSheet("color: #a6e3a1;")
        else:
            self.connection_label.setText("● Disconnected")
            self.connection_label.setStyleSheet("color: #f38ba8;")

    def set_last_action(self, action: str):
        """Update last action timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.timestamp_label.setText(f"{action} at {timestamp}")
