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
        self.ui = uic.loadUi(os.path.join(os.path.dirname(
            __file__), 'sample_menu_01.ui'), self)
        
      
        
        # 選択をcsvレイヤーのみに制限
        self.ui.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)
        
        # すでに選択されているcsvレイヤーを取得
        Startlayer = self.ui.mMapLayerComboBox.currentLayer()
        
        # tableにセット
        self.ui.mFieldComboBox.setLayer(Startlayer)
        
        # レイヤーが選択されるたびにtableをセット
        self.ui.mMapLayerComboBox.layerChanged['QgsMapLayer*'].connect(self.ui.mFieldComboBox.setLayer)

        self.ui.pushButton_run.clicked.connect(self.get_and_show_input_text)
        self.ui.pushButton_cancel.clicked.connect(self.close)
        
        # checkBox1 = QCheckBox("First", self.ui.listView)
        # checkBox2 = QCheckBox("Second", self.ui.listView)
        # checkBox3 = QCheckBox("Third", self.ui.listView)

        # # チェックボックスの配置
        # checkBox1.move(10, 0)
        # checkBox2.move(10, 50)
        # checkBox3.move(10, 90)
        
        

    def get_and_show_input_text(self):
        # テキストボックス値取得
        # text_value = self.ui.lineEdit.text()

        
        # 選択されたレイヤーを取得
        layer = self.ui.mMapLayerComboBox.currentLayer()

        #項目名にする列
        field_name = self.ui.mFieldComboBox.currentField()
        
        value_type = self.ui.comboBox.currentText()
        
            
        test_layer = QgsVectorLayer(
        "None",
            layer.name() + "CHANGE_MATRIX",
            "memory",
        )
        provider = test_layer.dataProvider()

        provider.addAttributes([QgsField('NAME', QVariant.String),])

        for feature in layer.getFeatures():
            
            if value_type == "string（文字）"

                provider.addAttributes(
                [QgsField(feature[field_name], QVariant.String),]
                )
                
            if value_type == "string（文字）"

                provider.addAttributes(
                [
                QgsField(feature[field_name], QVariant.String),
                ]
                )


        for field in layer.fields():
            fix = field.name().replace(' ', '').replace('　', '')
            
            list = [fix]

            for feature in layer.getFeatures():

                list.append(feature[field.name()])

            new_feature = QgsFeature()
            new_feature.setAttributes(list)
            provider.addFeature(new_feature)





        # feature = QgsFeature()
        # feature.setAttributes(['2',0])
        # provider.addFeature(feature)

        test_layer.updateFields()
        test_layer.updateExtents()
        QgsProject.instance().addMapLayer(test_layer)
        
        #メッセージ表示
        QMessageBox.information(None, 'メッセージ', 'tableの行列を入れ替えました。')

        """
        QgsField("name", QVariant.String),
        QgsField("age",  QVariant.Int),
        

        """
