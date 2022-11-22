#!/usr/bin/env micropython

# add imports
from initialize import *

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
    mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=620,
                                left_motor = left_motor, right_motor = right_motor)

    # move horizontal rack left to drop battery units in rechargeable battery space.
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    
    # turn into rechargeable battery to push energy units fully in
    pivot_gyro_turn(0, 15, -10, robot, gyro, bLeftTurn=True)

def watchTelevison():
    # bring rack back to position and right for watch tv
    run_for_motor_stalled(mm_horizontal, 10000, -30)
    mm_horizontal.reset()

    # turn back for watch tv
    pivot_gyro_turn(15, 0, 5, robot, gyro, bLeftTurn=False)

    # gyro staight to complete watch television
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=290,
                                left_motor = left_motor, right_motor = right_motor)

def oilPlatform():
    # move horizontal rack to the left to avoid wind turbine mission
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

    # lifting rack up to avoid hitting wind turbine
    mm_vertical.on_for_degrees(35, 1500, brake=True, block=True)

    # move forward to until left light sees black line
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_white, lightSensor = right_light)
    s.beep()
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_black, lightSensor = right_light)
    s.beep()

    # turn left to align with oil platform 
    # pivot_gyro_turn(0, 20, -25, robot, gyro, bLeftTurn=True)

    # gyro staight to complete oil platform
    # gyro.reset()
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 30, target_angle=-35, 
                                follow_for=my_follow_for_degrees, degrees=290,
                                left_motor = left_motor, right_motor = right_motor)

    # lifting rack up to release truck
    mm_vertical.on_for_degrees(35, 850, brake=True, block=True)

    # gyro staight backwards to realse the truck
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, -15, target_angle=-35, 
                                follow_for=follow_until_black, lightSensor = right_light)
    s.beep()

def windTurbine():
    # turn to align front with wind turbine
    # pivot_gyro_turn(15, -15, 47, robot, gyro, bLeftTurn=False)

    # gyro staight backwards to align with wind turbine
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, -15, target_angle=47, 
                                follow_for=my_follow_for_degrees, degrees=-200,
                                left_motor = left_motor, right_motor = right_motor)

    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -50)
    mm_vertical.reset()

    # loop for going back and forth
    loop = 0
    while(loop < 4):
        mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=47, 
                            follow_for=my_follow_for_degrees, degrees=70,
                            left_motor = left_motor, right_motor = right_motor)
        sleep(0.3)
        mdiff.follow_gyro_angle(4, 0, 0, -20, target_angle=47, 
                            follow_for=my_follow_for_degrees, degrees=-70,
                            left_motor = left_motor, right_motor = right_motor)
        sleep(0.3)
        loop = loop + 1
    s.beep()

    # pivot gyro to base
    pivot_gyro_turn(-15, 15, -15, robot, gyro, bLeftTurn=True)

    # backward gyro straight back to base
    mdiff.follow_gyro_angle(4, 0, 0, -50, target_angle=-15, 
                            follow_for=my_follow_for_degrees, degrees=-1300,
                            left_motor = left_motor, right_motor = right_motor)
    
    # sleep for run 5 and put rack up for run 5
    sleep(2)
    mm_vertical.on_for_degrees(35, 2300, brake=True, block=True)

def alignForWindTurbine():
    # move horizontal rack to the left to avoid wind turbine mission
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

    # lifting rack up to avoid hitting wind turbine
    mm_vertical.on_for_degrees(35, 1000, brake=True, block=True)

    # move forward to ensure reliablity
    mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=200,
                            left_motor = left_motor, right_motor = right_motor)

    # move forward to until left light sees black line

    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_white, lightSensor = right_light)
    s.beep()
    mdiff.follow_gyro_angle(4, 0, 0, 20, target_angle=0, 
                                follow_for=follow_until_black, lightSensor = right_light)
    s.beep()

    # move forward to align with wind turbine
    robot.reset()
    mdiff.follow_gyro_angle(4, 0, 0, 25, target_angle=0, 
                            follow_for=my_follow_for_degrees, degrees=100,
                            left_motor = left_motor, right_motor = right_motor)
    s.beep()

    # move turn to align with wind turbine
    pivot_gyro_turn(15, -15, 46, robot, gyro, bLeftTurn=False)


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
