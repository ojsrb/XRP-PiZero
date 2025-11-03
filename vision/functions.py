import math
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
from lib.utils import *

def euler_from_quaternion(quat: quat):
    t0 = +2.0 * (quat.w * quat.x + quat.y * quat.z)
    t1 = +1.0 - 2.0 * (quat.x * quat.x + quat.y * quat.y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (quat.w * quat.y - quat.z * quat.x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (quat.w * quat.z + quat.x * quat.y)
    t4 = +1.0 - 2.0 * (quat.y * quat.y + quat.z * quat.z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z

def estimatePoses(corners, marker_size, mtx, distortion):
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, r, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(r)
        tvecs.append(t)
        trash.append(nada)

    return rvecs, tvecs

def get_tag_positions(corners, marker_size, mtx, dst, ids):
    rvecs, tvecs = estimatePoses(corners, marker_size, mtx, dst)
    marker_positions = {}

    for i, marker_id in enumerate(ids):
        # Store the translation (i.e. position) information
        transform_translation_x = tvecs[i][0][0]
        transform_translation_y = tvecs[i][1][0]
        transform_translation_z = tvecs[i][2][0]

        # Store the rotation information
        rotation_matrix = np.eye(4)
        rotation_matrix[0:3, 0:3] = cv2.Rodrigues(np.array(rvecs[i]))[0]
        r = R.from_matrix(rotation_matrix[0:3, 0:3])
        quaternion = r.as_quat()

        transform_rotation_x = quaternion[0]
        transform_rotation_y = quaternion[1]
        transform_rotation_z = quaternion[2]
        transform_rotation_w = quaternion[3]

        # Euler angle format in radians
        roll_x, pitch_y, yaw_z = euler_from_quaternion(quat=quat(transform_rotation_x, transform_rotation_y, transform_rotation_z, transform_rotation_w))

        roll_x = math.degrees(roll_x)
        pitch_y = math.degrees(pitch_y)
        yaw_z = math.degrees(yaw_z)

        marker_positions[str(marker_id[0])] = vec3rotation(transform_translation_x, transform_translation_y, transform_translation_z, roll_x, pitch_y, yaw_z)

    return marker_positions