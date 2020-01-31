import cv2
import os
import socket
import time
import struct
import pickle

direction_command = ["w", "s", "d", "a"]
categories = ["forward", "stop", "right", "left"]

print("waiting for AI CAR")
HOST = '192.168.43.246'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
print('Socket created')
s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
print("connected to AI CAR")


def capture_data(direction_key, snapshot):
    # sub folder for picture to be stored
    sub_directory = categories[direction_command.index(direction_key)]
    data_dir = "DATASET DIRECTORY HERE" + sub_directory
    image_name = str(time.time()) + ".jpg"
    print(data_dir+image_name)
    os.chdir(data_dir)
    cv2.imwrite(image_name, snapshot)


while True:
    # video stream receive from car
    while len(data) < payload_size:
        data += conn.recv(2042)
    # decode frame
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(2042)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_ANYCOLOR)
    # display current received frame
    cv2.imshow('CAPTURING', cv2.resize(frame, (500, 320)))
    # capture key-board input
    key = cv2.waitKey(5)
    if key == ord("s") or key == ord('a') or key == ord("w") or key == ord("d"):
        # capture_data-set and forward control command
        capture_data(chr(key), frame)
        conn.send(bytes(chr(key), "utf-8"))
    elif key == ord('q'):
        # send exit command and a stop to car
        conn.send(bytes('q', "utf-8"))
        conn.send(bytes('s', "utf-8"))
        break
    elif key == ord('z'):  # backward
        conn.send(bytes(chr(key), "utf-8"))
    elif key == -1:
        # send a stop command when no key is pressed
        conn.send(bytes('s', "utf-8"))
    else:
        conn.send(bytes(chr(key), "utf-8"))


#####################################################

s.close()
cv2.destroyAllWindows()


