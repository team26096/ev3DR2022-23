#!/usr/bin/env micropython

# add imports
from initialize import *


def toyFactory():

    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -50)

    # bring rack up
    mm_vertical.on_for_degrees(40, 2300, brake=True, block=True)
    mm_vertical.reset
    sleep(4)

    #add run 5 code here
    #we reset mm_horizontal
    gyro.reset()
    robot.reset()
    mm_horizontal.reset()

    # gyro straight to align with toy factory
    robot.reset()
    robot.on_for_degrees(30, 30, 750)

    # turn right to align better with toy factory
    pivot_gyro_turn(15, 0, 48, robot, gyro, bLeftTurn=False)

    # gyro straight to align with toy factory
    robot.reset()
    robot.on_for_degrees(30, 30, 200)

    # move rack down a little bit
    robot.reset()
    mm_vertical.on_for_degrees(25, -750, brake=True, block=True)
    sleep(1)

    # pivot gyro back to 0
    pivot_gyro_turn(-35, 0, 0, robot, gyro, bLeftTurn=True)

def dinoToy():

    # go back to base and finish run!
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 60, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=2600,
                            left_motor = left_motor, right_motor = right_motor)

def run5():
    toyFactory()
    dinoToy()
