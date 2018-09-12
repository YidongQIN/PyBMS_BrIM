#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
main code for the _PyBMS_BrIM program.
"""
from BMS_BrIM.PyELMT import *
from BMS_BrIM.Py_Abstract import *
from BMS_BrIM.Py_Physical import *
from BMS_BrIM.Py_Inspect import *
from BMS_BrIM.Py_Sensor import *
# from BMS_BrIM.Py_Sensor_inLab_OB import *



if __name__ == '__main__':
    project = ProjGroups
    inspect = Inspection
    sensor = Sensor
    print("Now using ELMT_ALL.py, all available classes are:")
    available = dir()
    to_del = []
    for i in available:
        if i[0] == '_':
            to_del.append(i)
    for d in to_del:
        available.remove(d)
    print(available)
    print('======')
