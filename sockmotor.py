from time import sleep
import RPi.GPIO as GPIO

class SockMotor():

    def __init__(self, dir1, dir2, step1, step2, stepCount, delay, motorEnable, DIRECTION):
        DIR = dir1 #20
        self.STEP1 = step1 #21

        DIR2 = dir2 #16
        self.STEP2 = step2 #12
        self.motorEnable = motorEnable
        

        SPR = 48

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dir1, GPIO.OUT)
        GPIO.setup(dir2, GPIO.OUT)
        GPIO.setup(self.STEP1, GPIO.OUT)
        GPIO.setup(self.STEP2, GPIO.OUT)
        GPIO.setup(self.motorEnable, GPIO.OUT)
        
        GPIO.output(dir1, DIRECTION)
        GPIO.output(dir2, DIRECTION)
        GPIO.output(self.motorEnable, GPIO.HIGH)

        self.step_count = stepCount #SPR
        self.delay = delay #.0208
        
    def CycleMotor(self, motorNo):
        step = self.STEP1 if motorNo == 1 else self.STEP2
        
        for count in range(self.step_count):
            GPIO.output(step, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(step, GPIO.LOW)
            sleep(self.delay)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.output(self.motorEnable, GPIO.LOW)
        return

