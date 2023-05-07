import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication
from qfluentwidgets import PushButton, FluentIcon as FIF, ToolTipFilter, ToolTipPosition, InfoBar, InfoBarPosition
from .text_label import TextLabel
from .file_list import FileList
from .circle_label import CircleLabel
import os
import socket


class ServerSection(QWidget):
    def __init__(self, port: int, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        hostname = socket.gethostname()
        self.cur_dir = 'shared'
        self.host = socket.gethostbyname(hostname)
        self.port = port

        self.initStatus()
        self.initList()
        self.initControls()

    def initStatus(self):
        self.status = QHBoxLayout()
        self.status.setContentsMargins(0, 0, 0, 0)
        self.status.setSpacing(0)
        self.status.setAlignment(Qt.AlignCenter)

        self.logo = CircleLabel(color="green")

        self.ip = TextLabel(f"Exposed at: {self.host}:{self.port}")
        self.ip.setToolTip("Click to copy!")
        self.ip.setToolTipDuration(1000)
        self.ip.installEventFilter(ToolTipFilter(self.ip, 0, ToolTipPosition.TOP))
        self.ip.mousePressEvent = lambda e: self.copyTextToClipboard(f"{self.host}:{self.port}")

        self.status.addWidget(self.logo)
        self.status.addSpacing(5)
        self.status.addWidget(self.ip)
        self.layout.addLayout(self.status)

    def initList(self):
        self.list = FileList(open_handler=self.openHandler)
        self.loadDir()
        self.layout.addWidget(self.list)

    def initControls(self):
        control = QHBoxLayout()
        control.setContentsMargins(0, 5, 0, 10)
        control.setSpacing(0)
        control.setAlignment(Qt.AlignCenter)
        addBtn = PushButton('Add', None, FIF.ADD)
        delBtn = PushButton('Delete', None, FIF.DELETE)
        control.addWidget(addBtn)
        control.addSpacing(10)
        control.addWidget(delBtn)
        self.layout.addLayout(control)
        # self.list.clicked.connect(None)

    def loadDir(self):
        if not os.path.exists(self.cur_dir):
            os.mkdir(self.cur_dir)
        files = os.listdir(self.cur_dir)
        data = [(f, os.path.join(self.cur_dir, f)) if os.path.isfile(os.path.join(self.cur_dir, f)) else (f + '/', os.path.join(self.cur_dir, f)) for f in files]
        print(*data)
        self.list.updateList([("..", os.path.dirname(self.cur_dir))] + data if self.cur_dir != 'shared' else data)

    def openHandler(self, item):
        name, href = item.model().data(item, Qt.DisplayRole), item.model().get_href(item)
        print(href)

        if (os.path.isdir(href) or name == '..'):
            print("open dir: ", href)
            self.cur_dir = href
            self.loadDir()
        else:
            subprocess.Popen(['start', href], shell=True)

    def copyTextToClipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.createSuccessInfoBar("Copied!")

    def createSuccessInfoBar(self, text):
        # convenient class mothod
        InfoBar.success(
            title='成功',
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
