import os
import cv2
import numpy as np
import core_sup as cs
import time


def open_video_file():
    video_file = cv2.VideoCapture(source + "vid.mp4")  # Открытие видео
    if not video_file.isOpened():
        print("Can't open your video file")

    frame_w = video_file.get(cv2.CAP_PROP_FRAME_WIDTH)  # Высота кадра
    frame_h = video_file.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Ширина кадра
    frame_n = video_file.get(cv2.CAP_PROP_FRAME_COUNT)  # Количество кадров
    frame_f = video_file.get(cv2.CAP_PROP_FPS)  # FPS

    return video_file, [frame_w, frame_h, frame_n, frame_f]


def get_special_frame(video_file, pos):
    video_file.set(cv2.CAP_PROP_POS_FRAMES, pos)
    inf, frame = video_file.read()
    return frame


source = os.getcwd() + "\\"  # Получение расположения .exe
print("Wait")

cv2.setUseOptimized(cv2.useOptimized())
vid, frame_info = open_video_file()

# a = cs.BasisCurve('LIN', [frame_w, frame_h, frame_n - 500, frame_n - 100], [5, 0.5, 0])
# [mat_a, pix_storage_a] = a.get_surface()
# final_frame = cs.Frame(vid, pix_storage_a)

b = cs.BasisCurve('GAUSS', [frame_info[0],
                            frame_info[1],
                            frame_info[2] - 500,
                            frame_info[2] - 100], [250, 200, 300, 150, 400, 150])
[mat_b, pix_storage_b] = b.get_surface()
final_frame = cs.Frame(vid, pix_storage_b)

cs.save_result_frame(source, final_frame.get_frame())

# When everything done, release the video capture object
vid.release()

# Closes all the frames
cv2.destroyAllWindows()
