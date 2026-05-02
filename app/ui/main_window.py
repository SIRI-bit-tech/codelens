"""Main application window"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPushButton, QComboBox, QToolBar, QFileDialog, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

from app.config.settings import Settings
from app.config.constants import SUPPORTED_LANGUAGES, LANGUAGE_EXTENSIONS
from app.data.database import Database
from app.data.history_repo import HistoryRepository
from app.data.snippet_repo import SnippetRepository
from app.services.ai_service import AIService
from app.services.language_detector import LanguageDetector
from app.services.export_service import ExportService
from app.utils.keyring_helper import KeyringHelper
from app.utils.token_counter import TokenCounter
from app.utils.file_handler import FileHandler

from .code_editor import CodeEditor
from .explanation_panel import ExplanationPanel
from .chat_panel import ChatPanel
from .status_bar import CustomStatusBar
from .settings_dialog import SettingsDialog
from .history_panel import HistoryPanel
from .snippet_dialog import SnippetDialog
from .components.mode_selector import ModeSelector
from .components.loading_spinner import LoadingSpinner


class ExplainWorker(QThread):
    """Worker thread for code explanation"""

    chunk_received = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, ai_service, code, language, mode, stream):
        super().__init__()
        self.ai_service = ai_service
        self.code = code
        self.language = language
        self.mode = mode
        self.stream = stream
        self.is_running = True

    def run(self):
        """Run the explanation task"""
        try:
            if self.stream:
                result = self.ai_service.explain_code(
                    self.code,
                    self.language,
                    self.mode,
                    stream=True,
                    on_chunk=lambda chunk: self.chunk_received.emit(chunk) if self.is_running else None
                )
            else:
                result = self.ai_service.explain_code(
                    self.code,
                    self.language,
                    self.mode,
                    stream=False
                )
            if self.is_running:
                self.finished.emit(result)
        except Exception as e:
            if self.is_running:
                self.error.emit(str(e))

    def stop(self):
        """Stop the worker"""
        self.is_running = False


class ChatWorker(QThread):
    """Worker thread for chat"""

    chunk_received = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, ai_service, message, code, explanation, history, stream):
        super().__init__()
        self.ai_service = ai_service
        self.message = message
        self.code = code
        self.explanation = explanation
        self.history = history
        self.stream = stream
        self.is_running = True

    def run(self):
        """Run the chat task"""
        try:
            if self.stream:
                result = self.ai_service.chat(
                    self.message,
                    self.code,
                    self.explanation,
                    self.history,
                    stream=True,
                    on_chunk=lambda chunk: self.chunk_received.emit(chunk) if self.is_running else None
                )
            else:
                result = self.ai_service.chat(
                    self.message,
                    self.code,
                    self.explanation,
                    self.history,
                    stream=False
                )
            if self.is_running:
                self.finished.emit(result)
        except Exception as e:
            if self.is_running:
                self.error.emit(str(e))

    def stop(self):
        """Stop the worker"""
        self.is_running = False


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.database = Database()
        self.history_repo = HistoryRepository(self.database)
        self.snippet_repo = SnippetRepository(self.database)

        self.ai_service = None
        self.current_code = ""
        self.current_language = "auto"
        self.current_explanation = ""
        self.chat_history = []
        self.current_history_id = None

        self.explain_worker = None
        self.chat_worker = None

        self.init_ui()
        self.init_ai_service()
        self.apply_theme()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("CodeLens - AI Code Explainer")
        self.setGeometry(100, 100, 1400, 900)

        self.create_toolbar()
        self.create_central_widget()
        self.create_status_bar()
        self.create_shortcuts()

    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QAction("📂 Open File", self)
        open_action.triggered.connect(self.on_open_file)
        toolbar.addAction(open_action)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()
        self.language_combo.addItem("Auto", "auto")
        for lang in SUPPORTED_LANGUAGES:
            self.language_combo.addItem(lang.title(), lang)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        toolbar.addWidget(self.language_combo)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("Mode:"))
        self.mode_selector = ModeSelector()
        self.mode_selector.mode_changed.connect(self.on_mode_changed)
        toolbar.addWidget(self.mode_selector)

        toolbar.addSeparator()

        self.explain_btn = QPushButton("⚡ Explain")
        self.explain_btn.clicked.connect(self.on_explain_clicked)
        toolbar.addWidget(self.explain_btn)

        clear_btn = QPushButton("🔄 Clear")
        clear_btn.clicked.connect(self.on_clear_clicked)
        toolbar.addWidget(clear_btn)

        toolbar.addSeparator()

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.on_settings_clicked)
        toolbar.addWidget(settings_btn)

    def create_central_widget(self):
        """Create the central widget with panels"""
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.code_editor = CodeEditor()
        main_splitter.addWidget(self.code_editor)

        right_splitter = QSplitter(Qt.Orientation.Vertical)

        self.explanation_panel = ExplanationPanel()
        right_splitter.addWidget(self.explanation_panel)

        self.chat_panel = ChatPanel()
        self.chat_panel.message_sent.connect(self.on_chat_message_sent)
        self.chat_panel.clear_requested.connect(self.on_chat_cleared)
        right_splitter.addWidget(self.chat_panel)

        right_splitter.setSizes([650, 350])

        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([630, 770])

        main_layout.addWidget(main_splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = CustomStatusBar()
        self.setStatusBar(self.status_bar)

    def create_shortcuts(self):
        """Create keyboard shortcuts"""
        explain_shortcut = QKeySequence("Ctrl+Return")
        explain_action = QAction(self)
        explain_action.setShortcut(explain_shortcut)
        explain_action.triggered.connect(self.on_explain_clicked)
        self.addAction(explain_action)

        open_shortcut = QKeySequence("Ctrl+O")
        open_action = QAction(self)
        open_action.setShortcut(open_shortcut)
        open_action.triggered.connect(self.on_open_file)
        self.addAction(open_action)

        clear_shortcut = QKeySequence("Ctrl+L")
        clear_action = QAction(self)
        clear_action.setShortcut(clear_shortcut)
        clear_action.triggered.connect(self.on_clear_clicked)
        self.addAction(clear_action)

        settings_shortcut = QKeySequence("Ctrl+,")
        settings_action = QAction(self)
        settings_action.setShortcut(settings_shortcut)
        settings_action.triggered.connect(self.on_settings_clicked)
        self.addAction(settings_action)

    def init_ai_service(self):
        """Initialize AI service with API key"""
        api_key = KeyringHelper.get_api_key()
        if api_key:
            try:
                self.ai_service = AIService(api_key)
                # Don't test connection on startup to avoid rate limiting
                # Connection will be tested when user actually tries to explain code
                self.status_bar.set_connection_status(True)
            except Exception as e:
                self.status_bar.set_connection_status(False)
                QMessageBox.critical(
                    self,
                    "API Error",
                    f"Error initializing AI service: {str(e)}"
                )
        else:
            self.status_bar.set_connection_status(False)

    def on_open_file(self):
        """Handle open file action"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Code File",
            "",
            "All Supported Files (*.py *.js *.ts *.java *.cpp *.c *.cs *.go *.rs *.php *.rb *.swift *.kt *.sql *.html *.css *.json *.yaml *.sh *.r *.dart);;All Files (*.*)"
        )

        if file_path:
            content, error = FileHandler.read_file(file_path)
            if error:
                QMessageBox.critical(self, "Error", error)
            else:
                self.code_editor.setPlainText(content)
                extension = FileHandler.get_file_extension(file_path)
                detected_lang = LanguageDetector.detect_from_extension(extension)
                if detected_lang and self.settings.get_auto_detect_language():
                    self.set_language(detected_lang)
                self.status_bar.set_last_action("File opened")

    def on_language_changed(self, index):
        """Handle language selection change"""
        self.current_language = self.language_combo.itemData(index)
        self.status_bar.set_language(self.current_language)

    def on_mode_changed(self, mode):
        """Handle mode change"""
        pass

    def on_explain_clicked(self):
        """Handle explain button click"""
        if self.explain_worker and self.explain_worker.isRunning():
            self.explain_worker.stop()
            self.explain_worker.wait()
            self.explain_btn.setText("⚡ Explain")
            return

        code = self.code_editor.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "No Code", "Please paste or open some code first.")
            return

        if not self.ai_service:
            QMessageBox.warning(
                self,
                "No API Key",
                "Please add your Google Gemini API key in Settings (⚙️)"
            )
            self.on_settings_clicked()
            return

        self.current_code = code

        if self.current_language == "auto":
            detected_lang = LanguageDetector.detect_from_content(code)
            self.current_language = detected_lang
            self.status_bar.set_language(detected_lang)

        mode = self.mode_selector.get_current_mode()

        token_count = TokenCounter.estimate_tokens_for_code_explanation(code, mode)
        self.status_bar.set_token_count(token_count)

        self.explanation_panel.clear()
        self.explain_btn.setText("⏹ Stop")

        stream = self.settings.get_stream_responses()

        self.explain_worker = ExplainWorker(
            self.ai_service, code, self.current_language, mode, stream
        )
        self.explain_worker.chunk_received.connect(self.on_explanation_chunk)
        self.explain_worker.finished.connect(self.on_explanation_finished)
        self.explain_worker.error.connect(self.on_explanation_error)
        self.explain_worker.start()

        self.status_bar.set_last_action("Explaining code")

    def on_explanation_chunk(self, chunk):
        """Handle explanation chunk (streaming)"""
        self.explanation_panel.append_text(chunk)

    def on_explanation_finished(self, explanation):
        """Handle explanation completion"""
        self.current_explanation = explanation
        self.explain_btn.setText("⚡ Explain")
        self.status_bar.set_last_action("Explanation complete")

        if self.settings.get_save_history():
            mode = self.mode_selector.get_current_mode()
            self.current_history_id = self.history_repo.create(
                self.current_language,
                mode,
                self.current_code,
                explanation,
                []
            )

    def on_explanation_error(self, error):
        """Handle explanation error"""
        self.explain_btn.setText("⚡ Explain")
        QMessageBox.critical(self, "Error", f"Error generating explanation: {error}")
        self.status_bar.set_last_action("Error occurred")

    def on_chat_message_sent(self, message):
        """Handle chat message sent"""
        if not self.current_explanation:
            QMessageBox.warning(self, "No Explanation", "Please explain some code first before asking questions.")
            return

        if not self.ai_service:
            QMessageBox.warning(self, "No API Key", "Please add your API key in Settings.")
            return

        stream = self.settings.get_stream_responses()

        self.chat_worker = ChatWorker(
            self.ai_service,
            message,
            self.current_code,
            self.current_explanation,
            self.chat_history,
            stream
        )
        self.chat_worker.chunk_received.connect(self.on_chat_chunk)
        self.chat_worker.finished.connect(self.on_chat_finished)
        self.chat_worker.error.connect(self.on_chat_error)
        self.chat_worker.start()

        self.chat_history.append({"role": "user", "parts": [message]})

    def on_chat_chunk(self, chunk):
        """Handle chat chunk (streaming)"""
        if hasattr(self, '_current_chat_response'):
            self._current_chat_response += chunk
        else:
            self._current_chat_response = chunk
        self.chat_panel.add_ai_message_streaming(self._current_chat_response)

    def on_chat_finished(self, response):
        """Handle chat completion"""
        self._current_chat_response = ""
        self.chat_history.append({"role": "model", "parts": [response]})

        if self.current_history_id and self.settings.get_save_history():
            self.history_repo.update_chat_history(self.current_history_id, self.chat_history)

        self.status_bar.set_last_action("Chat response received")

    def on_chat_error(self, error):
        """Handle chat error"""
        QMessageBox.critical(self, "Error", f"Error in chat: {error}")

    def on_chat_cleared(self):
        """Handle chat cleared"""
        self.chat_history = []

    def on_clear_clicked(self):
        """Handle clear button click"""
        self.code_editor.clear()
        self.explanation_panel.clear()
        self.chat_panel.clear_messages()
        self.current_code = ""
        self.current_explanation = ""
        self.chat_history = []
        self.current_history_id = None
        self.status_bar.set_last_action("Cleared")

    def on_settings_clicked(self):
        """Handle settings button click"""
        dialog = SettingsDialog(self.settings, self)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec()

    def on_settings_changed(self):
        """Handle settings changed"""
        self.init_ai_service()
        self.apply_theme()

    def set_language(self, language):
        """Set the language in the combo box"""
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == language:
                self.language_combo.setCurrentIndex(i)
                break

    def apply_theme(self):
        """Apply the selected theme"""
        theme = self.settings.get_theme()
        if theme == "dark":
            self.load_dark_theme()
        elif theme == "light":
            self.load_light_theme()
        else:
            self.load_dark_theme()

    def load_dark_theme(self):
        """Load dark theme stylesheet"""
        dark_style = """
        QMainWindow, QWidget {
            background-color: #1e1e2e;
            color: #cdd6f4;
        }
        QToolBar {
            background-color: #181825;
            border-bottom: 1px solid #313244;
            padding: 5px;
        }
        QPushButton {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            padding: 5px 15px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #45475a;
        }
        QPushButton:pressed {
            background-color: #585b70;
        }
        QPushButton:checked {
            background-color: #89b4fa;
            color: #1e1e2e;
        }
        QComboBox {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            padding: 5px;
            border-radius: 3px;
        }
        QLineEdit, QPlainTextEdit, QTextEdit {
            background-color: #181825;
            color: #cdd6f4;
            border: 1px solid #313244;
            padding: 5px;
            border-radius: 3px;
        }
        QListWidget {
            background-color: #181825;
            color: #cdd6f4;
            border: 1px solid #313244;
        }
        QScrollBar:vertical {
            background-color: #181825;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background-color: #45475a;
            border-radius: 6px;
        }
        #userBubble {
            background-color: #89b4fa;
            color: #ffffff;
            border-radius: 12px;
        }
        #aiBubble {
            background-color: #2a2a3e;
            color: #e0e0e0;
            border-radius: 12px;
            border: 1px solid #3a3a4e;
        }
        """
        self.setStyleSheet(dark_style)

    def load_light_theme(self):
        """Load light theme stylesheet"""
        light_style = """
        QMainWindow, QWidget {
            background-color: #ffffff;
            color: #1e1e2e;
        }
        QToolBar {
            background-color: #f5f5f5;
            border-bottom: 1px solid #e0e0e0;
            padding: 5px;
        }
        QPushButton {
            background-color: #e0e0e0;
            color: #1e1e2e;
            border: 1px solid #c0c0c0;
            padding: 5px 15px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QPushButton:checked {
            background-color: #1e66f5;
            color: #ffffff;
        }
        QComboBox {
            background-color: #f5f5f5;
            color: #1e1e2e;
            border: 1px solid #c0c0c0;
            padding: 5px;
        }
        QLineEdit, QPlainTextEdit, QTextEdit {
            background-color: #ffffff;
            color: #1e1e2e;
            border: 1px solid #c0c0c0;
            padding: 5px;
        }
        #userBubble {
            background-color: #1e66f5;
            color: #ffffff;
            border-radius: 12px;
        }
        #aiBubble {
            background-color: #f5f5f5;
            color: #1e1e2e;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
        }
        """
        self.setStyleSheet(light_style)

    def closeEvent(self, event):
        """Handle window close event"""
        if self.explain_worker and self.explain_worker.isRunning():
            self.explain_worker.stop()
            self.explain_worker.wait()
        if self.chat_worker and self.chat_worker.isRunning():
            self.chat_worker.stop()
            self.chat_worker.wait()
        self.database.close()
        event.accept()
