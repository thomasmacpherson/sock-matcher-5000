from sockcamera import SockCamera

from sockmotor import SockMotor
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # setup pinmode


BUTTPIN = 23
HOMEPIN = 15

# Motor direction
CW = 0
CCW = 1

motorBelt = 1
motorTurntable = 2
GPIO.setup(BUTTPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HOMEPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

StepsPerSockTub = 158
CurrentSockTubNum = 0
global camera
camera = SockCamera()


pink = [160, 20, 245]
green = [44, 75, 52]
yellow = [60, 150, 180]
blue = [120, 70, 30]

red_range = 30
green_range = 35
blue_range = 35

colours = [pink, green, yellow, blue]
colour_names = ["pink","green","yellow", "blue"]


def waitForSock():
    # Switch conveyer belt motor on
    with SockMotor(dir1=20,
                   dir2=16,
                   step1=21,
                   step2=12,
                   stepCount=48,
                   delay=.0208,
                   motorEnable=14,
                   DIRECTION=CW) as mot:
        #mot.CycleMotor(motorTurntable)
        mot.CycleMotor(motorBelt)
        
        
def homePlatter():
    counter=0
    with SockMotor(dir1=20,
                   dir2=16,
                   step1=21,
                   step2=12,
                   stepCount=1,
                   delay=.0208,
                   motorEnable=14,
                   DIRECTION=CCW) as mot:
        while GPIO.input(HOMEPIN) == GPIO.HIGH:
            print("homing...")
            mot.CycleMotor(motorTurntable)
            counter = counter + 1
        print("homed, ready for sock")
        print(str(counter) + " steps turned")
        global CurrentSockTubNum
        CurrentSockTubNum = 0
            
        
        
def GoToSockTub(tubNum):
    global CurrentSockTubNum
    print("Go to Tubnum " + str(tubNum))
    Steps = (tubNum - CurrentSockTubNum) * StepsPerSockTub
    
    print(str(Steps) + " steps to go")
    
    CurrentSockTubNum = tubNum
    
    dir = CW
    
    if (Steps < 0):
        Steps = -Steps
        dir = CCW
    
    with SockMotor(dir1=20,
               dir2=16,
               step1=21,
               step2=12,
               stepCount=Steps,
               delay=.0208,
               motorEnable=14,
               DIRECTION=dir) as mot:
        mot.CycleMotor(motorTurntable)
    
    

#with SockMotor(dir1=20,
#               dir2=16,
#               step1=21,
#               step2=12,
#               stepCount=48,
#               delay=.0208,
#               motorEnable=14) as mot:

    
while True:
    #print(camera.ReadSockColour())
    
    #print("POINT1")
    if GPIO.input(BUTTPIN) == GPIO.LOW:
        socks_count = [0,0,0,0]
        print ("homing")
        homePlatter()
        
        while True:
            print("Waiting for sock")
            #waitForSock()
            
            current_colour = camera.ReadSockColour()
            print(current_colour)
            for index, colour in enumerate(colours):
                if (colour[0]-blue_range <= current_colour[0] <= colour[0]+blue_range) and (colour[1]-green_range <= current_colour[1] <= colour[1]+green_range) and (colour[2]-red_range <= current_colour[2] <= colour[2]+red_range):
                    print("colour match")
                    print(colour_names[index])
                    
                    #if socks_count[index] < 2:
                    #socks_count[index] = socks_count[index] + 1
                    GoToSockTub(index)
                    #else:
                    #GoToSockTub(4)
'''
 
#        sleep(2)
#        GoToSockTub(4)
#        
        GoToSockTub(2)
                
    else:
        # wait for sock
        sleep(0.1) # wait a bit and check again
        
       # '''
GPIO.cleanup()



    
    