import RPi.GPIO as GPIO
from time import sleep


class Servo_driver():
    def __init__(self, portNo):
        self.portNo = portNo;
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.portNo, GPIO.OUT)
        self.servoPWM = GPIO.PWM(self.portNo, 50)
        self.servoPWM.start(0)
        self.servoPWM.ChangeDutyCycle(2)


    def unlock(self):
        self.servoPWM.ChangeDutyCycle(5)
        sleep(0.5)
    
    def lock(self):
        self.servoPWM.ChangeDutyCycle(2) 
        sleep(0.5)

