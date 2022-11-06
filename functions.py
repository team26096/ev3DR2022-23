#!/usr/bin/env micropython

from time import time, sleep
import threading
import logging      
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering,
                           MoveTank, SpeedPercent, follow_for_ms, MediumMotor, LargeMotor)
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from portCheck import do_portcheck
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire, Wheel

class FollowGyroAngleErrorTooFast(Exception):
    """
    Raised when a gyro following robot has been asked to follow
    an angle at an unrealistic speed
    """
    pass     

#this function moves a motor until it cannot move anymore(stall)
def run_for_motor_stalled(motor, seconds, speed):
    motor.on(speed)
    motor.wait_until_not_moving(timeout=seconds)
    motor.stop()

class EV3DRTires(Wheel):
    """
    part number 41897
    comes in set 45544
    """
    def __init__(self):
        Wheel.__init__(self, 50, 15)

def robot_runfordegrees(robot, left_speed, right_speed, degrees):
    robot.on_for_degrees(left_speed, right_speed, degrees)

#this function turns the motor for a certain amount of degrees, 
#normally we can do this with the one line that is in the function 
#but to put it as a thread(that we will use towards the end of the run) 
#we needed to make a new function
def motor_runfordegrees(motor, speed, degrees):
    motor.on_for_degrees(speed, degrees)

def my_follow_for_degrees(tank, degrees, left_motor, right_motor):
    averagedegrees = (left_motor.position + right_motor.position)/2  
    if degrees >= 0:
        if averagedegrees >= degrees:
            return False
        else:
            return True
    # if the target degrees are less than 0, the robot is moving backwards
    else:
        if averagedegrees <= degrees:
            return False
        else:
            return True

def reset():
    mm_horizontal = MediumMotor(OUTPUT_D)
    mm_vertical = MediumMotor(OUTPUT_A)
    # the rack stalls at the left-most position in the background
    th = threading.Thread(target=RunForMotorStalled, args=(mm_horizontal, -20, 5000))
    th.daemon = True
    th.start()
    # rack stalls down to get to a known position
    RunForMotorStalled(mm_vertical, -15, 5000)
    # the rack goes up 350 degrees to start run 1
    mm_vertical.on_for_degrees(30, 350, brake=True, block=True)

def follow_until_white(tank, lightSensor):
    logfile = logging.getLogger('')
    light_intensity = (lightSensor.reflected_light_intensity)
    logfile.info('light = ' + str(light_intensity))
    if light_intensity >= 85:
        return False
    else:
        return True

def follow_until_black(tank,lightSensor):
    logfile = logging.getLogger('')
    light_intensity = lightSensor.reflected_light_intensity
    light_intensity = (lightSensor.reflected_light_intensity)
    logfile.info('light = ' + str(light_intensity))
    if light_intensity <= 10:
        return False
    else:
        return True

def pivot_gyro_turn(left_speed, right_speed, target_angle, 
robot, gyro, bLeftTurn = True):
    logfile = logging.getLogger('')
    CurGyro = gyro.angle
    logfile.info('gyro = ' + str(CurGyro))
    if  bLeftTurn == True:
        while CurGyro >= target_angle:
            logfile.info('gyro = ' + str(CurGyro))
            robot.on(left_speed, right_speed)
            CurGyro = gyro.angle
    else: 
        while CurGyro <= target_angle:
            logfile.info('gyro = ' + str(CurGyro))
            robot.on(left_speed, right_speed)
            CurGyro = gyro.angle

    robot.stop()

def do_calibrate():
    left_light = ColorSensor(INPUT_4)
    right_light = ColorSensor(INPUT_1)
    back_light = ColorSensor(INPUT_2)
    left_light.calibrate_white()
    right_light.calibrate_white()
    back_light.calibrate_white()
    s = Sound()
    s.beep()

def squareToWhite(speed, left_light, right_light, left_motor, right_motor):
    s = Sound()
    left_motor.on(speed)
    left_motor.stop_action = 'brake'
    right_motor.on(speed)
    right_motor.stop_action = 'brake'
    bLeftTargetReached = False
    bRightTargetReached = False
    logfile = logging.getLogger('')
    while ((bLeftTargetReached == False) or 
        (bRightTargetReached == False)):  
        left = left_light.reflected_light_intensity
        right = right_light.reflected_light_intensity
        logfile.info("right light = " + str(right_light.reflected_light_intensity))
        logfile.info("left light = " + str(left_light.reflected_light_intensity))
        if right >= 81:
            bRightTargetReached = True
            right_motor.stop()
        if left >= 90:
            bLeftTargetReached = True
            left_motor.stop()
            
    s.beep()

def squareToBlack(speed, left_light, right_light, left_motor, right_motor):
    s = Sound()
    left_motor.on(speed)
    left_motor.stop_action = 'hold'
    right_motor.on(speed)
    right_motor.stop_action = 'hold'
    bLeftTargetReached = False
    bRightTargetReached = False
    while ((bLeftTargetReached == False) or 
        (bRightTargetReached == False)):  
        left = left_light.reflected_light_intensity
        right = right_light.reflected_light_intensity
        if left <= 13:
            bLeftTargetReached = True
            left_motor.stop()
        if right <= 10:
            bRightTargetReached = True
            right_motor.stop()
    s.beep()

def BackwardStall(robot, speed, timeout):
    robot.on(speed,speed)
    robot.wait_until_not_moving(timeout)
    robot.stop()

def p_pivot_gyro_turn(left_speed, right_speed, target_angle,  
robot, gyro, bLeftTurn = True, error_margian = 2, p = 2):
    logfile = logging.getLogger('')
    CurGyro = gyro.angle
    logfile.info('gyro = ' + str(CurGyro))
    if  bLeftTurn == True:
        while CurGyro >= target_angle:
            error = CurGyro - target_angle
            # the correction value for left and right
            cl = 0
            cr = 0
            if error < 15:
                if cl < left_speed-4:
                    cl = cl+1
                if cr < right_speed-4:
                    cr = cr+1
            logfile.info('gyro = ' + str(CurGyro))
            robot.on(left_speed - cl, right_speed - cr)
            CurGyro = gyro.angle
    else: 
        while CurGyro <= target_angle:
            logfile.info('gyro = ' + str(CurGyro))
            robot.on(left_speed, right_speed)
            CurGyro = gyro.angle

    robot.stop()

def myPerfectSquare(left_target_light, right_target_light, left_motor, right_motor, maxSeconds):
    
    left_light = ColorSensor(INPUT_4)
    right_light = ColorSensor(INPUT_1)
    logfile = logging.getLogger('')
    s = Sound()
    robot = MoveTank(OUTPUT_B, OUTPUT_C)
    logfile.info('square to white starting')
    squareToWhite(10, left_light, right_light, left_motor, right_motor)
    robot.on_for_degrees(5, 5, 5)
    start_time = time()
    logfile.info('square to white completed, starting perfection')
    bLeftMotorStopped = False
    bRightMotorStopped = False
    lowSpeed = 2
    bLeftWheelPos = True
    bRightWheelPos = True
    left_motor.on(lowSpeed)
    right_motor.on(lowSpeed)
    logfile.info('starting perfection to the right light sensor: ' + str(right_target_light))
    logfile.info('starting perfection to the left light sensor: ' + str(left_target_light))
    elapsed_time = 0.0
    while not (bLeftMotorStopped == True and bRightMotorStopped == True) and elapsed_time < maxSeconds:
        CurRightLight = right_light.reflected_light_intensity
        logfile.info(str(time()) + ' Current right light = ' + str(CurRightLight))
        # checking for right light
        if CurRightLight == right_target_light:
            right_motor.stop()
            bRightMotorStopped = True
            s.beep()
            logfile.info(str(time()) + ' ****right light sensor on the target')
        elif CurRightLight < right_target_light:
            if bRightWheelPos == True or bRightMotorStopped:
                right_motor.stop()
                logfile.info(str(time()) + ' switching diretion on right motor')
                right_motor.on(-lowSpeed)
                bRightWheelPos = False
            bRightMotorStopped = False
            logfile.info(str(time()) + ' moving right motor with speed = ' + str(-lowSpeed))
        else:
            if bRightWheelPos == False or bRightMotorStopped:
                right_motor.stop()
                logfile.info(str(time()) + ' switching diretion on right motor')
                right_motor.on(lowSpeed)
                bRightWheelPos = True
            bRightMotorStopped = False
            logfile.info(str(time()) + ' moving right motor with speed = ' + str(lowSpeed))
        
        # checking for left light
        CurLeftLight = left_light.reflected_light_intensity
        logfile.info(str(time()) + ' Current left light = ' + str(CurLeftLight))
        if left_target_light == CurLeftLight:
            left_motor.stop()
            bLeftMotorStopped = True
            s.beep()
            logfile.info(str(time()) + ' ****left light sensor on the target')
        elif CurLeftLight < left_target_light:
            if bLeftWheelPos == True or bLeftMotorStopped:
                left_motor.stop()
                logfile.info(str(time()) + ' switching diretion on left motor')
                left_motor.on(-lowSpeed)
                bLeftWheelPos = False
            bLeftMotorStopped = False
            logfile.info(str(time()) + ' moving left motor with speed = ' + str(-lowSpeed))
        else:
            if bLeftWheelPos == False or bLeftMotorStopped:
                left_motor.stop()
                logfile.info(str(time()) + ' switching diretion on left motor')
                left_motor.on(lowSpeed)
                bLeftWheelPos = True
            bLeftMotorStopped = False
            logfile.info(str(time()) + ' moving left motor with speed = ' + str(lowSpeed))
        logfile.info(str(time()) + ":")
        cur_time = time()
        elapsed_time = round(cur_time - start_time, 2)
    left_motor.stop()
    right_motor.stop()

#function to turn and align back sensor to black
def backward_turn_until_black (light_sensor, robot, bLeftTurn=True):
    logfile = logging.getLogger('')

    if  bLeftTurn == True:
        robot.on(-15, 0)
    else: 
        robot.on(0, -15)

    light = light_sensor.reflected_light_intensity
    while light > 7:
        logfile.info('light_sensor = ' + str(light))
        light=light_sensor.reflected_light_intensity
        sleep(0.1)
        
    robot.stop()

#function to turn and align back sensor to black with forward motion
def forward_turn_until_black (light_sensor, robot, bLeftTurn=True):
    logfile = logging.getLogger('')

    if  bLeftTurn == True:
        robot.on(0, 15)
    else: 
        robot.on(15, 0)

    light = light_sensor.reflected_light_intensity
    while light > 7:
        logfile.info('light_sensor = ' + str(light))
        light=light_sensor.reflected_light_intensity
        sleep(0.1)
        
    robot.stop()

def pivot_turn_until_black(left_speed, right_speed, target_light, 
robot, lightSensor):
    logfile = logging.getLogger('')
    light = lightSensor.reflected_light_intensity
    logfile.info('light = ' + str(light))
    robot.on(left_speed, right_speed)
    while light >= target_light:
        logfile.info('light = ' + str(light))
        sleep(0.1)
        light = lightSensor.reflected_light_intensity

    logfile.info('light 1 = ' + str(light))    
    robot.stop()
