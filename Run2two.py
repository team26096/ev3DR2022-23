#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

def run2twoSelfSetup():
    #move rack right
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()
    mm_vertical.reset()
    mm_vertical.on_for_degrees(75, 400, brake=True, block=True)

def bringOilTruck():
    gyro.reset()
    robot.reset()

    # we are going forward till we reach oil truck while also resetting the rack
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=800, left_motor=left_motor, right_motor=right_motor)
    
    #bring rack down to catch oil truck
    run_for_motor_stalled(mm_vertical, 10000, -65)
    robot.reset()
    #come back to base while bringing truck
    robot.follow_gyro_angle(3, 0, 0, -65, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-700, left_motor=left_motor, right_motor=right_motor)

def setUpForRun3():
    # we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 65)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    #we reset mm_vertical
    mm_vertical.reset()

def run2two():
    run2twoSelfSetup()
    bringOilTruck()

run2two()