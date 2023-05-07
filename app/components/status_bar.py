from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from qfluentwidgets import TextWrap
from qfluentwidgets import FluentIcon as FIF, Icon
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush


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


class StatusBar(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.spacing = 10

        self.sucIcon = Icon(FIF.ACCEPT).pixmap(20, 20)
        self.fialIcon = Icon(FIF.CANCEL).pixmap(20, 20)
        self.logo = CircleLabel(color="green")

        font = QFont("Microsoft YaHei", 12, 50)
        self.ipBar = QLabel(TextWrap.wrap('Exposed at: 127.0.0.1:8888', 45, False)[0])
        self.ipBar.setFont(font)

        self.layout.addWidget(self.logo)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.ipBar)
