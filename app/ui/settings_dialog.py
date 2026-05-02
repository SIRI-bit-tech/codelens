"""Settings dialog window"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QSlider, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from app.config.settings import Settings
from app.config.constants import EXPLANATION_MODES, MODE_DISPLAY_NAMES, FONT_SIZE_MIN, FONT_SIZE_MAX
from app.utils.keyring_helper import KeyringHelper


class SettingsDialog(QDialog):
    """Settings configuration dialog"""

    settings_changed = pyqtSignal()

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()

        api_group = QGroupBox("API Configuration")
        api_layout = QVBoxLayout()

        api_label = QLabel("Google Gemini API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Enter your API key from https://aistudio.google.com")

        current_key = KeyringHelper.get_api_key()
        if current_key:
            self.api_key_input.setText(current_key)

        privacy_label = QLabel(
            "⚠️ Your code is sent to Google's Gemini API for explanation.\n"
            "See Google's privacy policy for details."
        )
        privacy_label.setStyleSheet("color: #f9e2af; font-size: 10px;")
        privacy_label.setWordWrap(True)

        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        api_layout.addWidget(privacy_label)
        api_group.setLayout(api_layout)

        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()

        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Light", "Dark"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()

        font_layout = QHBoxLayout()
        font_label = QLabel("Font Size:")
        self.font_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_slider.setMinimum(FONT_SIZE_MIN)
        self.font_slider.setMaximum(FONT_SIZE_MAX)
        self.font_slider.setValue(13)
        self.font_value_label = QLabel("13")
        self.font_slider.valueChanged.connect(
            lambda v: self.font_value_label.setText(str(v))
        )
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_slider)
        font_layout.addWidget(self.font_value_label)

        appearance_layout.addLayout(theme_layout)
        appearance_layout.addLayout(font_layout)
        appearance_group.setLayout(appearance_layout)

        behavior_group = QGroupBox("Behavior")
        behavior_layout = QVBoxLayout()

        mode_layout = QHBoxLayout()
        mode_label = QLabel("Default Explanation Mode:")
        self.mode_combo = QComboBox()
        for mode in EXPLANATION_MODES:
            self.mode_combo.addItem(MODE_DISPLAY_NAMES.get(mode, mode), mode)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()

        self.stream_checkbox = QCheckBox("Stream responses in real-time")
        self.stream_checkbox.setChecked(True)

        self.auto_detect_checkbox = QCheckBox("Auto-detect programming language")
        self.auto_detect_checkbox.setChecked(True)

        self.save_history_checkbox = QCheckBox("Save explanation history")
        self.save_history_checkbox.setChecked(True)

        behavior_layout.addLayout(mode_layout)
        behavior_layout.addWidget(self.stream_checkbox)
        behavior_layout.addWidget(self.auto_detect_checkbox)
        behavior_layout.addWidget(self.save_history_checkbox)
        behavior_group.setLayout(behavior_layout)

        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save_clicked)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addWidget(api_group)
        layout.addWidget(appearance_group)
        layout.addWidget(behavior_group)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_settings(self):
        """Load current settings into UI"""
        theme = self.settings.get_theme()
        theme_index = {"system": 0, "light": 1, "dark": 2}.get(theme, 0)
        self.theme_combo.setCurrentIndex(theme_index)

        self.font_slider.setValue(self.settings.get_font_size())

        default_mode = self.settings.get_default_mode()
        for i in range(self.mode_combo.count()):
            if self.mode_combo.itemData(i) == default_mode:
                self.mode_combo.setCurrentIndex(i)
                break

        self.stream_checkbox.setChecked(self.settings.get_stream_responses())
        self.auto_detect_checkbox.setChecked(self.settings.get_auto_detect_language())
        self.save_history_checkbox.setChecked(self.settings.get_save_history())

    def on_save_clicked(self):
        """Save settings"""
        api_key = self.api_key_input.text().strip()
        if api_key:
            KeyringHelper.set_api_key(api_key)

        theme = self.theme_combo.currentText().lower()
        self.settings.set_theme(theme)

        self.settings.set_font_size(self.font_slider.value())

        mode = self.mode_combo.currentData()
        self.settings.set_default_mode(mode)

        self.settings.set_stream_responses(self.stream_checkbox.isChecked())
        self.settings.set_auto_detect_language(self.auto_detect_checkbox.isChecked())
        self.settings.set_save_history(self.save_history_checkbox.isChecked())

        self.settings_changed.emit()
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully!")
        self.accept()
