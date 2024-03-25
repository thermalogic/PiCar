import RPi.GPIO as GPIO


class Motor:

    GO = 0
    BACK = 1
    STOP = 2
    LEFT = 3
    RIGHT = 4
    SPEED_100=100
    SPEED_75=75
    SPEED_50=50
    SPEED_25=25
    

    def __init__(self):
        self.Left_Black = 27 # Pin 13 IN3
        self.Left_Red =  22   # Pin 15 IN4 
        self.Right_Black = 17 # Pin 11 IN1
        self.Right_Red = 18   #  Pin 12   PCM_CLK
        
        self.Left_Enable = 24  # Pin  18  ENA 
        self.Right_Enable = 25  # Pin 22  ENB 
        
        self.MOTOR_STATE = Motor.STOP

        self.speed= Motor.SPEED_75 # default speed 
        self.turn_speed=50 # 左，右侧速度差。全速转向：速度差100% 一侧停止

        # init
        GPIO.setup(self.Left_Black, GPIO.OUT)
        GPIO.setup(self.Left_Red, GPIO.OUT)
        GPIO.setup(self.Right_Black, GPIO.OUT)
        GPIO.setup(self.Right_Red, GPIO.OUT)
        # speed PWM
        GPIO.setup(self.Left_Enable, GPIO.OUT)
        GPIO.setup(self.Right_Enable, GPIO.OUT)
        
        self.Left_Motor=GPIO.PWM(self.Left_Enable, 100)
        self.Left_Motor.start(0)
        self.Right_Motor=GPIO.PWM(self.Right_Enable,100)
        self.Right_Motor.start(0)

        self.DICT_CMD_ACTION = {Motor.GO: self.go,
                                Motor.BACK: self.back,
                                Motor.STOP: self.stop,
                                Motor.LEFT: self.turn_left,
                                Motor.RIGHT: self.turn_right
                                }

    def go(self):
        self.Left_Motor.ChangeDutyCycle(self.speed)
        GPIO.output(self.Left_Red, GPIO.HIGH)
        GPIO.output(self.Left_Black, GPIO.LOW)
        # 
        self.Right_Motor.ChangeDutyCycle(self.speed)
        GPIO.output(self.Right_Red, GPIO.HIGH)
        GPIO.output(self.Right_Black, GPIO.LOW)

    def back(self):
        self.Left_Motor.ChangeDutyCycle(self.speed)
        GPIO.output(self.Left_Red, GPIO.LOW)
        GPIO.output(self.Left_Black, GPIO.HIGH)
        self.Right_Motor.ChangeDutyCycle(self.speed)
        GPIO.output(self.Right_Red, GPIO.LOW)
        GPIO.output(self.Right_Black, GPIO.HIGH)

    def stop(self):
        self.Left_Motor.ChangeDutyCycle(0)
        GPIO.output(self.Left_Red, GPIO.LOW)
        GPIO.output(self.Left_Black, GPIO.LOW)
        self.Right_Motor.ChangeDutyCycle(0)
        GPIO.output(self.Right_Red, GPIO.LOW)
        GPIO.output(self.Right_Black, GPIO.LOW)

    def turn_left(self):
        cur_speed=int(self.speed*(1.0-self.turn_speed/100.0))
        self.Left_Motor.ChangeDutyCycle(cur_speed)
        GPIO.output(self.Left_Red, True)
        GPIO.output(self.Left_Black, False)
        self.Right_Motor.ChangeDutyCycle(self.speed)
        GPIO.output(self.Right_Red, GPIO.HIGH)
        GPIO.output(self.Right_Black, GPIO.LOW)

    def turn_right(self):
        self.Left_Motor.ChangeDutyCycle(self.speed)
        GPIO.output(self.Left_Red, GPIO.HIGH)
        GPIO.output(self.Left_Black, GPIO.LOW)
        cur_speed=int(self.speed*(1.0-self.turn_speed/100.0))
        self.Right_Motor.ChangeDutyCycle(cur_speed)
        GPIO.output(self.Right_Red, True)
        GPIO.output(self.Right_Black, False)
    

    def action(self, cmd_to_motor):
        if (cmd_to_motor != self.MOTOR_STATE):
            self.MOTOR_STATE = cmd_to_motor
            self.DICT_CMD_ACTION[cmd_to_motor]()
    
    def adjust_speed(self,set_speed):
        # 前进后退速度
        if (self.speed!=set_speed):
            self.speed=set_speed
            self.DICT_CMD_ACTION[self.MOTOR_STATE]()

    def adjust_turn_speed(self,set_turn_speed):
        # 转向速度 -控制2侧速度差
        if (self.turn_speed!=set_turn_speed):
            self.turn_speed=set_turn_speed
            if (self.MOTOR_STATE== Motor.LEFT):
               self.turn_left()
            elif (self.MOTOR_STATE== Motor.RIGHT): 
               self.turn_right()