import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
#GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

GPIO.setmode( GPIO.BOARD)

TRIG = 7                                   #Associate pin 23 to TRIG
ECHO = 12                                  #Associate pin 24 to ECHO

LED = 40

print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(LED,GPIO.OUT)                   #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in

print "Set-up completed..."


def blink():
	for _ in range(3):
		GPIO.output(LED, 1)
		time.sleep(0.2)
		GPIO.output(LED, 0)
		time.sleep(0.2)
		
blink()		
  
try:  
	while True:

		GPIO.output(TRIG, 0)                 		#Set TRIG as LOW
		print "Waiting For Sensor To Settle"
		time.sleep(0.5)                            	#Delay of 2 seconds
		
		print "Sensor settled..."
		
		GPIO.output(TRIG, 1)                  		#Set TRIG as HIGH
		time.sleep(0.00001)                      	#Delay of 0.00001 seconds
		GPIO.output(TRIG, 0)                 		#Set TRIG as LOW
		
		print "Sonic burst sent..."
		
		while GPIO.input(ECHO)==0:               	#Check whether the ECHO is LOW
			pulse_start = time.time()              	#Saves the last known time of LOW pulse
			#print "Inside ECHO 0"
			
		#print "Zero end"          
		
		while GPIO.input(ECHO)==1:               	#Check whether the ECHO is HIGH
			pulse_end = time.time()                	#Saves the last known time of HIGH pulse 
			#print "Inside ECHO 1"
			
		#print "Received"		
		
		pulse_duration = pulse_end - pulse_start	#Get pulse duration to a variable
		
		distance = pulse_duration * 17150        	#Multiply pulse duration by 17150 to get distance
		distance = round(distance, 2)            	#Round to two decimal points
		
		
		blink()
		if distance > 2 and distance < 400:      	#Check whether the distance is within range
			print "Distance:",distance - 0,"cm\n"  		#Print distance with 0.5 cm calibration
		else:
			print "Out Of Range\n"                   		#display out of range 
  
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "\nKeyboardInterrupt"					 	# print value of counter  
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  
