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
mdiff.follow_gyro_angle(4, 0, 0, SpeedPercent(20), target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=615,
                            right_motor = right_motor, left_motor = left_motor)
# move horizontal rack left to drop battery units in rechargeable battery space.
run_for_motor_stalled(mm_horizontal, 10000, 35)
# bring rack back to position and right for watch tv
mm_horizontal.reset()
run_for_motor_stalled(mm_horizontal, 10000, -35)
# gyro staight to complete watch television
gyro.reset()
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, SpeedPercent(20), target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=180,
                            right_motor = right_motor, left_motor = left_motor)
# move horizontal rack to the left to do wind turbine mission
left_motor.reset()
right_motor.reset()
run_for_motor_stalled(mm_horizontal, 10000, 35)
# move forward to align with white line in wind turbine
mdiff.follow_gyro_angle(4, 0, 0, SpeedPercent(20), target_angle=0, 
                            follow_for=follow_until_white, lightSensor = left_light)