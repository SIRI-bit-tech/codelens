"""CodeLens - AI Code Explainer Desktop Application

Main entry point for the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("CodeLens")
    app.setOrganizationName("CodeLens")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
