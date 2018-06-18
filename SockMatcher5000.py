from sockcamera import SockCamera

from sockmotor import SockMotor
import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
GPIO.setmode(GPIO.BCM) # setup pinmode


from RPLCD.gpio import CharLCD
from time import sleep
import RPi.GPIO as GPIO
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11], numbering_mode=GPIO.BCM)
lcd.clear()
lcd.write_string('SockMatcher 5000')
lcd.cursor_pos =(1,0)
lcd.write_string('Please wait')

BUTTPIN = 23
SHUTDOWNBUTTPIN = 4
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


pink = [100, 20, 220]
green = [44, 75, 52]
yellow = [60, 150, 180]
blue = [120, 70, 30]

red_range = 35
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
lcd.clear()
lcd.write_string('SockMatcher 5000')
lcd.cursor_pos =(1,0)
lcd.write_string('Press start')
    
while True:
    #print(camera.ReadSockColour())
    
    #print("POINT1")
    if GPIO.input(BUTTPIN) == GPIO.LOW:
        socks_count = [0,0,0,0]
        print ("homing")
        lcd.cursor_pos =(1,0)
        lcd.write_string('Homing...       ')
        homePlatter()
        time_out = 0
        #GoToSockTub(4) #Go to waste tub
        
        while True:
            print("Waiting for sock")
            lcd.cursor_pos =(1,0)
            lcd.write_string('Waiting for sock')
            waitForSock()
            time_out = time_out + 1
            if time_out > 15:
                break
            
            current_colour = camera.ReadSockColour()
            print(current_colour)
            for index, colour in enumerate(colours):
                if (colour[0]-blue_range <= current_colour[0] <= colour[0]+blue_range) and (colour[1]-green_range <= current_colour[1] <= colour[1]+green_range) and (colour[2]-red_range <= current_colour[2] <= colour[2]+red_range):
                    print("colour match")
                    print(colour_names[index])
                    lcd.clear()
                    lcd.write_string('SockMatcher 5000')
                    lcd.cursor_pos =(1,0)
                    lcd.write_string(colour_names[index] + " sock!")
                    GoToSockTub(index)
                    time_out = 0
    
    elif GPIO.input(SHUTDOWNBUTTPIN) == GPIO.LOW:
        call("sudo shutdown -h now", shell=True)
        
GPIO.cleanup()



    
    