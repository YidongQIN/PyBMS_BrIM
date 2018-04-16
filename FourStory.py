#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyOBobjects import *

fourstorey = Project('The 4 Story Model')
# 0. Parameters
story_num = PrmElmt('Storey_Number', 4)  # 4 storey means 5 plates
height = PrmElmt('Height', 300.0, des='Vertical space between two storeys')
height_top = PrmElmt('Height_top', 270.0, 'Height of the top story')
t_plate = PrmElmt('t', 13, 'Thickness of each plate')
l_plate = PrmElmt('l', 405.0, 'Length of each plate')
w_plate = PrmElmt('w', 303.0, 'Width of each plate')
d_hole = PrmElmt('d', 6.0, 'Diameter of hols in the plate')
x_clear = PrmElmt('x_clear', 50.0, 'x clearance from the edge to the hole')
y_clear = PrmElmt('y_clear', 24.0, 'y clearance from the edge to the hole')
x_num = PrmElmt('ncol', 7, 'Column Number of holes')
y_num = PrmElmt('nrow', 11, 'Column Number of holes')
t_colm = PrmElmt('Thick_column', 1.0, 'Thickness of each column')
w_colm = PrmElmt('Width_column', 25.0, 'Width of each column')
in_1 = PrmElmt('Interval_1', 36.2, 'interval from edge to the first column')
in_2 = PrmElmt('Interval_2', 26.8, 'interval from the first column to the second column')
in_3 = PrmElmt('Interval_3', 77.0, 'interval from the first column to the second column')
# the track? maybe not
d_track = PrmElmt('TrackDiameter', 18.0)
h1_track = PrmElmt('h1_track', 23.0)
h2_track = PrmElmt('h2_track', 6.0)
b_track = PrmElmt('Width_track', 49.0)
# some parameters out XML file
sec_par_group = Group('Section_Parameters',
                      story_num, height, height_top,
                      t_plate, l_plate, w_plate, d_hole,
                      x_clear, y_clear, x_num, y_num, t_colm, w_colm,
                      in_1, in_2, in_3,
                      d_track, h1_track, h2_track, b_track)
sec_par_group.attach_to(fourstorey)
total_height = story_num.v * height.v
y_clears = list(map(lambda e: e.value, [in_1, in_2, in_3, in_2, in_1]))
y_positions = [in_1.v + w_colm.v / 2]
for i in range(1, 4):
    y_i = y_positions[i - 1] + y_clears[i] + w_colm.v
    y_positions.append(y_i)
# 1. Materials
steel = Material('Steel1', mat_type="steel", des="steel of girder")
steel.mat_property(d="0", E="209", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
Group('Material Group', steel).attach_to(fourstorey)
# 2. Section
# 2.1 column
col_rect = Shape('rectangle',
                 Point(-w_colm.v / 2, -t_colm.v / 2),
                 Point(w_colm.v / 2, -t_colm.v / 2),
                 Point(w_colm.v / 2, t_colm.v / 2),
                 Point(-w_colm.v / 2, t_colm.v / 2))
col_sec = Section('Column', steel, col_rect)
col_sec.attach_to(fourstorey)
# 2.2 nut

# 2.4 track

# 3. FE elements
# 4. Loading Conditions
# 5. Geometric model
for i in range(story_num.v + 1):
    oneplate = BoltedPlate('Plate{}'.format(i),
                           t_plate.v, l_plate.v, w_plate.v, d_hole.v, x_clear.v, y_clear.v, x_num.v, y_num.v,
                           steel).as_elmt()
    oneplate.add_attr(Z=i * height.v)
    oneplate.attach_to(fourstorey)

for x in [0, l_plate.v]:
    for y in y_positions:
        onecol = Line(Point(0, 0, 0), Point(0, 0, total_height + 32),
                      col_sec,
                      'Column@{},{}'.format(x, y))
        onecol.add_attr(X=x, Y=y)
        onecol.attach_to(fourstorey)
# ---------------
fourstorey.save_project()
