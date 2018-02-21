# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Personal Work\2017\OnionSkinRenderer\onionSkinRenderer\2016\onionSkinRenderer\onionSkinRendererPreferences.ui'
#
# Created: Wed Feb 21 16:53:04 2018
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_onionSkinRendererPreferences(object):
    def setupUi(self, onionSkinRendererPreferences):
        onionSkinRendererPreferences.setObjectName("onionSkinRendererPreferences")
        onionSkinRendererPreferences.resize(280, 97)
        self.verticalLayout = QtGui.QVBoxLayout(onionSkinRendererPreferences)
        self.verticalLayout.setObjectName("verticalLayout")
        self.prefs_maxBuffer_layout = QtGui.QHBoxLayout()
        self.prefs_maxBuffer_layout.setObjectName("prefs_maxBuffer_layout")
        self.maxBuffer_label = QtGui.QLabel(onionSkinRendererPreferences)
        self.maxBuffer_label.setObjectName("maxBuffer_label")
        self.prefs_maxBuffer_layout.addWidget(self.maxBuffer_label)
        self.maxBuffer_spinBox = QtGui.QSpinBox(onionSkinRendererPreferences)
        self.maxBuffer_spinBox.setMinimum(1)
        self.maxBuffer_spinBox.setMaximum(10000)
        self.maxBuffer_spinBox.setProperty("value", 200)
        self.maxBuffer_spinBox.setObjectName("maxBuffer_spinBox")
        self.prefs_maxBuffer_layout.addWidget(self.maxBuffer_spinBox)
        self.verticalLayout.addLayout(self.prefs_maxBuffer_layout)
        self.prefs_relativeKeyCount_layout = QtGui.QHBoxLayout()
        self.prefs_relativeKeyCount_layout.setObjectName("prefs_relativeKeyCount_layout")
        self.relativeKeyCount_label = QtGui.QLabel(onionSkinRendererPreferences)
        self.relativeKeyCount_label.setObjectName("relativeKeyCount_label")
        self.prefs_relativeKeyCount_layout.addWidget(self.relativeKeyCount_label)
        self.relativeKeyCount_spinBox = QtGui.QSpinBox(onionSkinRendererPreferences)
        self.relativeKeyCount_spinBox.setMinimum(1)
        self.relativeKeyCount_spinBox.setMaximum(10)
        self.relativeKeyCount_spinBox.setProperty("value", 4)
        self.relativeKeyCount_spinBox.setObjectName("relativeKeyCount_spinBox")
        self.prefs_relativeKeyCount_layout.addWidget(self.relativeKeyCount_spinBox)
        self.verticalLayout.addLayout(self.prefs_relativeKeyCount_layout)
        self.prefs_dialogButtonBox = QtGui.QDialogButtonBox(onionSkinRendererPreferences)
        self.prefs_dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.prefs_dialogButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.prefs_dialogButtonBox.setObjectName("prefs_dialogButtonBox")
        self.verticalLayout.addWidget(self.prefs_dialogButtonBox)

        self.retranslateUi(onionSkinRendererPreferences)
        QtCore.QObject.connect(self.prefs_dialogButtonBox, QtCore.SIGNAL("accepted()"), onionSkinRendererPreferences.accept)
        QtCore.QObject.connect(self.prefs_dialogButtonBox, QtCore.SIGNAL("rejected()"), onionSkinRendererPreferences.reject)
        QtCore.QMetaObject.connectSlotsByName(onionSkinRendererPreferences)

    def retranslateUi(self, onionSkinRendererPreferences):
        onionSkinRendererPreferences.setWindowTitle(QtGui.QApplication.translate("onionSkinRendererPreferences", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.maxBuffer_label.setText(QtGui.QApplication.translate("onionSkinRendererPreferences", "Maximum Buffer Size", None, QtGui.QApplication.UnicodeUTF8))
        self.relativeKeyCount_label.setText(QtGui.QApplication.translate("onionSkinRendererPreferences", "Relative Keys Count", None, QtGui.QApplication.UnicodeUTF8))

