from qfluentwidgets import SettingCard, FluentIconBase, LineEdit, LineEditButton, FluentIcon as FIF
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from typing import Union


class EditSettingCard(SettingCard):
    """ Setting card with a push button """

    commit = pyqtSignal()

    def __init__(self, value, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------
        text: str
            the text of push button

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.edit = LineEdit(self)
        self.edit.setText(str(value))
        self.editBut = LineEditButton(FIF.ACCEPT, self)
        self.hBoxLayout.addWidget(self.edit, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.editBut, 0, Qt.AlignmentFlag.AlignTrailing)
        self.hBoxLayout.addSpacing(16)
        self.edit.returnPressed.connect(self.commit)
        self.editBut.clicked.connect(self.commit)
