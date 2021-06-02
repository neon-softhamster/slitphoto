import core_sup as cs
import gui_struture as gs
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import cv2
import os


class MainWindow(QMainWindow, gs.Ui_Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # button action of searching video file
        self.btn_explore_file.clicked.connect(self.search_name_file)

    def search_name_file(self):
        name_of_file = QFileDialog.getOpenFileName(self, "Open video file", os.getcwd(), "Video files (*.mp4)")
        # self.setText(name_of_file[0])
        self.add_video_frames(name_of_file[0])

    def add_video_frames(self, name_of_file):
        # add fst and last frame to grid
        frame_in_window = [FrameInWindow(name_of_file, 100, 600, 400, "fst"),
                           FrameInWindow(name_of_file, 400, 600, 400, "lst")]   # Задается путь к файлу,
        # номер кадра, шир. и высота

        self.fst_frame.setPixmap(frame_in_window[0].qt_img)
        self.lst_frame.setPixmap(frame_in_window[1].qt_img)

        self.fst_frame_text.setText('First frame in your video')
        self.grid.addWidget(self.fst_frame, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.grid.addWidget(self.fst_frame_text, 1, 0, Qt.AlignTop | Qt.AlignLeft)

        self.lst_frame_text.setText('Last frame in your video')
        self.grid.addWidget(self.lst_frame, 0, 2, Qt.AlignTop | Qt.AlignRight)
        self.grid.addWidget(self.lst_frame_text, 1, 2, Qt.AlignTop | Qt.AlignRight)

        self.setLayout(self.grid)


class FrameInWindow:
    def __init__(self, src, frame_n, w, h, numb):
        self.frame_n = frame_n
        self.w = w
        self.h = h
        self.number = numb

        # open video_file for usage
        self.video_file = cs.VideoFile(src)

        # convert the image to Qt format
        self.qt_img = self._convert_cv_qt(self.video_file.get_special_frame(self.frame_n))
        # display it

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
    source = os.getcwd() + "\\.vid.mp4"

    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
