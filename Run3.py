#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

def run3SelfStartUp():
    # we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 65)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    #we reset mm_vertical
    mm_vertical.reset()
def getOutOfBase():
    #we reset gyro
    gyro.reset()
    #we reset both motors
    robot.reset()
    #move rack to the right to avoid energy storage
    mm_horizontal.on_for_degrees(75, -475, brake=True, block=False)
    #gyro straight
    robot.cs = left_light
    robot.follow_gyro_angle(1.5, 0, 0, 45, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)
def alignWithSolarFarm():

    #turn right to approach solar farm
    pivot_gyro_turn(15, 0, 32, robot, gyro, bLeftTurn=False)

    #gyro straight to get in position for solar farm
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=32, 
                        follow_for=my_follow_for_degrees, degrees=870,
                        right_motor = right_motor, left_motor = left_motor)

    #we run mm_horizontal all the way to the left so we can collect solar units
    mm_horizontal.on_for_degrees(35, 300, brake=True, block=True)
def collectEnergyUnits():

    #turn to collect energy units from solar farm
    pivot_gyro_turn(20, 0, 75, robot, gyro, bLeftTurn=False)

    #gyro straight to collect the last solar unit (next to smart grid)
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=75, 
                        follow_for=my_follow_for_degrees, degrees=325,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to avoid smart grid and align to power to X
    pivot_gyro_turn(0, -20, 130, robot, gyro, bLeftTurn=False)
def dropToPX():
    #forward to get into PX
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=130, 
                        follow_for=my_follow_for_degrees, degrees=550,
                        right_motor = right_motor, left_motor = left_motor)

    #move rack to the right to bring units into PX
    mm_horizontal.on_for_degrees(-45, 400, brake=True, block=False)

    #turn to leave units in power to X
    pivot_gyro_turn(0, -20, 155, robot, gyro, bLeftTurn=False)

    #go back so that when we turn we are in alignment to approach smart grid
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=155, 
                        follow_for=my_follow_for_degrees, degrees=50,
                        right_motor = right_motor, left_motor = left_motor)
def alignToSmartGrid():
    #raise rack to avoid collision with smart grid lever
    mm_vertical.on_for_degrees(45, 500, brake=True, block=False)

    #get out of PX and go back until back sensor on white
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=155, 
                        follow_for=follow_until_back_white, lightSensor=back_light, range=10)

    #go back so that when we turn we are in alignment to approach smart grid
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=155, 
                        follow_for=my_follow_for_degrees, degrees=-150,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to align to smart grid
    pivot_gyro_turn(0, 20, 90, robot, gyro, bLeftTurn=True)

    #go forward till both front sensors are on white and then black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_white, lls=left_light, rls=right_light)
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)
def doSmartGrid():
    #move rack left to get in postition for Smart Grid
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()

    #Come back to grab lever
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=-75,
                        right_motor = right_motor, left_motor = left_motor)
    
    #Bring rack down to latch onto lever
    run_for_motor_stalled(mm_vertical, 10000, -65)
    mm_vertical.reset()

    #Pull lever to the right
    mm_horizontal.on_for_degrees(-35, 800, brake=True, block=True)
def doHybridCar():
    #raise rack to avoid collision with hybrid car
    mm_vertical.on_for_degrees(45, 250, brake=True, block=True)

    #go left to avoid toy factory
    mm_horizontal.on_for_degrees(45, 400, brake=True, block=False)

    #raise rack to avoid collision with hybrid car
    mm_vertical.on_for_degrees(45, 1025, brake=True, block=False)

    #Leave smart grid
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=400,
                        right_motor = right_motor, left_motor = left_motor)


    #go forward till both sensors are on white
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_white, lls=left_light, rls=right_light)

    #go forward till both sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)

    #go forward to get in postition for hybrid car
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=315,
                        right_motor = right_motor, left_motor = left_motor)
    
    #turn to get in position to align with hybrid car lever
    pivot_gyro_turn(0, -20, 135, robot, gyro, bLeftTurn=False)

    #go back to get in postition for hybrid car lever
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=135, 
                        follow_for=my_follow_for_degrees, degrees=-220,
                        right_motor = right_motor, left_motor = left_motor)
    
    #lower rack to push hybrid car lever
    mm_vertical.on_for_degrees(-60, 425, brake=True, block=True)

    sleep(1)

    #bring rack down to release hybrid car lever
    mm_vertical.on_for_degrees(-60, 775, brake=True, block=True)
def collectRB():
    #move rack to get RB
    mm_horizontal.on_for_degrees(-45, 150, brake=True, block=False)

    #go back to base
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 80, target_angle=145, 
                        follow_for=my_follow_for_degrees, degrees=1750,
                        right_motor = right_motor, left_motor = left_motor)
def setUpForRun4():
    # stall rack to the left
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()
def run3():
    logfile = logging.getLogger('')
    logfile.info('=====> run3 getOutOfBase start')
    getOutOfBase()
    logfile.info('=====> run3 getOutOfBase end')
    logfile.info('=====> alignWithSolarFarm start')
    alignWithSolarFarm()
    logfile.info('=====> alignWithSolarFarm end')
    logfile.info('=====> collectEnergyUnits start')
    collectEnergyUnits()
    logfile.info('=====> collectEnergyUnits end')
    logfile.info('=====> dropToPX start')
    dropToPX()
    logfile.info('=====> dropToPX end')
    logfile.info('=====> alignToSmartGrid start')
    alignToSmartGrid()
    logfile.info('=====> alignToSmartGrid end')
    logfile.info('=====> doSmartGrid start')
    doSmartGrid()
    logfile.info('=====> doSmartGrid end')
    logfile.info('=====> doHybridCar start')
    doHybridCar()
    logfile.info('=====> doHybridCar end')
    logfile.info('=====> collectRB start')
    collectRB()
    logfile.info('=====> collectRB end')