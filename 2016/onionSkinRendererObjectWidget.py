# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Christoph\OneDrive\Dokumente\maya\scripts\onionSkinRenderer\onionSkinRendererObjectWidget.ui'
#
# Created: Sun Sep 17 17:58:08 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_onionSkinObject_layout(object):
    def setupUi(self, onionSkinObject_layout):
        onionSkinObject_layout.setObjectName("onionSkinObject_layout")
        onionSkinObject_layout.resize(204, 38)
        self.horizontalLayout = QtGui.QHBoxLayout(onionSkinObject_layout)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(4, 2, 4, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.object_label = QtGui.QLabel(onionSkinObject_layout)
        self.object_label.setObjectName("object_label")
        self.horizontalLayout.addWidget(self.object_label)
        self.object_remove_btn = QtGui.QPushButton(onionSkinObject_layout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.object_remove_btn.sizePolicy().hasHeightForWidth())
        self.object_remove_btn.setSizePolicy(sizePolicy)
        self.object_remove_btn.setMinimumSize(QtCore.QSize(16, 16))
        self.object_remove_btn.setMaximumSize(QtCore.QSize(16, 16))
        self.object_remove_btn.setObjectName("object_remove_btn")
        self.horizontalLayout.addWidget(self.object_remove_btn)

        self.retranslateUi(onionSkinObject_layout)
        QtCore.QMetaObject.connectSlotsByName(onionSkinObject_layout)

    def retranslateUi(self, onionSkinObject_layout):
        onionSkinObject_layout.setWindowTitle(QtGui.QApplication.translate("onionSkinObject_layout", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.object_label.setText(QtGui.QApplication.translate("onionSkinObject_layout", "objectName", None, QtGui.QApplication.UnicodeUTF8))
        self.object_remove_btn.setText(QtGui.QApplication.translate("onionSkinObject_layout", "rm", None, QtGui.QApplication.UnicodeUTF8))

