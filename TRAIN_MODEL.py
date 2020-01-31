import numpy as np
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import cv2 as cv
import os
import pickle
import time
import random

img_size = 70
categories = ["forward", "stop", "right", "left"]
data_dir = "DATASET folder PATH"
training_data = []

#
NAME = "ROAD-SMART_{}".format(int(time.time()))
print(NAME)
board = TensorBoard(log_dir='logs/{}'.format((NAME)))


def pass_training_data():
    for category in categories:
        path = os.path.join(data_dir, category)
        class_num = categories.index(category)
        for img in os.listdir(path):
            try:
                image_path = os.path.join(path, img)
                picture = cv.imread(image_path, -1)
                picture = cv.resize(picture, (img_size, img_size))
                training_data.append([picture, class_num])
            except Exception as e:
                pass


pass_training_data()
random.shuffle(training_data)
# validate training data content
for sample in training_data[:10]:
    print("labels: ", sample[1])

x = []
y = []

for image, label in training_data:
    x.append(image)
    y.append(label)

images = np.array(x)
labels = np.array(y)

print(images.shape)



# reshape and save input and output array
# input images
images = images.reshape(-1, img_size, img_size, 3)
pickle_out = open("aix.pickle", "wb")
pickle.dump(images, pickle_out)
pickle_out.close()
# output images
pickle_out = open("aiy.pickle", "wb")
pickle.dump(labels, pickle_out)
pickle_out.close()

############################################################

# read input and output array
# input images
pickle_in = open("aix.pickle", "rb")
x = np.asarray(pickle.load(pickle_in))
pickle_in.close()
# output images
pickle_in = open("aiy.pickle", "rb")
y = np.asarray(pickle.load(pickle_in))
pickle_in.close()
x = x/255.0




# Define Network (CNN)
NeuralNet = Sequential()
NeuralNet.add(Conv2D(256, (3, 3), input_shape = x.shape[1:]))
NeuralNet.add(Activation("relu"))
NeuralNet.add(MaxPooling2D(pool_size=(2, 2)))


NeuralNet.add(Conv2D(128, (3, 3)))
NeuralNet.add(Activation("relu"))
NeuralNet.add(MaxPooling2D(pool_size=(2, 2)))


NeuralNet.add(Conv2D(64, (3, 3)))
NeuralNet.add(Activation("relu"))
NeuralNet.add(MaxPooling2D(pool_size=(2, 2)))

NeuralNet.add(Flatten())
NeuralNet.add(Dense(64))
NeuralNet.add(Activation("relu"))

NeuralNet.add(Dense(4))
NeuralNet.add(Activation("sigmoid"))

NeuralNet.compile(loss ="sparse_categorical_crossentropy", optimizer = "adam", metrics = ['accuracy'])
NeuralNet.fit(x, y, epochs = 10, callbacks=[board])

print(NAME)
NeuralNet.save("AI_car_model.h5")

