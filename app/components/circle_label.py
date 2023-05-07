from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class CircleLabel(QLabel):
    def __init__(self, color="green", parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        brush = QBrush(QColor(self.color))
        painter.setBrush(brush)
        radius = min(self.width(), self.height()) / 2 - 2
        center = self.rect().center()
        center.setY(center.y() + 2)
        painter.drawEllipse(center, radius, radius)
        super().paintEvent(event)
