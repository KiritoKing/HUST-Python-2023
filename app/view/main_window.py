from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import PushButton, ToolButton, FluentIcon as FIF
from qframelesswindow import FramelessWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import subprocess
from ..components.status_bar import StatusBar
from ..components.title_bar import CustomTitleBar
from ..components.server_sec import ServerSection
from .listen_window import ListenWindow


class MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.cur_dir = '/'

        self.setTitleBar(CustomTitleBar(self))
        self.qvLayout = QVBoxLayout(self)

        self.initLayout()
        self.initWindow()

    def initLayout(self):
        self.resize(500, 400)
        self.setMinimumSize(500, 400)
        self.setWindowTitle('PyQt LAN File Share')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        self.qvLayout.setSpacing(0)
        self.qvLayout.setContentsMargins(10, 50, 10, 10)
        self.qvLayout.setAlignment(Qt.AlignTop)

    def initWindow(self):
        # head bar
        self.head = QHBoxLayout()
        self.head.setContentsMargins(10, 0, 10, 0)
        addButton = PushButton(text='Add Listener', icon=FIF.ADD)
        addButton.clicked.connect(self.newListener)
        settingButton = ToolButton(FIF.SETTING)
        self.head.addWidget(addButton)
        self.head.setAlignment(addButton, Qt.AlignLeft)
        self.head.addWidget(settingButton)
        self.head.setAlignment(settingButton, Qt.AlignRight)
        self.qvLayout.addLayout(self.head)
        # server
        self.server = ServerSection(8888)
        self.qvLayout.addWidget(self.server)

    def newListener(self):
        lw = ListenWindow('127.0.0.1', 8888, self)
        lw.exec_()
