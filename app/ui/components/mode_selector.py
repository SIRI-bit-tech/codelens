"""Explanation mode selector tabs"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtCore import pyqtSignal
from app.config.constants import EXPLANATION_MODES, MODE_DISPLAY_NAMES


class ModeSelector(QWidget):
    """Tab-style selector for explanation modes"""

    mode_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = "overview"
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.button_group = QButtonGroup(self)
        self.buttons = {}

        for mode in EXPLANATION_MODES:
            btn = QPushButton(MODE_DISPLAY_NAMES.get(mode, mode))
            btn.setCheckable(True)
            btn.setProperty("mode", mode)
            btn.clicked.connect(lambda checked, m=mode: self.on_mode_clicked(m))

            self.button_group.addButton(btn)
            self.buttons[mode] = btn
            layout.addWidget(btn)

        self.buttons["overview"].setChecked(True)

        layout.addStretch()
        self.setLayout(layout)

    def on_mode_clicked(self, mode: str):
        """Handle mode button click"""
        self.current_mode = mode
        self.mode_changed.emit(mode)

    def get_current_mode(self) -> str:
        """Get currently selected mode"""
        return self.current_mode

    def set_mode(self, mode: str):
        """Set the current mode"""
        if mode in self.buttons:
            self.buttons[mode].setChecked(True)
            self.current_mode = mode
