# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Personal Work\2017\OnionSkinRenderer\onionSkinRenderer\2017\onionSkinRenderer\onionSkinRendererPreferences.ui'
#
# Created: Wed Feb 21 13:03:57 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_onionSkinRendererPreferences(object):
    def setupUi(self, onionSkinRendererPreferences):
        onionSkinRendererPreferences.setObjectName("onionSkinRendererPreferences")
        onionSkinRendererPreferences.resize(280, 97)
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

