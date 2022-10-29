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
class EV3DRTires(Wheel):
    """
    part number 41897
    comes in set 45544
    """
    def __init__(self):
        Wheel.__init__(self, 50, 15)
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3DRTires, 85.35)
mdiff.gyro=gyro
logfile = logging.getLogger('')
btn = Button()
def follow_until_black(tank, left_motor, right_motor, light):
    light_intensity = (light.reflected_light_intensity)
    if light_intensity <= 13:
        return False
    else:
        return True
def follow_until_white(tank, left_motor, right_motor, light):
    light_intensity = (light.reflected_light_intensity)
    if light_intensity >= 85:
        return False
    else:
        return True

def my_follow_for_degrees(tank, degrees, left_motor, right_motor):
    averagedegrees = (left_motor.position + right_motor.position)/2  
    if degrees >= 0:
        if averagedegrees >= degrees:
            return False
        else:
            return True
    # if the target degrees are less than 0, the robot is moving backwards
    else:
        if averagedegrees <= degrees:
            return False
        else:
            return True

def pivot_gyro_turn(left_speed, right_speed, target_angle, 
robot, gyro, bLeftTurn = True):
    logfile = logging.getLogger('')
    CurGyro = gyro.angle
    logfile.info('gyro = ' + str(CurGyro))
    if  bLeftTurn == True:
        while CurGyro >= target_angle:
            logfile.info('gyro = ' + str(CurGyro))
            robot.on(left_speed, right_speed)
            CurGyro = gyro.angle
    else: 
        while CurGyro <= target_angle:
            logfile.info('gyro = ' + str(CurGyro))
            robot.on(left_speed, right_speed)
            CurGyro = gyro.angle

def run_for_motor_stalled(motor, seconds, speed):
    motor.on(speed)
    motor.wait_until_not_moving(timeout=seconds)
    motor.stop()

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

#gyro straight
robot.follow_gyro_angle(3, 0, 0, SpeedPercent(25), target_angle=0, 
                    follow_for=follow_until_black, left_motor=left_motor, 
                    right_motor = right_motor, light=left_light)

#starts line following with left sensor
robot.cs = left_light
robot.follow_line(-1.5,0,0,15, target_light_intensity=45,
                follow_left_edge=True,
                off_line_count_max=500,
                sleep_time=0.01,
                follow_for=my_follow_for_degrees, degrees=900,
                left_motor = left_motor, right_motor = right_motor)

s.beep()

#gyro straight to get in position for solar farm
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, SpeedPercent(25), target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=600,
                    right_motor = right_motor, left_motor = left_motor)

#turn to collect energy units from solar farm
gyro.reset()
pivot_gyro_turn(0, 10, -5, robot, gyro, bLeftTurn=True)

#gyro straight to get in position for solar farm
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, SpeedPercent(25), target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=100,
                    right_motor = right_motor, left_motor = left_motor)

#turn to collect energy units from solar farm
gyro.reset()
pivot_gyro_turn(0, -20, 30, robot, gyro, bLeftTurn=False)

#gyro straight to collect the last solar unit (next to smart grid)
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, SpeedPercent(25), target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=320,
                    right_motor = right_motor, left_motor = left_motor)

#turn to drop energy units into power to X
gyro.reset()
pivot_gyro_turn(0, -20, 70, robot, gyro, bLeftTurn=False)

#gyro straight into power to X to drop energy units
gyro.reset()
right_motor.reset()
left_motor.reset()
robot.follow_gyro_angle(3, 0, 0, SpeedPercent(25), target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=500,
                    right_motor = right_motor, left_motor = left_motor)