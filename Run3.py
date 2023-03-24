#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *

#start of code
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
    mm_horizontal.on_for_degrees(75, -450, brake=True, block=False)
    #gyro straight
    robot.cs = left_light
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)

def alignWithSolarFarm():

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
    pivot_gyro_turn(0, -20, 135, robot, gyro, bLeftTurn=False)

def dropToPXv2():
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=135, 
                        follow_for=my_follow_for_degrees, degrees=-100,
                        right_motor = right_motor, left_motor = left_motor)

    #go forward until left sensor is on white, black, then white
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=135, 
                        follow_for=follow_until_left_white, lightSensor=left_light)
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=135, 
                        follow_for=follow_until_left_black, lightSensor=left_light)
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=135, 
                        follow_for=follow_until_left_white, lightSensor=left_light)

    #raise rack to avoid collision with smart grid lever
    mm_vertical.on_for_degrees(35, 250, brake=True, block=False)

    #move rack to the right to avoid collison with Smart Grid
    run_for_motor_stalled(mm_horizontal, 10000, -65)
    mm_horizontal.reset()
    
    #forward to get into PX
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=135, 
                        follow_for=my_follow_for_degrees, degrees=450,
                        right_motor = right_motor, left_motor = left_motor)

def alignToSmartGridv2():

    #get out of PX and go back until left sensor on white then black
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -20, target_angle=135, 
                        follow_for=follow_until_back_white, lightSensor=back_light)
    #robot.follow_gyro_angle(3, 0, 0, -20, target_angle=140, 
    #                 follow_for=follow_until_back_black, lightSensor=back_light)
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -20, target_angle=135, 
                        follow_for=my_follow_for_degrees, degrees=-100,
                        right_motor = right_motor, left_motor = left_motor)

    #robot.follow_gyro_angle(3, 0, 0, -35, target_angle=140, 
                        #follow_for=follow_until_back_white, lightSensor=back_light)

    #turn until back sensor is on black
    #forward_turn_until_config_back_white(back_light, robot, bLeftTurn=True)
    #forward_turn_until_config_back_black(back_light, robot, bLeftTurn=True)

    pivot_gyro_turn(0, 20, 90, robot, gyro, bLeftTurn=True)


    #raise rack to avoid collision with smart grid lever
    mm_vertical.on_for_degrees(35, 500, brake=True, block=False)

    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=125,
                        right_motor = right_motor, left_motor = left_motor)

    #go forward till both sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_white, lls=left_light, rls=right_light)

    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)


def newAlignToSmartGrid():
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=130, 
                        follow_for=my_follow_for_degrees, degrees=-150,
                        right_motor = right_motor, left_motor = left_motor)

    #go forward until left sensor is on white, black, then white
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=130, 
                        follow_for=follow_until_left_white, lightSensor=left_light)
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=130, 
                        follow_for=follow_until_left_black, lightSensor=left_light)
    robot.follow_gyro_angle(3, 0, 0, 35, target_angle=130, 
                        follow_for=follow_until_left_white, lightSensor=left_light)

    #move rack to the right to avoid collison with Smart Grid
    run_for_motor_stalled(mm_horizontal, 10000, -65)
    mm_horizontal.reset()

    #turn to get into position for PX
    forward_turn_until_config_back_white(back_light, robot, bLeftTurn=True)
    forward_turn_until_config_back_black(back_light, robot, bLeftTurn=True)

    #go forward till both sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)

def doSmartGridv2():
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
    #run_for_motor_stalled(mm_horizontal, 10000, -35)
    #mm_horizontal.reset()
    mm_horizontal.on_for_degrees(-35, 800, brake=True, block=True)


    #go forward till both sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)

def doHybridCarv2():
    
    #raise rack to avoid collision with hybrid car
    mm_vertical.on_for_degrees(35, 700, brake=True, block=True)
    #to avoid toy factory
    mm_horizontal.on_for_degrees(35, 400, brake=True, block=False)

    #Leave smart grid
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=400,
                        right_motor = right_motor, left_motor = left_motor)


    #go forward till both sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=90, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)

    #go forward to get in postition for hybrid car
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=350,
                        right_motor = right_motor, left_motor = left_motor)
    
    #trun to flick hybrid car lever
    pivot_gyro_turn(0, -20, 135, robot, gyro, bLeftTurn=False)

    #go back to get in postition for hybrid car
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=135, 
                        follow_for=my_follow_for_degrees, degrees=-300,
                        right_motor = right_motor, left_motor = left_motor)
    
    #lower rack to push hybrid car lever
    mm_vertical.on_for_degrees(-35, 600, brake=True, block=True)

    #lower rack to push hybrid car lever
    mm_vertical.on_for_degrees(35, 400, brake=True, block=True)

def collectRBv2():
    #go back to base
    robot.follow_gyro_angle(3, 0, 0, 80, target_angle=130, 
                        follow_for=my_follow_for_degrees, degrees=1500,
                        right_motor = right_motor, left_motor = left_motor)


def newDropPX():
   
    #Go back so that when we turn we do not hit smart grid
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=90, 
                        follow_for=my_follow_for_degrees, degrees=-200,
                        right_motor = right_motor, left_motor = left_motor)
   
    #get in front of Power To X
    pivot_gyro_turn(15, 0, 180, robot, gyro, bLeftTurn=False)

    #go forward to keep the units fully in PX
    robot.follow_gyro_angle(3, 0, 0, 40, target_angle=180, 
                        follow_for=my_follow_for_degrees, degrees=100,
                        right_motor = right_motor, left_motor = left_motor)

    #go back to complete smart grid
    robot.follow_gyro_angle(3, 0, 0, -40, target_angle=180, 
                        follow_for=my_follow_for_degrees, degrees=-100,
                        right_motor = right_motor, left_motor = left_motor)

    pivot_gyro_turn(0, 15, 90, robot, gyro, bLeftTurn=True)

#def newHybridCar():
    
def dropUnitstoPX():
    #raising rack to avoid water reservoir
    # lakshmi mm_vertical.on_for_degrees(75, 200, brake=True, block=False)

    #gyro straight into power to X to drop energy units
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 40, target_angle=122, 
                        follow_for=my_follow_for_degrees, degrees=650,
                        right_motor = right_motor, left_motor = left_motor)

    #turn to drop energy units into power to X
    pivot_gyro_turn(0, -20, 226, robot, gyro, bLeftTurn=False)

    #go back to align to leave power to X
    robot.reset()
    robot.on_for_degrees(-25, -25, 300, brake=True, block=True)

def doHybridCar():
    #go back to align with hybrid car
    robot.reset()
    snd.beep()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=226, 
                        follow_for=follow_until_left_white, lightSensor=left_light)
    snd.beep()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=226, 
                        follow_for=follow_until_left_black, lightSensor=left_light)
    snd.beep()
    robot.follow_gyro_angle(3, 0, 0, -35, target_angle=226, 
                        follow_for=follow_until_left_white, lightSensor=left_light)
    snd.beep()
    # go more back so robot is in line to push hybrid car lever
    robot.reset()
    robot.on_for_degrees(-25, -25, 65, brake=True, block=True)

    #raise the rack up to push hybrid car lever
    mm_vertical.on_for_degrees(35, 240, brake=True, block=True)

    #bring the rack down to release hybrid car lever
    mm_vertical.on_for_degrees(-75, 180, brake=True, block=True)

    #go forward to begin smart grid alignment
    robot.reset()
    robot.on_for_degrees(25, 25, 310, brake=True, block=True)

    #turn until back light is on white and then black
    forward_turn_until_config_back_white(back_light, robot, bLeftTurn=False)
    forward_turn_until_config_back_black(back_light, robot, bLeftTurn=False)

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
    #raise the rack up 
    mm_vertical.on_for_degrees(75, 420, brake=True, block=True)

    #move horizontal rack to the right to hook to lever on smart grid
    mm_horizontal.reset()
    mm_horizontal.on_for_degrees(75, -800, brake=True, block=True)

    #we run mm_vertical all the way down to grab lever for smart grid
    run_for_motor_stalled(mm_vertical, 10000, -75)
    mm_vertical.reset()

    #move horizontal rack left and pull smart grid
    run_for_motor_stalled(mm_horizontal, 10000, 25)
    mm_horizontal.reset()

def collectRB():
    
    snd.beep()
    #raising rack detach smart grid
    mm_vertical.on_for_degrees(75, 180, brake=True, block=True)

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
    
    #move rack to the right to avoid toy factory
    mm_horizontal.on_for_degrees(75, -600, brake=True, block=True)
    
    #final go back to base and grab RB
    robot.reset()
    robot.on_for_degrees(-95, -95, 1500, brake=True, block=True)
    #robot.follow_gyro_angle(3, 0, 0, -85, target_angle=315, 
    #                    follow_for=my_follow_for_degrees, degrees=-1500,
    #                   right_motor = right_motor, left_motor = left_motor)

def setUpForRun4():
    # stall rack to the left
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -35)
    mm_vertical.reset()

def run3():
    run3SelfStartUp()
    readAllValues()
    getOutOfBase()
    alignWithSolarFarm()
    collectEnergyUnits()
    dropToPXv2()
    alignToSmartGridv2()
    doSmartGridv2()
    doHybridCarv2()
    collectRBv2()
    # dropUnitstoPX()
    # doHybridCar()
    # alignForSmartGrid()
    # doSmartGrid()
    # collectRB()
    # setUpForRun4()

run3()