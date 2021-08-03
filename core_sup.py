import math as m
import os
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, \
    CAP_PROP_FPS
import cv2
import numpy as np


class VideoFile:
    def __init__(self, path):
        if path == "":
            self.video_f = VideoCapture()  # Открытие видео
        else:
            self.video_f = VideoCapture(path)

    def get_video_info(self):
        return [self.video_f.get(CAP_PROP_FRAME_WIDTH),     # Ширина кадра
                self.video_f.get(CAP_PROP_FRAME_HEIGHT),    # Высота кадра
                self.video_f.get(CAP_PROP_FRAME_COUNT),     # Количество кадров
                self.video_f.get(CAP_PROP_FPS)]             # FPS

    def get_video_flow(self):
        return self.video_f

    def get_special_frame(self, pos):
        self.video_f.set(CAP_PROP_POS_FRAMES, pos)
        inf, frame = self.video_f.read()
        return frame

    def __del__(self):
        self.video_f.release()


class BasisCurve:
    def __init__(self, curve_type, box, curve_param):
        self.lst_param = []
        self.param = curve_param  # param - list [k1, k2, k3]
        self.type = curve_type  # curve_type = CLASSIC, LIN, GAUSS or SIN
        self.lst_box = box  # box - [frame_w, frame_h, 1st frame in box, last frame in box]
        self.mat = []
        self.min = box[3]
        self.max = box[2]

        # creates list of parameters for current type of curve
        if self.type == 'LIN':
            for i in range(3):
                self.lst_param.append(0)
        elif self.type == 'GAUSS':
            for i in range(6):
                self.lst_param.append(0)
        elif self.type == 'CLASSIC':
            for i in range(1):
                self.lst_param.append(0)

        # initiation of list of parameters
        for i in range(len(self.param)):
            self.lst_param[i] = self.param[i]

    # if curve value is higher or lower than t_min or t_max, cut this peaks
    def _cut_peaks(self, t):
        if t < self.lst_box[2]:
            t = self.lst_box[2]
        elif t > self.lst_box[3]:
            t = self.lst_box[3]
        return t

    def _curve_proc(self, t):
        if t < self.lst_box[2]:
            t = self.lst_box[2]
        elif t > self.lst_box[3]:
            t = self.lst_box[3]

        if t > self.max:
            self.max = t
        elif t < self.min:
            self.min = t
        return t

    def _calc_surface(self):
        # generation of matrix (surface in discrete space) with h = height of frame and w = width of frame
        for i in range(int(self.lst_box[0])):
            self.mat.append([0] * int(self.lst_box[1]))

        if self.type == 'LIN':
            for x in range(int(self.lst_box[0])):
                for y in range(int(self.lst_box[1])):
                    self.mat[x][y] = round(self.lst_param[0] * x +
                                           self.lst_param[1] * y +
                                           self.lst_param[2])

                    self.mat[x][y] = self._curve_proc(self.mat[x][y])

        elif self.type == 'GAUSS':
            for x in range(int(self.lst_box[0])):
                for y in range(int(self.lst_box[1])):
                    self.mat[x][y] = round(self.lst_param[0] *
                                           m.exp(((x - self.lst_param[1]) / self.lst_param[2]) ** 2) *
                                           m.exp(((y - self.lst_param[3]) / self.lst_param[4]) ** 2) +
                                           self.lst_param[5])

                    self.mat[x][y] = self._curve_proc(self.mat[x][y])

        self.pix_storage = PixelStorage([self.min, self.max], self.type)
        self.pix_storage.set_pixel_data(self.mat, self.lst_box)

        return self.mat

    # getter that gives curve made by _calc_surface
    def get_surface(self):
        self.mat = self._calc_surface()
        return self.mat, self.pix_storage


class PixelStorage:
    def __init__(self, t_lim, mode_type):
        self.type = mode_type
        self.t1 = t_lim[0]
        self.t2 = t_lim[1]

        self.pix_index_table = []
        for i in range(2):
            self.pix_index_table.append([0] * int(self.t2 - self.t1 + 1))
        for j in range(int(self.t2 - self.t1 + 1)):
            self.pix_index_table[0][j] = int(self.t1 + j)

        self.empty = []

    def set_pixel_data(self, mat, frame_param):
        for x_i in range(int(frame_param[0])):
            for y_i in range(int(frame_param[1])):
                self.pix_index_table[1][int(mat[x_i][y_i] - self.t1)] += 1
                self.empty.append([0] * int(self.t2 - self.t1 + 1))
                if self.pix_index_table[1][int(mat[x_i][y_i] - self.t1)] > len(self.pix_index_table) - 2:
                    self.pix_index_table = self.pix_index_table + self.empty
                    self.empty = []
                self.pix_index_table[1 + self.pix_index_table[1][int(mat[x_i][y_i] - self.t1)]][int(mat[x_i][y_i] - self.t1)] = [x_i, y_i]

    def get_nb_of_frames(self):
        return int(self.t2 - self.t1) + 1

    def get_table(self):
        return self.pix_index_table


class Frame:
    def __init__(self, video, pix_storage, mode_type, t_minmax):
        if mode_type == 'LIN' or mode_type == 'GAUSS':
            # go to first frame and creates empty frame
            video.set(CAP_PROP_POS_FRAMES, pix_storage.pix_index_table[0][0] - 1)
            self.pet, self.result_frame = video.read()
            for i in range(pix_storage.get_nb_of_frames()):
                ret, frame = video.read()
                for j in range(pix_storage.pix_index_table[1][i]):
                    xy = pix_storage.pix_index_table[2 + j][i]
                    self.result_frame[int(xy[1]):int(xy[1] + 1), int(xy[0]):int(xy[0] + 1)] = frame[
                                                                                              int(xy[1]):int(xy[1] + 1),
                                                                                              int(xy[0]):int(xy[0] + 1)]
        elif mode_type == 'CLASSIC':
            # in this case pix_storage means slit position, so:
            slit_pos = pix_storage
            # go to first frame and creates empty frame
            video.set(CAP_PROP_POS_FRAMES, t_minmax[0])
            h = int(video.get(CAP_PROP_FRAME_HEIGHT))
            self.result_frame = np.zeros((h, int(t_minmax[1] - t_minmax[0]), 3), np.uint8)
            for i in range(int(t_minmax[1] - t_minmax[0])):
                ret, frame = video.read()
                self.result_frame[0:h, i:(i+1)] = frame[0:h, slit_pos:(slit_pos + 1)]

    def get_frame(self):
        return self.result_frame


# noinspection PySimplifyBooleanCheck
def save_result_frame(final_frame):
    i = 1
    if os.path.exists(os.getcwd() + "\\Results") is True:
        while os.path.exists(os.getcwd() + "\\Results\\Pic_" + str(i) + ".png") is True:
            i += 1
        else:
            cv2.imwrite(os.getcwd() + "\\Results\\Pic_" + str(i) + ".png", final_frame)
    else:
        os.mkdir(os.getcwd() + "\\Results")
        cv2.imwrite(os.getcwd() + "\\Results\\Pic_1.png", final_frame)