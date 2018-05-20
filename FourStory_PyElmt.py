#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'YidongQIN'

from PyElement import *
from PySensor import *

fourstoreyPE = ProjGroups('PyElmt 4-Story Model')
# 0. Parameters
story_num = OBPrmElmt('Storey_Number', 4, role='Input')  # 4 storey means 5 plates
height = OBPrmElmt('Height', 300.0, des='Vertical space between two storeys', role='Input')
height_top = OBPrmElmt('Height_top', 270.0, 'Height of the top story', role='Input')
t_plate = OBPrmElmt('t', 13, 'Thickness of each plate', role='Input')
l_plate = OBPrmElmt('l', 405.0, 'Length of each plate', role='Input')
w_plate = OBPrmElmt('w', 303.0, 'Width of each plate', role='Input')
d_hole = OBPrmElmt('d', 6.0, 'Diameter of hols in the plate', role='Input')
x_clear = OBPrmElmt('x_clear', 50.0, 'x clearance from the edge to the hole', role='Input')
y_clear = OBPrmElmt('y_clear', 24.0, 'y clearance from the edge to the hole', role='Input')
x_num = OBPrmElmt('ncol', 7, 'Column Number of holes', role='Input')
y_num = OBPrmElmt('nrow', 11, 'Column Number of holes', role='Input')
t_colm = OBPrmElmt('Thick_column', 1.0, 'Thickness of each column', role='Input')
w_colm = OBPrmElmt('Width_column', 25.0, 'Width of each column', role='Input')
in_1 = OBPrmElmt('Interval_1', 36.2, 'interval from edge to the first column', role='Input')
in_2 = OBPrmElmt('Interval_2', 26.8, 'interval from the first column to the second column', role='Input')
in_3 = OBPrmElmt('Interval_3', 77.0, 'interval from the first column to the second column', role='Input')
# the track? maybe not
d_track = OBPrmElmt('TrackDiameter', 18.0)
h1_track = OBPrmElmt('h1_track', 23.0)
h2_track = OBPrmElmt('h2_track', 6.0)
b_track = OBPrmElmt('Width_track', 49.0)
# sec_par_group = Group('Parameters',
#                       story_num, height, height_top,
#                       t_plate, l_plate, w_plate, d_hole,
#                       x_clear, y_clear, x_num, y_num, t_colm, w_colm,
#                       in_1, in_2, in_3,
#                       d_track, h1_track, h2_track, b_track)
# sec_par_group.attach_to(fourstorey)
# some parameters out XML file
total_height = story_num.v * height.v
y_clears = list(map(lambda e: e.value, [in_1, in_2, in_3, in_2, in_1]))
y_positions = [in_1.v + w_colm.v / 2]
for i in range(1, 4):
    y_i = y_positions[i - 1] + y_clears[i] + w_colm.v
    y_positions.append(y_i)
# 1. Materials
steel = OBMaterial('Steel1', mat_type="steel", des="steel of girder")
steel.mat_property(d="0", E="209", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
OBGroup('Material Group', steel).attach_to(fourstoreyPE)
# 2. Section
# 2.1 column
col_rect = OBShape('rectangle',
                   OBPoint(-w_colm.v / 2, -t_colm.v / 2),
                   OBPoint(w_colm.v / 2, -t_colm.v / 2),
                   OBPoint(w_colm.v / 2, t_colm.v / 2),
                   OBPoint(-w_colm.v / 2, t_colm.v / 2))
col_sec = OBSection('Column', steel, col_rect)
col_sec.attach_to(fourstoreyPE)