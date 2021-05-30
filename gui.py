import core as c
import core_sup as cs
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject
import sys
import cv2
import os


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SlitPhoto v0.01")
        # self.setFixedSize(1100, 800)
        self.move(300, 150)
        self.grid = QGridLayout()
        frame_in_window1 = FrameInWindow(source, 100, 500, 300)  # Задается путь к файлу, номер кадра, шир. и высота
        frame_in_window2 = FrameInWindow(source, 400, 500, 300)
        frame_in_window1.add_frame2win("fst", self.grid)
        frame_in_window2.add_frame2win("lst", self.grid)
        self.setLayout(self.grid)


class FrameInWindow:
    def __init__(self, src, frame_n, w, h):
        self.frame_n = frame_n
        self.w = w
        self.h = h

        # open video_file for usage
        self.video_file = cs.VideoFile(src)

        # convert the image to Qt format
        self.qt_img = self._convert_cv_qt(self.video_file.get_special_frame(self.frame_n))
        # display it

    def add_frame2win(self, fst_or_lst, grid):
        if fst_or_lst == "fst":
            # create the label that holds the image
            frame_label = QLabel()
            frame_label.setPixmap(self.qt_img)
            text_label = QLabel('1st frame in your video')

            grid.addWidget(frame_label, 0, 0)
            grid.addWidget(text_label, 1, 0)
        elif fst_or_lst == "lst":
            # create the label that holds the image
            frame_label = QLabel()
            frame_label.setPixmap(self.qt_img)
            text_label = QLabel('lst frame in your video')

            grid.addWidget(frame_label, 0, 1)
            grid.addWidget(text_label, 1, 1)
        else:
            print("FrameInWindow last arg can be \"fst\" or \"lst\" only")

        self.video_file.__del__()

    def _convert_cv_qt(self, cv_img):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.w, self.h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    source = os.getcwd() + "\\"

    app = QApplication(sys.argv)
    a = App()

    a.show()
    sys.exit(app.exec_())
