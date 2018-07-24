#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
MARC Bridge with sensors.
"""

from BMS_BrIM import *

MARC = ProjGroups("MARC_sensor")
# 0. Parameter
span_num = Parameter(1,"span_num", 11)
x_spacing = Parameter(2, "x_spacing", 108.0)
y_spacing = Parameter(3, "y_spacing", 84)
z_height = Parameter(4, "z_height", 108)
MARC.prm_group.append(span_num, x_spacing, y_spacing, z_height)
x_spacing.set_dbconfig('MARC_sensor', 'parameter')
x_spacing.set_mongo_doc()
# 1. Material
# 1.1 Steel for truss chord
# 1.2 Concrete for deck
# 2. Sections
# 2.1 bottom chord 6*6*0.375
# 2.2 top chord 6*6*0.3125
# 2.3 vertical chord 6*6*.025
# 2.4 web radius=1
# 3. Nodes
# 4. Structure Elements = Mechanical View
# 5. Equipments = Geometry View
# 6.

ShowTree(MARC.openBrIM)
