#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import reduce

from ClassPyOpenBrIM import *

fourstorey = Project('The 4 Story Model')
# 1. Materials
steel = Material('Steel1', mat_type="steel", des="steel of girder")
steel.mat_property(d="0", E="209", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
Group('Material Group', steel).attach_to(fourstorey)

# 2. Sections
# 2.0 sec_par
story_num = PrmElmt('Storey_Number', 4)  # 4 storey means 5 plates
height = PrmElmt('Height', 300.0, des='Vertical space between two storeys')
height_top = PrmElmt('Height_top', 270.0, 'Height of the top story')
t_plate = PrmElmt('Thick_plate', 13, 'Thickness of each plate')
l_plate = PrmElmt('Length_plate', 405.0, 'Length of each plate')
w_plate = PrmElmt('Width_plate', 303.0, 'Width of each plate')
d_hole = PrmElmt('D_hole', 6.0, 'Diameter of hols in the plate')
x_interval = PrmElmt('x_hole', 50.0, 'x distance from the edge to the center of hole')
y_interval = PrmElmt('x_hole', 24.0, 'y distance from the edge to the center of hole')
x_num = PrmElmt('ColNumber_holes', 7, 'Column Number of holes')
y_num = PrmElmt('RowNumber_holes', 11, 'Column Number of holes')
t_colm = PrmElmt('Thick_column', 1.0, 'Thickness of each column')
w_colm = PrmElmt('Width_column', 25.0, 'Width of each column')

#         i1      i2      i3      i4      i5
# L4L:    3.15    3.25    7.58    2.27    3.50
# L4R:    3.87    2.24    7.75    2.79    3.70
# L3L:    3.45    2.86    7.61    2.48    3.18
# L3R:    3.90    2.40    7.60    2.70    3.72

in_1 = PrmElmt('Interval_1', 36.2, 'interval from edge to the first column')
in_2 = PrmElmt('Interval_2', 26.8, 'interval from the first column to the second column')
in_3 = PrmElmt('Interval_3', 77.0, 'interval from the first column to the second column')
# the track? maybe not
d_track = PrmElmt('TrackDiameter', 18.0)
h1_track = PrmElmt('h1_track', 23.0)
h2_track = PrmElmt('h2_track', 6.0)
b_track = PrmElmt('Width_track', 49.0)
sec_par_group = Group('Section_Parameters', story_num, height, height_top, t_plate, l_plate, w_plate, d_hole,
                      x_interval, y_interval, x_num, y_num, t_colm, w_colm, in_1, in_2, in_3, d_track, h1_track,
                      h2_track, b_track, )
sec_par_group.attach_to(fourstorey)
# not in OpenBrIM
x_space = (l_plate.value - 2 * x_interval.value) / (x_num.value - 1)
y_space = (w_plate.value - 2 * y_interval.value) / (y_num.value - 1)
total_height = story_num.v * height.v

# 2.1 plate definition
# use ObjTypeDef = 1 to set it as just a definition not an actual object
plate_def = Surface(Point(0, 0),
                    Point(l_plate.value, 0),
                    Point(l_plate.value, w_plate.value),
                    Point(0, w_plate.value),
                    thick_par=t_plate,
                    material_obj=steel,
                    surface_name='PlateDef')
plate_def.add_sub(PrmElmt('ObjTypeDef', 1))
holes = []
for i in range(x_num.value):
    for j in range(y_num.value):
        hole = Circle('hole_{}_{}'.format(i, j), radius=d_hole.value / 2,
                      x=x_interval.value + i * x_space,
                      y=y_interval.value + j * y_space)
        hole.add_sub(PrmElmt('IsCutout', 1))
        holes.append(hole)
plate_def.add_sub(*holes)
plate_def.attach_to(fourstorey)

# 2.2 column
col_rect = Shape('thin column',
                 Point(-w_colm.v / 2, -t_colm.v / 2),
                 Point(w_colm.v / 2, -t_colm.v / 2),
                 Point(w_colm.v / 2, t_colm.v / 2),
                 Point(-w_colm.v / 2, t_colm.v / 2))
col_sec = Section('Column', steel, col_rect)
col_sec.attach_to(fourstorey)
# 2.3 nut
# 2.4 track

# 3. FE elements
# 4. Loading Conditions
# 5. Geometric model
# 5.1 plates
for i in range(story_num.v + 1):
    level = Extends(plate_def)
    level.add_attr(Z=i * height.v)
    level.attach_to(fourstorey)

# 5.2 columns
col_def = Line(Point(0, 0, 0), Point(0, 0, total_height), col_sec, 'ColumnDef')
col_def.add_par('ObjTyepDef',1)
col_def.attach_to(fourstorey)

y_intervals = list(map(lambda e: e.value, [in_1, in_2, in_3, in_2, in_1]))
y_positions=[in_1.v+w_colm.v/2]
for i in range(1,4):
    y_i=y_positions[i-1]+y_intervals[i]+w_colm.v
    y_positions.append(y_i)
print(y_positions)
for x in [0, l_plate.v]:
    for y in y_positions:
        column = Extends(col_def)
        column.add_attr(X=str(x), Y=str(y))
        column.attach_to(fourstorey)
# ---------------
ShowTree(fourstorey)
fourstorey.save_project()
