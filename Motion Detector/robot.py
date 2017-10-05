import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library


GPIO.setmode( GPIO.BOARD)

PINWL = 38
PINWR = 40

PINDIR_L = 29
PINDIR_R = 31


print "Distance measurement in progress"

GPIO.setup(PINWL,GPIO.OUT)
GPIO.setup(PINWR,GPIO.OUT)

GPIO.setup(PINDIR_L,GPIO.OUT)
GPIO.setup(PINDIR_R,GPIO.OUT)

WL = GPIO.PWM(PINWL,5)
WR = GPIO.PWM(PINWR,5)


WL.start(0)
WR.start(0)

try:  
	while True:
	

		GPIO.output(PINDIR_L, 1)
		GPIO.output(PINDIR_R, 1)
		
		"""
		for i in range (100):
			WL.ChangeDutyCycle(i)
			WR.ChangeDutyCycle(i)
			time.sleep(0.1)
		"""
		print "ChangeDutyCycle",50
		WL.ChangeDutyCycle(0)
		WR.ChangeDutyCycle(0)
		time.sleep(2)
		
		GPIO.output(PINDIR_L, 1)
		GPIO.output(PINDIR_R, 1)
		
		print "ChangeDutyCycle",90
		WL.ChangeDutyCycle(90)
		WR.ChangeDutyCycle(90)
		time.sleep(2)		
		


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