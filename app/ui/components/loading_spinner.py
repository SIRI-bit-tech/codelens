"""Animated loading spinner widget"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen


class LoadingSpinner(QWidget):
    """Animated loading spinner"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.setFixedSize(40, 40)

    def start(self):
        """Start the spinner animation"""
        self.timer.start(50)
        self.show()

    def stop(self):
        """Stop the spinner animation"""
        self.timer.stop()
        self.hide()

    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        """Paint the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)

        pen = QPen(QColor("#89b4fa"))
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        for i in range(8):
            alpha = 255 - (i * 30)
            pen.setColor(QColor(137, 180, 250, alpha))
            painter.setPen(pen)
            painter.drawLine(0, -15, 0, -10)
            painter.rotate(45)
