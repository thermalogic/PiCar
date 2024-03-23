#
# 配置/home/cmh/.bashrc为登录启动
# 配置/etc/rc.local为开机启动无效
# 配置irremote 32 gpio1 2 在系统中/boot/config.txt
#
import evdev
import RPi.GPIO as GPIO
import time
from .motor import Motor
from .led import Led

def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            return device

def irremote_worker(motor,led):
    """irremote thread worker function"""
    # irremote code 
    # 21 keys
    # code   key   action
    # 24     2      GO
    # 8      4      Right
    # 90     6      Left
    # 82     8      Back
    # 28     5      Stop

    #  ZTE TV Box
    # code       key   action
    # 71(0x47)    ^     GO
    # 72(0x48)    <     Left
    # 73(0x49)    OK     Stop
    # 74(0x4A)    >     Right
    # 75(0x4B)         Back
      
    #dict_irremote_code={24:Motor.GO,90:Motor.LEFT,8:Motor.RIGHT,
    #                 82:Motor.BACK,28:Motor.STOP}
    
    dict_irremote_code={71:Motor.GO,
                        72:Motor.LEFT,
                        73:Motor.STOP,
                        74:Motor.RIGHT,
                        75:Motor.BACK
                        }
    
    device = get_ir_device()
    while True:
        time.sleep(0.001)
        next_event = device.read_one()
        if (next_event):
            if next_event.value in  dict_irremote_code.keys():
                cur_action=dict_irremote_code[next_event.value]
                motor.action(cur_action)
                led.action(cur_action)
            
