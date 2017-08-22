import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)


pipes = [[0xe7 ,0xe7 ,0xe7 ,0xe7 ,0xe7] , [ 0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]


radio = NRF24(GPIO , spidev.SpiDev())
radio.begin(1,18)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_HIGH)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

#radio.openReadingPipe(1 , pipes[1])
radio.openWritingPipe(pipes[1])
radio.printDetails()

#While writing cannot listning 
#radio.startListening() 


try:  
    while True:
        message= list("SPI Tharinda")
        print( "Set the message of {}".format(message))


        #Check for ack
        if radio.isAckPayloadAvailable():
            returnedPL = []
            radio.read( returnedPL , radio.getDynamicPayloadSize() )
            print("ACK recived {}".format(returnedPL))
        else:
            print("ACK not recived")

        time.sleep(1)
  
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "KeyboardInterrupt\n"
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  
    print "GPIO clenup suceess\n"






