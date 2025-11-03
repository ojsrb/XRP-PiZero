import serial
import struct
import communication.driverstation as driverstation

telemetry = {
    'voltage': 0.0,
    'status': 0,
    'last_update': 0
}

ser: serial.Serial

def start():
    ser = serial.Serial('/dev/serial0', 115200, timeout=0.1)

def send_movement(vx, vy, vr):
    start_byte = 0xFF
    checksum= (vx + vy + vr) & 0xFF

    data = struct.pack('Bbbbb', start_byte, vx, vy, vr, checksum)
    ser.write(data)

def send_stop():
    ser.write(b'\xAA')

def check_for_messages(robot_time):
    if robot_time - telemetry['last_update'] > 0.5:
        return False

    if ser.in_waiting > 2:
        start = ser.read(1)[0]

        if start == 0xAA:
            driverstation.set_robot_status(False, robot_time)
            driverstation.send_message("ESTOP sent on UART.", robot_time)
            return False

        if start == 0xFE:
            error_code = ser.read(1)[0]
            driverstation.set_robot_status(False, robot_time)
            driverstation.send_message(f"Error code {error_code} on UART.", robot_time)

        if start == 0xFD:
            if ser.in_waiting >= 5:
                voltage_bytes = ser.read(4)
                voltage = struct.unpack('f', voltage_bytes)[0]
                status = ser.read(1)[0]

                telemetry['voltage'] = voltage
                telemetry['status'] = status
                telemetry['last_update'] = robot_time

                driverstation.send_telemetry(telemetry, robot_time)
