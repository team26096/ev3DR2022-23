#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

#add run 4 code here
def run4SelfStartUp():
    # stall rack to the left
    run_for_motor_stalled(mm_horizontal, 10000, -65)
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    mm_vertical.reset()

def recharableBattery():
    gyro.reset()

    # move horizontal rack left to drop battery units in rechargeable battery space.
    mm_horizontal.on_for_degrees(75, 750, brake=True, block=False)

    # gyro straight to align with rechargeable battery
    robot.reset() 
    robot.follow_gyro_angle(1.5, 0, 0, 45, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=635,
                                left_motor = left_motor, right_motor = right_motor)
    
    # turn left into rechargeable battery to push energy units fully in
    pivot_gyro_turn(0, 20, -20, robot, gyro, bLeftTurn=True)

    # go forward to get units completely in target area
    robot.reset() 
    robot.follow_gyro_angle(1.5, 0, 0, 40, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=40,
                                left_motor = left_motor, right_motor = right_motor)

def watchTelevison():
    # bring rack back to position and right for recharable battery
    mm_horizontal.on_for_degrees(75, -500, brake=True, block=False)

    # turn right back from recharable battery
    pivot_gyro_turn(0, -20, 0, robot, gyro, bLeftTurn=False)

    # bring rack back to position and right for recharable battery
    mm_horizontal.on_for_degrees(75, -250, brake=True, block=True)

    # gyro staight to complete watch television
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 20, target_angle=0, 
                                follow_for=my_follow_for_degrees, degrees=320,
                                left_motor = left_motor, right_motor = right_motor)

def fuelTruck():
    # lifting rack up to avoid hitting wind turbine
    # mm_vertical.on_for_degrees(75, 700, brake=True, block=True)
    mm_vertical.on_for_degrees(75, 420, brake=True, block=False)

    # move horizontal rack to the left to avoid watch televsion mission
    mm_horizontal.on_for_degrees(75, 800, brake=True, block=True)

    # move forward to until right light sees black line
    robot.follow_gyro_angle(3, 0, 0, 40, target_angle=-5, 
                                follow_for=follow_until_right_white, lightSensor = right_light)
    snd.beep()
    robot.follow_gyro_angle(3, 0, 0, 40, target_angle=-5, 
                                follow_for=follow_until_right_black, lightSensor = right_light)
    snd.beep()

    # turn so we do not hit wind turbine
    pivot_gyro_turn(0, 20, -25, robot, gyro, bLeftTurn=True)

    # move forward to get truck in circle
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=-25, 
                                follow_for=my_follow_for_degrees, degrees=175,
                                left_motor = left_motor, right_motor = right_motor)
    
    # lifting rack up to avoid bring back truck with us
    #mm_vertical.on_for_degrees(75, 1500, brake=True, block=True)
    mm_vertical.on_for_degrees(75, 900, brake=True, block=True)
    #sleep(1)

    # move backwards to until right light sees white line
    robot.follow_gyro_angle(3, 0, 0, -20, target_angle=-5, 
                                follow_for=follow_until_right_white, lightSensor = right_light)
    snd.beep()
    # robot.follow_gyro_angle(3, 0, 0, -20, target_angle=-5, 
    #                             follow_for=follow_until_right_black, lightSensor = right_light)
    # snd.beep()

    # move turn to align with wind turbine
    pivot_gyro_turn(20, -20, 45, robot, gyro, bLeftTurn=False)

def windTurbine():
    # bring rack down for wind turbine
    #mm_vertical.on_for_degrees(75, -1000, brake=True, block=False)
    mm_vertical.on_for_degrees(75, -600, brake=True, block=False)

    # gyro staight backwards to align with wind turbine ***200
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=45, 
                                follow_for=my_follow_for_degrees, degrees=-120,
                                left_motor = left_motor, right_motor = right_motor)
    
    # bring rack down for wind turbine
    #mm_vertical.on_for_degrees(75, -1200, brake=True, block=True)
    mm_vertical.on_for_degrees(75, -720, brake=True, block=True)

    # loop for going back and forth
    # robot.reset()
    # robot.follow_gyro_angle(3, 0, 0, 45, target_angle=35, 
    #                     follow_for=my_follow_for_degrees, degrees=210,
    #                     left_motor = left_motor, right_motor = right_motor)
    # sleep(0.5)
    loop = 0
    while(loop < 4):
        forwardDegrees = 210 + (loop * 15)
        robot.reset()
        robot.follow_gyro_angle(3, 0, 0, 45, target_angle=45, 
                            follow_for=my_follow_for_degrees, degrees=forwardDegrees,
                            left_motor = left_motor, right_motor = right_motor)
        sleep(0.5)
        robot.reset()
        robot.follow_gyro_angle(3, 0, 0, -45, target_angle=45, 
                            follow_for=my_follow_for_degrees, degrees=-180,
                            left_motor = left_motor, right_motor = right_motor)
        loop = loop + 1

    # robot.reset()
    # robot.follow_gyro_angle(3, 0, 0, -45, target_angle=35, 
    #                     follow_for=my_follow_for_degrees, degrees=-120,
    #                     left_motor = left_motor, right_motor = right_motor)

    # pivot gyro to base
    pivot_gyro_turn(-20, 20, -10, robot, gyro, bLeftTurn=True)

    # bring rack to the right to avoid hitting energy units in rechargeable battery
    mm_horizontal.on_for_degrees(50, -75, brake=True, block=False)

    # backward gyro straight back to base
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -75, target_angle=-10, 
                            follow_for=my_follow_for_degrees, degrees=-1250,
                            left_motor = left_motor, right_motor = right_motor)

    # turn to make transition from run 4 to 5 easier
    pivot_gyro_turn(-20, 20, -80, robot, gyro, bLeftTurn=True)

def setUpForRun5():
    # bring rack down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    mm_vertical.reset()

    # bring rack up
    # mm_vertical.on_for_degrees(75, 1900, brake=True, block=True)
    mm_vertical.on_for_degrees(75, 1140, brake=True, block=True)

def run4two(): 
    recharableBattery()
    watchTelevison()
    fuelTruck()
    windTurbine()
    #setUpForRun5()