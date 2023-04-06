#!/usr/bin/env micropython

from initialize import *

snd.speak('front')
i=0
while (i<15):
    left_light._ensure_mode(left_light.MODE_REF_RAW)
    right_light._ensure_mode(left_light.MODE_REF_RAW)
    lvalue = left_light.value(0)
    rvalue = right_light.value(0)
    logfile.info('RAW lvalue=' + str(lvalue) + ' rvalue=' + str(rvalue))
    left_light._ensure_mode(left_light.MODE_COL_REFLECT)
    right_light._ensure_mode(left_light.MODE_COL_REFLECT)
    lvalue = left_light.value(0)
    rvalue = right_light.value(0)
    logfile.info('REFLECT lvalue=' + str(lvalue) + ' rvalue=' + str(rvalue))
    logfile.info('----')
    i = i + 1;
    snd.beep()
    sleep(4)

snd.speak('back')
sleep(5)
i=0
while (i<15):
    back_light._ensure_mode(back_light.MODE_REF_RAW)
    bvalue = back_light.value(0)
    logfile.info('RAW lvalue=' + str(bvalue))
    back_light._ensure_mode(back_light.MODE_COL_REFLECT)
    bvalue = back_light.value(0)
    logfile.info('REFLECT lvalue=' + str(bvalue))
    logfile.info('----')
    i = i + 1;
    snd.beep()
    sleep(4)