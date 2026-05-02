"""Syntax-highlighted code editor widget"""

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QPainter, QTextFormat, QFont, QSyntaxHighlighter, QTextCharFormat
import re

try:
    from PyQt6.Qsci import QsciScintilla, QsciLexerPython
    QSCI_AVAILABLE = True
except ImportError:
    QSCI_AVAILABLE = False


class LineNumberArea(QWidget):
    """Line number area for code editor"""

    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return self.code_editor.line_number_area_width()

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class SimpleSyntaxHighlighter(QSyntaxHighlighter):
    """Simple syntax highlighter for common programming constructs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#cba6f7"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "\\bdef\\b", "\\bclass\\b", "\\bif\\b", "\\belse\\b", "\\belif\\b",
            "\\bfor\\b", "\\bwhile\\b", "\\breturn\\b", "\\bimport\\b", "\\bfrom\\b",
            "\\btry\\b", "\\bexcept\\b", "\\bfinally\\b", "\\bwith\\b", "\\bas\\b",
            "\\bfunction\\b", "\\bconst\\b", "\\blet\\b", "\\bvar\\b", "\\bpublic\\b",
            "\\bprivate\\b", "\\bprotected\\b", "\\bstatic\\b", "\\bvoid\\b", "\\bint\\b",
        ]
        for keyword in keywords:
            self.highlighting_rules.append((re.compile(keyword), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a6e3a1"))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6c7086"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r"//[^\n]*"), comment_format))
        self.highlighting_rules.append((re.compile(r"#[^\n]*"), comment_format))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#fab387"))
        self.highlighting_rules.append((re.compile(r"\b[0-9]+\.?[0-9]*\b"), number_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)


class CodeEditor(QPlainTextEdit):
    """Code editor with line numbers and syntax highlighting"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)

        font = QFont("Courier New", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        self.setTabStopDistance(40)

        self.highlighter = SimpleSyntaxHighlighter(self.document())

    def line_number_area_width(self):
        """Calculate width needed for line numbers"""
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        """Update line number area width"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """Update line number area on scroll"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        """Paint line numbers"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#181825"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#6c7086"))
                painter.drawText(0, int(top), self.line_number_area.width() - 5, self.fontMetrics().height(),
                                Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
