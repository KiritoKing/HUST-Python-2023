# coding:utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QGuiApplication, QFont
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)


class Config(QConfig):
    """ Config of application """
    port = ConfigItem("Common", "Port", 8889, RangeValidator(0, 65535))


cfg = Config()
qconfig.load('app/config/config.json', cfg)
