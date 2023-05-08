from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QDialog
from qfluentwidgets import InfoBar, InfoBarPosition, ToolButton, FluentIcon as FIF, LineEdit, LineEditButton
from qframelesswindow import FramelessDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from os import path
import subprocess
from ..components.file_list import FileList
from ..components.text_label import TextLabel
from ..components.title_bar import CustomTitleBar
from ..utils.client import Client
from .setting_interface import SettingInterface


class SettingWindow(FramelessDialog):
    portChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.resize(800, 600)
        self.setMinimumSize(500, 400)
        self.setTitleBar(CustomTitleBar(self))
        self.setWindowTitle(f'Settings')
        self.setWindowIcon(QIcon('app/resources/settings.png'))

        self.initUi()

    def initUi(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.settingInterface = SettingInterface(self)
        self.settingInterface.portChanged.connect(self.portChanged)
        self.hBoxLayout.setContentsMargins(10, 50, 10, 10)
        self.hBoxLayout.addWidget(self.settingInterface)
        self.titleBar.raise_()
        theme = 'light'
        with open(f'app/resources/qss/{theme}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
