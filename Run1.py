#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

#start of code
def run1SelftStart():
    #we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 50)
    #we reset mm_horizontal
    mm_horizontal.reset()
    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -75)
    #we reset mm_vertical
    mm_vertical.reset()

def getOutOfBase():
    #we reset gyro
    gyro.reset()
    #we reset both motors
    robot.reset()
    #we move robot forward to the end of base area
    robot.follow_gyro_angle(1.5, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=500,
                    right_motor = right_motor, left_motor = left_motor)

    #we turn gyro to align with the hydroelectric dam 
    pivot_gyro_turn(0, 15, -39, robot, gyro, bLeftTurn=True)

def lift1WaterUnit():
    #moving to catch water units
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=205,
                right_motor = right_motor, left_motor = left_motor)

    #move to the right
    mm_horizontal.on_for_degrees(45, -700, brake=True, block=False)

    #lifting water unit up 
    mm_vertical.on_for_degrees(55, 1000, brake=True, block=True)

def hydroelectricDam():
    #going forward to align with the hydroelectric dam lever
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 25, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=230,
                right_motor = right_motor, left_motor = left_motor)

    #raising rack up to push lever
    mm_vertical.on_for_degrees(75, 1100, brake=True, block=True) 
    
def alignToPowerPlant():
    robot.reset()
    #starting to align to power plant
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=400,
                right_motor = right_motor, left_motor = left_motor)
    #pivoting to 0 so the robot can move forward and align to the black line
    pivot_gyro_turn(20, -20, 0, robot, gyro, bLeftTurn=False)
    #aligning one light sensor to black so we can move the other one in later and complete the power plant mission
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=0, 
            follow_for=follow_until_white, lightSensor=right_light)
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=0, 
            follow_for=follow_until_black, lightSensor=right_light)
    #moving vertical rack all the way up
    mm_vertical.on_for_degrees(35, 100, brake=True, block=False)
    #align robot to face to power plant  
    pivot_gyro_turn(15, 0, 90, robot, gyro, bLeftTurn=False)
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0,15, target_angle=90, 
            follow_for=follow_until_front_black, lls=left_light, rls=right_light)
    #coming backward to power plant mission
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -20, target_angle=90, 
            follow_for=my_follow_for_degrees, degrees=-87,
            right_motor = right_motor, left_motor = left_motor)
    #catching the power unit at the front 
    run_for_motor_stalled(mm_vertical, 10000, -85) 
    mm_vertical.reset() 

    run_for_motor_stalled(mm_horizontal, 10000, 60)
    mm_horizontal.reset() 
    #lifting up to release the last power unit
    mm_vertical.on_for_degrees(75, 2300, brake=True, block=True)
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 20, target_angle=90, 
            follow_for=my_follow_for_degrees, degrees=175,
            right_motor = right_motor, left_motor = left_motor)


def comeBackToBase():
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0,-90, target_angle=90, 
             follow_for=my_follow_for_degrees, degrees=-250,
             right_motor = right_motor, left_motor = left_motor)
    pivot_gyro_turn(35, 0, 155, robot, gyro, bLeftTurn=False)
    robot.reset()
    robot.on_for_degrees(95, 95, 1600, brake=True, block=True)
    # robot.follow_gyro_angle(1.5, 0, 0, 90, target_angle=155, 
    #         follow_for=my_follow_for_degrees, degrees=1600,
    #         right_motor = right_motor, left_motor = left_motor)

def setUpForRun2():
    # # bring rack down
    # run_for_motor_stalled(mm_vertical, 10000, -75)
    # mm_vertical.reset

    # # bring rack up
    # mm_vertical.on_for_degrees(65, 1800, brake=True, block=True)
    
    #move rack left
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

def run1():
    getOutOfBase()
    lift1WaterUnit()
    hydroelectricDam()
    alignToPowerPlant()
    comeBackToBase()
    setUpForRun2()

