#!/usr/bin/env micropython

from initialize import *
from functions import *

def configureColor():

    # snd.speak('Starting color calibration.')

    # frontCalibrate = False
    # backCalibrate = False
    # # read white values 
    # while (frontCalibrate == False or backCalibrate == False):

    #     if btn.check_buttons(buttons=['up']):
    #         do_calibrate()
    #         frontCalibrate = True
    #         logfile.info("frontCalibrate done")
    #     elif btn.check_buttons(buttons=['down']):
    #         do_calibrate_back()
    #         backCalibrate = True
    #         logfile.info("backCalibrate done") 
    
    # snd.beep()
    # snd.speak('Color calibration done.')
    # logfile.info("Color calibration is done")


    # sleep(1)
    logfile.info("Starting white sensing.")
    snd.speak('Starting white sensing.')
    leftWhite = -1000
    rightWhite = -1000
    backWhite = -1000

    # read white values 
    while (leftWhite == -1000 or rightWhite == -1000 or backWhite == -1000):

        if btn.check_buttons(buttons=['up']):
            leftWhite = left_light.reflected_light_intensity
            rightWhite = right_light.reflected_light_intensity
            snd.beep()
            logfile.info('Left light = ' + str(leftWhite))
            logfile.info('Right light = ' + str(rightWhite))
        # elif btn.check_buttons(buttons=['right']):
        #     rightWhite = right_light.reflected_light_intensity
        #     snd.beep()
        #     logfile.info('Right light = ' + str(rightWhite))
        elif btn.check_buttons(buttons=['down']):
            backWhite = back_light.reflected_light_intensity
            snd.beep()
            logfile.info('Back light = ' + str(backWhite))
    
    snd.beep()

    sleep(1)
    logfile.info("White sensing is done.")
    snd.speak('White sensing is done.')


    leftBlack = -1000
    rightBlack = -1000
    backBlack = -1000

    logfile.info("Starting black sensing.")
    snd.speak('Starting black sensing.')


     # read black values 
    while (leftBlack == -1000 or rightBlack == -1000 or backBlack == -1000):

        if btn.check_buttons(buttons=['up']):
            leftBlack = left_light.reflected_light_intensity
            rightBlack = right_light.reflected_light_intensity
            snd.beep()
            logfile.info('Left light = ' + str(leftBlack))
            logfile.info('Right light = ' + str(rightBlack))
        # elif btn.check_buttons(buttons=['right']):
        #     rightBlack = right_light.reflected_light_intensity
        #     snd.beep()
        #     logfile.info('Right light = ' + str(rightBlack))
        elif btn.check_buttons(buttons=['down']):
            backBlack = back_light.reflected_light_intensity
            snd.beep()
            logfile.info('Back light = ' + str(backBlack))

    snd.beep()
    logfile.info("Black sensing is done.")
    snd.speak('Black sensing is done.')

    sleep(1)

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

    logfile.info("finished writing file")
    snd.speak('Finished writing file.')


    snd.beep()

configureColor()