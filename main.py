import vision.vision as vision
from lib.utils import *
import communication.driverstation as ds
import communication.xrp_controller as xrp
import config
import socket
import json
import time

start_time = time.time()
robot_time = 0

# initialize communication w/ driver station
ds.start()

# start comms with pico (XRP Controller)
# xrp.start()

# define robot parts
# main_cam = vision.Camera(0)

position = vec3(0,0,0)
vx = 0 # -1 to 1
vy = 0
vr = 0

robot_state = False

ESTOP = False

while not ESTOP:
    robot_time = time.time() - start_time
    command = None

    if ds.status():
        ds.send_telemetry({
            'voltage': 100.0,
            'status': 0
        }, robot_time)
        command = ds.get_command(robot_time)

    if command:
        if command['type'] == 'set_robot_status':
            robot_state = command['value']
        elif command['type'] == 'move':
            if robot_state:
                vx = command['vx']
                vy = command['vy']
                vr = command['vr']
                xrp.send_movement(vx, vy, vr)
        elif command['type'] == 'stop':
            vx = 0
            vy = 0
            vr = 0
            ESTOP = True
            xrp.send_stop()
            break

    # if not xrp.check_for_messages(robot_time):
    #     ESTOP = True
    #     xrp.send_stop()
    #     break


    # position = vision.estimate_position(main_cam)


