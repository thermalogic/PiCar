#
# led
#
import RPi.GPIO as GPIO
import time
import threading
from .motor import Motor

class Led:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.LEFT_LED = 14  # pin 8
        self.RIGHT_LED = 21 # pin 40   
        GPIO.setup(self.LEFT_LED, GPIO.OUT)
        GPIO.setup(self.RIGHT_LED, GPIO.OUT)
        for i in range(5):
            GPIO.output(self.LEFT_LED, GPIO.LOW)
            GPIO.output(self.RIGHT_LED, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.LEFT_LED, GPIO.HIGH)
            GPIO.output(self.RIGHT_LED, GPIO.HIGH)
            time.sleep(0.2)
        self.blink_thread_on=False   
        self.LED_STATE = Motor.STOP


    def go(self):
        GPIO.output(self.LEFT_LED, GPIO.HIGH)
        GPIO.output(self.RIGHT_LED, GPIO.HIGH)

    def turn_right(self):
        GPIO.output(self.LEFT_LED, GPIO.LOW)
        GPIO.output(self.RIGHT_LED, GPIO.HIGH)
     
    def turn_left(self):
        GPIO.output(self.LEFT_LED, GPIO.HIGH)
        GPIO.output(self.RIGHT_LED, GPIO.LOW)

    def stop(self):
        GPIO.output(self.LEFT_LED, GPIO.LOW)
        GPIO.output(self.RIGHT_LED, GPIO.LOW)


    def action(self,motor_state):
        self.LED_STATE = motor_state
        if self.LED_STATE == Motor.GO:
            self.go()
        elif self.LED_STATE ==  Motor.STOP:
            self.stop()
        elif not self.blink_thread_on:
           self.led_blink() 
      
    def led_blink_worker(self):
        while True:
            while self.LED_STATE ==  Motor.BACK:
                self.stop()
                time.sleep(0.2)
                self.go()
                time.sleep(0.2)
        
            while self.LED_STATE ==  Motor.LEFT:
                GPIO.output(self.LEFT_LED, GPIO.HIGH)
                GPIO.output(self.RIGHT_LED, GPIO.LOW)
                time.sleep(0.2)
                GPIO.output(self.LEFT_LED, GPIO.LOW)
                time.sleep(0.2)    

            while self.LED_STATE == Motor.RIGHT:
                GPIO.output(self.LEFT_LED, GPIO.LOW)
                GPIO.output(self.RIGHT_LED, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(self.RIGHT_LED, GPIO.LOW)
                time.sleep(0.2)    


    def led_blink(self):
        self.blink_thread = threading.Thread(target=self.led_blink_worker,daemon=True)
        self.blink_thread.start()
        self.blink_thread_on=True

 