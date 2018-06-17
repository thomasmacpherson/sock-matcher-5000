from RPLCD.gpio import CharLCD
from time import sleep
import RPi.GPIO as GPIO
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)

colours = ["Pink", "Green", "Blue", "Yellow"]
while True:
    for colour in colours:
        lcd.clear()
        lcd.write_string('SockMatcher 5000')
        lcd.cursor_pos =(1,0)
        lcd.write_string(colour + " sock!")
        sleep(1)