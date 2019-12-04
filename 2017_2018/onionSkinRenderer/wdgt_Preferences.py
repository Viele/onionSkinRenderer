# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Personal Work\2019\onionSkinRenderer\onionSkinRendererPreferences.ui'
#
# Created: Sun Apr 21 22:39:53 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_onionSkinRendererPreferences(object):
    def setupUi(self, onionSkinRendererPreferences):
        onionSkinRendererPreferences.setObjectName("onionSkinRendererPreferences")
        onionSkinRendererPreferences.resize(279, 157)
        self.verticalLayout = QtWidgets.QVBoxLayout(onionSkinRendererPreferences)
        self.verticalLayout.setObjectName("verticalLayout")
        self.prefs_maxBuffer_layout = QtWidgets.QHBoxLayout()
        self.prefs_maxBuffer_layout.setObjectName("prefs_maxBuffer_layout")
        self.maxBuffer_label = QtWidgets.QLabel(onionSkinRendererPreferences)
        self.maxBuffer_label.setObjectName("maxBuffer_label")
        self.prefs_maxBuffer_layout.addWidget(self.maxBuffer_label)
        self.maxBuffer_spinBox = QtWidgets.QSpinBox(onionSkinRendererPreferences)
        self.maxBuffer_spinBox.setMinimum(1)
        self.maxBuffer_spinBox.setMaximum(10000)
        self.maxBuffer_spinBox.setProperty("value", 200)
        self.maxBuffer_spinBox.setObjectName("maxBuffer_spinBox")
        self.prefs_maxBuffer_layout.addWidget(self.maxBuffer_spinBox)
        self.verticalLayout.addLayout(self.prefs_maxBuffer_layout)
        self.prefs_relativeKeyCount_layout = QtWidgets.QHBoxLayout()
        self.prefs_relativeKeyCount_layout.setObjectName("prefs_relativeKeyCount_layout")
        self.relativeKeyCount_label = QtWidgets.QLabel(onionSkinRendererPreferences)
        self.relativeKeyCount_label.setObjectName("relativeKeyCount_label")
        self.prefs_relativeKeyCount_layout.addWidget(self.relativeKeyCount_label)
        self.relativeKeyCount_spinBox = QtWidgets.QSpinBox(onionSkinRendererPreferences)
        self.relativeKeyCount_spinBox.setMinimum(1)
        self.relativeKeyCount_spinBox.setMaximum(10)
        self.relativeKeyCount_spinBox.setProperty("value", 4)
        self.relativeKeyCount_spinBox.setObjectName("relativeKeyCount_spinBox")
        self.prefs_relativeKeyCount_layout.addWidget(self.relativeKeyCount_spinBox)
        self.verticalLayout.addLayout(self.prefs_relativeKeyCount_layout)
        self.prefs_outlineWidth = QtWidgets.QHBoxLayout()
        self.prefs_outlineWidth.setObjectName("prefs_outlineWidth")
        self.outlineWidth_label = QtWidgets.QLabel(onionSkinRendererPreferences)
        self.outlineWidth_label.setObjectName("outlineWidth_label")
        self.prefs_outlineWidth.addWidget(self.outlineWidth_label)
        self.outlineWidth_spinBox = QtWidgets.QSpinBox(onionSkinRendererPreferences)
        self.outlineWidth_spinBox.setMinimum(1)
        self.outlineWidth_spinBox.setMaximum(512)
        self.outlineWidth_spinBox.setProperty("value", 3)
        self.outlineWidth_spinBox.setObjectName("outlineWidth_spinBox")
        self.prefs_outlineWidth.addWidget(self.outlineWidth_spinBox)
        self.verticalLayout.addLayout(self.prefs_outlineWidth)
        self.prefs_tintSeed = QtWidgets.QHBoxLayout()
        self.prefs_tintSeed.setObjectName("prefs_tintSeed")
        self.tintSeed_label = QtWidgets.QLabel(onionSkinRendererPreferences)
        self.tintSeed_label.setObjectName("tintSeed_label")
        self.prefs_tintSeed.addWidget(self.tintSeed_label)
        self.tintSeed_spinBox = QtWidgets.QSpinBox(onionSkinRendererPreferences)
        self.tintSeed_spinBox.setObjectName("tintSeed_spinBox")
        self.prefs_tintSeed.addWidget(self.tintSeed_spinBox)
        self.verticalLayout.addLayout(self.prefs_tintSeed)
        self.prefs_dialogButtonBox = QtWidgets.QDialogButtonBox(onionSkinRendererPreferences)
        self.prefs_dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.prefs_dialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.prefs_dialogButtonBox.setObjectName("prefs_dialogButtonBox")
        self.verticalLayout.addWidget(self.prefs_dialogButtonBox)

        self.retranslateUi(onionSkinRendererPreferences)
        QtCore.QObject.connect(self.prefs_dialogButtonBox, QtCore.SIGNAL("accepted()"), onionSkinRendererPreferences.accept)
        QtCore.QObject.connect(self.prefs_dialogButtonBox, QtCore.SIGNAL("rejected()"), onionSkinRendererPreferences.reject)
        QtCore.QMetaObject.connectSlotsByName(onionSkinRendererPreferences)

    def retranslateUi(self, onionSkinRendererPreferences):
        onionSkinRendererPreferences.setWindowTitle(QtWidgets.QApplication.translate("onionSkinRendererPreferences", "Dialog", None, -1))
        self.maxBuffer_label.setText(QtWidgets.QApplication.translate("onionSkinRendererPreferences", "Maximum Buffer Size", None, -1))
        self.relativeKeyCount_label.setText(QtWidgets.QApplication.translate("onionSkinRendererPreferences", "Relative Keys Count", None, -1))
        self.outlineWidth_label.setText(QtWidgets.QApplication.translate("onionSkinRendererPreferences", "Outline Width", None, -1))
        self.tintSeed_label.setText(QtWidgets.QApplication.translate("onionSkinRendererPreferences", "Tint Seed", None, -1))

