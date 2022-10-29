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
                            follow_for=follow_until_white,
                             left_motor = left_motor, right_motor = right_motor, light = left_light)