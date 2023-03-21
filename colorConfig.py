#!/usr/bin/env micropython

from initialize import *
from functions import *
from portCheck import *

def configureColor():
    leftWhite = -1000
    rightWhite = -1000
    backWhite = -1000
    leftBlack = -1000
    rightBlack = -1000
    backBlack = -1000

    logfile.info("front.")
    snd.speak('front.')
    # read front values 
    while (leftWhite == -1000 or rightWhite == -1000):
        if btn.check_buttons(buttons=['up']):
            leftWhite = left_light.reflected_light_intensity
            rightWhite = right_light.reflected_light_intensity
            logfile.info('leftWhite = ' + str(leftWhite))
            logfile.info('rightWhite = ' + str(rightWhite))

    snd.beep()

    while (leftBlack == -1000 or rightBlack == -1000):
        if btn.check_buttons(buttons=['down']):
            leftBlack = left_light.reflected_light_intensity
            rightBlack = right_light.reflected_light_intensity
            logfile.info('leftBlack = ' + str(leftBlack))
            logfile.info('rightBlack = ' + str(rightBlack))
        
    snd.beep()

    logfile.info("front sensing is done.")
    snd.speak('front done.')    

    logfile.info("back.")
    snd.speak('back.')

    # read black values 
    while (backBlack == -1000 or backWhite == -1000):
        if btn.check_buttons(buttons=['up']):
            backWhite = back_light.reflected_light_intensity
            snd.beep()
            logfile.info('backWhite = ' + str(backWhite))
        elif btn.check_buttons(buttons=['down']):
            backBlack = back_light.reflected_light_intensity
            snd.beep()
            logfile.info('backBlack = ' + str(backBlack))
            

    logfile.info("Back done.")
    snd.speak('Back done.')
 
    logfile.info("writing file")
    snd.speak('Writing file.')

    #Write values to file
    f = open("ConfiguredColor.txt", "w")
    f.write(str(leftWhite)+'\n')
    f.write(str(rightWhite)+'\n')
    f.write(str(backWhite)+'\n')
    f.write(str(leftBlack)+'\n')
    f.write(str(rightBlack)+'\n')
    f.write(str(backBlack)+'\n')
    f.close()

    logfile.info("finished writing")
    snd.speak('Finished writing.')

    snd.beep()

# do portcheck
while True:
    if do_portcheck() == True:
        break

configureColor()