import os
import cv2
import numpy as np
import core_sup as cs
import time


if __name__ == "__main__":
    source = os.getcwd() + "\\"  # Получение расположения .exe

    cv2.setUseOptimized(cv2.useOptimized())
    video_file = cs.VideoFile(source)
    vid = video_file.get_video_flow()
    frame_info = video_file.get_video_info()

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
