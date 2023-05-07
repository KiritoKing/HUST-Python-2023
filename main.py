# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from app.view.main_window import MainWindow


# enable dpi scale
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

w = MainWindow()
w.show()

sys.exit(app.exec_())
