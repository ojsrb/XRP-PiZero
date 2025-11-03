import socket
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5000))
server.listen(1)
print("awaiting connection...")
conn, addr = server.accept()
conn.settimeout(0.1)
print("connected")
conn.send(json.dumps({'type': 'connected', 'ip': addr[0], 'port': addr[1] }).encode('utf-8'))

def reconnect():
    print("reconnecting...")
    conn, addr = server.accept()
    conn.settimeout(0.1)
    print("connected")

def get_command(robot_time):
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            command = json.loads(data)
            send_message(command, robot_time)
            return command
        else:
            return None
    except socket.timeout:
        return None

def set_robot_status(value: bool, robot_time):
    conn.send(json.dumps({'type': 'set_robot_status', 'value': value, 'robot_time': robot_time}).encode('utf-8'))

def send_message(message, robot_time):
    conn.send(json.dumps({'type': 'message', 'message': message, 'robot_time': robot_time}).encode('utf-8'))

def send_telemetry(telemetry, robot_time):
    conn.send(json.dumps({'type': 'telemetry', 'telemetry': telemetry, 'robot_time': robot_time}).encode('utf-8'))
