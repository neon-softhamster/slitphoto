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
        self.add_video_frames()

    def search_name_file(self):
        name_of_file = QFileDialog.getOpenFileName(self, "Open video file", os.getcwd(), "Video files (*.mp4)")
        self.path.setText(name_of_file[0])

    def add_video_frames(self):
        # add fst and last frame to grid
        frame_in_window1 = FrameInWindow(source, 100, 600, 400)  # Задается путь к файлу, номер кадра, шир. и высота
        frame_in_window2 = FrameInWindow(source, 400, 600, 400)
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

    def _convert_cv_qt(self, cv_img):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.w, self.h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def add_frame2win(self, fst_or_lst, grid):
        # create the label that holds the image
        frame_label = QLabel()
        frame_label.setPixmap(self.qt_img)
        text_label = QLabel()
        if fst_or_lst == "fst":
            text_label.setText('First frame in your video')
            grid.addWidget(frame_label, 0, 0, Qt.AlignTop | Qt.AlignLeft)
            grid.addWidget(text_label, 1, 0, Qt.AlignTop | Qt.AlignLeft)
        elif fst_or_lst == "lst":
            text_label.setText('Last frame in your video')
            grid.addWidget(frame_label, 0, 2, Qt.AlignTop | Qt.AlignRight)
            grid.addWidget(text_label, 1, 2, Qt.AlignTop | Qt.AlignRight)
        else:
            print("FrameInWindow last arg can be \"fst\" or \"lst\" only")
        text_label.setFont(QtGui.QFont('SansSerif', 18))

        self.video_file.__del__()


if __name__ == "__main__":
    source = os.getcwd() + "\\.vid.mp4"

    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
