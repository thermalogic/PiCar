import RPi.GPIO as GPIO
import time
from .motor import *
from .led import *
import tm1637
import statistics

CLK = 1 #BCM
DIO = 0
tm = tm1637.TM1637(clk=CLK, dio=DIO,brightness=7)

class Ultrasonic:
    VALUE_TIMEOUT=1000 # 超声信号超时。返回数值

    def __init__(self):
        self.TRIGGER =6 # pin 31 
        self.ECHO = 5   # pin 29
        # ultrasonic
        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        self.count_timeout = 10000 # 不取时间，采用控制循环等待次数，减少线程工作时间
        self.avoid_distance=20 # 避撞距离

    def _get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.TRIGGER, True)
        # set Trigger after 0.1ms to LOW
        time.sleep(0.0001) # 取0.1ms，避免多线程时间精度有限问题
        GPIO.output(self.TRIGGER, False)
        
        echo_count=self.count_timeout 
        while (GPIO.input(self.ECHO) == 0) and echo_count>0:
            echo_count-=1  
     
        # 非控制循环次数退出的数据才有效
        if (echo_count>0):
            StartTime = time.time()
     
            echo_count=self.count_timeout 
            while (GPIO.input(self.ECHO) == 1) and echo_count>0:
                echo_count-=1  
     
            if (echo_count>0):
                StopTime = time.time()
                TimeElapsed = StopTime - StartTime
                cm = (TimeElapsed * 34300) / 2  # multiply with the sonic speed (34300 cm/s)and divide by 2, because there and back
                return  cm
        return Ultrasonic.VALUE_TIMEOUT
       
    def get_distance(self):
        current_value=1000
        for _ in range(100):
            current_value=self._get_distance()
            if (current_value!=Ultrasonic.VALUE_TIMEOUT):# 超声信号超声，测量失败
               break
        return current_value
              
    def worker(self, motor,led):
        """ul thread worker function"""
        while True:
            time.sleep(0.1)
            self.distance=self.get_distance()
            # display 
            tm.number(int(self.distance))
            # print ("Measured Distance = %.1f cm" % dist)
            if (motor.MOTOR_STATE == Motor.GO or motor.MOTOR_STATE == Motor.LEFT or motor.MOTOR_STATE == Motor.RIGHT):
                if (self.distance < self.avoid_distance):
                    led.stop()
                    motor.action(Motor.STOP)
                    time.sleep(0.1)
                    motor.action(Motor.BACK)
                    time.sleep(0.3)
                    motor.action(Motor.STOP)
