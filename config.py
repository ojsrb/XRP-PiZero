import cv2
import csv
from lib.utils import *

# program configs
overrun_time = 50

# AprilTag configs
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
aruco_marker_side_length = 0.106

# Field Configs
config_filename = "lib/field.csv"
with open(config_filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    tag_positions_list = list(reader)[1:]
    tag_positions = {}
    for i in tag_positions_list:
        tag_positions[str(i[0])] = vec3(i[1], i[2], i[3])

# Communication configs
xrp_addr = 0x08
