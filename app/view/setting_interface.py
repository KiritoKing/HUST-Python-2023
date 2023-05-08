# coding:utf-8
# from config import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard,
                            ColorSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog
from ..components.text_label import TextLabel
from ..components.edit_setting_card import EditSettingCard
import os
from ..common.config import cfg


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.initUi()
        self.initQss()
        self.initLayout()

    def initUi(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.commonGroup = SettingCardGroup("Common", self.scrollWidget)
        self.downloadFolderCard = PushSettingCard("Clear", FIF.DELETE, "Download Folder",
                                                  os.path.join(os.getcwd(), 'downloaded'), self.commonGroup)
        self.portCard = EditSettingCard(cfg.port, FIF.SYNC, "Port", "The port to broadcast in LAN", self.commonGroup)

    def initQss(self):
        self.scrollWidget.setObjectName('scrollWidget')
        theme = 'light'
        try:
            with open(f'app/resources/qss/{theme}/setting_interface.qss', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except:
            print("QSS file not found!")

    def initLayout(self):
        self.commonGroup.addSettingCard(self.downloadFolderCard)
        self.commonGroup.addSettingCard(self.portCard)

        self.expandLayout.setSpacing(20)
        self.expandLayout.setContentsMargins(10, 10, 10, 10)
        self.expandLayout.addWidget(self.commonGroup)
