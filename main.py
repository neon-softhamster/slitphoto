import numpy as np

import core

# windows after qt designer
import window.main_win as mainwindow
import window.classic_setup_win as csw
import window.moving_setup_win as msw
import window.gauss_setup_win as gsw

# Qt imports
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGraphicsDropShadowEffect, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QEvent

# other useful stuff
import time
import webbrowser
import os
import sys
import random
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, \
    COLOR_BGR2RGB, cvtColor, setUseOptimized, useOptimized

# range slider made by Talley Lambert (https://github.com/tlambert03/QtRangeSlider)
from qtrangeslider._labeled import QLabeledRangeSlider
from qtrangeslider.qtcompat.QtCore import Qt
from qtrangeslider.qtcompat.QtWidgets import QApplication, QWidget


# Объект, который будет перенесён в другой поток для выполнения кода
class RenderThread(QtCore.QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(RenderThread, self).__init__(*args, **kwargs)

    def run(self):
        # change status of Go! button (it goes inactive)
        mw.render_btn.setText("Wait")
        mw.render_btn.setEnabled(False)

        if mw.mode == "CLASSIC":
            final_frame = core.Frame(mw.video_f, mw.slit_position, mw.mode, [mw.RS.value()[0], mw.RS.value()[1]])

            # saves picture to /Result folder (creates folder if there is no such folder)
            core.save_result_frame(final_frame.get_frame())
        elif mw.mode == "LIN":
            a = core.BasisCurve(mw.mode,
                                [mw.video_f.get(CAP_PROP_FRAME_WIDTH),
                               mw.video_f.get(CAP_PROP_FRAME_HEIGHT),
                               mw.RS.value()[0],
                               mw.RS.value()[1]],
                                mw.lin_params)
            pix_storage_a = a.get_surface()[1]
            final_frame = core.Frame(mw.video_f, pix_storage_a, mw.mode, [mw.RS.value()[0], mw.RS.value()[1]])

            # saves picture to /Result folder (creates folder if there is no such folder)
            core.save_result_frame(final_frame.get_frame())
        elif mw.mode == "GAUSS":
            a = core.BasisCurve(mw.mode,
                                [mw.video_f.get(CAP_PROP_FRAME_WIDTH),
                               mw.video_f.get(CAP_PROP_FRAME_HEIGHT),
                               mw.RS.value()[0],
                               mw.RS.value()[1]],
                                mw.lin_params)
            pix_storage_a = a.get_surface()[1]
            final_frame = core.Frame(mw.video_f, pix_storage_a, mw.mode, [mw.RS.value()[0], mw.RS.value()[1]])

            # saves picture to /Result folder (creates folder if there is no such folder)
            core.save_result_frame(final_frame.get_frame())

        # change status of Go! button (makes it active)
        mw.render_btn.setText("Go!")
        mw.render_btn.setEnabled(True)

        self.finished.emit()


# Window for settings of classic mode
class ClassicSetupWin(QWidget, csw.Ui_Setup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle('Setup window for classic slit mode')

        self.frame.setMouseTracking(True)
        self.frame.installEventFilter(self)

        # generates list of shadow effects
        self.shadow_effect = shadows(self)
        # adding shadows
        self.save_btn.setGraphicsEffect(self.shadow_effect[0])
        self.frame.setGraphicsEffect(self.shadow_effect[1])

        # ACTIONS #
        self.save_btn.clicked.connect(self.transmit_setup_to_main_win)

    def eventFilter(self, o, e):
        if o is self.frame and e.type() == QtCore.QEvent.MouseMove:
            self.slit_pos_text_field.setValue(round(mw.video_f.get(CAP_PROP_FRAME_HEIGHT) / 450 * e.x()))
        return super().eventFilter(o, e)

    # transmit settings to main window, works when Save button clicked
    def transmit_setup_to_main_win(self):
        mw.slit_position = int(self.slit_pos_text_field.value())
        mw.render_btn.setEnabled(True)
        mw.mode = "CLASSIC"
        self.close()


# Window for settings of moving slit mode
class MovingSetupWin(QWidget, msw.Ui_Setup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle('Setup window for moving slit mode')

        # generates list of shadow effects
        self.shadow_effect = shadows(self)
        # adding shadows
        self.save_btn.setGraphicsEffect(self.shadow_effect[0])
        self.frame.setGraphicsEffect(self.shadow_effect[1])

        # ACTIONS #
        self.save_btn.clicked.connect(self.transmit_setup_to_main_win)

    # transmit settings to main window, works when Save button clicked
    def transmit_setup_to_main_win(self):
        mw.lin_params = [float(self.x_inclin.value()), float(self.y_inclin.value()), float(self.t_shift.value())]
        mw.render_btn.setEnabled(True)
        mw.mode = "LIN"
        self.close()


# Window for settings of gauss mode
class GaussSetupWin(QWidget, gsw.Ui_Setup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle('Setup window for gauss mode')

        self.frame.setMouseTracking(True)
        self.frame.installEventFilter(self)

        # generates list of shadow effects
        self.shadow_effect = shadows(self)
        # adding shadows
        self.save_btn.setGraphicsEffect(self.shadow_effect[0])
        self.frame.setGraphicsEffect(self.shadow_effect[1])

        # ACTIONS #
        self.save_btn.clicked.connect(self.transmit_setup_to_main_win)

    def eventFilter(self, o, e):
        if o is self.frame and e.type() == QtCore.QEvent.MouseMove:
            self.v_shift.setValue(round(mw.video_f.get(CAP_PROP_FRAME_HEIGHT) / 450 * e.x()))
            self.h_shift.setValue(round(mw.video_f.get(CAP_PROP_FRAME_HEIGHT) / 450 * e.y()))
        return super().eventFilter(o, e)

    # transmit settings to main window, works when Save button clicked
    def transmit_setup_to_main_win(self):
        mw.lin_params = [float(self.intense.value()), float(self.h_shift.value()), float(self.h_range.value()),
                         float(self.v_shift.value()), float(self.v_range.value()), float(self.t_shift.value())]
        mw.render_btn.setEnabled(True)
        mw.mode = "GAUSS"
        self.close()


# Main window
class MainWindow(QMainWindow, mainwindow.Ui_Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # Some global values
        self.name_of_file = ["", ""]
        self.n0 = 0
        self.pic = QPixmap()
        self.mode = ""

        # default SETUP parameters
        self.slit_position = 0                          # for classic mode
        self.lin_params = np.zeros(3, float)            # for moving slit mode
        self.gauss_params = np.zeros(6, float)          # for gauss mode

        # generates list of shadow effects
        self.shadow_effect = shadows(self)
        # adding shadows
        self.btn_explore_file.setGraphicsEffect(self.shadow_effect[2])
        self.render_btn.setGraphicsEffect(self.shadow_effect[3])
        self.how_to_btn.setGraphicsEffect(self.shadow_effect[4])
        self.setup_btn.setGraphicsEffect(self.shadow_effect[5])

        # add stock img to main window
        self.fst_frame.setPixmap(QPixmap("resources" + os.sep + "fst.jpg"))
        self.lst_frame.setPixmap(QPixmap("resources" + os.sep + "lst.jpg"))
        self.fst_frame.setGraphicsEffect(self.shadow_effect[0])
        self.lst_frame.setGraphicsEffect(self.shadow_effect[1])

        # making Setup and Go buttons disabled for a while
        self.render_btn.setEnabled(False)
        self.setup_btn.setEnabled(False)

        # adding slider
        self.RS = QLabeledRangeSlider(Qt.Horizontal)

        # creates CV2 video, so it can be reached from any func or meth of program. Also no need to read file every
        # time you want to change frame
        self.video_f = VideoCapture()

        # ACTIONS HERE #
        # button action of searching video file
        self.btn_explore_file.clicked.connect(self.search_name_file)

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
        self.gauss_radio_btn.clicked.connect(self.gauss_mode_selected)

        # slider moved
        self.RS.valueChanged.connect(self.select_frame)

        # "how to" button clicked
        self.how_to_btn.clicked.connect(lambda: webbrowser.open('https://github.com/neon-softhamster/slitphoto#usage'))

    # changes mode to classic
    def classic_mode_selected(self):
        self.mode = "CLASSIC"

    # changes mode to moving slit
    def moving_mode_selected(self):
        self.mode = "LIN"

    # changes mode to gauss
    def gauss_mode_selected(self):
        self.mode = "GAUSS"

    # function starts when Go! button clicked. This starts making final picture
    def render_frame(self):
        # create thread
        self.thread = QtCore.QThread()

        # object to do things in thread
        self.thread_obj = RenderThread()

        # replace object to thread
        self.thread_obj.moveToThread(self.thread)

        # # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.thread_obj.run)
        self.thread_obj.finished.connect(self.thread.quit)

        # start thread
        self.thread.start()

    # Opens one of the setup windows (which one depends on selected mode)
    def open_setup(self):
        if self.mode == "CLASSIC":
            classic_setup_win.setStyleSheet(style)
            classic_setup_win.slit_pos_text_field.setMaximum(self.video_f.get(CAP_PROP_FRAME_WIDTH))
            classic_setup_win.show()

            # transmit data from MainWindow to SetupWindow
            # add frame width
            classic_setup_win.frame_width_label.setText(
                "<< " + str(int(self.video_f.get(CAP_PROP_FRAME_WIDTH))) + " px >>")

            # add frame
            classic_setup_win.frame.setPixmap(self.convert_cv2qt(450, self.RS.value()[0]))
            classic_setup_win.frame_layout.addWidget(classic_setup_win.frame)

            # set random slit position
            classic_setup_win.slit_pos_text_field.setValue(
                random.randint(1, int(self.video_f.get(CAP_PROP_FRAME_WIDTH))))

        elif self.mode == "LIN":
            moving_setup_win.setStyleSheet(style)
            moving_setup_win.show()

            # transmit data from MainWindow to SetupWindow
            moving_setup_win.frame_width_label.setText(
                "<< " + str(int(self.video_f.get(CAP_PROP_FRAME_WIDTH))) + " px >>")

            # add frame
            moving_setup_win.frame.setPixmap(self.convert_cv2qt(450, self.RS.value()[0]))
            moving_setup_win.frame_layout.addWidget(moving_setup_win.frame)

        elif self.mode == "GAUSS":
            gauss_setup_win.setStyleSheet(style)
            gauss_setup_win.show()

            # transmit data from MainWindow to SetupWindow
            gauss_setup_win.frame_width_label.setText(
                "<< " + str(int(self.video_f.get(CAP_PROP_FRAME_WIDTH))) + " px >>")

            # add frame
            gauss_setup_win.frame.setPixmap(self.convert_cv2qt(450, self.RS.value()[0]))
            gauss_setup_win.frame_layout.addWidget(gauss_setup_win.frame)

            # change shift to first range slider value
            gauss_setup_win.t_shift.setValue(int(self.RS.value()[0]))

    # opens system window to search files to open
    def search_name_file(self):
        self.name_of_file = QFileDialog.getOpenFileName(self, "Open video file", os.getcwd(), "Video files (*.mp4)")
        if self.name_of_file[0] != "":
            # closes previous video and closes setup window
            self.video_f.release()
            if classic_setup_win.isEnabled():
                classic_setup_win.close()
            if moving_setup_win.isEnabled():
                moving_setup_win.close()
            if gauss_setup_win.isEnabled():
                gauss_setup_win.close()

            self.video_f.open(self.name_of_file[0])
            self.isVideoLoaded = True
            self.setup_btn_activation()

            # adding range slider RS to layout
            self.slider_layout.addWidget(self.RS)

            # update slider limits
            self.RS.setRange(0, int(self.video_f.get(CAP_PROP_FRAME_COUNT)) - 1)
            self.RS.setValue((int(0.25*self.video_f.get(CAP_PROP_FRAME_COUNT)), int(0.75*self.video_f.get(CAP_PROP_FRAME_COUNT))))

            self.set_frames_to_grid(self.RS.value()[0], self.RS.value()[1])
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
        self.set_frames_to_grid(self.RS.value()[0], self.RS.value()[1])

    # Convert from an opencv image to QPixmap (necessary to add pic to qt layout)
    def convert_cv2qt(self, height, n):  # input is height (ip pixels), that will be in window, n - nb of frame
        if abs(self.n0 - n) > 8:
            self.video_f.set(CAP_PROP_POS_FRAMES, n)  # go to n frame
            self.n0 = n
            inf, cv_img = self.video_f.read()  # reading frame to cv pic
            rgb_image = cvtColor(cv_img, COLOR_BGR2RGB)
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
        if self.classics_radio_btn.isChecked() is True or self.moves_radio_btn_2.isChecked() is True or self.gauss_radio_btn.isChecked() is True:
            self.isSetupSelected = True

        if self.isSetupSelected is True and self.isVideoLoaded is True:
            self.setup_btn.setEnabled(True)


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


if __name__ == "__main__":
    setUseOptimized(useOptimized())
    app = QApplication(sys.argv)

    # creates setup windows
    classic_setup_win = ClassicSetupWin()
    moving_setup_win = MovingSetupWin()
    gauss_setup_win = GaussSetupWin()

    with open("style.qss", "r") as s:
        style = s.read()

    app.setStyleSheet(style)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
