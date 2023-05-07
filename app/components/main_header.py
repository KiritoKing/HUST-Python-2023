from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import PushButton, ToolButton
from qfluentwidgets import FluentIcon as FIF


class MainHeader(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.addButton = PushButton(text='Add Listener', icon=FIF.ADD)
        self.settingButton = ToolButton(FIF.SETTING)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.settingButton)
        self.layout.setAlignment(self.addButton, Qt.AlignLeft)
        self.layout.setAlignment(self.settingButton, Qt.AlignRight)
