import socket
import serial
import pickle
import cv2
import struct
# you will have to pip install pySerial serial

arduino = serial.Serial('/dev/ttyUSB0',115200)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('your SERver IP HERE', 8080))
connection = client_socket.makefile('wb')


cam = cv2.VideoCapture(-1)

cam.set(3, 100)
cam.set(4, 70)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


while 1:
    # send video stream
    
    ret, frame = cam.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)
    
    # receive control signal
    data = client_socket.recv(1024)
    data_decode = data.decode("utf-8")
    print(data_decode)
    arduino.write(bytes(str(data),"utf-8"))
    if data_decode == 'q':
        break



cam.release()
client_socket.close()
arduino.close()





