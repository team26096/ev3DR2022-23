#!/usr/bin/env micropython

from time import time, sleep         
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering,
                           MoveTank, SpeedPercent, follow_for_ms, MediumMotor, LargeMotor)
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.power import PowerSupply
import logging

def do_portcheck():
    s = Sound()
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(name='')
    log.info('****Starting Portcheck****')
    btn = Button()
    
    #Verify that port 'B' is the right large motor
    try:
        log.info('Checking large motor on Port B')
        motor = LargeMotor(OUTPUT_B)
    except:
        log.info('Failed on Port B')
        s.speak('Large Motor on port B is not connected. Please connect and try again.')
        return False

    #Verify that port 'C' is the left large motor
    try:
        log.info('Checking large motor on Port C')
        motor = LargeMotor(OUTPUT_C)    
    except:
        log.info('Failed on Port C')
        s.speak('Large Motor on port C is not connected. Please connect and try again.')
        return False

    #Verify that port 'A' is the vertical medium motor
    try:
        log.info('Checking medium motor on Port A')
        mm_vertical = MediumMotor(OUTPUT_A)
    except:
        log.info('Failed on Port A')
        s.speak('Medium Motor on port A is not connected. Please connect and try again.')
        return False

    #Verify that port 'D' is the horizontal medium motor
    try:
        log.info('Checking medium motor on Port D')
        mm_horizontal = MediumMotor(OUTPUT_D)
    except:
        log.info('Failed on Port D')
        s.speak('Medium Motor on port D is not connected. Please connect and try again.')
        return False

    #Verify that port '3' is the gyro sensor
    try:
        gyro = GyroSensor(INPUT_3)
    except:
        print('33333')
        s.speak('Gyro Sensor on port 3 is not connected. Please connect and try again.')
        return False

    #Verify that port '4' is the left light sensor
    try:
        left_light = ColorSensor(INPUT_4)
    except:
        print('44444')
        s.speak('Left Light Sensor on port 4 is not connected. Please connect and try again.')
        return False

    #Verify that port '1' is the right light sensor
    try:
        right_light = ColorSensor(INPUT_1)
    except:
        print('11111')
        s.speak('Right Light Sensor on port 1 is not connected. Please connect and try again.')
        return False
        
    #Verify that port '2' is the back light sensor
    try:
        back_light = ColorSensor(INPUT_2)
    except:
        print('22222')
        s.speak('Back Light Sensor on port 2 is not connected. Please connect and try again.')
        return False

    # gyro flow check
    firstGyroValue = gyro.angle
    sleep(2)
    secondGyroValue = gyro.angle
    if int(firstGyroValue) != int(secondGyroValue):
        s.speak('gyro is flowing')
        return False

    # check if large motors are moving
    right_motor = LargeMotor(OUTPUT_C)
    left_motor = LargeMotor(OUTPUT_B)
    right_motor.reset()
    sleep(0.5)
    right_motor.on_for_degrees(10, 30)
    if abs(30-right_motor.position) > 15:
        log.info('right motor position: ' + str(right_motor.position))
        s.speak('the right motor aint workin')
        return False

    left_motor.reset()
    sleep(0.5)
    left_motor.on_for_degrees(10, 30)
    if abs(30-left_motor.position) > 15:
        log.info('left motor position: ' + str(left_motor.position))
        s.speak('the left motor aint workin')
        return False

    # battery checker
    ps = PowerSupply()
    log.info('battery current: ' + str(ps.measured_amps))
    log.info('battery volts: ' + str(ps.measured_volts))
    if ps.measured_volts < 7.0:
        log.info('the battery is low')
        s.speak('The battery is low, please charge and try again')
        return False

    s.speak('All ports are connected!')

    return True