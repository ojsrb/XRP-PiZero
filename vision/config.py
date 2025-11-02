import cv2
import csv

# program configs
overrun_time = 50

# AprilTag configs
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
aruco_marker_side_length = 0.106

# Field Configs
config_filename = "field.csv"
with open(config_filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    tag_positions_list = list(reader)[1:]
    tag_positions = {}
    for i in tag_positions_list:
        tag_positions[int(i[0])] = [float(i[1]), float(i[2]), float(i[3])]


print(tag_positions)