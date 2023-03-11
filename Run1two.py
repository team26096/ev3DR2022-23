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
                    follow_for=my_follow_for_degrees, degrees=450,
                    right_motor = right_motor, left_motor = left_motor)

    #we turn gyro to align with the hydroelectric dam 
    pivot_gyro_turn(0, 15, -38, robot, gyro, bLeftTurn=True)

def lift1WaterUnit():
    #moving to catch water units
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-38, 
                follow_for=my_follow_for_degrees, degrees=205,
                right_motor = right_motor, left_motor = left_motor)

   #lifting water unit up 
    mm_vertical.on_for_degrees(55, 900, brake=True, block=True)
   
    #move to the right
    mm_horizontal.on_for_degrees(45, -600, brake=True, block=True)


def hydroelectricDam():
    #going forward to align with the hydroelectric dam lever
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 25, target_angle=-38, 
                follow_for=my_follow_for_degrees, degrees=250,
                right_motor = right_motor, left_motor = left_motor)

    #raising rack up to push lever
    mm_vertical.on_for_degrees(75, 1100, brake=True, block=True) 
    
    #Bring rack down to release lever
    mm_vertical.on_for_degrees(-75, 800, brake=True, block=True) 

def dropWaterUnit1():
    robot.reset()
    #Go forward to align to Water Reservoir circle
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-38, 
                follow_for=my_follow_for_degrees, degrees=305,
                right_motor = right_motor, left_motor = left_motor)
    
    #Move rack left to leave unit in circle
    #mm_horizontal.on_for_degrees(45, 800, brake=True, block=True)
    run_for_motor_stalled(mm_horizontal, 10000, 50)
    mm_horizontal.reset()

    #Bring rack down in order to drop unit in circle
    run_for_motor_stalled(mm_vertical, 10000, -75)

    #we reset mm_vertical
    mm_vertical.reset()

    #Move back to release unit in circle
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -35, target_angle=-38, 
                follow_for=my_follow_for_degrees, degrees=-125,
                right_motor = right_motor, left_motor = left_motor)

    #Move rack right to leave unit in circle
    mm_horizontal.on_for_degrees(45, -100, brake=True, block=True)

    #Pivot turn to gyro -15
    pivot_gyro_turn(0, -15, -15, robot, gyro, bLeftTurn=False)

def alignToPowerPlant():
    robot.reset()
    #aligning one light sensor to black so we can move the other one in later and complete the power plant mission
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-15, 
            follow_for=follow_until_white, lightSensor=right_light)
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-15, 
            follow_for=follow_until_black, lightSensor=right_light)

    #align robot to face to power plant
    pivot_gyro_turn(15, 0, 90, robot, gyro, bLeftTurn=False)

    #moving vertical rack all the way up
    mm_vertical.on_for_degrees(75, 2200, brake=True, block=True)

    # move rack to the right
    run_for_motor_stalled(mm_horizontal, 10000, -65)
    mm_horizontal.reset()

    # move forward for both light sensors on black
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0,15, target_angle=90, 
            follow_for=follow_until_front_black, lls=left_light, rls=right_light)

    #coming backward to power plant mission
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -20, target_angle=90, 
            follow_for=my_follow_for_degrees, degrees=-100,
            right_motor = right_motor, left_motor = left_motor)

    #moving vertical rack halfway down to get ready to lift lever up
    mm_vertical.on_for_degrees(75, -1200, brake=True, block=True)

    # move rack to the left to have beam pick lever up
    run_for_motor_stalled(mm_horizontal, 10000, 60)
    mm_horizontal.reset()

    #lifting up to release the energy units
    mm_vertical.on_for_degrees(75, 1000, brake=True, block=True)
    robot.reset()

    # move forward 175 to fully push lever to the back
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 20, target_angle=90, 
            follow_for=my_follow_for_degrees, degrees=160,
            right_motor = right_motor, left_motor = left_motor)

    # move rack to the right to avoid hitting the orange ramp
    mm_horizontal.on_for_degrees(45, -450, brake=True, block=False)

    # move back 175 degrees to align for middle unit
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -20, target_angle=90, 
            follow_for=my_follow_for_degrees, degrees=-125,
            right_motor = right_motor, left_motor = left_motor)

    # stall rack down to get units out
    run_for_motor_stalled(mm_vertical, 10000, -75)


def comeBackToBase():
    # move backwards 250 degrees to avoid hitting powerplant
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0,-90, target_angle=90, 
             follow_for=my_follow_for_degrees, degrees=-250,
             right_motor = right_motor, left_motor = left_motor)

    # pivot turn to align with base
    pivot_gyro_turn(35, 0, 148, robot, gyro, bLeftTurn=False)
    
    # come back to base
    robot.reset()
    robot.on_for_degrees(95, 95, 1600, brake=True, block=True)

def setUpForRun2():
    # # bring rack down
    # run_for_motor_stalled(mm_vertical, 10000, -75)
    # mm_vertical.reset

    # # bring rack up
    # mm_vertical.on_for_degrees(65, 1800, brake=True, block=True)
    
    #move rack left
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

def run1two():
    getOutOfBase()
    lift1WaterUnit()
    hydroelectricDam()
    dropWaterUnit1()
    alignToPowerPlant()
    comeBackToBase()
    # setUpForRun2()

readAllValues()
# run1SelftStart()
run1two()

