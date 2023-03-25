#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

def run5SelfSetup():
    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    mm_vertical.reset()
    # bring rack up
    mm_vertical.on_for_degrees(75, 1140, brake=True, block=True)

def toyFactory():
    #add run 5 code here
    gyro.reset()
    robot.reset()

    # gyro straight to align with toy factory
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 45, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=1000,
                            left_motor = left_motor, right_motor = right_motor)

    # turn right to align better with toy factory
    pivot_gyro_turn(25, 0, 90, robot, gyro, bLeftTurn=False)

    # gyro straight to align with toy factory
    robot.reset()
    robot.on_for_degrees(20, 20, 80)

    # move rack down a little bit
    mm_vertical.on_for_degrees(75, -950, brake=True, block=True)
    sleep(0.4)

    # pivot gyro back to 0
    pivot_gyro_turn(-35, 0, 15, robot, gyro, bLeftTurn=True)

def dinoToy():

    # go back to base and finish run!
    robot.reset()
    robot.on_for_degrees(95, 95, 2500)
    # robot.follow_gyro_angle(3, 0, 0, 85, target_angle=0, 
    #                        follow_for=my_follow_for_degrees, degrees=2500,
    #                        left_motor = left_motor, right_motor = right_motor)

def run5():
    toyFactory()
    dinoToy()