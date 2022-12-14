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
'''
def do_calibrate():
    left_light = ColorSensor(INPUT_4)
    right_light = ColorSensor(INPUT_1)
    left_light.calibrate_white()
    right_light.calibrate_white()
    s = Sound()
    s.beep()
'''

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

def do_robot_test():
    #robot = MoveTank(OUTPUT_B, OUTPUT_C)
    robot.STOP_ACTION_COAST = 'coast'
    left_motor.reset()
    right_motor.reset()
    start_time=time() 
    logfile = logging.getLogger('')

    #resetting gyro
    sleep(.250)
    gyro.reset()
    s.beep()

    #line following
    robot.cs = right_light
    robot.follow_line(-1.5,0,0,15, target_light_intensity=56,
                follow_left_edge=False,
                off_line_count_max=500,
                sleep_time=0.01,
                follow_for=my_follow_for_degrees, degrees=920,
                left_motor = left_motor, right_motor = right_motor)
    s.beep()

    #resetting the gyro & resetting the motors
    gyro.reset()
    right_motor.reset()
    left_motor.reset()
    
    #gyro straight
    robot.follow_gyro_angle(3, 0, 0, SpeedPercent(25), target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=940,
                            right_motor = right_motor, left_motor = left_motor)

    #pivot gyro turn test
    pivot_gyro_turn(0, -20, 140, robot, gyro, bLeftTurn=False)  
    
    #resetting medium motors
    mm_vertical.reset()
    mm_horizontal.reset()
    
    #running medium motors test
    mm_vertical.on_for_degrees(50, 1800, brake=True, block=True)
    mm_vertical.on_for_degrees(50, -1800, brake=True, block=True)
    mm_horizontal.on_for_degrees(15, 300, brake=True, block=True)
    mm_horizontal.on_for_degrees(15, -300, brake=True, block=True)

#calling our functions
do_robot_test()