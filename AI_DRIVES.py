import socket
import numpy as np
from tensorflow import keras
import cv2 as cv
import struct
import pickle
# load model
model = keras.models.load_model("/home/amazing/Desktop/ROADSMART/main/AI_car_model.h5")
img_size = 70
categories2 = ["forward", "stop", "right", "left"]
categories = ['w', 's', 'd', 'a']


def prepare(f):

    pic = cv.resize(f, (img_size, img_size))
    pic = pic.reshape(-1, img_size, img_size,3)
    return pic/255.0


print("waiting for AI CAR")
HOST = 'YOUR SEVER IP HERE'
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
    frame = cv.imdecode(frame, cv.IMREAD_ANYCOLOR)

    # display current received frame
    cv.imshow("DRIVE", cv.resize(frame, (500, 320)))
    # change frame to right format for model
    frame = prepare(frame)
    predictions = model.predict([frame])
    direction = categories[np.argmax(predictions)]

    data_to_send = direction
    print(categories2[categories.index(direction)])

    key = cv.waitKey(1)
    if key == ord('q'):
        conn.send(bytes('s', "utf-8")) # send s to stop car motors
        conn.send(bytes('q', "utf-8"))
        break
    conn.send(bytes(data_to_send, "utf-8"))

conn.close()
cv.destroyAllWindows()
