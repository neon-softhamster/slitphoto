# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classic_setup_win_template.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setup(object):
    def setupUi(self, Setup):
        Setup.setObjectName("Setup")
        Setup.resize(902, 698)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Setup.sizePolicy().hasHeightForWidth())
        Setup.setSizePolicy(sizePolicy)
        self.save_btn = QtWidgets.QPushButton(Setup)
        self.save_btn.setGeometry(QtCore.QRect(780, 600, 101, 81))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.save_btn.setFont(font)
        self.save_btn.setObjectName("save_btn")
        self.verticalLayoutWidget = QtWidgets.QWidget(Setup)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 881, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.frame_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setObjectName("frame_layout")
        self.label = QtWidgets.QLabel(Setup)
        self.label.setGeometry(QtCore.QRect(30, 620, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame_width_label = QtWidgets.QLabel(Setup)
        self.frame_width_label.setGeometry(QtCore.QRect(300, 520, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.frame_width_label.setFont(font)
        self.frame_width_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_width_label.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_width_label.setObjectName("frame_width_label")
        self.slit_pos_text_field = QtWidgets.QLineEdit(Setup)
        self.slit_pos_text_field.setGeometry(QtCore.QRect(180, 620, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.slit_pos_text_field.setFont(font)
        self.slit_pos_text_field.setObjectName("slit_pos_text_field")

        self.retranslateUi(Setup)
        QtCore.QMetaObject.connectSlotsByName(Setup)

    def retranslateUi(self, Setup):
        _translate = QtCore.QCoreApplication.translate
        Setup.setWindowTitle(_translate("Setup", "Form"))
        self.save_btn.setText(_translate("Setup", "Save"))
        self.label.setText(_translate("Setup", "Slit position:"))
        self.frame_width_label.setText(_translate("Setup", "<<  >>"))
