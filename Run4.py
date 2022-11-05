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
def mission1():
    logfile.info("first mission is starting")
    gyro.reset()
    sleep(0.5)
    
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
    logfile.info("alighned with rechargable battery")
    # move horizontal rack left to drop battery units in rechargeable battery space.
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    logfile.info("first mission is finished")

def mission2():
    logfile.info("second mission is starting")
    # bring rack back to position and right for watch tv
    mm_horizontal.reset()
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    logfile.info("ready for watch television")

    # gyro staight to complete watch television
    left_motor.reset()
    right_motor.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=300,
                                right_motor = right_motor, left_motor = left_motor)
    logfile.info("second mission is finished")

def mission3():
    logfile.info("third mission is starting")
    # move horizontal rack to the left to do wind turbine mission
    run_for_motor_stalled(mm_horizontal, 10000, 35)

    # lifting rack up to avoid hitting wind turbine
    mm_vertical.on_for_degrees(100, 1500, brake=True, block=False)

    # move forward to align with white line in wind turbine
    gyro.reset()
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
    logfile.info("alighned with oil platform")

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
    logfile.info("third mission is finished")

def mission4():
    logfile.info("fourth mission is starting")
    # turn to align front with wind turbine
    backward_turn_until_black (right_light, robot, bLeftTurn=False)

    # move robot backward
    gyro.reset()
    left_motor.reset()
    right_motor.reset()
    mdiff.follow_gyro_angle(4, 0, 0, -50, target_angle=0, 
                                follow_for=follow_until_white, lightSensor = right_light)
    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -50)
    
    logfile.info("starting back and forth loop for wind turbine")
    # move back and forward for wind turbine
    loop = 0
    while(True):
        if (loop < 4):
            mdiff.follow_gyro_angle(4, 0, 0, 70, target_angle=0, 
                                follow_for=follow_until_white, lightSensor = right_light)
            sleep(2)
            mdiff.follow_gyro_angle(4, 0, 0, -70, target_angle=0, 
                                follow_for=follow_until_white, lightSensor = right_light)
            sleep(2)
        loop = loop + 1
    logfile.info("fourth mission is finished")
    

'''
mission1()
mission2()
mission3()
mission4()
'''
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
                            follow_for=my_follow_for_degrees, degrees=300,
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
backward_turn_until_black (right_light, robot, bLeftTurn=False)

# move robot backward
gyro.reset()
left_motor.reset()
right_motor.reset()
mdiff.follow_gyro_angle(4, 0, 0, -20, target_angle=0, 
                            follow_for=follow_until_white, lightSensor = right_light)

#we run mm_vertical all the way down
run_for_motor_stalled(mm_vertical, 10000, -50)

# move back and forward for wind turbine
loop = 0
while(loop < 4):
    mdiff.follow_gyro_angle(4, 0, 0, 90, target_angle=0, 
                            follow_for=follow_until_white, lightSensor = right_light)
    sleep(0.5)
    mdiff.follow_gyro_angle(4, 0, 0, -90, target_angle=0, 
                            follow_for=follow_until_white, lightSensor = right_light)
    sleep(0.5)
    loop = loop + 1

