import typing
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListView, QFileDialog, QLabel, QStyledItemDelegate
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QSize
from PyQt5.QtGui import QFont
from qfluentwidgets import PushButton
from qfluentwidgets import FluentIcon as FIF


class ListModel(QAbstractListModel):
    def __init__(self, data: list) -> None:
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex()) -> int:
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][0]

    def get_href(self, index: QModelIndex):
        return self._data[index.row()][1]


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item = index.model().data(index, Qt.DisplayRole)
        if item is not None:
            text = str(item)
        else:
            text = ""
        painter.drawText(option.rect, Qt.AlignLeft, text)

    def sizeHint(self, option, index):
        return QSize(100, 20)


class FileList(QWidget):
    def __init__(self, data=[], open_handler=lambda item: print("Open: ", item.model().get_href(item)), parent: QWidget = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(0)

        self.list = QListView()
        self.list.setContentsMargins(5, 10, 5, 10)
        self.list.setSpacing(5)
        font = QFont("Microsoft YaHei", 12, 50)
        self.list.setFont(font)
        # self.list.clicked.connect(lambda item: print(item.model().get_href(item)))
        self.list.doubleClicked.connect(open_handler)
        self.layout.addWidget(self.list)
        self.updateList(data)
        self.layout.addSpacing(10)

    def updateList(self, data):
        listModel = ListModel(data)
        self.list.setModel(listModel)
