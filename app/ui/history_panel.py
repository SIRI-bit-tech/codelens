"""History panel showing past explanations"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from typing import List, Dict


class HistoryPanel(QWidget):
    """Panel displaying explanation history"""

    history_selected = pyqtSignal(dict)
    history_deleted = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_items = []
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        header_layout = QHBoxLayout()
        header_label = QLabel("📜 History")
        header_label.setStyleSheet("font-weight: bold; font-size: 13px;")

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setMaximumWidth(40)
        self.refresh_btn.setToolTip("Refresh history")

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        button_layout = QHBoxLayout()
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        self.delete_btn.setEnabled(False)

        button_layout.addStretch()
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(header_layout)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_history(self, history: List[Dict]):
        """Load history items into the list"""
        self.history_items = history
        self.list_widget.clear()

        for item in history:
            language = item.get("language", "unknown")
            mode = item.get("mode", "unknown")
            created_at = item.get("created_at", "")
            code_preview = item.get("code", "")[:50].replace("\n", " ")

            display_text = f"{language.upper()} | {mode}\n{code_preview}...\n{created_at}"

            list_item = QListWidgetItem(display_text)
            list_item.setData(1, item["id"])
            self.list_widget.addItem(list_item)

    def on_item_clicked(self, item: QListWidgetItem):
        """Handle history item click"""
        history_id = item.data(1)
        for hist_item in self.history_items:
            if hist_item["id"] == history_id:
                self.history_selected.emit(hist_item)
                self.delete_btn.setEnabled(True)
                break

    def on_delete_clicked(self):
        """Handle delete button click"""
        current_item = self.list_widget.currentItem()
        if current_item:
            reply = QMessageBox.question(
                self,
                "Delete History",
                "Are you sure you want to delete this history entry?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                history_id = current_item.data(1)
                self.history_deleted.emit(history_id)
                self.list_widget.takeItem(self.list_widget.row(current_item))
                self.delete_btn.setEnabled(False)

    def clear_selection(self):
        """Clear the current selection"""
        self.list_widget.clearSelection()
        self.delete_btn.setEnabled(False)
