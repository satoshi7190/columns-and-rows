"""
/***************************************************************************
 Sample
                                 A QGIS plugin
 QGIS Sample Plugin
                              -------------------
        begin                : 2021-06-30
        git sha              : $Format:%H$
        copyright            : (C) 2021 by MIERUNE Inc.
        email                : info@mierune.co.jp
        license              : GNU General Public License v2.0
 ***************************************************************************/
"""

import os

# QGIS-API
from qgis.PyQt import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *


# uiファイルの定義と同じクラスを継承する
class SampleMenu02(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join(os.path.dirname(
            __file__), 'sample_menu_02.ui'), self)

        # ラムダ式でもconnectできる
        self.ui.pushButton_run.clicked.connect(
            lambda: self.get_and_show_input_text('\nlambda sample'))
        self.ui.pushButton_cancel.clicked.connect(lambda: self.close())

    def get_and_show_input_text(self, suffix: str):
        # テキストボックス値取得
        text_value = self.ui.lineEdit.text()
        # テキストボックス値をメッセージ表示
        QMessageBox.information(None, 'ウィンドウ名', text_value + suffix)
