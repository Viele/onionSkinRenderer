# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Christoph\OneDrive\Dokumente\maya\scripts\onionSkinRenderer\onionSkinRendererObjectWidget.ui'
#
# Created: Mon Aug 21 12:06:21 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_onionSkinObject_layout(object):
    def setupUi(self, onionSkinObject_layout):
        onionSkinObject_layout.setObjectName("onionSkinObject_layout")
        onionSkinObject_layout.resize(204, 38)
        self.horizontalLayout = QtWidgets.QHBoxLayout(onionSkinObject_layout)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(4, 2, 4, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.object_label = QtWidgets.QLabel(onionSkinObject_layout)
        self.object_label.setObjectName("object_label")
        self.horizontalLayout.addWidget(self.object_label)
        self.object_remove_btn = QtWidgets.QPushButton(onionSkinObject_layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
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
        onionSkinObject_layout.setWindowTitle(QtWidgets.QApplication.translate("onionSkinObject_layout", "Form", None, -1))
        self.object_label.setText(QtWidgets.QApplication.translate("onionSkinObject_layout", "objectName", None, -1))
        self.object_remove_btn.setText(QtWidgets.QApplication.translate("onionSkinObject_layout", "rm", None, -1))

