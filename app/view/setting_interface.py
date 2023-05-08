# coding:utf-8
# from config import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard,
                            ColorSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)
from qfluentwidgets import InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog
from ..components.text_label import TextLabel
from ..components.edit_setting_card import EditSettingCard
import os
from ..common.config import cfg
import shutil
from ..common.get_resource import get_resource


class SettingInterface(ScrollArea):
    portChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.downloadPath = os.path.join(os.getcwd(), 'downloaded')

        self.initUi()
        self.initQss()
        self.initLayout()

    def initUi(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.commonGroup = SettingCardGroup("Common", self.scrollWidget)
        self.downloadFolderCard = PushSettingCard("Clear", FIF.DELETE, "Download Folder", self.downloadPath, self.commonGroup)
        self.downloadFolderCard.clicked.connect(self.handleClear)
        self.portCard = EditSettingCard(cfg.port, FIF.SYNC, "Port", "The port to broadcast in LAN", self.commonGroup)
        self.portCard.commit.connect(self.handleChangePort)
        self.aboutGroup = SettingCardGroup("About", self.scrollWidget)
        self.aboutCard = HyperlinkCard(
            "https://github.com/KiritoKing/HUST-Python",
            'Visit Github Repo',
            FIF.CODE,
            'Source',
            'Visit my github repo to check the codes',
            self.aboutGroup)

    def initQss(self):
        self.scrollWidget.setObjectName('scrollWidget')
        theme = 'light'
        try:
            with open(get_resource('style.qss'), encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except:
            print("QSS file not found!")

    def initLayout(self):
        self.commonGroup.addSettingCard(self.downloadFolderCard)
        self.commonGroup.addSettingCard(self.portCard)

        self.aboutGroup.addSettingCard(self.aboutCard)

        self.expandLayout.setSpacing(20)
        self.expandLayout.setContentsMargins(10, 10, 10, 10)
        self.expandLayout.addWidget(self.commonGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def createSuccessInfoBar(self, text="Refreshed!"):
        # convenient class mothod
        InfoBar.success(
            title='',
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )

    def createErrorInfoBar(self, text):
        InfoBar.error(
            title='',
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )

    def handleClear(self):
        if os.path.exists(self.downloadPath) and os.path.isdir(self.downloadPath):
            shutil.rmtree(self.downloadPath)
            print("Cleared!")
        self.createSuccessInfoBar("Cleared!")

    def handleChangePort(self):
        try:
            port = int(self.portCard.edit.text())
            if (port != cfg.port.value):
                cfg.set(cfg.port, port)
                self.portChanged.emit(int(self.portCard.edit.text()))
            self.createSuccessInfoBar("Port changed!")
        except:
            self.createErrorInfoBar("Invalid port!")
