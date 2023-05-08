from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QInputDialog
from qfluentwidgets import PushButton, ToolButton, FluentIcon as FIF
from qframelesswindow import FramelessWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from ..components.title_bar import CustomTitleBar
from ..components.server_sec import ServerSection
from .listen_window import ListenWindow
from ..utils.server import Server


class MainWindow(FramelessWindow):
    server_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.cur_dir = '/'

        self.setTitleBar(CustomTitleBar(self))
        self.qvLayout = QVBoxLayout(self)
        self.server = Server(8888)
        self.server_running = False

        self.initLayout()
        self.initWindow()

        self.server.start()

    @property
    def server_running(self):
        return self._server_running

    @server_running.setter
    def server_running(self, value):
        self._server_running = value
        self.server_changed.emit(value)

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
        self.head.setContentsMargins(10, 0, 10, 20)
        addButton = PushButton(text='Add Listener', icon=FIF.ADD)
        addButton.clicked.connect(self.newListener)
        settingButton = ToolButton(FIF.SETTING)
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
        self.server_panel = ServerSection(8888)
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
        self.server_panel.loadDir()
        self.server_panel.createSuccessInfoBar('Refreshed!')

    def closeEvent(self, a0) -> None:
        self.server.stop()
        print('Server stopped!')
        return super().closeEvent(a0)
