#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
MARC Bridge with sensors.
Input all data into MongoDB.
"""

from BMS_BrIM import *

MARC = ProjGroups("MARC_sensor")
# 0. Parameter
span_num = Parameter(1, "span_num", 11)
x_spacing = Parameter(2, "x_spacing", 108.0)
y_spacing = Parameter(3, "y_spacing", 84)
z_height = Parameter(4, "z_height", 108)
MARC.prm_group.append(span_num, x_spacing, y_spacing, z_height)
# 1. Material
# 1.1 Steel for truss chord
steel = Material(1, 'Steel', d="0.0000007345", E="29000", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
# 1.2 Concrete for deck
concrete = Material(2, 'Concrete', d='0.0000002248', E="3604.9965", a="0.0000055", Fc28="4")
MARC.mat_group.append(steel, concrete)
# 2. Sections
# 2.0 Section Parameters
BottomChord_width = Parameter(11, 'BottomChord_width', 0)
BottomChord_depth = Parameter(12, "BottomChord_depth", 6)
BottomChord_thickness = Parameter(13, "BottomChord_thickness", 0.375)
TopChord_width = Parameter(14, "TopChord_width", 6)
TopChord_depth = Parameter(15, "TopChord_depth", 6)
TopChord_thickness = Parameter(16, "TopChord_thickness", 0.3125)
deck_thick = Parameter(17, "deck_thick", "5")
VertiBeam_width = Parameter(18, "VertiBeam_width", 6)
VertiBeam_depth = Parameter(19, "VertiBeam_depth", 6)
VertiBeam_thickness = Parameter(20, "VertiBeam_thickness", 0.25)
WebRadius = Parameter(21, "WebRadius", 1)
MARC.prm_group.append(BottomChord_width, BottomChord_depth,
                      BottomChord_thickness, TopChord_width,
                      TopChord_depth, TopChord_thickness,
                      deck_thick, VertiBeam_width, VertiBeam_depth,
                      VertiBeam_thickness, WebRadius)
# 2.1 bottom chord 6*6*0.375
sect_bottom=Section()
# 2.2 top chord 6*6*0.3125
# 2.3 vertical chord 6*6*.025
# 2.4 web radius=1
# 3. Nodes
# 4. Structure Elements = Mechanical View
# 5. Equipments = Geometry View
# 6.

ShowTree(MARC.openBrIM)
MARC.prm_group.show_structure()