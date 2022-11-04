#!/usr/bin/env micropython

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
#start of code
#we run mm_horizontal all the way to the left 
run_for_motor_stalled(mm_horizontal, 10000, 35)
#we reset mm_horizontal
mm_horizontal.reset()
#we run mm_vertical all the way down
run_for_motor_stalled(mm_vertical, 10000, -50)
#we reset mm_vertical
mm_vertical.reset()
#we reset gyro
gyro.reset()
#we reset both motors
robot.reset()

#we move robot forward to the end of base area
robot.on_for_degrees(25, 25, 500, brake=True, block=True)

#we turn gyro to align with the hydroelectric dam 
pivot_gyro_turn(0, 10, -35, robot, gyro, bLeftTurn=True)

#moving to catch water units
robot.on_for_degrees(25, 25, 215, brake=True, block=True)

#move to the right
mm_horizontal.on_for_degrees(35, -500, brake=True, block=True)

#lifting water unit up 
mm_vertical.on_for_degrees(100, 900, brake=True, block=True)

#moving more right to not bump into the mission
#mm_horizontal.on_for_degrees(-35, -500, brake=True, block=True)

#going forward to drop water unit
robot.on_for_degrees(25, 25, 300, brake=True, block=True)

#raising rack up to push lever
mm_vertical.on_for_degrees(100, 1100, brake=True, block=True)

#going forward to water reservoir
robot.on_for_degrees(25, 25, 275, brake=True, block=True)

#moving water unit above reservoir
mm_horizontal.on_for_degrees(15, 600, brake=True, block=True)

#moving vertical all the way down
mm_vertical.on_for_degrees(15, -800, brake=True, block=True)

#going back to release the water unit into the reservoir
robot.on_for_degrees(25, 25, -75, brake=True, block=True)

#moving rack to the right
run_for_motor_stalled(mm_horizontal, 10000, -25)

#going forward to align with other water units
robot.on_for_degrees(25, 25, 700, brake=True, block=True)

#moving to left to release water units
run_for_motor_stalled(mm_horizontal, 10000, 25)

'''
#we lift up the water unit to hook onto water reservoir
mm_vertical.on_for_degrees(100, 900, brake=True, block=True)
#we grab the water unit and move the rack away from the hydroelectric dam
mm_horizontal.on_for_degrees(35, -800, brake=True, block=True)
#moving forward to align with the hydroelectric dam dropping mechanism
robot.on_for_degrees(25, 25, 225, brake=True, block=True)
#dropping water unit which'll realease energy unit, is going 600 more than previous step
mm_vertical.on_for_degrees(75, 600, brake=True, block=True)
#coming down to avoid crashing into our mission
mm_vertical.on_for_degrees(75, -600, brake=True, block=True)
#going forward after hydroelectric dam
robot.on_for_degrees(25, 25, 300, brake=True, block=True)
'''