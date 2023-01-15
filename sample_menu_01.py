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
class SampleMenu01(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "sample_menu_01.ui"), self
        )

        # 選択をcsvレイヤーのみに制限
        self.ui.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)

        # すでに選択されているcsvレイヤーを取得
        Startlayer = self.ui.mMapLayerComboBox.currentLayer()

        # tableにセット
        self.ui.mFieldComboBox.setLayer(Startlayer)

        # レイヤーが選択されるたびにtableをセット
        self.ui.mMapLayerComboBox.layerChanged["QgsMapLayer*"].connect(
            self.ui.mFieldComboBox.setLayer
        )

        self.ui.pushButton_run.clicked.connect(self.get_and_show_input_text)
        self.ui.pushButton_cancel.clicked.connect(self.close)

    def get_and_show_input_text(self):

        # 選択されたレイヤーを取得
        layer = self.ui.mMapLayerComboBox.currentLayer()

        # 項目名にする列
        field_name = self.ui.mFieldComboBox.currentField()

        # データタイプの取得
        value_type = self.ui.comboBox.currentText()

        # 空白削除オプション
        space_removal = self.ui.checkBox.checkState() == QtCore.Qt.Checked
        

        output_layer = QgsVectorLayer(
            "None",
            layer.name() + "_CHANGE_MATRIX",
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

            if space_removal:
                fix.replace(" ", "").replace("　", "")

            list = [fix]

            for feature in layer.getFeatures():

                list.append(feature[field.name()])

            new_feature = QgsFeature()
            new_feature.setAttributes(list)
            provider.addFeature(new_feature)

        output_layer.updateFields()
        output_layer.updateExtents()
        #QgsProject.instance().addMapLayer(output_layer)
        
        
        for feature in output_layer.getFeatures():
            exp = QgsExpression(f"to_int( {feature[2]} )")
            print(exp.evaluate())
            
        
        
        # exp = QgsExpression("segments_to_lines( $geometry )")
        # context = QgsExpressionContext()
        # context.setFeature(self.mesh_feat)
        # line_geom = exp.evaluate(context)

        # メッセージ表示
        #QMessageBox.information(None, "メッセージ", "CSVの行列を入れ替えました。")
