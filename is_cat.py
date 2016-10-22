import sys
import json
from os.path import join, dirname
import cv2
from watson_developer_cloud import VisualRecognitionV3
import serial
from api_key import API_KEY

API_VERSION = '2016-05-20'
IMAGE_NAME = 'test.png'

LOADING = bytes([1])
IS_CAT = bytes([2])
IS_MAYBE_CAT = bytes([3])
IS_NOT_CAT = bytes([4])

if (len(sys.argv) < 2):
    sys.exit('Arduino Serial Port Required')

arduino_serial_port = sys.argv[1]
arduino_serial = serial.Serial(arduino_serial_port)

cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
video_capture = cv2.VideoCapture(0)

while True:
    _, frame = video_capture.read()
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

arduino_serial.write(LOADING)
cv2.imwrite('test.png', frame)

visual_recognition = VisualRecognitionV3(API_VERSION, api_key=API_KEY)

with open(IMAGE_NAME, 'rb') as image_file:
    data = visual_recognition.classify(images_file=image_file)

classes = data['images'][0]['classifiers'][0]['classes']

maybe_cat = False
is_cat = False

for image_class in classes:
    if image_class['class'] == 'mammal':
        maybe_cat = True
    if image_class['class'] == 'cat':
        is_cat = True

if is_cat:
    arduino_serial.write(IS_CAT)
elif maybe_cat:
    arduino_serial.write(IS_MAYBE_CAT)
else:
    arduino_serial.write(IS_NOT_CAT)
