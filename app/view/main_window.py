from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import PushButton, ToolButton, FluentIcon as FIF
from qframelesswindow import FramelessWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from os import path
import subprocess
from ..components.status_bar import StatusBar
from ..components.title_bar import CustomTitleBar
from ..components.file_list import FileList
from ..utils.client import Client
from .listen_window import ListenWindow


class MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.cur_dir = '/'

        self.setTitleBar(CustomTitleBar(self))
        self.qvLayout = QVBoxLayout(self)

        self.status = StatusBar()
        self.initLayout()
        self.initWindow()
        self.prepareData()

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
        # status bar
        self.qvLayout.addWidget(self.status)
        self.file_list = FileList(open_handler=self.openHandler)
        self.qvLayout.addWidget(self.file_list)

    def prepareData(self):
        with Client('127.0.0.1', 8888) as client:
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
        with Client('127.0.0.1', 8888) as client:
            if (href == '' or href == '..' or href[-1] == '/'):
                data = client.get_folder(self.cur_dir)
                print(*data)
                print(href)
                self.file_list.updateList([("..", "..")] + data if self.cur_dir != '/' else data)
            else:
                print('open file: ', href)
                p = client.get_file(path.join(self.cur_dir, href))
                subprocess.Popen(['start', p], shell=True)

    def newListener(self):
        lw = ListenWindow('127.0.0.1', 8888, self)
        lw.exec_()
