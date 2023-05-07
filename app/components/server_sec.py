from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import PushButton, FluentIcon as FIF
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush
from .text_label import TextLabel
from .file_list import FileList
import os
import socket


class CircleLabel(QLabel):
    def __init__(self, color="green", parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        brush = QBrush(QColor(self.color))
        painter.setBrush(brush)
        radius = min(self.width(), self.height()) / 2 - 2
        center = self.rect().center()
        center.setY(center.y() + 2)
        painter.drawEllipse(center, radius, radius)
        super().paintEvent(event)


class ServerSection(QWidget):
    def __init__(self, port: int, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        hostname = socket.gethostname()
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
        self.status.addWidget(self.logo)
        self.status.addSpacing(5)
        self.status.addWidget(self.ip)
        self.layout.addLayout(self.status)

    def initList(self):
        self.list = FileList()
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
        if not os.path.exists('shared'):
            os.mkdir('shared')
        files = os.listdir('shared')
        data = [(f, os.path.join(os.getcwd(), 'shared', f)) if os.path.isfile(os.path.join('shared', f)) else (f + '/', os.path.join(os.getcwd(), 'shared', f)) for f in files]
        print(*data)
        self.list.updateList(data)

    def openHandler(self, item):
        name, href = item.model().data(item, Qt.DisplayRole), item.model().get_href(item)
        # if (name == '..'):
        #     base = os.path.dirname(os.path.dirname(self.cur_dir))
        #     self.cur_dir = base if base == '/' else base + '/'
        # elif (href == '' or href[-1] == '/'):
        #     self.cur_dir += href
        # print(href)
        # with Client('127.0.0.1', 8888) as client:
        #     if (href == '' or href == '..' or href[-1] == '/'):
        #         data = client.get_folder(self.cur_dir)
        #         print(*data)
        #         print(href)
        #         self.file_list.updateList([("..", "..")] + data if self.cur_dir != '/' else data)
        #     else:
        #         print('open file: ', href)
        #         p = client.get_file(os.path.join(self.cur_dir, href))
        #         subprocess.Popen(['start', p], shell=True)
