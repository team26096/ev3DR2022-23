#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

#add run 4 code here
def run4SelfStartUp():
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

def recharableBattery():
    gyro.reset()

    # gyro straight to align with rechargeable battery
    robot.reset() 
    mdiff.follow_gyro_angle(4, 0, 0, 35, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=620,
                                left_motor = left_motor, right_motor = right_motor)

    # move horizontal rack left to drop battery units in rechargeable battery space.
    mm_horizontal.on_for_degrees(50, 750, brake=True, block=True)
    
    # turn into rechargeable battery to push energy units fully in
    pivot_gyro_turn(0, 15, -10, robot, gyro, bLeftTurn=True)

def watchTelevison():
    # bring rack back to position and right for watch tv
    mm_horizontal.on_for_degrees(50, -750, brake=True, block=True)

    # turn back from watch tv
    pivot_gyro_turn(15, 0, 5, robot, gyro, bLeftTurn=False)

    # gyro staight to complete watch television
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=325,
                                left_motor = left_motor, right_motor = right_motor)

def windTurbine():
    # gyro staight backwards to align with wind turbine ***200
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, -25, target_angle=45, 
                                follow_for=my_follow_for_degrees, degrees=-100,
                                left_motor = left_motor, right_motor = right_motor)

    # bring rack down for wind turbine
    mm_vertical.on_for_degrees(75, -1900, brake=True, block=True)

    # loop for going back and forth ***70
    loop = 0
    while(loop < 4):
        mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=45, 
                            follow_for=my_follow_for_degrees, degrees=80,
                            left_motor = left_motor, right_motor = right_motor)
        sleep(0.4)
        mdiff.follow_gyro_angle(4, 0, 0, -30, target_angle=45, 
                            follow_for=my_follow_for_degrees, degrees=-80,
                            left_motor = left_motor, right_motor = right_motor)
        loop = loop + 1

    # pivot gyro to base
    pivot_gyro_turn(-15, 15, -15, robot, gyro, bLeftTurn=True)

    # backward gyro straight back to base
    mdiff.follow_gyro_angle(4, 0, 0, -75, target_angle=-15, 
                            follow_for=my_follow_for_degrees, degrees=-1350,
                            left_motor = left_motor, right_motor = right_motor)


def alignForWindTurbine():
    # move horizontal rack to the left to avoid wind turbine mission
    mm_horizontal.on_for_degrees(50, 750, brake=True, block=True)


    # lifting rack up to avoid hitting wind turbine
    mm_vertical.on_for_degrees(75, 1900, brake=True, block=True)

    # move forward to ensure reliablity
    mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=200,
                            left_motor = left_motor, right_motor = right_motor)

    # move forward to until left light sees black line
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_right_white, lightSensor = right_light)
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_right_black, lightSensor = right_light)

    # move forward to align with wind turbine
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=50,
                            left_motor = left_motor, right_motor = right_motor)
    
    # move turn to align with wind turbine
    pivot_gyro_turn(15, -15, 45, robot, gyro, bLeftTurn=False)

def setUpForRun5():
    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

    # bring rack up
    mm_vertical.on_for_degrees(35, 1900, brake=True, block=True)

def run4(): 
    recharableBattery()
    watchTelevison()
    alignForWindTurbine()
    windTurbine()
    setUpForRun5()

readAllValues()
run4SelfStartUp()
run4()