import os
import cv2
import numpy as np
import core_sup as cs
import time


if __name__ == '__main__':
    source = os.getcwd() + "\\"  # Получение расположения .exe
    print("Wait")

    cv2.setUseOptimized(cv2.useOptimized())
    vid = cv2.VideoCapture(source + "vid.mp4")  # Открытие видео
    if not vid.isOpened():
        print("Can't open your video file")

    frame_w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # Высота кадра
    frame_h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Ширина кадра
    frame_n = vid.get(cv2.CAP_PROP_FRAME_COUNT)  # Количество кадров
    frame_f = vid.get(cv2.CAP_PROP_FPS)  # FPS

    # a = cs.BasisCurve('LIN', [frame_w, frame_h, frame_n - 500, frame_n - 100], [5, 0.5, 0])
    # [mat_a, pix_storage_a] = a.get_surface()
    # final_frame = cs.Frame(vid, pix_storage_a)

    b = cs.BasisCurve('GAUSS', [frame_w, frame_h, frame_n - 500, frame_n - 100], [250, 200, 300, 150, 400, 150])
    [mat_b, pix_storage_b] = b.get_surface()
    final_frame = cs.Frame(vid, pix_storage_b)

    cs.save_result_frame(source, final_frame.get_frame())

    # When everything done, release the video capture object
    vid.release()

    # Closes all the frames
    cv2.destroyAllWindows()
