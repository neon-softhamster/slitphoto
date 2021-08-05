# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'moving_setup_win_template.ui'
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
        self.label_2 = QtWidgets.QLabel(Setup)
        self.label_2.setGeometry(QtCore.QRect(290, 620, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.x_inclin = QtWidgets.QDoubleSpinBox(Setup)
        self.x_inclin.setGeometry(QtCore.QRect(170, 620, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.x_inclin.setFont(font)
        self.x_inclin.setMinimum(-10.0)
        self.x_inclin.setMaximum(10.0)
        self.x_inclin.setSingleStep(0.1)
        self.x_inclin.setProperty("value", 0.0)
        self.x_inclin.setObjectName("x_inclin")
        self.y_inclin = QtWidgets.QDoubleSpinBox(Setup)
        self.y_inclin.setGeometry(QtCore.QRect(430, 620, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.y_inclin.setFont(font)
        self.y_inclin.setMinimum(-10.0)
        self.y_inclin.setMaximum(10.0)
        self.y_inclin.setSingleStep(0.1)
        self.y_inclin.setProperty("value", 0.0)
        self.y_inclin.setObjectName("y_inclin")
        self.label_3 = QtWidgets.QLabel(Setup)
        self.label_3.setGeometry(QtCore.QRect(550, 620, 61, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.t_shift = QtWidgets.QDoubleSpinBox(Setup)
        self.t_shift.setGeometry(QtCore.QRect(620, 620, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.t_shift.setFont(font)
        self.t_shift.setDecimals(0)
        self.t_shift.setMaximum(100000.0)
        self.t_shift.setObjectName("t_shift")

        self.retranslateUi(Setup)
        QtCore.QMetaObject.connectSlotsByName(Setup)

    def retranslateUi(self, Setup):
        _translate = QtCore.QCoreApplication.translate
        Setup.setWindowTitle(_translate("Setup", "Form"))
        self.save_btn.setText(_translate("Setup", "Save"))
        self.label.setText(_translate("Setup", "Inclination 1:"))
        self.frame_width_label.setText(_translate("Setup", "<<  >>"))
        self.label_2.setText(_translate("Setup", "Inclination 2:"))
        self.label_3.setText(_translate("Setup", "Shift:"))