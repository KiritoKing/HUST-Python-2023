from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QDialog
from qfluentwidgets import InfoBar, InfoBarPosition, ToolButton, FluentIcon as FIF, LineEdit, LineEditButton
from PyQt5.QtCore import Qt
from os import path
import subprocess
from ..components.file_list import FileList
from ..components.text_label import TextLabel
from ..utils.client import Client


class ListenWindow(QDialog):
    def __init__(self, host: str = None, port: int = None, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.host = host
        self.port = port
        self.cur_dir = '/'

        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.resize(500, 300)
        self.setMinimumSize(500, 300)
        self.setWindowTitle(f'PyQt LAN Listener')

        self.initUi()

        if (self.host is not None and self.port is not None):
            self.listen_addr.setText(f"{host}:{port}")

        self.loadDir()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.headHLayout = QHBoxLayout()
        self.headHLayout.setAlignment(Qt.AlignLeft)
        self.headHLayout.setContentsMargins(10, 5, 10, 0)
        self.headHLayout.setSpacing(0)
        title = TextLabel(f"Listening at")
        self.headHLayout.addWidget(title)
        self.listen_addr = LineEdit()
        self.listen_addr.setMinimumWidth(200)
        self.listen_addr.returnPressed.connect(self.commitAddr)
        commit = LineEditButton(FIF.ACCEPT)
        commit.clicked.connect(self.commitAddr)
        self.headHLayout.addSpacing(5)
        self.headHLayout.addWidget(self.listen_addr, 0, Qt.AlignmentFlag.AlignTrailing)
        self.headHLayout.addWidget(commit)

        ref = ToolButton(FIF.SYNC)
        ref.clicked.connect(self.refresh)
        self.headHLayout.addWidget(ref, 1, Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(self.headHLayout)

        self.file_list = FileList(open_handler=self.openHandler)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.file_list)

    def loadDir(self, path='/'):
        if (self.host is not None and self.port is not None):
            with Client(self.host, self.port) as client:
                data = client.get_folder()
                print(*data)
                self.file_list.updateList(data)

    def openHandler(self, item):
        name, href = item.model().data(item, Qt.DisplayRole), item.model().get_href(item)
        if (name == '..'):
            base = path.dirname(path.dirname(self.cur_dir))
            self.cur_dir = base if base == '/' else base + '/'
        elif (href == '' or href[-1] == '/'):
            self.cur_dir += href
        print(href)
        with Client(self.host, self.port) as client:
            if (href == '' or href == '..' or href[-1] == '/'):
                data = client.get_folder(self.cur_dir)
                print(*data)
                print(href)
                self.file_list.updateList([("..", "..")] + data if self.cur_dir != '/' else data)
            else:
                print('open file: ', href)
                p = client.get_file(path.join(self.cur_dir, href))
                subprocess.Popen(['start', p], shell=True)

    def createSuccessInfoBar(self, text="Refreshed!"):
        # convenient class mothod
        InfoBar.success(
            title='',
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=1000,
            parent=self
        )

    def refresh(self):
        self.loadDir(self.cur_dir)
        self.createSuccessInfoBar()

    def createErrorInfoBar(self, text):
        InfoBar.error(
            title='',
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=1000,
            parent=self
        )

    def isPortValid(self, port: str):
        try:
            port = int(port)
            return 0 <= port <= 65535
        except:
            return False

    def isIpValid(self, ip: str):
        try:
            ip = ip.split('.')
            if len(ip) != 4:
                return False
            for i in ip:
                if not (0 <= int(i) <= 255):
                    return False
            return True
        except:
            return False

    def commitAddr(self):
        addr = self.listen_addr.text()
        if not (addr == '' or ':' not in addr):
            host, port = addr.split(':')
            if self.isIpValid(host) and self.isPortValid(port):
                self.host, self.port = host, int(port)
                try:
                    self.loadDir()
                    self.createSuccessInfoBar("Connected!")
                except:
                    self.createErrorInfoBar("Connection failed!")
                    self.host, self.port = None, None
                    self.file_list.updateList([])
                return
        self.createErrorInfoBar("Invalid address!")
        self.listen_addr.setText(f"{self.host}:{self.port}" if self.host is not None and self.port is not None else "")
