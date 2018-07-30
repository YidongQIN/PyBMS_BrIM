#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

PyOBJ inherits from PyOB->PyPackOB and PyDB, as well as other software like PySAP2K in the future.
and then is used for PyElement, PySensor or PyInspection.

PyOpenBrIM->PyPackOB  PyDatabase  Py_other_interface...
\__________________________________________/
                     |
                   *PyOBJ*
                     |
/------------------------------------------\ 
PyElement   PySensor  PyInspection  Py...

"""

from BMS_BrIM.Py_Abstract import *
from BMS_BrIM.Py_Inspect import *
from BMS_BrIM.Py_Sensor_inLab_OB import *
from BMS_BrIM.Py_Sensor import *



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
