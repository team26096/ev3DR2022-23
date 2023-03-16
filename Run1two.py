#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

#start of code
def run1SelftStart():
    #we run mm_horizontal all the way to the left 
    #run_for_motor_stalled(mm_horizontal, 10000, 15)
    #we reset mm_horizontal
    mm_horizontal.reset()
    #we run mm_vertical all the way down
    #run_for_motor_stalled(mm_vertical, 10000, -15)
    #we reset mm_vertical
    mm_vertical.reset()

def getOutOfBase():
    #we reset gyro
    gyro.reset()
    #we reset both motors
    robot.reset()
    #we move robot forward to the end of base area
    robot.follow_gyro_angle(1.5, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=450,
                    right_motor = right_motor, left_motor = left_motor)

    #we turn gyro to align with the hydroelectric dam 
    pivot_gyro_turn(0, 15, -39, robot, gyro, bLeftTurn=True)

def lift1WaterUnit():
    #moving to catch water units
    robot.reset()
    robot.on_for_degrees(25, 25, 200, brake=False, block=True)
    # robot.follow_gyro_angle(1.5, 0, 0, 25, target_angle=-39, 
    #             follow_for=my_follow_for_degrees, degrees=200,
    #             right_motor = right_motor, left_motor = left_motor)

   #lifting water unit up 
    #mm_vertical.on_for_degrees(55, 900, brake=True, block=False)
    mm_vertical.on_for_degrees(55, 850, brake=True, block=True)
   
    #move to the right
    mm_horizontal.on_for_degrees(45, -580, brake=True, block=True)


def hydroelectricDam():
    #going forward to align with the hydroelectric dam lever
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 15, target_angle=-39, 
               follow_for=my_follow_for_degrees, degrees=270,
               right_motor = right_motor, left_motor = left_motor)
    
    #raising rack up to push lever
    #mm_vertical.on_for_degrees(75, 1100, brake=True, block=True)
    mm_vertical.on_for_degrees(75, 400, brake=True, block=True)
    
    #Bring rack down to release lever
    #mm_vertical.on_for_degrees(-75, 800, brake=True, block=True)
    mm_vertical.on_for_degrees(-75, 250, brake=True, block=True)

def dropWaterUnit1():
    #Go forward to align to Water Reservoir circle
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 15, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=250,
                right_motor = right_motor, left_motor = left_motor)

    #Move rack left to leave unit in circle
    run_for_motor_stalled(mm_horizontal, 10000, 50)
    mm_horizontal.reset()

    #Bring rack down in order to drop unit in circle
    mm_vertical.on_for_degrees(-75, 600, brake=True, block=True)

    #Move back to release unit in circle
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -35, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=-125,
                right_motor = right_motor, left_motor = left_motor)

    #Move rack right to leave unit in circle
    mm_horizontal.on_for_degrees(45, -100, brake=True, block=True)

    #Pivot turn to gyro -18
    pivot_gyro_turn(0, -20, -17, robot, gyro, bLeftTurn=False)

def newAlign():
    # move rack in position for power plant
    mm_horizontal.on_for_degrees(45, 100, brake=True, block=False)

    # moving vertical rack up to get ready to lift lever
    mm_vertical.on_for_degrees(75, 570, brake=True, block=False)

    #aligning one light sensor to black so we can move the other one in later and complete the power plant mission
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 45, target_angle=-17, 
            follow_for=follow_until_white, lightSensor=right_light)
    robot.follow_gyro_angle(1.5, 0, 0, 45, target_angle=-17, 
            follow_for=follow_until_black, lightSensor=right_light)
    robot.follow_gyro_angle(1.5, 0, 0, 45, target_angle=-17, 
            follow_for=follow_until_white, lightSensor=right_light)

    #align robot to face to power plant
    pivot_gyro_turn(10, -10, 85, robot, gyro, bLeftTurn=False)

    # move forward for both light sensors on black
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 20, target_angle=90, 
            follow_for=follow_until_front_black, lls=left_light, rls=right_light)
            
    # move back 100 degrees to align for middle unit
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -15, target_angle=90, 
            follow_for=my_follow_for_degrees, degrees=-90,
            right_motor = right_motor, left_motor = left_motor)

    # stall rack down to get units out
    run_for_motor_stalled(mm_vertical, 10000, -75)

    #we reset mm_vertical
    mm_vertical.reset()


def comeBackToBase():
    # move backwards 250 degrees to avoid hitting powerplant
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0,-90, target_angle=90, 
             follow_for=my_follow_for_degrees, degrees=-150,
             right_motor = right_motor, left_motor = left_motor)

    # pivot turn to align with base
    pivot_gyro_turn(35, 0, 148, robot, gyro, bLeftTurn=False)
    
    # come back to base
    robot.reset()
    robot.on_for_degrees(95, 95, 1600, brake=True, block=True)

def setUpForRun2():
    #move rack left
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

def run1two():
    run1SelftStart()
    getOutOfBase()
    lift1WaterUnit()
    hydroelectricDam()
    dropWaterUnit1()
    newAlign()
    # alignToPowerPlant()
    comeBackToBase()
    # setUpForRun2()

readAllValues()
# run1SelftStart()
run1two()

