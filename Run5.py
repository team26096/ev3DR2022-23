#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

def run5SelfSetup():
    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    mm_vertical.reset()
    run_for_motor_stalled(mm_horizontal, 10000, 65)
    mm_horizontal.reset()
    # bring rack right and up
    mm_horizontal.on_for_degrees(75, -400, brake=True, block=False)
    mm_vertical.on_for_degrees(75, 1140, brake=True, block=True)
def toyFactory():
    #add run 5 code here
    gyro.reset()
    robot.reset()

    # gyro straight to align with toy factory
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 50, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=1000,
                            left_motor = left_motor, right_motor = right_motor)

    # turn right to align better with toy factory
    pivot_gyro_turn(25, 0, 90, robot, gyro, bLeftTurn=False)

    # gyro straight to align with toy factory
    robot.reset()
    robot.on_for_degrees(20, 20, 110)

    # move rack down a little bit
    mm_vertical.on_for_degrees(75, -850, brake=True, block=True)
    sleep(0.4)

    # pivot gyro back to 0
    pivot_gyro_turn(-35, 0, 15, robot, gyro, bLeftTurn=True)
def dinoToy():
    # go back to base and finish run!
    robot.reset()
    robot.on_for_degrees(95, 95, 2575)
def run5():
    logfile = logging.getLogger('')
    logfile.info('=====> run 5 toyFactory start')
    toyFactory()
    logfile.info('=====> run 5 toyFactory end')
    logfile.info('=====> run 5 dinoToy start')
    dinoToy()
    logfile.info('=====> run 5 dinoToy end')