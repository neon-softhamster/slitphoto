import core as c
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
        self.display_width = 1100
        self.display_height = 700
        # create the label that holds the image
        self.image_label = QLabel(self)
        # self.image_label.resize(self.display_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('1st frame will be here')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        # don't need the grey image now
        # grey = QPixmap(self.display_width, self.display_height)
        # grey.fill(QColor('darkGray'))
        # self.image_label.setPixmap(grey)

        # convert the image to Qt format
        qt_img = self.convert_cv_qt(self.get_cv_frame(os.getcwd() + "\\"))
        # display it
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def get_cv_frame(self, path):
        vid, frame_info = c.open_video_file(path)
        frame = c.get_special_frame(vid, 100)
        return frame


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
