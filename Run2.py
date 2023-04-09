#!/usr/bin/env micropython

# add imports
from initialize import *
from functions import *
#!/usr/bin/env micropython

def run2SelfSetup():
    #move rack left
    # mm_vertical.reset()
    #mm_vertical.on_for_degrees(75, 1100, brake=True, block=True)
    run_for_motor_stalled(mm_horizontal, 10000, 35)
    mm_horizontal.reset()
def getOutOfBase():
    # gyro straight until the lcs sees black and white
    gyro.reset()
    # move rack to the middle for energy storage
    mm_horizontal.on_for_degrees(45, -400, brake=True, block=False)
    # move forward to get out of base
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, 35, target_angle=0, 
                        follow_for=follow_until_left_black, lightSensor=left_light)
    pivot_gyro_turn(15, 0, 30, robot, gyro, bLeftTurn=False)
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
    
    #follow gyro until right sensor is on black
    robot.follow_gyro_angle(3, 0, 0, 15, target_angle=0, 
                    follow_for=follow_until_right_black, lightSensor=right_light, range=6)

    #make sure the robot is aligned completely to energy storage
    if (gyro.angle > 0):
        pivot_gyro_turn(-5, 5, 0, robot, gyro, bLeftTurn=True)
    elif (gyro.angle < 0):
        pivot_gyro_turn(5, -5, 0, robot, gyro, bLeftTurn=False)

    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, 25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=160, left_motor=left_motor, right_motor=right_motor)
def doEnergyStorage():
    #move rack left to get in position to catch storage tray
    mm_horizontal.on_for_degrees(55, 125, brake=True, block=True)

    #go down to drop units into energy storage bin
    mm_vertical.on_for_degrees(75, -1090, brake=True, block=True)
def doOilPlatform():
    # move backward to align robot with oil platform
    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=0, 
                    follow_for=follow_until_right_white, lightSensor=right_light)

    robot.follow_gyro_angle(3, 0, 0, -15, target_angle=0, 
                    follow_for=follow_until_right_black, lightSensor=right_light, range=6)

    #move rack left to get under pump
    mm_horizontal.on_for_degrees(55, 260, brake=True, block=True)

    #raise rack 3 times to pump fuel units into truck
    loop = 0
    while(loop < 3):
        mm_vertical.on_for_degrees(85, 740, brake=True, block=True)
        mm_vertical.on_for_degrees(85, -740, brake=True, block=True)   
        loop = loop + 1

    #Turn tight to align with the return home base
    pivot_gyro_turn(15, -15, 8, robot, gyro, bLeftTurn=False)

    #move rack right to get under pump
    mm_horizontal.on_for_degrees(65, -275, brake=True, block=False)

    # come back to base
    robot.reset()
    robot.follow_gyro_angle(1.5, 0, 0, -90, target_angle=8, 
                    follow_for=my_follow_for_degrees, degrees=-1300, left_motor=left_motor, right_motor=right_motor)
def setUpForOilTruck():
    run_for_motor_stalled(mm_horizontal, 10000, -35)
    mm_horizontal.reset()

    while True:
        if btn.check_buttons(buttons=['enter']):
            snd.beep()
            break
        sleep(0.1)
def bringOilTruck():
    gyro.reset()
    robot.reset()

    #move rack up
    mm_vertical.on_for_degrees(75, 740, brake=True, block=False)
    # move rack left to get in position for oil truck
    mm_horizontal.on_for_degrees(75, 680, brake=True, block=False)

    # we are going forward till we reach fuel truck while also resetting the rack
    robot.follow_gyro_angle(3, 0, 0, 50, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=720, left_motor=left_motor, right_motor=right_motor)
    
    #bring rack down to catch oil truck
    mm_vertical.on_for_degrees(65, -740, brake=True, block=True)

    #Come back slightly and sleep so that we grab fuel truck
    robot.reset()
    robot.follow_gyro_angle(3, 0, 0, -10, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-30, left_motor=left_motor, right_motor=right_motor)
    sleep(0.5)
   
    #come back slightly more to pull truck from its hinged position
    robot.follow_gyro_angle(3, 0, 0, -10, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-200, left_motor=left_motor, right_motor=right_motor)
    
    #come back to base while bringing truck
    robot.follow_gyro_angle(3, 0, 0, -25, target_angle=0, 
                    follow_for=my_follow_for_degrees, degrees=-740, left_motor=left_motor, right_motor=right_motor)
def setUpForRun3():
    # we run mm_horizontal all the way to the left 
    run_for_motor_stalled(mm_horizontal, 10000, 65)
    #we reset mm_horizontal
    mm_horizontal.reset()

    #we run mm_vertical all the way down
    run_for_motor_stalled(mm_vertical, 10000, -65)
    #we reset mm_vertical
    mm_vertical.reset()
def run2():
    logfile = logging.getLogger('')
    logfile.info('=====> run2 getOutOfBase start')
    getOutOfBase()
    logfile.info('=====> run2 getOutOfBase end')
    logfile.info('=====> run2 alignForEnergyStorage start')
    alignForEnergyStorage()
    logfile.info('=====> run2 alignForEnergyStorage end')
    logfile.info('=====> run2 doEnergyStorage start')
    doEnergyStorage()
    logfile.info('=====> run2 doEnergyStorage end')
    logfile.info('=====> run2 doOilPlatform start')
    doOilPlatform()
    logfile.info('=====> run2 doOilPlatform end')
    logfile.info('=====> run2 setUpForOilTruck start')
    setUpForOilTruck()
    logfile.info('=====> run2 setUpForOilTruck end')
    logfile.info('=====> run2 bringOilTruck start')
    bringOilTruck()
    logfile.info('=====> run2 bringOilTruck end')