# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_template.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(1002, 674)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 189, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 189, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 189, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 189, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Window.setPalette(palette)
        self.App = QtWidgets.QWidget(Window)
        self.App.setObjectName("App")
        self.gridLayoutWidget = QtWidgets.QWidget(self.App)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1001, 671))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setSpacing(10)
        self.grid.setObjectName("grid")
        self.lst_frame = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lst_frame.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.lst_frame.setText("")
        self.lst_frame.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lst_frame.setObjectName("lst_frame")
        self.grid.addWidget(self.lst_frame, 0, 2, 1, 1)
        self.fst_frame = QtWidgets.QLabel(self.gridLayoutWidget)
        self.fst_frame.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.fst_frame.setText("")
        self.fst_frame.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.fst_frame.setObjectName("fst_frame")
        self.grid.addWidget(self.fst_frame, 0, 0, 1, 1)
        self.lst_frame_text = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lst_frame_text.setFont(font)
        self.lst_frame_text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lst_frame_text.setText("")
        self.lst_frame_text.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lst_frame_text.setObjectName("lst_frame_text")
        self.grid.addWidget(self.lst_frame_text, 1, 2, 1, 1)
        self.fst_frame_text = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.fst_frame_text.setFont(font)
        self.fst_frame_text.setText("")
        self.fst_frame_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.fst_frame_text.setObjectName("fst_frame_text")
        self.grid.addWidget(self.fst_frame_text, 1, 0, 1, 1)
        self.btn_explore_file = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_explore_file.sizePolicy().hasHeightForWidth())
        self.btn_explore_file.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_explore_file.setFont(font)
        self.btn_explore_file.setFlat(False)
        self.btn_explore_file.setObjectName("btn_explore_file")
        self.grid.addWidget(self.btn_explore_file, 0, 1, 1, 1)
        Window.setCentralWidget(self.App)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "SlitPhoto v0.01"))
        self.btn_explore_file.setText(_translate("Window", "Explore video file"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())