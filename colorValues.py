#!/usr/bin/env micropython

from initialize import *

def readColorValues():
    while (True):
        if btn.check_buttons(buttons=['left']):
            leftWhite = left_light.reflected_light_intensity
            logfile.info('Left light = ' + str(leftWhite))
        elif btn.check_buttons(buttons=['right']):
            rightWhite = right_light.reflected_light_intensity
            logfile.info('Right light = ' + str(rightWhite))
        elif btn.check_buttons(buttons=['down']):
            backWhite = back_light.reflected_light_intensity
            logfile.info('Back light = ' + str(backWhite))

readColorValues()