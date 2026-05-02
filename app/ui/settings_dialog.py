"""Settings dialog window"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QSlider, QGroupBox, QMessageBox, QTabWidget, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from app.config.settings import Settings
from app.config.constants import (
    EXPLANATION_MODES, MODE_DISPLAY_NAMES, FONT_SIZE_MIN, FONT_SIZE_MAX,
    AI_PROVIDERS, AI_PROVIDER_DISPLAY_NAMES
)
from app.utils.keyring_helper import KeyringHelper


class SettingsDialog(QDialog):
    """Settings configuration dialog"""

    settings_changed = pyqtSignal()

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(550)
        self.setMinimumHeight(500)
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()

        # API Configuration Group
        api_group = QGroupBox("API Configuration")
        api_layout = QVBoxLayout()

        # Provider selection
        provider_layout = QHBoxLayout()
        provider_label = QLabel("AI Provider:")
        self.provider_combo = QComboBox()
        for provider in AI_PROVIDERS:
            self.provider_combo.addItem(AI_PROVIDER_DISPLAY_NAMES[provider], provider)
        self.provider_combo.currentIndexChanged.connect(self.on_provider_changed)
        provider_layout.addWidget(provider_label)
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()

        # API Key inputs for each provider
        self.api_key_widgets = {}
        
        # Gemini
        gemini_label = QLabel("Google Gemini API Key:")
        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_key_input.setPlaceholderText("Get from https://aistudio.google.com")
        gemini_key = KeyringHelper.get_api_key("gemini")
        if gemini_key:
            self.gemini_key_input.setText(gemini_key)
        self.api_key_widgets["gemini"] = (gemini_label, self.gemini_key_input)

        # OpenAI
        openai_label = QLabel("OpenAI API Key:")
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setPlaceholderText("Get from https://platform.openai.com/api-keys")
        openai_key = KeyringHelper.get_api_key("openai")
        if openai_key:
            self.openai_key_input.setText(openai_key)
        self.api_key_widgets["openai"] = (openai_label, self.openai_key_input)

        # Claude
        claude_label = QLabel("Anthropic Claude API Key:")
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.claude_key_input.setPlaceholderText("Get from https://console.anthropic.com")
        claude_key = KeyringHelper.get_api_key("claude")
        if claude_key:
            self.claude_key_input.setText(claude_key)
        self.api_key_widgets["claude"] = (claude_label, self.claude_key_input)

        # Add all API key fields
        api_layout.addLayout(provider_layout)
        api_layout.addWidget(gemini_label)
        api_layout.addWidget(self.gemini_key_input)
        api_layout.addWidget(openai_label)
        api_layout.addWidget(self.openai_key_input)
        api_layout.addWidget(claude_label)
        api_layout.addWidget(self.claude_key_input)

        privacy_label = QLabel(
            "⚠️ Your code is sent to the selected AI provider for explanation.\n"
            "See each provider's privacy policy for details."
        )
        privacy_label.setStyleSheet("color: #f9e2af; font-size: 10px;")
        privacy_label.setWordWrap(True)

        api_layout.addWidget(privacy_label)
        api_group.setLayout(api_layout)

        # Appearance Group
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

        # Behavior Group
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

        # Buttons
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

    def on_provider_changed(self, index):
        """Handle provider selection change"""
        # Just update the UI to show which provider is selected
        # All API keys are always visible
        pass

    def load_settings(self):
        """Load current settings into UI"""
        # Load AI provider
        provider = self.settings.get_ai_provider()
        for i in range(self.provider_combo.count()):
            if self.provider_combo.itemData(i) == provider:
                self.provider_combo.setCurrentIndex(i)
                break

        # Load theme
        theme = self.settings.get_theme()
        theme_index = {"system": 0, "light": 1, "dark": 2}.get(theme, 0)
        self.theme_combo.setCurrentIndex(theme_index)

        # Load font size
        self.font_slider.setValue(self.settings.get_font_size())

        # Load default mode
        default_mode = self.settings.get_default_mode()
        for i in range(self.mode_combo.count()):
            if self.mode_combo.itemData(i) == default_mode:
                self.mode_combo.setCurrentIndex(i)
                break

        # Load checkboxes
        self.stream_checkbox.setChecked(self.settings.get_stream_responses())
        self.auto_detect_checkbox.setChecked(self.settings.get_auto_detect_language())
        self.save_history_checkbox.setChecked(self.settings.get_save_history())

    def on_save_clicked(self):
        """Save settings"""
        # Save selected provider
        provider = self.provider_combo.currentData()
        self.settings.set_ai_provider(provider)

        # Save all API keys
        gemini_key = self.gemini_key_input.text().strip()
        if gemini_key:
            KeyringHelper.set_api_key("gemini", gemini_key)

        openai_key = self.openai_key_input.text().strip()
        if openai_key:
            KeyringHelper.set_api_key("openai", openai_key)

        claude_key = self.claude_key_input.text().strip()
        if claude_key:
            KeyringHelper.set_api_key("claude", claude_key)

        # Check if selected provider has an API key
        selected_provider_key = KeyringHelper.get_api_key(provider)
        if not selected_provider_key:
            QMessageBox.warning(
                self,
                "No API Key",
                f"Please enter an API key for {AI_PROVIDER_DISPLAY_NAMES[provider]} before saving."
            )
            return

        # Save other settings
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
