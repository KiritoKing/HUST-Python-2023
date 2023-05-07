from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from qfluentwidgets import ToolButton
from qfluentwidgets import FluentIcon as FIF

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from os import path
import subprocess
from ..components.main_header import MainHeader
from ..components.status_bar import StatusBar
from ..components.title_bar import CustomTitleBar
from ..components.file_list import FileList
from ..components.text_label import TextLabel
from ..utils.client import Client


class ListenWindow(QWidget):
    def __init__(self, host: str, port: int, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.host = host
        self.port = port

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 40, 10, 10)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.headHLayout = QHBoxLayout()
        self.headHLayout.setContentsMargins(0, 0, 0, 0)
        self.headHLayout.setSpacing(0)
        info = TextLabel(f"Listening at: {host}:{port}")
        self.headHLayout.addWidget(info)
        self.headHLayout.setAlignment(info, Qt.AlignCenter)
        ref = ToolButton(FIF.SETTING)
        self.headHLayout.addWidget(ref)
        self.headHLayout.setAlignment(ref, Qt.AlignRight)
        self.layout.addLayout(self.headHLayout)

    def prepareData(self):
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
