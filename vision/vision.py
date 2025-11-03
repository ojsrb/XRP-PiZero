import cv2
import config
import time
import vision.functions as functions
from lib.utils import *

cam = cv2.VideoCapture(0)

aruco_dict = config.aruco_dict
marker_size = config.aruco_marker_side_length
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

cv_file = cv2.FileStorage('lib/calibration_chessboard.yaml', cv2.FILE_STORAGE_READ)
mtx = cv_file.getNode('K').mat()
dst = cv_file.getNode('D').mat()
cv_file.release()

class Camera:
    def __init__(self, num: int, offset: vec3 = vec3(0,0,0)):
        self.video = cv2.VideoCapture(num)
        self.offset = offset

    def get_frame(self):
        ret, frame = self.video.read()
        return frame

def estimate_position(cam: Camera, show_camera: bool = False):
    position = vec3(0,0,0)

    frame = cam.get_frame()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        estimated_positions = []

        tag_positions = functions.get_tag_positions(corners, marker_size, mtx, dst, ids)
        for i in ids:
            tag_relative_position = tag_positions[str(i[0])]
            tag_absolute_position = config.tag_positions[str(i[0])]
            estimated_positions.append(tag_absolute_position - tag_relative_position)

        estimated_position = vec3(0,0,0)
        for i in estimated_positions:
            estimated_position += i

        estimated_position = estimated_position.mul(1/len(estimated_positions)) + cam.offset


    if show_camera:
        cv2.imshow("camera", frame)

    cam.release()

if __name__ == '__main__':
    main()