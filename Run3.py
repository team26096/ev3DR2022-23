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
def getOutOfBase():
    #we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    #we reset mm_vertical
    mm_vertical.reset()

    #we reset gyro
    gyro.reset()
    #we reset both motors
    robot.reset()
    #gyro straight
    robot.cs = left_light
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)
    s.beep()

def alignWithSolarFarm():

    #move rack to the right to avoid energy storage
    mm_horizontal.on_for_degrees(35, -450, brake=True, block=True)

    #turn right to approach solar farm
    #sss gyro.reset()
    pivot_gyro_turn(10, 0, 32, robot, gyro, bLeftTurn=False)
    s.beep()

    #gyro straight to get in position for solar farm
    #gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=32, 
                        follow_for=my_follow_for_degrees, degrees=870,
                        right_motor = right_motor, left_motor = left_motor)

    #we run mm_horizontal all the way to the left so we can collect solar units
    #run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.on_for_degrees(35, 350, brake=True, block=True)

def collectEnergyUnits():

    #move forward to collect the first solar unit
    # robot.follow_gyro_angle(3, 0, 0, 25, target_angle=32, 
    #                     follow_for=my_follow_for_degrees, degrees=50,
    #                     right_motor = right_motor, left_motor = left_motor)

    #turn to collect energy units from solar farm
    #pivot_gyro_turn(0, -20, 32, robot, gyro, bLeftTurn=False)
    pivot_gyro_turn(20, 0, 70, robot, gyro, bLeftTurn=False)

    #gyro straight to collect the last solar unit (next to smart grid)
    #sss gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=70, 
                        follow_for=my_follow_for_degrees, degrees=350,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to avoid smart grid and align to power to X
    #sss gyro.reset()
    #pivot_gyro_turn(0, -20, 40, robot, gyro, bLeftTurn=False)
    pivot_gyro_turn(0, -20, 130, robot, gyro, bLeftTurn=False)


def dropUnitstoPX():
    #raising rack to avoid water reservoir
    mm_vertical.on_for_degrees(100, 500, brake=True, block=True)

    #gyro straight into power to X to drop energy units
    #gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=130, 
                        follow_for=my_follow_for_degrees, degrees=450,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to drop energy units into power to X
    #sss gyro.reset()
    #pivot_gyro_turn(0, -20, 40, robot, gyro, bLeftTurn=False)
    pivot_gyro_turn(0, -20, 145, robot, gyro, bLeftTurn=False)


    #gyro straight into power to X
    #gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=145,
                        follow_for=my_follow_for_degrees, degrees=225,
                        right_motor = right_motor, left_motor = left_motor)
         
    #leave energy units in power to X and avoid water resorvior
    mm_vertical.on_for_degrees(35, 1000, brake=True, block=True)

    #go back to align to leave power to X
    robot.reset()
    robot.on_for_degrees(-25, -25, 300, brake=True, block=True)
    s.beep()
    
    #turn until back light is on black
    backward_turn_until_black(back_light, robot, bLeftTurn=False)
    s.beep()

def alignForSmartGrid():
    #starts line following with back sensor to smart grid
    robot.reset()
    robot.cs = back_light
    #line follow backward until it's been 3.7 seconds
    robot.follow_line(-1.2, 0, 0, -15, target_light_intensity=56,
                    follow_left_edge=False,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=follow_for_ms, ms=3700)
    s.beep()

def doSmartGrid():

    #move horizontal rack to the right to hook to lever on smart grid
    mm_horizontal.reset()
    mm_horizontal.on_for_degrees(50, -300, brake=True, block=True)

    #we run mm_vertical all the way down to grab lever for smart grid
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

    #move horizontal rack left and pull smart grid
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

def collectRB():
    gyro.reset()
    robot.reset()
    #raising rack detach smart grid
    mm_vertical.on_for_degrees(35, 300, brake=True, block=True)

    #go back to head to base and collect RB
    #robot.reset()
    robot.on_for_degrees(-25, -25, 300, brake=True, block=True)
    s.beep()

    #turning to align robot to base and pick up RB
    #gyro.reset()
    pivot_gyro_turn(0, -10, 30, robot, gyro, bLeftTurn=False)
    s.beep()

    #go backward to collect RB
    robot.reset()
    robot.on_for_degrees(-25, -25, 200, brake=True, block=True)
    s.beep()
    
    #move rack to the right to avoid toy factory
    mm_horizontal.on_for_degrees(35, -800, brake=True, block=True)

    #Turn more so the robot ends up completely in base
    pivot_gyro_turn(0, -10, 45, robot, gyro, bLeftTurn=False)
    s.beep()
    
    #final go back to base and grab RB
    robot.on_for_degrees(-25, -25, 1500, brake=True, block=True)
    s.beep()

getOutOfBase()
alignWithSolarFarm()
collectEnergyUnits()
dropUnitstoPX()
alignForSmartGrid()
doSmartGrid()
collectRB()