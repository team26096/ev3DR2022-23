#!/usr/bin/env micropython

# add imports here
from Run1two import *
from Run2two import *
from Run3 import *
from Run4two import *
from Run5 import *
from initialize import *
from functions import *

# start queen code now 

# main program starts here

snd.speak('Reading Color Values')
# Read color values
readAllValues()

#setup for run 1
run1SelftStart()

transitStart = time()
transitEnd = transitStart
r1Time = 0
r2Transit = 0
r2Time = 0
r3Transit = 0
r3Time = 0
r4Transit = 0
r4Time = 0
r5Transit = 0
r5Time = 0

snd.speak('starting button sequence')
# start button sequence
while True:
    if btn.check_buttons(buttons=['enter']):
        snd.beep()
        # when the enter button is pressed, the robot will play run1
        startTime = time()
        run1two()
        endTime = time()
        r1Time = round(endTime-startTime,2)
        transitStart = time()
        transitEnd = 0
        run2twoSelfSetup()
    elif btn.check_buttons(buttons=['up']):
        snd.beep()
        # when the up button is pressed, the robot will play run2
        transitEnd = time()
        r2Transit = round(transitEnd-transitStart,2)
        transitStart = 0
        startTime = time()
        run2two()
        endTime = time()
        r2Time = round(endTime-startTime,2)
        transitStart = time()
        transitEnd = 0
        run3SelfStartUp()
    elif btn.check_buttons(buttons=['right']):
        snd.beep()
        # when the right button is pressed, the robot will play run3
        transitEnd = time()
        r3Transit = round(transitEnd-transitStart,2)
        transitStart = 0
        startTime = time()
        run3()
        endTime = time()
        r3Time = round(endTime-startTime,2)
        transitStart = time()
        transitEnd = 0
        run4SelfStartUp()
    elif btn.check_buttons(buttons=['down']):
        snd.beep()
        # when the down button is pressed, the robot will play run4
        transitEnd = time()
        r4Transit = round(transitEnd-transitStart,2)
        transitStart = 0
        startTime = time()
        run4two()
        endTime = time()
        r4Time = round(endTime-startTime,2)
        transitStart = time()
        transitEnd = 0
        run5SelfSetup()
    elif btn.check_buttons(buttons=['left']):
        snd.beep()
        # when the left button is pressed, the robot will play run5
        transitEnd = time()
        r5Transit = round(transitEnd-transitStart,2)
        transitStart = 0
        startTime = time()
        run5()
        endTime = time()
        r5Time = round(endTime-startTime,2)

        logfile.info('>>>>>> run 1 time: ' + str(r1Time) + 'secs')
        logfile.info('>>>>>> run 2 Transit: ' + str(r2Transit) + 'secs')
        logfile.info('>>>>>> run 2 time: ' + str(r2Time) + 'secs')
        logfile.info('>>>>>> run 3 Transit: ' + str(r3Transit) + 'secs')
        logfile.info('>>>>>> run 3 time: ' + str(r3Time) + 'secs')
        logfile.info('>>>>>> run 4 Transit: ' + str(r4Transit) + 'secs')
        logfile.info('>>>>>> run 4 time: ' + str(r4Time) + 'secs')
        logfile.info('>>>>>> run 5 Transit: ' + str(r5Transit) + 'secs')
        logfile.info('>>>>>> run 5 time: ' + str(r5Time) + 'secs')
        totalRunTime = r1Time + r2Time + r3Time + r4Time + r5Time
        totalTransit = r2Transit + r3Transit + r4Transit + r5Transit
        logfile.info('>>>>>> total run time: ' + str(totalRunTime) + 'secs')
        logfile.info('>>>>>> total transit time: ' + str(totalTransit) + 'secs')
        logfile.info('>>>>>> TOTAL TIME: ' + str(totalRunTime + totalTransit) + 'secs')
    
    sleep(0.1)