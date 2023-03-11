#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *
#!/usr/bin/env micropython

def run2twoSelfSetup():
    #move rack left
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()
    mm_vertical.reset()
    mm_vertical.on_for_degrees(75, 2300, brake=True, block=True)

def getOutOfBase():
    # gyro straight until the lcs sees black and white
    gyro.reset()
    # move rack to the middle for energy storage
    mm_horizontal.on_for_degrees(50, -250, brake=True, block=False)
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 25, target_angle=0, 
                        follow_for=follow_until_black, lightSensor=left_light)

def alignForEnergyStorage():
    #line follow to energy storage
    robot.reset()
    robot.cs = left_light

    #begin line follow, go certain distance to catch line
    robot.follow_line(1.2, 0, 0, 15, target_light_intensity=56,
                    follow_left_edge=False,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=my_follow_for_degrees, degrees=500, left_motor=left_motor, right_motor=right_motor)
    
    #begin line follow, go until white L junction near energy storage
    robot.follow_line(1.2, 0, 0, 15, target_light_intensity=56,
                    follow_left_edge=False,
                    off_line_count_max=500,
                    sleep_time=0.01,
                    follow_for=follow_until_right_white, lightSensor=right_light)
    
    #follow gyro until both front sensors are on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=0, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)

    #make sure the robot is aligned completely to energy storage
    if (gyro.angle > 0):
        pivot_gyro_turn(-10, 10, 0, robot, gyro, bLeftTurn=True)
    elif (gyro.angle < 0):
        pivot_gyro_turn(10, -10, 0, robot, gyro, bLeftTurn=False)
    snd.beep()
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=160, left_motor=left_motor, right_motor=right_motor)
    snd.beep()

def doEnergyStorage():
    #go down to drop units into energy storage bin
    run_for_motor_stalled(mm_vertical, 10000, -75)
    mm_vertical.reset()
    snd.beep()

def doOilPlatform():

    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=0, 
                    follow_for=follow_until_right_white, lightSensor=right_light)


    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=0, 
                    follow_for=follow_until_front_black, lls=left_light, rls=right_light)

    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=0, 
                    follow_for=follow_until_right_white, lightSensor=right_light)
              

    #come back to get in position for oil platform
    #robot.reset()
    #robot.follow_gyro_angle(3, 0, 0, -25, target_angle=0, 
    #                follow_for=my_follow_for_degrees, degrees=-317, left_motor=left_motor, right_motor=right_motor)

    #move rack left to get under pump
    mm_horizontal.on_for_degrees(65, 250, brake=True, block=True)

    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                   follow_for=my_follow_for_degrees, degrees=20, left_motor=left_motor, right_motor=right_motor)


    #raise rack 3 times to pump fuel units into truck
    loop = 0
    while(loop < 3):
        mm_vertical.on_for_degrees(80, 1800, brake=True, block=True)
        sleep(0.1)
        mm_vertical.on_for_degrees(80, -1800, brake=True, block=True)   
        loop = loop + 1

    snd.beep()

    #Turn tight to align with the return home base
    pivot_gyro_turn(15, -15, 18, robot, gyro, bLeftTurn=False)

    #move rack right to get under pump
    mm_horizontal.on_for_degrees(65, -650, brake=True, block=False)

    # come back to base
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -75, target_angle=18, 
                    follow_for=my_follow_for_degrees, degrees=-1300, left_motor=left_motor, right_motor=right_motor)

def setUpForOilPlatform():
    #move rack right
    mm_vertical.reset()
    mm_vertical.on_for_degrees(75, 1500, brake=True, block=False)
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()
    sleep(3)


def bringOilTruck():
    gyro.reset()
    robot.reset()

    mm_horizontal.on_for_degrees(75, 710, brake=True, block=True)

    # we are going forward till we reach oil truck while also resetting the rack
    robot.follow_gyro_angle(3, 0, 0, 45, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=750, left_motor=left_motor, right_motor=right_motor)
    
    #bring rack down to catch oil truck
    run_for_motor_stalled(mm_vertical, 10000, -65)
    robot.reset()
    #come back to base while bringing truck
    robot.follow_gyro_angle(3, 0, 0, -10, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-100, left_motor=left_motor, right_motor=right_motor)
    #come back to base while bringing truck
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-750, left_motor=left_motor, right_motor=right_motor)

def setUpForRun3():
    # we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 65)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    #we reset mm_vertical
    mm_vertical.reset()

def run2two():
    readAllValues()
    run2twoSelfSetup()
    getOutOfBase()
    alignForEnergyStorage()
    doEnergyStorage()
    doOilPlatform()
    setUpForOilPlatform()
    bringOilTruck()
 #   setUpForRun3()

run2two()