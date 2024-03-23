import RPi.GPIO as GPIO
import time
from .motor import *
from .led import *


class Ultrasonic:

    def __init__(self):
        self.TRIGGER = 31  # GPIO 6
        self.ECHO = 29   # GPIO  5
        # ultrasonic
        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        self.count_timeout = 10000 # 不取时间，采用控制循环等待次数，减少线程工作时间
        self.distance = self.get_distance()

    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.TRIGGER, True)
       # set Trigger after 0.01ms to LOW
        time.sleep(0.0001) # 取0.1ms，避免多线程时间的精度有限问题
        GPIO.output(self.TRIGGER, False)

        count=self.count_timeout 
        while (GPIO.input(self.ECHO) == 0) and count>0:
            count-=1  
        StartTime = time.time()
   
        count=self.count_timeout 
        while (GPIO.input(self.ECHO) == 1) and count>0:
             count-=1  
        StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        cm = (TimeElapsed * 34300) / 2  # multiply with the sonic speed (34300 cm/s)and divide by 2, because there and back
        return cm

    def worker(self, motor):
        """ul thread worker function"""
        while True:
            time.sleep(0.1)
            self.distance=self.get_distance()
            # print ("Measured Distance = %.1f cm" % dist)
            if (motor.MOTOR_STATE == Motor.GO or motor.MOTOR_STATE == Motor.LEFT or motor.MOTOR_STATE == Motor.RIGHT):
                if (self.distance < 30):
                    led_stop()
                    motor.action(Motor.STOP)
                    time.sleep(0.1)
                    motor.action(Motor.BACK)
                    time.sleep(0.3)
                    motor.action(Motor.STOP)
