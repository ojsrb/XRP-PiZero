import cv2
import config

aruco_dict = config.aruco_dict

marker_id = 42
marker_size = 200

marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
cv2.imwrite(f"marker_{marker_id}.png", marker_image)