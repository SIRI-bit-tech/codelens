"""Snippet library dialog"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QInputDialog
)
from PyQt6.QtCore import pyqtSignal
from typing import List, Dict


class SnippetDialog(QDialog):
    """Dialog for managing code snippets"""

    snippet_selected = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.snippets = []
        self.setWindowTitle("Snippet Library")
        self.setModal(True)
        self.setMinimumSize(600, 400)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()

        header_label = QLabel("📚 Code Snippets")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search snippets...")
        self.search_input.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        button_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.on_load_clicked)
        self.load_btn.setEnabled(False)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        self.delete_btn.setEnabled(False)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.reject)

        self.list_widget.itemClicked.connect(self.on_item_clicked)

        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        layout.addWidget(header_label)
        layout.addLayout(search_layout)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_snippets(self, snippets: List[Dict]):
        """Load snippets into the list"""
        self.snippets = snippets
        self.refresh_list()

    def refresh_list(self, filter_text: str = ""):
        """Refresh the snippet list with optional filter"""
        self.list_widget.clear()

        for snippet in self.snippets:
            name = snippet.get("name", "Unnamed")
            language = snippet.get("language", "unknown")
            tags = snippet.get("tags", "")

            if filter_text:
                search_text = f"{name} {language} {tags}".lower()
                if filter_text.lower() not in search_text:
                    continue

            display_text = f"{name}\n{language.upper()}"
            if tags:
                display_text += f" | Tags: {tags}"

            list_item = QListWidgetItem(display_text)
            list_item.setData(1, snippet["id"])
            self.list_widget.addItem(list_item)

    def on_search_changed(self, text: str):
        """Handle search text change"""
        self.refresh_list(text)

    def on_item_clicked(self, item: QListWidgetItem):
        """Handle item click"""
        self.load_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle item double click"""
        self.on_load_clicked()

    def on_load_clicked(self):
        """Handle load button click"""
        current_item = self.list_widget.currentItem()
        if current_item:
            snippet_id = current_item.data(1)
            for snippet in self.snippets:
                if snippet["id"] == snippet_id:
                    self.snippet_selected.emit(snippet)
                    self.accept()
                    break

    def on_delete_clicked(self):
        """Handle delete button click"""
        current_item = self.list_widget.currentItem()
        if current_item:
            reply = QMessageBox.question(
                self,
                "Delete Snippet",
                "Are you sure you want to delete this snippet?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                snippet_id = current_item.data(1)
                self.snippets = [s for s in self.snippets if s["id"] != snippet_id]
                self.list_widget.takeItem(self.list_widget.row(current_item))
                self.load_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
