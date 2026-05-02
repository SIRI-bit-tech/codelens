"""Chat message bubble widget"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt


class MessageBubble(QWidget):
    """A chat message bubble"""

    def __init__(self, message: str, is_user: bool, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)

        bubble_layout = QVBoxLayout()
        bubble_layout.setContentsMargins(15, 10, 15, 10)
        bubble_layout.setSpacing(5)

        role_label = QLabel("You" if self.is_user else "CodeLens")
        role_label.setStyleSheet("font-weight: bold; font-size: 12px; margin-bottom: 2px;")

        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        message_label.setStyleSheet("font-size: 13px; line-height: 1.5;")

        bubble_layout.addWidget(role_label)
        bubble_layout.addWidget(message_label)

        bubble_widget = QWidget()
        bubble_widget.setLayout(bubble_layout)
        bubble_widget.setMaximumWidth(600)  # Limit bubble width like ChatGPT

        if self.is_user:
            bubble_widget.setObjectName("userBubble")
            main_layout.addStretch()
            main_layout.addWidget(bubble_widget)
        else:
            bubble_widget.setObjectName("aiBubble")
            main_layout.addWidget(bubble_widget)
            main_layout.addStretch()

        self.setLayout(main_layout)
