#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

def run5SelfSetup():
    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

    # bring rack up
    mm_vertical.on_for_degrees(35, 1900, brake=True, block=True)
    sleep(4)

def toyFactory():
    #add run 5 code here
    #we reset mm_horizontal
    gyro.reset()
    robot.reset()
    mm_horizontal.reset()

    # gyro straight to align with toy factory
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 35, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=1000,
                            left_motor = left_motor, right_motor = right_motor)

    # turn right to align better with toy factory
    pivot_gyro_turn(15, 0, 90, robot, gyro, bLeftTurn=False)

    # gyro straight to align with toy factory
    # robot.reset()
    # robot.on_for_degrees(20, 20, 50)

    # move rack down a little bit
    mm_vertical.on_for_degrees(30, -950, brake=True, block=True)
    sleep(1)

    # pivot gyro back to 0
    pivot_gyro_turn(-20, 20, 0, robot, gyro, bLeftTurn=True)

def dinoToy():

    # go back to base and finish run!
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 60, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=2500,
                            left_motor = left_motor, right_motor = right_motor)

def run5():
    toyFactory()
    dinoToy()

