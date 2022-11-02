#!/usr/bin/env micropython

#add imports here
import os
import threading  
import logging
from time import time, sleep
from ev3dev2 import motor
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering,
                           MoveTank, SpeedPercent, follow_for_ms, MediumMotor, LargeMotor)
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
#from functions import *
from ev3dev2._platform.fake import OUTPUT_C
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire, Wheel
from functions import *
from functions import follow_until_black
from functions import follow_until_white

s = Sound()
robot = MoveTank(OUTPUT_B, OUTPUT_C)
gyro = GyroSensor(INPUT_3)
robot.gyro = gyro
mm_horizontal = MediumMotor(OUTPUT_D)
mm_vertical = MediumMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_C)
left_motor = LargeMotor(OUTPUT_B)
left_light = ColorSensor(INPUT_4)
right_light = ColorSensor(INPUT_1)
back_light = ColorSensor(INPUT_2)
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3DRTires, 85.35)
mdiff.gyro=gyro
logfile = logging.getLogger('')
btn = Button()

#add run 4 code here
gyro.reset()
sleep(0.5)
logfile = logging.getLogger('')
logfile.info('gyro before = ' + str(gyro.angle))
left_motor.reset()
right_motor.reset()
run_for_motor_stalled(mm_horizontal, 10000, -35)

#we reset mm_horizontal
mm_horizontal.reset()

#we run mm_vertical all the way down
run_for_motor_stalled(mm_vertical, 10000, -50)

# gyro straight to align with rechargeable battery 
mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=615,
                            right_motor = right_motor, left_motor = left_motor)

# move horizontal rack left to drop battery units in rechargeable battery space.
run_for_motor_stalled(mm_horizontal, 10000, 35)

# bring rack back to position and right for watch tv
mm_horizontal.reset()
run_for_motor_stalled(mm_horizontal, 10000, -35)

# gyro staight to complete watch television
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=280,
                            right_motor = right_motor, left_motor = left_motor)

# move horizontal rack to the left to do wind turbine mission
run_for_motor_stalled(mm_horizontal, 10000, 35)

# lifting rack up to avoid hitting wind turbine
mm_vertical.on_for_degrees(100, 1500, brake=True, block=False)

# move forward to align with white line in wind turbine
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                            follow_for=follow_until_white, lightSensor = right_light)
s.beep()
mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                            follow_for=follow_until_black, lightSensor = right_light)
s.beep()

# turn left to align with oil platform 
pivot_gyro_turn(0, 20, -15, robot, gyro, bLeftTurn=True)

# gyro staight to complete oil platform
gyro.reset()
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=200,
                            right_motor = right_motor, left_motor = left_motor)

# gyro staight backwards to realse the truck
gyro.reset()
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, -20, target_angle=0, 
                            follow_for=follow_until_white, lightSensor = right_light)

# turn to align front with wind turbine
pivot_gyro_turn(20, -20, 60, robot, gyro, bLeftTurn=False)

# commenting v1 plan for wind turbine bucket thing
'''
# turn left to align with oil platform 
pivot_gyro_turn(0, 20, -10, robot, gyro, bLeftTurn=True)
gyro.reset()
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, -20, target_angle=0, 
                            follow_for=follow_until_black, lightSensor = right_light)
mdiff.follow_gyro_angle(4, 0, 0, -20, target_angle=0, 
                            follow_for=follow_until_white, lightSensor = right_light)
        
#we run mm_vertical all the way down
run_for_motor_stalled(mm_vertical, 10000, -50)
gyro.reset()
left_motor.reset()
right_motor.reset()
robot.on_for_degrees(-25, -25, 80, brake=True, block=True)

# the robot will push the lever 4 times to get the energy units
loop = 0
while(True):
    if (loop < 4):
        run_for_motor_stalled(mm_horizontal, 10000, -50)
        sleep(2)
        run_for_motor_stalled(mm_horizontal, 10000, 50) 
        sleep(2)
    loop = loop + 1
'''