import core_sup as cs
import gui_struture as gs
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import cv2
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, \
    CAP_PROP_FPS
import os
from range_slider import QRangeSlider


class MainWindow(QMainWindow, gs.Ui_Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.name_of_file = ["", ""]

        # generates shadow effects for buttons
        self.shadow_effect = []
        for i in range(6):
            self.shadow_effect.append(QGraphicsDropShadowEffect())
            self.shadow_effect[i].setBlurRadius(20)
            self.shadow_effect[i].setXOffset(0)
            self.shadow_effect[i].setYOffset(5)
            self.shadow_effect[i].setColor(QtGui.QColor(40, 40, 40))

        # add stock img
        self.fst_frame.setPixmap(QPixmap("resources\\fst.jpg"))
        self.lst_frame.setPixmap(QPixmap("resources\\lst.jpg"))
        self.fst_frame.setGraphicsEffect(self.shadow_effect[0])
        self.lst_frame.setGraphicsEffect(self.shadow_effect[1])

        # adding shadows
        self.btn_explore_file.setGraphicsEffect(self.shadow_effect[2])
        self.render_btn.setGraphicsEffect(self.shadow_effect[3])
        self.how_to_btn.setGraphicsEffect(self.shadow_effect[4])

        # adding slider
        self.RS = QRangeSlider()

        # creates CV2 video, so it can be reached from any func or meth of program. Also no need to read file every
        # time you want to change frame
        self.video_f = VideoCapture()

        # ACTIONS HERE #
        # button action of searching video file
        self.btn_explore_file.clicked.connect(self.search_name_file)

        # slider actions
        self.RS.endValueChanged.connect(self.select_frame)
        self.RS.startValueChanged.connect(self.select_frame)

    def search_name_file(self):
        self.name_of_file = QFileDialog.getOpenFileName(self, "Open video file", os.getcwd(), "Video files (*.mp4)")
        if self.name_of_file[0] != "":
            self.video_f.release()
            self.video_f.open(self.name_of_file[0])

            # adding range slider RS to layout
            self.slider_layout.addWidget(self.RS)

            # update slider limits
            self.RS.setMin(0)
            self.RS.setMax(int(self.video_f.get(CAP_PROP_FRAME_COUNT)))
            self.RS.setStart(50)
            self.RS.setEnd(self.video_f.get(CAP_PROP_FRAME_COUNT) - 50)
            self.set_frames_to_grid(self.RS.getRange()[0], self.RS.getRange()[1])
        else:
            pass

    def set_frames_to_grid(self, fst_n, lst_n):
        self.fst_frame.setPixmap(self.convert_cv2qt(320, fst_n))
        self.lst_frame.setPixmap(self.convert_cv2qt(320, lst_n))

        # add frames and text to grid
        self.grid.addWidget(self.fst_frame, 0, 0)
        self.grid.addWidget(self.lst_frame, 0, 1)

    def select_frame(self):
        self.set_frames_to_grid(self.RS.getRange()[0], self.RS.getRange()[1])

    # Convert from an opencv image to QPixmap (necessary to add pic to qt layout)
    def convert_cv2qt(self, height, n):  # input is height (ip pixels), that will be in window, n - nb of frame
        self.video_f.set(CAP_PROP_POS_FRAMES, n)    # go to n frame
        inf, cv_img = self.video_f.read()   # reading frame to cv pic
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        aspect_ratio = self.video_f.get(CAP_PROP_FRAME_WIDTH) / self.video_f.get(CAP_PROP_FRAME_HEIGHT)
        p = convert_to_qt_format.scaled(round(aspect_ratio * height), height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    source = os.getcwd() + "\\.vid.mp4"

    app = QApplication(sys.argv)

    with open("style.qss", "r") as s:
        style = s.read()

    app.setStyleSheet(style)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
