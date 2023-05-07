from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from qfluentwidgets import TextWrap
from PyQt5.QtGui import QFont


class TextLabel(QLabel):
    def __init__(self, text: str = "", font: str = "Microsoft YaHei", size: int = 12, weight: int = 50, parent=None):
        super().__init__(parent)
        self.setText(TextWrap.wrap(text, 45, False)[0])
        font = QFont(font, size, weight)
        self.setFont(font)
