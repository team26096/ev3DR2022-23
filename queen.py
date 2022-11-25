#!/usr/bin/env micropython

# add imports here
from Run1 import *
from Run2 import *
from Run3 import *
from Run4 import *
from Run5 import *
from initialize import *
from portCheck import *
from functions import *

# start queen code now 

# main program starts here

# do portcheck
while True:
    if do_portcheck() == True:
        break

snd.speak('Reading Color Values')
# Read color values
readAllValues()

snd.speak('starting button sequence')
# start button sequence
while True:
    if btn.check_buttons(buttons=['enter']): 
        snd.beep()
        # when the enter button is pressed, the robot will play run1
        run1()
    elif btn.check_buttons(buttons=['up']): 
        snd.beep()
        # when the up button is pressed, the robot will play run2
        run2()
    elif btn.check_buttons(buttons=['right']): 
        snd.beep()
        # when the right button is pressed, the robot will play run3
        run3()
    elif btn.check_buttons(buttons=['down']): 
        snd.beep()
        # when the down button is pressed, the robot will play run4
        run4()
    elif btn.check_buttons(buttons=['left']): 
        snd.beep()
        # when the left button is pressed, the robot will play run5
        run5()
