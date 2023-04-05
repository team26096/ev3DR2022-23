#!/usr/bin/env micropython

from initialize import *

while True:
    left_light._ensure_mode(left_light.MODE_REF_RAW)
    right_light._ensure_mode(left_light.MODE_REF_RAW)
    lvalue = left_light.value(0)
    rvalue = right_light.value(0)
    logfile.info('RAW lvalue=' + str(lvalue) + ' rvalue=' + str(rvalue))
    left_light._ensure_mode(left_light.MODE_COL_REFLECT)
    value = left_light.value(0)
    rvalue = right_light.value(0)
    logfile.info('REFLECT lvalue=' + str(lvalue) + ' rvalue=' + str(rvalue))
    logfile.info('----')
    snd.beep()
    sleep(4)