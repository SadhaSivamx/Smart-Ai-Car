import cv2
from ultralytics import YOLO
import RPi.GPIO as GPIO          
from time import sleep
model=YOLO("Ball.onnx")
import numpy as np
from picamera2 import Picamera2
piCam=Picamera2()
piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format='RGB888'
piCam.preview_configuration.align()
piCam.configure('preview')
piCam.start()
import math

in1 = 24
in2 = 23
en = 25
in3 = 16
in4 = 20
enx = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

GPIO.setup(en,GPIO.OUT)
GPIO.setup(enx,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


p=GPIO.PWM(en,1000)
p.start(50)
q=GPIO.PWM(enx,1000)
q.start(50)

print("\n")    

def init():    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(en,GPIO.OUT)
    GPIO.setup(enx,GPIO.OUT)

def forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)

def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)

def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
GPIO.cleanup()
init()
while True:
	frame=piCam.capture_array()
	frame=cv2.rotate(frame, cv2.ROTATE_180)
	results=model.predict(source=frame,conf=0.05,verbose=False)
	try:
		x=results[0]
		box = x.boxes[0]
		anss=box.xyxy[0].tolist()
		start_point = (int(anss[0]),int(anss[1]))
		end_point = (int(anss[2]),int(anss[3]))
		pointx=((int(anss[0])+int(anss[2]))//2)
		pointy = ((int(anss[1]) + int(anss[3])) // 2)
		color = (255, 0, 0)
		thickness = 3
		frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
		frame = cv2.circle(frame, (pointx, pointy), radius=3, color=(0, 0, 255), thickness=-1)
		
		Size=math.dist(start_point,end_point)
		
		print("Size : ",Size)
		
		if Size>=200:
			backward()
		elif Size<=120:
			forward()
		else:
			stop()
		print(Data)
	except:
		pass
	cv2.imshow('picam',frame)
	if cv2.waitKey(1)==ord('q'):
		break
cv2.destroyAllWindows()
GPIO.cleanup()
