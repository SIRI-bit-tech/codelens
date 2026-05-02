"""Follow-up chat panel widget"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from .components.message_bubble import MessageBubble


class ChatPanel(QWidget):
    """Panel for follow-up chat about the code"""

    message_sent = pyqtSignal(str)
    clear_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        header_label = QLabel("💬 Follow-up Chat")
        header_label.setStyleSheet("font-weight: bold; font-size: 13px; padding: 5px;")

        self.clear_btn = QPushButton("🗑️ Clear Chat")
        self.clear_btn.clicked.connect(self.on_clear_clicked)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_btn)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout()
        self.messages_layout.setContentsMargins(5, 5, 5, 5)
        self.messages_layout.setSpacing(10)
        self.messages_layout.addStretch()
        self.messages_widget.setLayout(self.messages_layout)

        self.scroll_area.setWidget(self.messages_widget)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(5, 5, 5, 5)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a question about the code...")
        self.input_field.returnPressed.connect(self.on_send_clicked)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.on_send_clicked)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(header_layout)
        layout.addWidget(self.scroll_area)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def on_send_clicked(self):
        """Handle send button click"""
        message = self.input_field.text().strip()
        if message:
            self.add_message(message, is_user=True)
            self.message_sent.emit(message)
            self.input_field.clear()

    def on_clear_clicked(self):
        """Handle clear button click"""
        self.clear_messages()
        self.clear_requested.emit()

    def add_message(self, message: str, is_user: bool):
        """Add a message to the chat"""
        bubble = MessageBubble(message, is_user)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        self.scroll_to_bottom()

    def show_thinking_indicator(self):
        """Show 'AI is thinking' indicator"""
        thinking_label = QLabel("CodeLens is thinking...")
        thinking_label.setStyleSheet("""
            font-size: 13px;
            color: #a6adc8;
            font-style: italic;
            padding: 10px;
        """)
        thinking_label.setObjectName("thinking_indicator")
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, thinking_label)
        self.scroll_to_bottom()

    def remove_thinking_indicator(self):
        """Remove the thinking indicator"""
        for i in range(self.messages_layout.count()):
            widget = self.messages_layout.itemAt(i).widget()
            if widget and widget.objectName() == "thinking_indicator":
                self.messages_layout.removeWidget(widget)
                widget.deleteLater()
                break

    def add_ai_message_streaming(self, message: str):
        """Add or update AI message for streaming"""
        # Remove thinking indicator if present
        self.remove_thinking_indicator()
        
        count = self.messages_layout.count()
        if count > 1:
            last_widget = self.messages_layout.itemAt(count - 2).widget()
            if isinstance(last_widget, MessageBubble) and not last_widget.is_user:
                self.messages_layout.removeWidget(last_widget)
                last_widget.deleteLater()

        self.add_message(message, is_user=False)

    def clear_messages(self):
        """Clear all messages"""
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def set_enabled(self, enabled: bool):
        """Enable or disable chat input"""
        self.input_field.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
