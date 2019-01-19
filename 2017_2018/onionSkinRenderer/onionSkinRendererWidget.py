# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\doris\Documents\GitHub\onionSkinRenderer\onionSkinRendererWidget.ui'
#
# Created: Sat Jan 19 14:03:11 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_onionSkinRenderer(object):
    def setupUi(self, onionSkinRenderer):
        onionSkinRenderer.setObjectName("onionSkinRenderer")
        onionSkinRenderer.resize(404, 497)
        self.onionSkinRenderer_mainLayout = QtWidgets.QWidget(onionSkinRenderer)
        self.onionSkinRenderer_mainLayout.setObjectName("onionSkinRenderer_mainLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.onionSkinRenderer_mainLayout)
        self.verticalLayout_3.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.onionSkins_grp = QtWidgets.QGroupBox(self.onionSkinRenderer_mainLayout)
        self.onionSkins_grp.setTitle("")
        self.onionSkins_grp.setObjectName("onionSkins_grp")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.onionSkins_grp)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.onionFrames_tab = QtWidgets.QTabWidget(self.onionSkins_grp)
        self.onionFrames_tab.setStyleSheet("")
        self.onionFrames_tab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.onionFrames_tab.setObjectName("onionFrames_tab")
        self.relative_tab = QtWidgets.QWidget()
        self.relative_tab.setObjectName("relative_tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.relative_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.relative_frame = QtWidgets.QFrame(self.relative_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.relative_frame.sizePolicy().hasHeightForWidth())
        self.relative_frame.setSizePolicy(sizePolicy)
        self.relative_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.relative_frame.setMaximumSize(QtCore.QSize(100000, 16777215))
        self.relative_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.relative_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.relative_frame.setObjectName("relative_frame")
        self.relative_frame_layout = QtWidgets.QVBoxLayout(self.relative_frame)
        self.relative_frame_layout.setSpacing(3)
        self.relative_frame_layout.setContentsMargins(0, 4, 4, 4)
        self.relative_frame_layout.setObjectName("relative_frame_layout")
        self.horizontalLayout_3.addWidget(self.relative_frame)
        self.relative_settings_layout = QtWidgets.QVBoxLayout()
        self.relative_settings_layout.setObjectName("relative_settings_layout")
        self.relative_keyframes_chkbx = QtWidgets.QCheckBox(self.relative_tab)
        self.relative_keyframes_chkbx.setChecked(True)
        self.relative_keyframes_chkbx.setObjectName("relative_keyframes_chkbx")
        self.relative_settings_layout.addWidget(self.relative_keyframes_chkbx)
        self.relative_step_layout = QtWidgets.QHBoxLayout()
        self.relative_step_layout.setObjectName("relative_step_layout")
        self.relative_step_label = QtWidgets.QLabel(self.relative_tab)
        self.relative_step_label.setObjectName("relative_step_label")
        self.relative_step_layout.addWidget(self.relative_step_label)
        self.relative_step_spinBox = QtWidgets.QSpinBox(self.relative_tab)
        self.relative_step_spinBox.setMinimum(1)
        self.relative_step_spinBox.setObjectName("relative_step_spinBox")
        self.relative_step_layout.addWidget(self.relative_step_spinBox)
        self.relative_settings_layout.addLayout(self.relative_step_layout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.relative_settings_layout.addItem(spacerItem)
        self.relative_tint_strength_label = QtWidgets.QLabel(self.relative_tab)
        self.relative_tint_strength_label.setObjectName("relative_tint_strength_label")
        self.relative_settings_layout.addWidget(self.relative_tint_strength_label)
        self.relative_tint_strength_slider = QtWidgets.QSlider(self.relative_tab)
        self.relative_tint_strength_slider.setStyleSheet("QSlider{\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: 4px;\n"
"background: rgb(150, 150, 150);\n"
"}\n"
"QSlider::handle{\n"
"height: 8px;\n"
"background: rgb(50, 50, 50);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: -4px -4px;\n"
"}\n"
"QSlider::groove{\n"
"background: grey;\n"
"}\n"
"QSlider::sub-page{\n"
"background: rgb(75, 75, 75);\n"
"}\n"
"QSlider::add-page{\n"
"background: rgb(150, 150, 150);\n"
"}")
        self.relative_tint_strength_slider.setMaximum(100)
        self.relative_tint_strength_slider.setProperty("value", 100)
        self.relative_tint_strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.relative_tint_strength_slider.setObjectName("relative_tint_strength_slider")
        self.relative_settings_layout.addWidget(self.relative_tint_strength_slider)
        self.relative_tint_color_label = QtWidgets.QLabel(self.relative_tab)
        self.relative_tint_color_label.setObjectName("relative_tint_color_label")
        self.relative_settings_layout.addWidget(self.relative_tint_color_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.relative_pastTint_btn = QtWidgets.QPushButton(self.relative_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.relative_pastTint_btn.sizePolicy().hasHeightForWidth())
        self.relative_pastTint_btn.setSizePolicy(sizePolicy)
        self.relative_pastTint_btn.setStyleSheet("background-color:rgb(255, 26, 75)")
        self.relative_pastTint_btn.setObjectName("relative_pastTint_btn")
        self.horizontalLayout_2.addWidget(self.relative_pastTint_btn)
        self.relative_futureTint_btn = QtWidgets.QPushButton(self.relative_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.relative_futureTint_btn.sizePolicy().hasHeightForWidth())
        self.relative_futureTint_btn.setSizePolicy(sizePolicy)
        self.relative_futureTint_btn.setStyleSheet("background-color: rgb(20, 255, 114)")
        self.relative_futureTint_btn.setObjectName("relative_futureTint_btn")
        self.horizontalLayout_2.addWidget(self.relative_futureTint_btn)
        self.relative_settings_layout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.relative_settings_layout)
        self.onionFrames_tab.addTab(self.relative_tab, "")
        self.absolute_tab = QtWidgets.QWidget()
        self.absolute_tab.setObjectName("absolute_tab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.absolute_tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.absolute_frame = QtWidgets.QFrame(self.absolute_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.absolute_frame.sizePolicy().hasHeightForWidth())
        self.absolute_frame.setSizePolicy(sizePolicy)
        self.absolute_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.absolute_frame.setMaximumSize(QtCore.QSize(10000, 16777215))
        self.absolute_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.absolute_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.absolute_frame.setObjectName("absolute_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.absolute_frame)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.absolute_list = QtWidgets.QListWidget(self.absolute_frame)
        self.absolute_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.absolute_list.setObjectName("absolute_list")
        self.verticalLayout_2.addWidget(self.absolute_list)
        self.absolute_add_layout = QtWidgets.QHBoxLayout()
        self.absolute_add_layout.setObjectName("absolute_add_layout")
        self.absolute_add_spinBox = QtWidgets.QSpinBox(self.absolute_frame)
        self.absolute_add_spinBox.setMinimum(-100000)
        self.absolute_add_spinBox.setMaximum(100000)
        self.absolute_add_spinBox.setObjectName("absolute_add_spinBox")
        self.absolute_add_layout.addWidget(self.absolute_add_spinBox)
        self.absolute_add_btn = QtWidgets.QPushButton(self.absolute_frame)
        self.absolute_add_btn.setObjectName("absolute_add_btn")
        self.absolute_add_layout.addWidget(self.absolute_add_btn)
        self.absolute_addCrnt_btn = QtWidgets.QPushButton(self.absolute_frame)
        self.absolute_addCrnt_btn.setObjectName("absolute_addCrnt_btn")
        self.absolute_add_layout.addWidget(self.absolute_addCrnt_btn)
        self.absolute_clear_btn = QtWidgets.QPushButton(self.absolute_frame)
        self.absolute_clear_btn.setObjectName("absolute_clear_btn")
        self.absolute_add_layout.addWidget(self.absolute_clear_btn)
        self.verticalLayout_2.addLayout(self.absolute_add_layout)
        self.horizontalLayout_4.addWidget(self.absolute_frame)
        self.absolute_settings_layout = QtWidgets.QVBoxLayout()
        self.absolute_settings_layout.setObjectName("absolute_settings_layout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.absolute_settings_layout.addItem(spacerItem1)
        self.absolute_tint_strength_label = QtWidgets.QLabel(self.absolute_tab)
        self.absolute_tint_strength_label.setObjectName("absolute_tint_strength_label")
        self.absolute_settings_layout.addWidget(self.absolute_tint_strength_label)
        self.absolute_tint_strength_slider = QtWidgets.QSlider(self.absolute_tab)
        self.absolute_tint_strength_slider.setStyleSheet("QSlider{\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: 4px;\n"
"background: rgb(150, 150, 150);\n"
"}\n"
"QSlider::handle{\n"
"height: 8px;\n"
"background: rgb(50, 50, 50);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: -4px -4px;\n"
"}\n"
"QSlider::groove{\n"
"background: grey;\n"
"}\n"
"QSlider::sub-page{\n"
"background: rgb(75, 75, 75);\n"
"}\n"
"QSlider::add-page{\n"
"background: rgb(150, 150, 150);\n"
"}")
        self.absolute_tint_strength_slider.setMaximum(100)
        self.absolute_tint_strength_slider.setProperty("value", 100)
        self.absolute_tint_strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.absolute_tint_strength_slider.setObjectName("absolute_tint_strength_slider")
        self.absolute_settings_layout.addWidget(self.absolute_tint_strength_slider)
        self.absolute_tint_label = QtWidgets.QLabel(self.absolute_tab)
        self.absolute_tint_label.setObjectName("absolute_tint_label")
        self.absolute_settings_layout.addWidget(self.absolute_tint_label)
        self.absolute_tint_btn = QtWidgets.QPushButton(self.absolute_tab)
        self.absolute_tint_btn.setStyleSheet("background:rgb(200, 200, 50)")
        self.absolute_tint_btn.setObjectName("absolute_tint_btn")
        self.absolute_settings_layout.addWidget(self.absolute_tint_btn)
        self.horizontalLayout_4.addLayout(self.absolute_settings_layout)
        self.onionFrames_tab.addTab(self.absolute_tab, "")
        self.verticalLayout.addWidget(self.onionFrames_tab)
        self.global_layout = QtWidgets.QHBoxLayout()
        self.global_layout.setSpacing(6)
        self.global_layout.setContentsMargins(10, -1, 10, 5)
        self.global_layout.setObjectName("global_layout")
        self.globalOpacity_label = QtWidgets.QLabel(self.onionSkins_grp)
        self.globalOpacity_label.setObjectName("globalOpacity_label")
        self.global_layout.addWidget(self.globalOpacity_label)
        self.globalOpacity_slider = QtWidgets.QSlider(self.onionSkins_grp)
        self.globalOpacity_slider.setStyleSheet("QSlider{\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: 4px;\n"
"background: rgb(150, 150, 150);\n"
"}\n"
"QSlider::handle{\n"
"height: 8px;\n"
"background: rgb(50, 50, 50);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: -4px -4px;\n"
"}\n"
"QSlider::groove{\n"
"background: grey;\n"
"}\n"
"QSlider::sub-page{\n"
"background: rgb(75, 75, 75);\n"
"}\n"
"QSlider::add-page{\n"
"background: rgb(150, 150, 150);\n"
"}")
        self.globalOpacity_slider.setMaximum(100)
        self.globalOpacity_slider.setProperty("value", 99)
        self.globalOpacity_slider.setOrientation(QtCore.Qt.Horizontal)
        self.globalOpacity_slider.setObjectName("globalOpacity_slider")
        self.global_layout.addWidget(self.globalOpacity_slider)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.global_layout.addItem(spacerItem2)
        self.toggleRenderer_btn = QtWidgets.QPushButton(self.onionSkins_grp)
        self.toggleRenderer_btn.setObjectName("toggleRenderer_btn")
        self.global_layout.addWidget(self.toggleRenderer_btn)
        self.verticalLayout.addLayout(self.global_layout)
        self.onionType_layout = QtWidgets.QHBoxLayout()
        self.onionType_layout.setContentsMargins(10, -1, 10, 5)
        self.onionType_layout.setObjectName("onionType_layout")
        self.onionType_label = QtWidgets.QLabel(self.onionSkins_grp)
        self.onionType_label.setObjectName("onionType_label")
        self.onionType_layout.addWidget(self.onionType_label)
        self.onionType_cBox = QtWidgets.QComboBox(self.onionSkins_grp)
        self.onionType_cBox.setObjectName("onionType_cBox")
        self.onionType_cBox.addItem("")
        self.onionType_cBox.addItem("")
        self.onionType_cBox.addItem("")
        self.onionType_layout.addWidget(self.onionType_cBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.onionType_layout.addItem(spacerItem3)
        self.drawBehind_chkBx = QtWidgets.QCheckBox(self.onionSkins_grp)
        self.drawBehind_chkBx.setChecked(True)
        self.drawBehind_chkBx.setObjectName("drawBehind_chkBx")
        self.onionType_layout.addWidget(self.drawBehind_chkBx)
        self.verticalLayout.addLayout(self.onionType_layout)
        self.verticalLayout_3.addWidget(self.onionSkins_grp)
        self.onionObjects_grp = QtWidgets.QGroupBox(self.onionSkinRenderer_mainLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.onionObjects_grp.sizePolicy().hasHeightForWidth())
        self.onionObjects_grp.setSizePolicy(sizePolicy)
        self.onionObjects_grp.setObjectName("onionObjects_grp")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.onionObjects_grp)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.onionObjects_list = QtWidgets.QListWidget(self.onionObjects_grp)
        self.onionObjects_list.setBaseSize(QtCore.QSize(2, 1))
        self.onionObjects_list.setFrameShadow(QtWidgets.QFrame.Plain)
        self.onionObjects_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.onionObjects_list.setObjectName("onionObjects_list")
        self.horizontalLayout.addWidget(self.onionObjects_list)
        self.onionObjects_btn_layout = QtWidgets.QVBoxLayout()
        self.onionObjects_btn_layout.setObjectName("onionObjects_btn_layout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.onionObjects_btn_layout.addItem(spacerItem4)
        self.onionObjects_add_btn = QtWidgets.QPushButton(self.onionObjects_grp)
        self.onionObjects_add_btn.setObjectName("onionObjects_add_btn")
        self.onionObjects_btn_layout.addWidget(self.onionObjects_add_btn)
        self.onionObjects_remove_btn = QtWidgets.QPushButton(self.onionObjects_grp)
        self.onionObjects_remove_btn.setObjectName("onionObjects_remove_btn")
        self.onionObjects_btn_layout.addWidget(self.onionObjects_remove_btn)
        self.onionObjects_clear_btn = QtWidgets.QPushButton(self.onionObjects_grp)
        self.onionObjects_clear_btn.setObjectName("onionObjects_clear_btn")
        self.onionObjects_btn_layout.addWidget(self.onionObjects_clear_btn)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.onionObjects_btn_layout.addItem(spacerItem5)
        self.horizontalLayout.addLayout(self.onionObjects_btn_layout)
        self.verticalLayout_3.addWidget(self.onionObjects_grp)
        onionSkinRenderer.setCentralWidget(self.onionSkinRenderer_mainLayout)
        self.onionSkinRenderer_menubar = QtWidgets.QMenuBar(onionSkinRenderer)
        self.onionSkinRenderer_menubar.setGeometry(QtCore.QRect(0, 0, 404, 21))
        self.onionSkinRenderer_menubar.setObjectName("onionSkinRenderer_menubar")
        self.menubar_settings = QtWidgets.QMenu(self.onionSkinRenderer_menubar)
        self.menubar_settings.setObjectName("menubar_settings")
        onionSkinRenderer.setMenuBar(self.onionSkinRenderer_menubar)
        self.statusbar = QtWidgets.QStatusBar(onionSkinRenderer)
        self.statusbar.setObjectName("statusbar")
        onionSkinRenderer.setStatusBar(self.statusbar)
        self.settings_clearBuffer = QtWidgets.QAction(onionSkinRenderer)
        self.settings_clearBuffer.setCheckable(False)
        self.settings_clearBuffer.setObjectName("settings_clearBuffer")
        self.settings_autoClearBuffer = QtWidgets.QAction(onionSkinRenderer)
        self.settings_autoClearBuffer.setCheckable(True)
        self.settings_autoClearBuffer.setChecked(True)
        self.settings_autoClearBuffer.setObjectName("settings_autoClearBuffer")
        self.settings_preferences = QtWidgets.QAction(onionSkinRenderer)
        self.settings_preferences.setObjectName("settings_preferences")
        self.menubar_settings.addAction(self.settings_clearBuffer)
        self.menubar_settings.addAction(self.settings_autoClearBuffer)
        self.menubar_settings.addAction(self.settings_preferences)
        self.onionSkinRenderer_menubar.addAction(self.menubar_settings.menuAction())

        self.retranslateUi(onionSkinRenderer)
        self.onionFrames_tab.setCurrentIndex(0)
        self.onionType_cBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(onionSkinRenderer)

    def retranslateUi(self, onionSkinRenderer):
        onionSkinRenderer.setWindowTitle(QtWidgets.QApplication.translate("onionSkinRenderer", "OnionSkinRenderer", None, -1))
        self.relative_keyframes_chkbx.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Keyframes", None, -1))
        self.relative_step_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Relative Step", None, -1))
        self.relative_tint_strength_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Tint Strength", None, -1))
        self.relative_tint_color_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Tint Color", None, -1))
        self.relative_pastTint_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Past", None, -1))
        self.relative_futureTint_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Future", None, -1))
        self.onionFrames_tab.setTabText(self.onionFrames_tab.indexOf(self.relative_tab), QtWidgets.QApplication.translate("onionSkinRenderer", "Relative", None, -1))
        self.absolute_add_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Add", None, -1))
        self.absolute_addCrnt_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Current", None, -1))
        self.absolute_clear_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Clear", None, -1))
        self.absolute_tint_strength_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Tint Strength", None, -1))
        self.absolute_tint_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Tint Color", None, -1))
        self.absolute_tint_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Absolute", None, -1))
        self.onionFrames_tab.setTabText(self.onionFrames_tab.indexOf(self.absolute_tab), QtWidgets.QApplication.translate("onionSkinRenderer", "Absolute", None, -1))
        self.globalOpacity_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Global Opacity", None, -1))
        self.toggleRenderer_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Toggle Renderer", None, -1))
        self.onionType_label.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Onion Type", None, -1))
        self.onionType_cBox.setItemText(0, QtWidgets.QApplication.translate("onionSkinRenderer", "Shaded", None, -1))
        self.onionType_cBox.setItemText(1, QtWidgets.QApplication.translate("onionSkinRenderer", "Shape", None, -1))
        self.onionType_cBox.setItemText(2, QtWidgets.QApplication.translate("onionSkinRenderer", "Outline", None, -1))
        self.drawBehind_chkBx.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Draw Behind", None, -1))
        self.onionObjects_grp.setTitle(QtWidgets.QApplication.translate("onionSkinRenderer", "Onion Objects", None, -1))
        self.onionObjects_add_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Add Selected", None, -1))
        self.onionObjects_remove_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Remove Selected", None, -1))
        self.onionObjects_clear_btn.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Clear", None, -1))
        self.menubar_settings.setTitle(QtWidgets.QApplication.translate("onionSkinRenderer", "Settings", None, -1))
        self.settings_clearBuffer.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Clear Buffer", None, -1))
        self.settings_autoClearBuffer.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Auto Clear Buffer", None, -1))
        self.settings_preferences.setText(QtWidgets.QApplication.translate("onionSkinRenderer", "Preferences", None, -1))

