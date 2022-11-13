#!/usr/bin/env micropython

# add imports
from initialize import *

#add run 5 code here
#we reset mm_horizontal
gyro.reset
robot.reset
mm_horizontal.reset()

#we run mm_vertical all the way down
run_for_motor_stalled(mm_vertical, 10000, -35)
mm_vertical.reset()

# gyro straight to align with toy factory
robot.reset
robot.on_for_degrees(30, 30, 850)

# move rack all the way up for toy factory
robot.reset
mm_vertical.on_for_degrees(50, 1800, brake=True, block=False)

# turn right to align better with toy factory
pivot_gyro_turn(15, 0, 15, robot, gyro, bLeftTurn=True)

# move rack all the way to the right
#robot.reset
#run_for_motor_stalled(mm_horizontal, 10000, -35)
#mm_horizontal.reset()

# move rack back and all the way to the right again for maximum reliablity
#robot.reset
#run_for_motor_stalled(mm_horizontal, 10000, 35)
#mm_horizontal.reset()
#robot.reset
#run_for_motor_stalled(mm_horizontal, 10000, -35)
#mm_horizontal.reset()

# turn back for going to other base. 
#robot.reset
#pivot_gyro_turn(0, 15, 15, robot, gyro, bLeftTurn=True)

# go forward till base
#robot.reset
#robot.on_for_degrees(70, 70, 10000)
