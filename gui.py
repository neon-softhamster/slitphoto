import core_sup as cs
import gui_struture as gs
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import cv2
import os
from range_slider import QRangeSlider


class MainWindow(QMainWindow, gs.Ui_Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.name_of_file = ["", ""]

        #adding slider
        self.RS = QRangeSlider()
        self.slider_layout.addWidget(self.RS)

        shadow_effect = []
        for i in range(5):
            shadow_effect.append(QGraphicsDropShadowEffect())
            shadow_effect[i].setBlurRadius(20)
            shadow_effect[i].setXOffset(0)
            shadow_effect[i].setYOffset(5)
            shadow_effect[i].setColor(QtGui.QColor(40, 40, 40))

        # add stock img
        self.fst_frame.setPixmap(QPixmap("resources\\fst.jpg"))
        self.lst_frame.setPixmap(QPixmap("resources\\lst.jpg"))
        self.fst_frame.setGraphicsEffect(shadow_effect[0])
        self.lst_frame.setGraphicsEffect(shadow_effect[1])

        # adding shadows
        self.btn_explore_file.setGraphicsEffect(shadow_effect[2])
        self.render_btn.setGraphicsEffect(shadow_effect[3])
        self.how_to_btn.setGraphicsEffect(shadow_effect[4])

        ### ACTIONS HERE ###
        # button action of searching video file
        self.btn_explore_file.clicked.connect(self.search_name_file)

        # slider actions
        self.RS.endValueChanged.connect(self.select_frame)
        self.RS.startValueChanged.connect(self.select_frame)

    def search_name_file(self):
        self.name_of_file = QFileDialog.getOpenFileName(self, "Open video file", os.getcwd(), "Video files (*.mp4)")
        if self.name_of_file[0] != "":
            frame_in_window = [FrameInWindow(self.name_of_file[0], 0, 320, "fst"),
                               FrameInWindow(self.name_of_file[0], 0, 320, "lst")]  # path to file, number of frame & h

            self.set_frames_to_grid(frame_in_window)

            # update slider limits
            # self.RS.setRange(0, int(frame_in_window[0].video_file.get_video_info()[2]))

            # clean up all frames
            for i in frame_in_window:
                i.__del__()
        else:
            pass

    def set_frames_to_grid(self, frame_in_window):
        self.fst_frame.setPixmap(frame_in_window[0].qt_img)
        self.lst_frame.setPixmap(frame_in_window[1].qt_img)

        # add frames and text to grid
        self.grid.addWidget(self.fst_frame, 0, 0)
        self.grid.addWidget(self.lst_frame, 0, 1)

        # set up selectors limits

    def select_frame(self):
        if self.name_of_file[0] != "":
            print(round(self.RS.getRange()[0]), round(self.RS.getRange()[1]))
            frame_in_window = [FrameInWindow(self.name_of_file[0], self.RS.getRange()[0],
                                             320, "fst"),
                               FrameInWindow(self.name_of_file[0], self.RS.getRange()[1],
                                             320, "lst")]

            self.set_frames_to_grid(frame_in_window)

            # clean up all frames
            for i in frame_in_window:
                i.__del__()
        else:
            pass


class FrameInWindow:
    def __init__(self, src, frame_n, h, numb):
        self.frame_n = frame_n
        self.h = h
        self.number = numb

        # open video_file for usage
        self.video_file = cs.VideoFile(src)
        self.aspect_ratio = self.video_file.get_video_info()[0] / self.video_file.get_video_info()[1]

        # convert the image to Qt format
        self.qt_img = self._convert_cv_qt(self.video_file.get_special_frame(self.frame_n))

    def _convert_cv_qt(self, cv_img):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(round(self.aspect_ratio * self.h), self.h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def __del__(self):
        self.video_file.__del__()


if __name__ == "__main__":
    source = os.getcwd() + "\\.vid.mp4"

    app = QApplication(sys.argv)

    with open("style.qss", "r") as s:
        style = s.read()
    
    app.setStyleSheet(style)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
