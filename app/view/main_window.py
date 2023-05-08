from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QInputDialog
from qfluentwidgets import PushButton, ToolButton, FluentIcon as FIF
from qframelesswindow import FramelessWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from ..components.title_bar import CustomTitleBar
from ..components.server_sec import ServerSection
from .listen_window import ListenWindow
from ..utils.server import Server
from .setting_window import SettingWindow
from ..common.config import Config as cfg
from ..common.get_resource import get_resource
import asyncio


class MainWindow(FramelessWindow):
    server_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.cur_dir = '/'

        self.setTitleBar(CustomTitleBar(self))
        self.qvLayout = QVBoxLayout(self)
        self.server_running = False

        self.initLayout()
        self.initWindow()
        self.titleBar.raise_()

        asyncio.run(self.runServer())

    @property
    def server_running(self):
        return self._server_running

    @server_running.setter
    def server_running(self, value):
        self._server_running = value
        self.server_changed.emit(value)

    async def runServer(self):
        if self.server_running:
            self.server.stop()
            self.server_running = False
        port = cfg.port.value
        self.server = Server(port)
        await asyncio.to_thread(self.server.start)
        self.server_running = True
        self.server_panel.updatePort(port)

    def runServerAsync(self):
        asyncio.run(self.runServer())

    def initLayout(self):
        self.resize(500, 400)
        self.setMinimumSize(500, 400)
        self.setWindowTitle('PyQt LAN File Share')
        self.setWindowIcon(QIcon(get_resource('icon.png')))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        self.qvLayout.setSpacing(0)
        self.qvLayout.setContentsMargins(10, 50, 10, 10)
        self.qvLayout.setAlignment(Qt.AlignTop)

    def initWindow(self):
        # head bar
        self.head = QHBoxLayout()
        self.head.setContentsMargins(10, 0, 10, 20)
        addButton = PushButton(text='Add Listener', icon=FIF.ADD)
        addButton.clicked.connect(self.newListener)
        settingButton = ToolButton(FIF.SETTING)
        settingButton.clicked.connect(self.settingHandler)
        syncButton = ToolButton(FIF.SYNC)
        syncButton.clicked.connect(self.refresh)
        self.head.addWidget(addButton)
        self.head.setAlignment(addButton, Qt.AlignLeft)
        self.head.addStretch(1)
        self.head.addWidget(syncButton)
        self.head.addSpacing(5)
        self.head.addWidget(settingButton)
        self.qvLayout.addLayout(self.head)
        # server
        self.server_panel = ServerSection(cfg.port.value)
        self.qvLayout.addWidget(self.server_panel)

    def newListener(self):
        # addr, ok = QInputDialog.getText(self, 'New Listener', 'Enter IP Address with port:')
        # if ok:
        #     host, port = addr.split(':')
        #     port = int(port)
        lw = ListenWindow(parent=self)
        lw.show()
        # lw.exec_()

    def refresh(self):
        self.runServerAsync()
        self.server_panel.createSuccessInfoBar('Restarted!')

    def closeEvent(self, a0) -> None:
        self.server.stop()
        print('Server stopped!')
        return super().closeEvent(a0)

    def portChangeHandler(self):
        self.runServerAsync()

    def settingHandler(self):
        sw = SettingWindow(parent=self)
        sw.portChanged.connect(self.portChangeHandler)
        sw.show()
        # self.settingWindow.show()
