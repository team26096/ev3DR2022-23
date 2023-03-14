#!/usr/bin/env micropython

import ev3dev2.sensor as sensor
import ev3dev2.sensor.lego as lego_sensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

# Initialize the color sensor object
left_light = lego_sensor.ColorSensor(INPUT_4)
right_light = lego_sensor.ColorSensor(INPUT_1)
back_light = lego_sensor.ColorSensor(INPUT_2)

# Set the color sensor mode to "raw reflected light"
#left_light.mode = left_light.MODE_REF_RAW
left_light._mode('REF-RAW')

# right_light.mode = right_light.MODE_REF_RAW
# back_light.mode = back_light.MODE_REF_RAW

# I think value(0) corresponds to red color, green is 1 and blue is 2
print("left Raw value:", left_light._value(0))
# print("right Raw value:", right_light.value(0))
# print("back Raw value:", back_light.value(0))