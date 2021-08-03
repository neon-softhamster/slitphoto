import core_sup as cs

# windows after qt designer
import main_win as gs
import classic_setup_win as csw
import moving_setup_win as msw

# Qt imports
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGraphicsDropShadowEffect, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# other useful stuff
import os
import sys
import random
import cv2
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT

# range slider made by
from range_slider import QRangeSlider


# generates shadow effects for buttons. Used in all windows
def shadows(self):
    self.shadow_effect = []
    for i in range(6):
        self.shadow_effect.append(QGraphicsDropShadowEffect())
        self.shadow_effect[i].setBlurRadius(20)
        self.shadow_effect[i].setXOffset(0)
        self.shadow_effect[i].setYOffset(5)
        self.shadow_effect[i].setColor(QtGui.QColor(40, 40, 40))
    return self.shadow_effect


# Window for settings of classic mode
class ClassicSetupWin(QWidget, csw.Ui_Setup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # generates list of shadow effects
        self.shadow_effect = shadows(self)
        # adding shadows
        self.save_btn.setGraphicsEffect(self.shadow_effect[0])

        # ACTIONS #
        self.save_btn.clicked.connect(self.transmit_setup_to_main_win)

    # transmit settings to main window, works when Save button clicked
    def transmit_setup_to_main_win(self):
        mw.slit_position = int(self.slit_pos_text_field.text())
        mw.render_btn.setEnabled(True)
        mw.mode = "CLASSIC"
        self.close()


# Window for settings of moving slit mode
class MovingSetupWin(QWidget, msw.Ui_Setup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # generates list of shadow effects
        self.shadow_effect = shadows(self)

        # adding shadows
        self.save_btn.setGraphicsEffect(self.shadow_effect[0])

        # ACTIONS #
        self.save_btn.clicked.connect(self.transmit_setup_to_main_win)

    # transmit settings to main window, works when Save button clicked
    def transmit_setup_to_main_win(self):
        mw.lin_params = [float(self.x_inclin.text()), float(self.y_inclin.text()), float(self.t_shift.text())]
        mw.render_btn.setEnabled(True)
        mw.mode = "LIN"
        self.close()


# Main window
class MainWindow(QMainWindow, gs.Ui_Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # Some global values
        self.name_of_file = ["", ""]
        self.n0 = 0
        self.pic = QPixmap()
        self.mode = ""

        # creates setup window
        self.classic_setup_win = ClassicSetupWin()
        self.moving_setup_win = MovingSetupWin()

        # default SETUP parameters
        self.slit_position = 0  # for classic mode
        self.lin_params = [0.1, 0.1, 0]  # for moving slit mode

        # generates list of shadow effects
        self.shadow_effect = shadows(self)
        # adding shadows
        self.btn_explore_file.setGraphicsEffect(self.shadow_effect[2])
        self.render_btn.setGraphicsEffect(self.shadow_effect[3])
        self.how_to_btn.setGraphicsEffect(self.shadow_effect[4])
        self.setup_btn.setGraphicsEffect(self.shadow_effect[5])

        # add stock img to main window
        self.fst_frame.setPixmap(QPixmap("resources\\fst.jpg"))
        self.lst_frame.setPixmap(QPixmap("resources\\lst.jpg"))
        self.fst_frame.setGraphicsEffect(self.shadow_effect[0])
        self.lst_frame.setGraphicsEffect(self.shadow_effect[1])

        # making Setup and Go buttons disabled for a while
        self.render_btn.setEnabled(False)
        self.setup_btn.setEnabled(False)

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

        # activating setup and go buttons
        self.isSetupSelected = False
        self.isVideoLoaded = False
        self.classics_radio_btn.clicked.connect(self.setup_btn_activation)
        self.moves_radio_btn_2.clicked.connect(self.setup_btn_activation)

        # setup button action
        self.setup_btn.clicked.connect(self.open_setup)

        # Go button action
        self.render_btn.clicked.connect(self.render_frame)

        # mode selection
        self.classics_radio_btn.clicked.connect(self.classic_mode_selected)
        self.moves_radio_btn_2.clicked.connect(self.moving_mode_selected)

    # changes mode to classic
    def classic_mode_selected(self):
        self.mode = "CLASSIC"

    # changes mode to moving slit
    def moving_mode_selected(self):
        self.mode = "LIN"

    # function starts when Go! button clicked. This starts making final picture
    def render_frame(self):
        if self.mode == "CLASSIC":
            video_file = cs.VideoFile(self.name_of_file[0])
            vid = video_file.get_video_flow()
            frame_info = video_file.get_video_info()

            final_frame = cs.Frame(vid, self.slit_position, self.mode, [self.RS.getRange()[0], self.RS.getRange()[1]])

            # saves picture to /Result folder (creates folder if there is no such folder)
            cs.save_result_frame(final_frame.get_frame())

            # When everything done, release the video capture object
            vid.release()
        elif self.mode == "LIN":
            video_file = cs.VideoFile(self.name_of_file[0])
            vid = video_file.get_video_flow()
            frame_info = video_file.get_video_info()

            a = cs.BasisCurve(self.mode, [frame_info[0], frame_info[1],
                              self.RS.getRange()[0],
                              self.RS.getRange()[1]],
                              self.lin_params)
            [mat_a, pix_storage_a] = a.get_surface()
            final_frame = cs.Frame(vid, pix_storage_a, self.mode, [self.RS.getRange()[0], self.RS.getRange()[1]])

            # saves picture to /Result folder (creates folder if there is no such folder)
            cs.save_result_frame(final_frame.get_frame())

            # When everything done, release the video capture object
            vid.release()

    # Opens one of the setup windows (which one depends on selected mode)
    def open_setup(self):
        if self.mode == "CLASSIC":
            self.classic_setup_win.setStyleSheet(style)
            self.classic_setup_win.show()

            # transmit data from MainWindow to SetupWindow
            self.classic_setup_win.frame_width_label.setText(
                "<< " + str(int(self.video_f.get(CAP_PROP_FRAME_WIDTH))) + " px >>")
            # self.classic_setup_win.frame_layout.addWidget(self.fst_frame)
            self.classic_setup_win.slit_pos_text_field.setValue(
                random.randint(1, int(self.video_f.get(CAP_PROP_FRAME_WIDTH))))
            self.set_frames_to_grid(self.RS.getRange()[0], self.RS.getRange()[1])
        elif self.mode == "LIN":
            self.moving_setup_win.setStyleSheet(style)
            self.moving_setup_win.show()

            # transmit data from MainWindow to SetupWindow
            self.moving_setup_win.frame_width_label.setText(
                "<< " + str(int(self.video_f.get(CAP_PROP_FRAME_WIDTH))) + " px >>")

    # opens system window to search files to open
    def search_name_file(self):
        self.name_of_file = QFileDialog.getOpenFileName(self, "Open video file", os.getcwd(), "Video files (*.mp4)")
        if self.name_of_file[0] != "":
            self.video_f.release()
            self.video_f.open(self.name_of_file[0])
            self.isVideoLoaded = True
            self.setup_btn_activation()

            # adding range slider RS to layout
            self.slider_layout.addWidget(self.RS)

            # update slider limits
            self.RS.setMin(0)
            self.RS.setMax(int(self.video_f.get(CAP_PROP_FRAME_COUNT)))

            # this lines change values of range sliders, so triggers call to set_frames_to_grid func and, sometimes,
            # set_frames_to_grid asks for wrong frames
            # self.RS.setStart(50)
            # self.RS.setEnd(int(self.video_f.get(CAP_PROP_FRAME_COUNT) - 50))
            self.set_frames_to_grid(50, int(self.video_f.get(CAP_PROP_FRAME_COUNT) - 50))
        else:
            pass

    # add frames from video to main window (replace stock images or previous frames)
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
        if abs(self.n0 - n) > 8:
            self.video_f.set(CAP_PROP_POS_FRAMES, n)  # go to n frame
            self.n0 = n
            inf, cv_img = self.video_f.read()  # reading frame to cv pic
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            aspect_ratio = self.video_f.get(CAP_PROP_FRAME_WIDTH) / self.video_f.get(CAP_PROP_FRAME_HEIGHT)
            p = convert_to_qt_format.scaled(round(aspect_ratio * height), height, Qt.KeepAspectRatio)
            self.pic = QPixmap.fromImage(p)
            return self.pic
        else:
            return self.pic

    # makes setup button active when mode is selected AND video is opened
    def setup_btn_activation(self):
        if self.classics_radio_btn.isChecked() is True or self.moves_radio_btn_2.isChecked() is True:
            self.isSetupSelected = True

        if self.isSetupSelected is True and self.isVideoLoaded is True:
            self.setup_btn.setEnabled(True)


if __name__ == "__main__":
    cv2.setUseOptimized(cv2.useOptimized())
    app = QApplication(sys.argv)

    with open("style.qss", "r") as s:
        style = s.read()

    app.setStyleSheet(style)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
