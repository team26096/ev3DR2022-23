#!/usr/bin/env micropython

# add imports here
from Run1 import *
from Run3 import *
from Run4 import *
from Run5 import *
from initialize import *
from portCheck import *

# start queen code now 
s = Sound()
btn = Button()

# do portcheck
while True:
    if do_portcheck() == True:
        break

s.speak('starting button sequence')
# start button sequence

while True:
    # print(btn.buttons_pressed)
    if btn.check_buttons(buttons=['enter']): 
        s.beep()
        # when the enter button is pressed, the robot will play run1
        run1()
    elif btn.check_buttons(buttons=['up']): 
        s.beep()
        # when the up button is pressed, the robot will play run3
        run3()
    elif btn.check_buttons(buttons=['right']): 
        s.beep()
        # when the right button is pressed, the robot will play run4
        run4()
    elif btn.check_buttons(buttons=['down']): 
        s.beep()
        # when the down button is pressed, the robot will play xxx
    elif btn.check_buttons(buttons=['left']): 
        s.beep()
        # when the left button is pressed, the robot will play run5
        run5()
