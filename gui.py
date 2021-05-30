import core as c
import core_sup as cs
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject
import sys
import cv2
import os


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SlitPhoto v0.01")
        self.setFixedSize(1100, 800)


class FrameInWindow:
    def __init__(self, src, frame_n, w, h):
        self.source = src
        self.frame_n = frame_n
        self.w = w
        self.h = h

        # open video_file for usage
        self.video_file = cs.VideoFile(self.source)
        self.vid = self.video_file.get_video_flow()
        self.frame_info = self.video_file.get_video_info()

        # create the label that holds the image
        self.frame_label = QLabel()
        # create a text label
        self.textLabel = QLabel('1st frame in your video')

        # create a vertical box layout and add the two labels
        vbox_pic = QVBoxLayout()
        vbox_pic.addWidget(self.frame_label)
        vbox_pic.setContentsMargins(25, 25, 1100 - (25 + self.w), 800 - (25 + self.h))
        # set the vbox layout as the widgets layout
        a.setLayout(vbox_pic)

        # create subtext for this pic
        vbox_text = QVBoxLayout()
        vbox_text.addWidget(self.textLabel)
        vbox_text.setContentsMargins(25 + self.w, 25 + self.h, 1100 - 25, 800 - 25)
        a.setLayout(vbox_text)

        # convert the image to Qt format
        qt_img = self.convert_cv_qt(self.get_cv_frame())
        # display it
        self.frame_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.w, self.h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def get_cv_frame(self):
        frame = self.video_file.get_special_frame(self.frame_n)
        return frame


if __name__ == "__main__":
    source = os.getcwd() + "\\"

    app = QApplication(sys.argv)
    a = App()
    frame_in_window = FrameInWindow(source, 100, 500, 300) # Задается путь к файлу, номмер кадра, ширина и высота

    a.show()
    sys.exit(app.exec_())
