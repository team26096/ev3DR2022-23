#!/usr/bin/env micropython

# add imports
from initialize import *

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
    #we move robot forward to the end of base area
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=500,
                    right_motor = right_motor, left_motor = left_motor)

    #we turn gyro to align with the hydroelectric dam 
    pivot_gyro_turn(0, 10, -39, robot, gyro, bLeftTurn=True)

def lift1WaterUnit():
    #moving to catch water units
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=205,
                right_motor = right_motor, left_motor = left_motor)

    #move to the right
    mm_horizontal.on_for_degrees(35, -700, brake=True, block=True)

    #lifting water unit up 
    mm_vertical.on_for_degrees(35, 1000, brake=True, block=True)

def hydroelectricDam():
    #going forward to align with the hydroelectric dam lever
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=250,
                right_motor = right_motor, left_motor = left_motor)

    #raising rack up to push lever
    mm_vertical.on_for_degrees(35, 1100, brake=True, block=True)
    sleep(0.25)
    #going a little down
    mm_vertical.on_for_degrees(35, -900, brake=True, block=True)

def waterReservoirUnit1():
    robot.reset()
    #going forward to water reservoir
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=-39, 
                        follow_for=my_follow_for_degrees, degrees=275,
                        right_motor = right_motor, left_motor = left_motor)

    #moving water unit above reservoir
    mm_horizontal.on_for_degrees(35, 600, brake=True, block=True)

    #moving vertical all the way down
    mm_vertical.on_for_degrees(35, -650, brake=True, block=True)
    robot.reset()
    #going back to release the water unit into the reservoir
    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=-75,
                right_motor = right_motor, left_motor = left_motor)
    #resetting mm_horizontal
    mm_horizontal.reset()
    
    #moving rack to the right
    mm_horizontal.on_for_degrees(35, -600, brake=True, block=True)

def collectWaterUnits():
    robot.reset()
    #going forward to align with other water units
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=-39, 
                follow_for=my_follow_for_degrees, degrees=600,
                right_motor = right_motor, left_motor = left_motor)
    #moving to left to release water units
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    #resetting mm_horizontal
    mm_horizontal.reset()
    #preparing to collect the last two water unit
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

    #this code is to go backwards and collect the 2 units
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=0, 
            follow_for=my_follow_for_degrees, degrees=-350,
            right_motor = right_motor, left_motor = left_motor)
    #lift the rack up to get our water units into the reservoir
    mm_vertical.on_for_degrees(35, 1500, brake=True, block=True)

    #coming 300 backwards to align with the water reservoir hook
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0,-15, target_angle=0, 
                follow_for=my_follow_for_degrees, degrees=-150,
                right_motor = right_motor, left_motor = left_motor)
    #bringing rack down to hang the water units
    mm_vertical.on_for_degrees(35, -1300, brake=True, block=True)
    #go forward to release the water units
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0,15, target_angle=0, 
                follow_for=my_follow_for_degrees, degrees=125,
                right_motor = right_motor, left_motor = left_motor)
    #bring horizontal rack to the right
    run_for_motor_stalled(mm_horizontal, 10000, -35)

def dropInnovationProject():
    robot.follow_gyro_angle(3, 0, 0,15, target_angle=-39, 
            follow_for=my_follow_for_degrees, degrees=400,
            right_motor = right_motor, left_motor = left_motor)
    

def alignToPowerPlant():
    gyro.reset()
    #turning to align with the line in front of the power plant mission
    pivot_gyro_turn(10, 0, 50, robot, gyro, bLeftTurn=False)
    #squaring to the line in front of the power plant mission
    squareToBlack(15, left_light, right_light, left_motor, right_motor)
    #gyro straight until the back sensor hits black
    gyro.reset()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=0, 
                follow_for=follow_until_black, lightSensor=back_light)
    pivot_turn_until_black(-5, -15, 7, robot, right_light)

def run1():
    getOutOfBase()
    lift1WaterUnit()
    hydroelectricDam()
    waterReservoirUnit1()
    dropInnovationProject()
    #collectWaterUnits()
    # alignToPowerPlant()
