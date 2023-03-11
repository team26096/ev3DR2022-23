#!/usr/bin/env micropython

import ev3dev2.sensor as sensor
import ev3dev2.sensor.lego as lego_sensor

# Initialize the color sensor object
color_sensor = lego_sensor.ColorSensor()

# Set the color sensor mode to "raw reflected light"
color_sensor.mode = sensor.MODE_REFLECT_RAW

# Read the raw sensor value
raw_value = color_sensor.value(0)

# I think value(0) corresponds to red color, green is 1 and blue is 2
print("Raw value:", raw_value)