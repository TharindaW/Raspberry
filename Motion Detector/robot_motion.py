# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import numpy as np
import argparse

import RPi.GPIO as GPIO


GPIO.setmode( GPIO.BOARD)

PINWL = 38
PINWR = 40

PINDIR_L = 29
PINDIR_R = 31

GPIO.setup(PINWL,GPIO.OUT)
GPIO.setup(PINWR,GPIO.OUT)

GPIO.setup(PINDIR_L,GPIO.OUT)
GPIO.setup(PINDIR_R,GPIO.OUT)

WL = GPIO.PWM(PINWL,5)
WR = GPIO.PWM(PINWR,5)


WL.start(0)
WR.start(0)

            

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-r", "--radius", type = int, help = "radius of Gaussian blur; must be odd")
args = vars(ap.parse_args())


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1024, 928)
camera.framerate = 32
camera.hflip = False
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(1024, 928))

# allow the camera to warmup
time.sleep(0.1)

try:

	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array

		orig = image.copy()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
		(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
		image = orig.copy()
		cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)
		cv2.circle(image, (512, 464), 10, (0, 255, 0), 2)
		
		# Draw a diagonal red line with thickness of 5 px
		cv2.line(image,maxLoc,(512, 464),(0,0,255),1)
		
		
		
		WL.ChangeDutyCycle(maxLoc)
		WR.ChangeDutyCycle(maxLoc)
		
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(image, 'MSC IN AI - Robot Project ' ,(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)


		# display the results of our newly improved method
		cv2.imshow("Robust", image)
		
		
		# show the frame
		#cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
		
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "KeyboardInterrupt\n"					 	# print value of counter  
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit		