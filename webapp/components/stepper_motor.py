import RPi.GPIO as GPIO
import time

class Stepper_Motor:

    CLOCKWISE = 1
    ANTICLOCKWISE = 2
   
    def __init__(self,IN1,IN2,IN3,IN4):

        
        self.DICT_CMD_ACTION = { Stepper_Motor.CLOCKWISE: self.step_clockwise,
                                Stepper_Motor.ANTICLOCKWISE: self.step_anticlockwise
                              }


        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        # init
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

        # Define constants
        self.DEG_PER_STEP = 1.8
        self.STEPS_PER_REVOLUTION = int(360 / self.DEG_PER_STEP)
        
    # Function to move the stepper motor one step anticlockwise
    def step_anticlockwise(self,delay, steps):
        for _ in range(steps):
            for coil in [self.IN1,self.IN2,self.IN3,self.IN4]:
                GPIO.output(coil, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(coil, GPIO.LOW)

    # Function to move the stepper motor one step clockwise
    def step_clockwise(self,delay, steps):
        for _ in range(steps):
            for coil in [self.IN4,self.IN3,self.IN2,self.IN1]:
                GPIO.output(coil, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(coil, GPIO.LOW)


    def action(self, cmd_to_motor):
        delay=0.005
        steps= int(self.STEPS_PER_REVOLUTION/10)
        self.DICT_CMD_ACTION[cmd_to_motor](delay,steps)

