"""Chat message bubble widget"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor


class MessageBubble(QWidget):
    """A chat message bubble"""

    def __init__(self, message: str, is_user: bool, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        self.init_ui()

    def create_avatar(self, is_user: bool):
        """Create a simple circular avatar"""
        size = 32
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw circle
        if is_user:
            painter.setBrush(QColor("#89b4fa"))  # Blue for user
        else:
            painter.setBrush(QColor("#a6e3a1"))  # Green for AI
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, size, size)
        
        painter.end()
        return pixmap

    def _is_dark_theme(self):
        """Check if dark theme is active by checking parent widget background"""
        # Simple heuristic: check if background is dark
        return True  # Default to dark theme styling
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(12)

        # Create avatar
        avatar_label = QLabel()
        avatar_label.setPixmap(self.create_avatar(self.is_user))
        avatar_label.setFixedSize(32, 32)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Message text - NO text selection to avoid highlighting
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        
        # Set style based on user or AI
        if self.is_user:
            message_label.setStyleSheet("""
                font-size: 14px; 
                line-height: 1.6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: #313244;
                color: #cdd6f4;
                padding: 10px 14px;
                border-radius: 18px;
                border: none;
            """)
        else:
            message_label.setStyleSheet("""
                font-size: 14px; 
                line-height: 1.6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: transparent;
                color: #cdd6f4;
                padding: 0px;
                border: none;
            """)
        
        message_label.setMaximumWidth(650)

        if self.is_user:
            main_layout.addStretch()
            main_layout.addWidget(message_label)
            main_layout.addWidget(avatar_label)
        else:
            main_layout.addWidget(avatar_label)
            main_layout.addWidget(message_label)
            main_layout.addStretch()

        self.setLayout(main_layout)
