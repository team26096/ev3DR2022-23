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
logfile = logging.getLogger('')

#add run 4 code here
def mission1():
    gyro.reset()
    logfile.info('gyro before = ' + str(gyro.angle))
    robot.reset()
    run_for_motor_stalled(mm_horizontal, 10000, -35)

    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

    # gyro straight to align with rechargeable battery 
    mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=620,
                                left_motor = left_motor, right_motor = right_motor)

    # move horizontal rack left to drop battery units in rechargeable battery space.
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    # turn into rechargeable battery to push energy units fully in
    pivot_gyro_turn(0, 15, -10, robot, gyro, bLeftTurn=True)

def mission2():
    # bring rack back to position and right for watch tv
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()
    # turn back for watch tv
    pivot_gyro_turn(15, 0, 5, robot, gyro, bLeftTurn=False)
    # gyro staight to complete watch television
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=265,
                                left_motor = left_motor, right_motor = right_motor)

def mission3():
    # move horizontal rack to the left to avoid wind turbine mission
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

    # lifting rack up to avoid hitting wind turbine
    mm_vertical.on_for_degrees(100, 1500, brake=True, block=False)

    # move forward to until left light sees black line
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_black, lightSensor = left_light)
    s.beep()

    # turn left to align with oil platform 
    # pivot_gyro_turn(0, 20, -25, robot, gyro, bLeftTurn=True)

    # gyro staight to complete oil platform
    # gyro.reset()
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=-35, 
                                follow_for=my_follow_for_degrees, degrees=270,
                                left_motor = left_motor, right_motor = right_motor)

    # lifting rack up to release truck
    mm_vertical.on_for_degrees(100, 850, brake=True, block=False)

    # gyro staight backwards to realse the truck
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, -15, target_angle=-35, 
                                follow_for=follow_until_black, lightSensor = right_light)

def mission4():
    # turn to align front with wind turbine
    pivot_gyro_turn(-10, 15, -25, robot, gyro, bLeftTurn=True)

    backward_turn_until_black (right_light, robot, bLeftTurn=False)
    s.beep()

    # turn to align front with wind turbine
    forward_turn_until_black (left_light, robot, bLeftTurn=False)
    s.beep()
    
    # gyro staight backwards to realse the truck
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, -15, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=-50,
                                left_motor = left_motor, right_motor = right_motor)

    # align bucket on rack with wind turbine
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

    # we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)

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


mission1()
mission2()
mission3()
# mission4()


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
'''
