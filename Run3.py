#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

#start of code
def run3SelfStartUp():
    # we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 25)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -25)
    #we reset mm_vertical
    mm_vertical.reset()

def getOutOfBase():
    #we reset gyro
    gyro.reset()
    #we reset both motors
    robot.reset()
    #gyro straight
    robot.cs = left_light
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)

def alignWithSolarFarm():

    #move rack to the right to avoid energy storage
    mm_horizontal.on_for_degrees(75, -450, brake=True, block=True)

    #turn right to approach solar farm
    pivot_gyro_turn(15, 0, 32, robot, gyro, bLeftTurn=False)

    #gyro straight to get in position for solar farm
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=32, 
                        follow_for=my_follow_for_degrees, degrees=870,
                        right_motor = right_motor, left_motor = left_motor)

    #we run mm_horizontal all the way to the left so we can collect solar units
    mm_horizontal.on_for_degrees(35, 350, brake=True, block=True)

def collectEnergyUnits():

    #turn to collect energy units from solar farm
    pivot_gyro_turn(20, 0, 75, robot, gyro, bLeftTurn=False)

    #gyro straight to collect the last solar unit (next to smart grid)
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=75, 
                        follow_for=my_follow_for_degrees, degrees=325,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to avoid smart grid and align to power to X
    pivot_gyro_turn(0, -20, 122, robot, gyro, bLeftTurn=False)


def dropUnitstoPX():
    #raising rack to avoid water reservoir
    mm_vertical.on_for_degrees(75, 200, brake=True, block=False)

    #gyro straight into power to X to drop energy units
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 40, target_angle=122, 
                        follow_for=my_follow_for_degrees, degrees=650,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to drop energy units into power to X
    pivot_gyro_turn(0, -20, 230, robot, gyro, bLeftTurn=False)
         
    #leave energy units in power to X and avoid water resorvior
    mm_vertical.on_for_degrees(75, 1000, brake=True, block=True)

    #go back to align to leave power to X
    robot.reset()
    robot.on_for_degrees(-25, -25, 270, brake=True, block=True)
    
    #turn until back light is on black
    forward_turn_until_black(back_light, robot, bLeftTurn=False)

def alignForSmartGrid():
    #starts line following with back sensor to smart grid
    robot.reset()
    robot.cs = back_light
    #line follow backward until left light is on black
    robot.follow_line(-1.2, 0, 0, -15, target_light_intensity=48,
                    follow_left_edge=True,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=follow_until_black, lightSensor=left_light)
    robot.follow_line(-1.2, 0, 0, -15, target_light_intensity=48,
                    follow_left_edge=True,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=follow_for_ms, ms=1500)

def doSmartGrid():
    #move horizontal rack to the right to hook to lever on smart grid
    mm_horizontal.reset()
    mm_horizontal.on_for_degrees(75, -800, brake=True, block=True)

    #we run mm_vertical all the way down to grab lever for smart grid
    run_for_motor_stalled(mm_vertical, 10000, -75)
    mm_vertical.reset()

    #move horizontal rack left and pull smart grid
    run_for_motor_stalled(mm_horizontal, 10000, 25)
    mm_horizontal.reset()

def hybridCar():
    #raising rack detach smart grid
    mm_vertical.on_for_degrees(75, 300, brake=True, block=True)

    # move back a bit
    robot.on_for_degrees(-25, -25, 40, brake=True, block=True)

    # pivot gyro turn to align with hybrid car
    pivot_gyro_turn(-20, 20, 235, robot, gyro, bLeftTurn=True)

    # move back a bit to align with hybrid car lever
    robot.on_for_degrees(-25, -25, 60, brake=True, block=True)

    # move rack down to move lever up.
    run_for_motor_stalled(mm_vertical, 10000, -75)


def collectRB():
    #raising rack all the way to detach smart grid & hybrid car
    mm_vertical.on_for_degrees(75, 1000, brake=True, block=True)

    #move rack to the right to avoid toy factory
    mm_horizontal.on_for_degrees(75, -600, brake=True, block=True)

    #go back to head to base and collect RB
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=270, 
                        follow_for=my_follow_for_degrees, degrees=-500,
                        right_motor = right_motor, left_motor = left_motor)

    #turning to align robot to base and pick up RB
    pivot_gyro_turn(0, -20, 315, robot, gyro, bLeftTurn=False)

    #go backward to collect RB
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=315, 
                        follow_for=my_follow_for_degrees, degrees=-150,
                        right_motor = right_motor, left_motor = left_motor)

    
    #final go back to base and grab RB
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -85, target_angle=315, 
                        follow_for=my_follow_for_degrees, degrees=-1500,
                        right_motor = right_motor, left_motor = left_motor)

def setUpForRun4():
    # stall rack to the left
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

def run3():
    getOutOfBase()
    alignWithSolarFarm()
    collectEnergyUnits()
    dropUnitstoPX()
    alignForSmartGrid()
    doSmartGrid()
    hybridCar()
    collectRB
    setUpForRun4()
    
run3()