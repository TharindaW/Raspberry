import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)


pipes = [[0xe7 ,0xe7 ,0xe7 ,0xe7 ,0xe7] , [ 0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO , spidev.SpiDev())
radio.begin(0,17)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_HIGH)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1 , pipes[1])
radio.printDetails()

radio.startListening()


try:  
    while True:
        ackPL = [1]

        time.sleep(1)

        while not radio.available(0):
            time.sleep(1)

        receivedMessage = []
        radio.read( receivedMessage , radio.getDynamicPayloadSize())

        print( "Received {}".format(receivedMessage))
        print( "Translating the received message into unicode characters...")

        string = ""

        for n in receivedMessage:
            if( n>=32 and n<=126):
                string +=chr(n)

        print( string)

        radio.writeAckPayload( 1 , ackPL , len(ackPL))

        print( "Loaded payload reply of {}".format(ackPL) )
  
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









