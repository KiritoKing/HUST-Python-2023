import sys
import os


def get_resource(path: str):
    if hasattr(sys, '_MEIPASS'):
    # PyInstaller打包后，sys._MEIPASS指向解压后的临时文件夹
        return os.path.join(sys._MEIPASS, 'resources', path)
    else:
    # 直接运行Python脚本时，使用当前脚本所在的目录
        p = os.path.join(os.getcwd(), 'app', 'resources', path)
        print(p)
        return p
