import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QFileDialog
from qfluentwidgets import PushButton, FluentIcon as FIF, ToolTipFilter, ToolTipPosition, InfoBar, InfoBarPosition
from .text_label import TextLabel
from .file_list import FileList
from .circle_label import CircleLabel
import os
import socket
import shutil


class ServerSection(QWidget):
    def __init__(self, port: int, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        hostname = socket.gethostname()
        self.cur_dir = 'shared'
        self.host = socket.gethostbyname(hostname)
        self.port = port

        self.initStatus()
        self.layout.addSpacing(5)
        self.initList()
        self.initControls()

    def createStatus(self, color="green"):
        self.status = QHBoxLayout()
        self.status.setContentsMargins(0, 0, 0, 0)
        self.status.setSpacing(0)
        self.status.setAlignment(Qt.AlignCenter)

        self.logo = CircleLabel(color)

        self.ip = TextLabel(f"Exposed at: {self.host}:{self.port}")
        self.ip.setToolTip("Click to copy!")
        self.ip.setToolTipDuration(1000)
        self.ip.installEventFilter(ToolTipFilter(self.ip, 0, ToolTipPosition.TOP))
        self.ip.mousePressEvent = lambda e: self.copyTextToClipboard(f"{self.host}:{self.port}")

        self.status.addWidget(self.logo)
        self.status.addSpacing(5)
        self.status.addWidget(self.ip)

        return self.status

    def initStatus(self):
        self.createStatus()
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
        addBtn.clicked.connect(self.addFile)
        delBtn = PushButton('Delete', None, FIF.DELETE)
        delBtn.clicked.connect(lambda: self.delHandler(self.list.list.currentIndex()))
        control.addWidget(addBtn)
        control.addSpacing(10)
        control.addWidget(delBtn)
        self.layout.addLayout(control)

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
            subprocess.Popen(['start', f"{os.path.join(os.getcwd(),href)}"], shell=True)

    def delHandler(self, item):
        name, href = item.model().data(item, Qt.DisplayRole), item.model().get_href(item)
        print('del: ', href)
        if (name == '..'):
            return
        if (os.path.isdir(href)):
            shutil.rmtree(href)
        else:
            os.remove(href)
        self.loadDir()

    def copyTextToClipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.createSuccessInfoBar("Copied!")

    def addFile(self):
        file_paths, _ = QFileDialog.getOpenFileNames(None, "Select files", "", "All Files (*)")
        print(file_paths)
        for file in file_paths:
            shutil.copyfile(file, os.path.join(self.cur_dir, os.path.basename(file)))
        self.loadDir()

    def handle_server_changed(self, running):
        new_status = self.createStatus("green" if running else "red")
        self.status.replaceWidget(self.status.itemAt(0).widget(), new_status)

    def createSuccessInfoBar(self, text):
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

    def updatePort(self, port):
        self.port = port
        self.ip.setText(f"Exposed at: {self.host}:{self.port}")
        self.loadDir()
