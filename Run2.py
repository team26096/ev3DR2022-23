#!/usr/bin/env micropython

# add imports
from initialize import *


def getOutOfBase():

    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -50)
    mm_vertical.reset

    # bring rack up
    mm_vertical.on_for_degrees(40, 1750, brake=True, block=True)
    sleep(1)
    
    #move rack left 
    run_for_motor_stalled(mm_horizontal, 10000, 25)
    mm_horizontal.reset()
  
    # gyro straight until the lcs sees black and white
    gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)

def alignForEnergyStorage():
    
    #move rack to the middle for energy storage
    mm_horizontal.reset()
    mm_horizontal.on_for_degrees(50, -400, brake=True, block=True)

    #line follow to energy storage
    robot.reset()
    robot.cs = left_light
    
    #begin line follow
    robot.follow_line(1.2, 0, 0, 15, target_light_intensity=56,
                    follow_left_edge=False,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=follow_until_black, lightSensor=right_light)
    s.beep()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=160, left_motor=left_motor, right_motor=right_motor)
    s.beep()

def doEnergyStorage():
    
    #go down to drop units into energy storage bin
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

def doOilPlatform():
    
    #come back to get in position for oil platform
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-300, left_motor=left_motor, right_motor=right_motor)

    #move rack left to get under pump
    mm_horizontal.reset()
    mm_horizontal.on_for_degrees(50, 400, brake=True, block=True)

    #raise rack 4 times to pump fuel units into truck
    loop = 0
    while(loop < 4):
        mm_vertical.on_for_degrees(40, 900, brake=True, block=True)
        sleep(0.3)
        mm_vertical.on_for_degrees(40, -900, brake=True, block=True)   
        loop = loop + 1
    s.beep()
    # come back to base
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -50, target_angle=30, 
                    follow_for=my_follow_for_degrees, degrees=-1300, left_motor=left_motor, right_motor=right_motor)

def run2():
    getOutOfBase()
    alignForEnergyStorage()
    doEnergyStorage()
    doOilPlatform()

