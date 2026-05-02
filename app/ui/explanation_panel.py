"""Explanation display panel with markdown rendering"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import markdown
import re


class ExplanationPanel(QWidget):
    """Panel for displaying AI-generated explanations"""

    copy_requested = pyqtSignal()
    save_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_text = ""
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.setReadOnly(True)

        font = QFont("Segoe UI", 11)
        self.text_browser.setFont(font)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)

        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.clicked.connect(self.on_copy_clicked)

        self.save_txt_btn = QPushButton("💾 Save as TXT")
        self.save_txt_btn.clicked.connect(lambda: self.on_save_clicked("txt"))

        self.save_md_btn = QPushButton("💾 Save as MD")
        self.save_md_btn.clicked.connect(lambda: self.on_save_clicked("md"))

        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.save_txt_btn)
        button_layout.addWidget(self.save_md_btn)
        button_layout.addStretch()

        layout.addWidget(self.text_browser)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_text(self, text: str):
        """Set explanation text (markdown)"""
        self.current_text = text
        html = self.markdown_to_html(text)
        self.text_browser.setHtml(html)

    def append_text(self, text: str):
        """Append text for streaming"""
        self.current_text += text
        html = self.markdown_to_html(self.current_text)
        self.text_browser.setHtml(html)
        scrollbar = self.text_browser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear(self):
        """Clear the explanation"""
        self.current_text = ""
        self.text_browser.clear()

    def markdown_to_html(self, md_text: str) -> str:
        """Convert markdown to HTML with custom styling"""
        html_content = markdown.markdown(
            md_text,
            extensions=['fenced_code', 'tables', 'nl2br']
        )

        styled_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    color: #cdd6f4;
                    background-color: #1e1e2e;
                    padding: 15px;
                }}
                h1, h2, h3 {{
                    color: #89b4fa;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }}
                h1 {{ font-size: 24px; }}
                h2 {{ font-size: 20px; }}
                h3 {{ font-size: 16px; }}
                p {{
                    margin: 10px 0;
                }}
                code {{
                    background-color: #181825;
                    color: #a6e3a1;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 13px;
                }}
                pre {{
                    background-color: #181825;
                    color: #cdd6f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    border-left: 3px solid #89b4fa;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    color: #cdd6f4;
                }}
                ul, ol {{
                    margin: 10px 0;
                    padding-left: 30px;
                }}
                li {{
                    margin: 5px 0;
                }}
                strong {{
                    color: #f9e2af;
                    font-weight: bold;
                }}
                em {{
                    color: #cba6f7;
                    font-style: italic;
                }}
                blockquote {{
                    border-left: 4px solid #89b4fa;
                    padding-left: 15px;
                    margin: 15px 0;
                    color: #a6adc8;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        return styled_html

    def on_copy_clicked(self):
        """Handle copy button click"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_text)
        QMessageBox.information(self, "Copied", "Explanation copied to clipboard!")

    def on_save_clicked(self, format_type: str):
        """Handle save button click"""
        if not self.current_text:
            QMessageBox.warning(self, "No Content", "There is no explanation to save.")
            return

        if format_type == "txt":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Explanation", "", "Text Files (*.txt)"
            )
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Explanation", "", "Markdown Files (*.md)"
            )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_text)
                QMessageBox.information(self, "Saved", f"Explanation saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
