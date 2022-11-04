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

#start of code

#we reset mm_horizontal
mm_horizontal.reset()

#we run mm_horizontal all the way to the left 
run_for_motor_stalled(mm_horizontal, 10000, 35)

#we reset mm_vertical
mm_vertical.reset()

#we run mm_vertical all the way down
run_for_motor_stalled(mm_vertical, 10000, -35)

#we reset gyro
gyro.reset()
#we reset both motors
robot.reset()

#gyro straight
robot.cs = left_light
robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=follow_until_black, lightSensor=left_light)
s.beep()

#move rack to the right to avoid energy storage
mm_horizontal.reset()
mm_horizontal.on_for_degrees(35, -300, brake=True, block=True)

#turn right to approach solar farm
gyro.reset()
pivot_gyro_turn(10, 0, 30, robot, gyro, bLeftTurn=False)
s.beep()

#gyro straight to get in position for solar farm
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=850,
                    right_motor = right_motor, left_motor = left_motor)

#we run mm_horizontal all the way to the left so we can collect solar units
run_for_motor_stalled(mm_horizontal, 10000, 35)

#move forward to collect the first solar unit
robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=20,
                    right_motor = right_motor, left_motor = left_motor)

#turn to collect energy units from solar farm
gyro.reset()
pivot_gyro_turn(0, -22, 30, robot, gyro, bLeftTurn=False)

#gyro straight to collect the last solar unit (next to smart grid)
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=370,
                    right_motor = right_motor, left_motor = left_motor)

#turn to avoid smart grid and align to power to X
gyro.reset()
pivot_gyro_turn(0, -20, 40, robot, gyro, bLeftTurn=False)

#raising rack to avoid water reservoir
mm_vertical.on_for_degrees(100, 500, brake=True, block=False)

#gyro straight into power to X to drop energy units
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=400,
                    right_motor = right_motor, left_motor = left_motor)

#turn to drop energy units into power to X
gyro.reset()
pivot_gyro_turn(0, -15, 40, robot, gyro, bLeftTurn=False)

#gyro straight into power to X
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=290,
                    right_motor = right_motor, left_motor = left_motor)

#leave energy units in power to X and avoid water resorvior
mm_vertical.on_for_degrees(100, 1000, brake=True, block=False)

#go back to align to leave power to X
robot.on_for_degrees(-25, -25, 245, brake=True, block=True)

#start aligning with smart grid
gyro.reset()
pivot_gyro_turn(0, -20, 105, robot, gyro, bLeftTurn=False)

#starts line following with back sensor to smart grid
left_motor.reset()
right_motor.reset()
robot.cs = back_light
robot.follow_line(-1, 0, 0, -15, target_light_intensity=56,
                 follow_left_edge=True,
                 off_line_count_max=500,
                 sleep_time=0.01,
                 follow_for=my_follow_for_degrees, degrees=-600,
                 left_motor = left_motor, right_motor = right_motor)

#move horizontal rack to the right to hook to lever on smart grid
mm_horizontal.reset()
mm_horizontal.on_for_degrees(50, -625, brake=True, block=True)

#we run mm_vertical all the way down to grab lever for smart grid
run_for_motor_stalled(mm_vertical, 10000, -35)

#move horizontal rack left and pull smart grid
run_for_motor_stalled(mm_horizontal, 10000, 50)


