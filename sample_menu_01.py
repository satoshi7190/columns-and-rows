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

import unicodedata


# uiファイルの定義と同じクラスを継承する
class SampleMenu01(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "sample_menu_01.ui"), self
        )

        # 選択をベクターレイヤーのみに制限
        self.ui.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)

        # すでに選択されているベクターレイヤーを取得
        setlayer = self.ui.mMapLayerComboBox.currentLayer()

        # FieldComboBoxにセット
        self.ui.mFieldComboBox.setLayer(setlayer)

        # レイヤーが選択されるたびにtableビューをセット
        self.ui.mMapLayerComboBox.layerChanged["QgsMapLayer*"].connect(self.set_table)

        # tableが選択されるたびにtableビューをセット
        self.ui.mFieldComboBox.fieldChanged.connect(self.set_table)
        
        self.ui.checkBox.stateChanged.connect(self.set_table)
        self.ui.checkBox_2.stateChanged.connect(self.set_table)
        self.ui.checkBox_3.stateChanged.connect(self.set_table)
        self.ui.checkBox_4.stateChanged.connect(self.set_table)


        self.ui.pushButton_run.clicked.connect(self.get_and_show_input_text)
        self.ui.pushButton_cancel.clicked.connect(self.close)

        # テーブルを作成して値を設定
        self.set_table()

    def set_table(self):

        # 選択されたレイヤーを取得
        layer = self.ui.mMapLayerComboBox.currentLayer()
        
        # 選択されたfieldを取得
        self.ui.mFieldComboBox.setLayer(layer)

        # 項目名にする列
        field_name = self.ui.mFieldComboBox.currentField()

        # データタイプの取得
        value_type = self.ui.comboBox.currentText()

        # 空白削除オプション 先頭列
        space_removal_first = self.ui.checkBox.checkState() == QtCore.Qt.Checked

        # Unicode正規化オプション 先頭列
        unicode_first = self.ui.checkBox_2.checkState() == QtCore.Qt.Checked

        # 空白削除オプション 先頭列以外
        space_removal_other = self.ui.checkBox_3.checkState() == QtCore.Qt.Checked

        # Unicode正規化オプション 先頭列以外
        unicode_other = self.ui.checkBox_4.checkState() == QtCore.Qt.Checked

        front_row_name = str(field_name)

        # 横列作成
        self.ui.tableWidget.setColumnCount(layer.featureCount() + 1)
        self.ui.tableWidget.setRowCount(len(layer.attributeList()))

        Header_Labels_list = [front_row_name]

        for feature in layer.getFeatures():

            new_field_name = str(feature[field_name])

            Header_Labels_list.append(new_field_name)

        self.ui.tableWidget.setHorizontalHeaderLabels(Header_Labels_list)

        for Column, field in enumerate(layer.fields()):
            fix = field.name()

            if fix == field_name:
                continue

            if space_removal_first:
                fix = fix.replace(" ", "").replace("　", "")

            if unicode_first:
                fix = unicodedata.normalize("NFKC", fix)

            list = [fix]

            for feature in layer.getFeatures():

                value = feature[field.name()]

                if space_removal_other:

                    value = str(feature[field.name()]).replace(" ", "").replace("　", "")

                if unicode_other:

                    value = unicodedata.normalize("NFKC", value)

                if value_type == "string（文字）":
                    exp = value

                if value_type == "integer（少数を含まない数字）":
                    exp = QgsExpression(f"to_int( {value} )").evaluate()

                if value_type == "real（少数を含む数字）":
                    exp = QgsExpression(f"to_real( {value} )").evaluate()

                list.append(exp)

                for row, deta in enumerate(list):

                    self.ui.tableWidget.setItem(Column, row, QTableWidgetItem(f"{deta}"))


    def get_and_show_input_text(self):

        # 選択されたレイヤーを取得
        layer = self.ui.mMapLayerComboBox.currentLayer()

        # 項目名にする列
        field_name = self.ui.mFieldComboBox.currentField()

        # データタイプの取得
        value_type = self.ui.comboBox.currentText()

        # 空白削除オプション 先頭列
        space_removal_first = self.ui.checkBox.checkState() == QtCore.Qt.Checked

        # Unicode正規化オプション 先頭列
        unicode_first = self.ui.checkBox_2.checkState() == QtCore.Qt.Checked

        # 空白削除オプション 先頭列以外
        space_removal_other = self.ui.checkBox_3.checkState() == QtCore.Qt.Checked

        # Unicode正規化オプション 先頭列以外
        unicode_other = self.ui.checkBox_4.checkState() == QtCore.Qt.Checked

        output_layer = QgsVectorLayer(
            "None",
            layer.name() + "_COLUMNS_ROWS",
            "memory",
        )
        provider = output_layer.dataProvider()

        front_row_name = str(field_name)

        provider.addAttributes([QgsField(front_row_name, QVariant.String)])

        for feature in layer.getFeatures():

            new_field_name = str(feature[field_name])

            if value_type == "string（文字）":
                provider.addAttributes([QgsField(new_field_name, QVariant.String)])

            if value_type == "integer（少数を含まない数字）":
                provider.addAttributes([QgsField(new_field_name, QVariant.Int)])

            if value_type == "real（少数を含む数字）":
                provider.addAttributes([QgsField(new_field_name, QVariant.Double)])

        for field in layer.fields():
            fix = field.name()

            if fix == field_name:
                continue

            if space_removal_first:
                fix = fix.replace(" ", "").replace("　", "")

            if unicode_first:
                fix = unicodedata.normalize("NFKC", fix)

            list = [fix]

            for feature in layer.getFeatures():

                value = feature[field.name()]

                if space_removal_other:

                    value = str(feature[field.name()]).replace(" ", "").replace("　", "")

                if unicode_other:

                    value = unicodedata.normalize("NFKC", value)

                if value_type == "string（文字）":
                    exp = value

                if value_type == "integer（少数を含まない数字）":
                    exp = QgsExpression(f"to_int( {value} )").evaluate()

                if value_type == "real（少数を含む数字）":
                    exp = QgsExpression(f"to_real( {value} )").evaluate()

                list.append(exp)

            new_feature = QgsFeature()
            new_feature.setAttributes(list)
            provider.addFeature(new_feature)

        output_layer.updateFields()
        output_layer.updateExtents()
        QgsProject.instance().addMapLayer(output_layer)

        # for feature in output_layer.getFeatures():

        # exp = QgsExpression("segments_to_lines( $geometry )")
        # context = QgsExpressionContext()
        # context.setFeature(self.mesh_feat)
        # line_geom = exp.evaluate(context)

        # メッセージ表示
        QMessageBox.information(None, "メッセージ", "行列を入れ替えたジオメトリなしレイヤーを作成しました。")


