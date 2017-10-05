# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import numpy as np
import argparse
import cv2


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
	
	# Draw a diagonal red line with thickness of 1 px
	cv2.line(image,maxLoc,(512, 464),(0,0,255),1)
	
	text1 = "Location:",maxLoc," Max Intensity ",maxVal
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(image, 'MSC IN AI - Robot Project ' ,(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)
	
	print text1

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