#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

def run2SelfSetup():
    #move rack left
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()
    mm_vertical.reset()
    mm_vertical.on_for_degrees(75, 2300, brake=True, block=True)



def getOutOfBase():
    # gyro straight until the lcs sees black and white
    gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)

def alignForEnergyStorage():
    
    #move rack to the middle for energy storage
    mm_horizontal.on_for_degrees(50, -250, brake=True, block=True)

    #line follow to energy storage
    robot.reset()
    robot.cs = left_light

    #begin line follow, go certain distance to catch line
    robot.follow_line(1.2, 0, 0, 15, target_light_intensity=56,
                    follow_left_edge=False,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=my_follow_for_degrees, degrees=500, left_motor=left_motor, right_motor=right_motor)
    snd.beep()
    #begin line follow, go until white L junction near energy storage
    robot.follow_line(1.2, 0, 0, 15, target_light_intensity=56,
                    follow_left_edge=False,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=follow_until_right_white, lightSensor=right_light)
    snd.beep()
    #follow gyro until both front sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=0, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)
    snd.beep()
    #make sure the robot is aligned completely to energy storage
    if (gyro.angle > 0):
        pivot_gyro_turn(-10, 10, 0, robot, gyro, bLeftTurn=True)
    elif (gyro.angle < 0):
        pivot_gyro_turn(10, -10, 0, robot, gyro, bLeftTurn=False)
    
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=160, left_motor=left_motor, right_motor=right_motor)

def doEnergyStorage():
    
    #go down to drop units into energy storage bin
    run_for_motor_stalled(mm_vertical, 10000, -75)
    mm_vertical.reset()

def doOilPlatform():
    
    #come back to get in position for oil platform
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-317, left_motor=left_motor, right_motor=right_motor)

    #move rack left to get under pump
    mm_horizontal.on_for_degrees(65, 250, brake=True, block=True)

    #raise rack 3 times to pump fuel units into truck
    loop = 0
    while(loop < 3):
        mm_vertical.on_for_degrees(80, 1250, brake=True, block=True)
        sleep(0.1)
        mm_vertical.on_for_degrees(80, -1250, brake=True, block=True)   
        loop = loop + 1

    #Turn tight to align with the return home base
    pivot_gyro_turn(15, -15, 22, robot, gyro, bLeftTurn=False)

    # come back to base
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -75, target_angle=22, 
                    follow_for=my_follow_for_degrees, degrees=-950, left_motor=left_motor, right_motor=right_motor)
    #turn back to zero degrees gyro to return to base
    pivot_gyro_turn(-15, 15, 0, robot, gyro, bLeftTurn=True)
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -75, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-575, left_motor=left_motor, right_motor=right_motor)

def bringOilTruck():
    sleep(1)
    gyro.reset()
    robot.reset()
        
    #move rack right to get into base
    mm_horizontal.on_for_degrees(-65, -250, brake=True, block=True)

    mm_vertical.reset()
    mm_vertical.on_for_degrees(75, 1000, brake=True, block=True)
            
    # we are going forward till we reach oil truck while also resetting the rack
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=-10, 
                    follow_for=my_follow_for_degrees, degrees=800, left_motor=left_motor, right_motor=right_motor)
    
    #bring rack down to catch oil truck
    run_for_motor_stalled(mm_vertical, 10000, -65)              
    #come back to base while bringing truck
    robot.follow_gyro_angle(3, 0, 0, -75, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-690, left_motor=left_motor, right_motor=right_motor)



def setUpForRun3():
    # we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 65)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    #we reset mm_vertical
    mm_vertical.reset()

def run2():
    getOutOfBase()
    alignForEnergyStorage()
    doEnergyStorage()
    doOilPlatform()
    setUpForRun3()
    bringOilTruck()

readAllValues()
run2SelfSetup()
run2()
