import cv2
import config
import time
import numpy as np
import math
import functions

cam = cv2.VideoCapture(0)

aruco_dict = config.aruco_dict
marker_size = config.aruco_marker_side_length
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

cv_file = cv2.FileStorage('calibration_chessboard.yaml', cv2.FILE_STORAGE_READ)
mtx = cv_file.getNode('K').mat()
dst = cv_file.getNode('D').mat()
cv_file.release()

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

camera = Camera()

while True:
    start_time = time.perf_counter()

    frame = cam.read()[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)


    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        tag_positions = functions.get_tag_positions(corners, marker_size, mtx, dst, ids)
        for i in ids:
            tag_relative_position = tag_positions[i]
            tag_absolute_position = config.tag_positions[i]

    cv2.imshow("camera", frame)

    if cv2.waitKey(1) & 0xFF == 32:
        break

    end_time = time.perf_counter()
    loop_time = round((end_time - start_time) * 1000)
    if loop_time > config.overrun_time:
        print("loop overrun")

cam.release()
cv2.destroyAllWindows()