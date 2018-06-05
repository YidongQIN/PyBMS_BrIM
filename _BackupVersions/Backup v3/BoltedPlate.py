from PyOpenBrIM import *

proj = OBProject('Bolted Plate', 'template')
t = OBPrmElmt('t', 13, 'Thickness of each plate')
l = OBPrmElmt('l', 405.0, 'Length of each plate')
w = OBPrmElmt('w', 303.0, 'Width of each plate')
d = OBPrmElmt('d', 6.0, 'Diameter of hols in the plate')
x_clear = OBPrmElmt('x_clear', 50.0, 'x clearance from the edge to the hole')
y_clear = OBPrmElmt('y_clear', 24.0, 'y clearance from the edge to the hole')
col_num = OBPrmElmt('ncol', 7, 'Column Number of holes')
row_num = OBPrmElmt('nrow', 11, 'Row Number of holes')
# x_space = PrmElmt('x_space','(l - 2 * x_clear) / (ncol - 1)')
# y_space = PrmElmt('y_space','(w - 2 * y_clear) / (nrow - 1)')
x_sp = (l.v-2*x_clear.v)/(col_num.v-1)
y_sp = (l.v-2*y_clear.v)/(row_num.v-1)
parameters = [t, l, w, d, x_clear, y_clear, col_num, row_num]
proj.sub(*parameters)

plate_def = OBSurface(OBPoint(0, 0),
                      OBPoint(l.v, 0),
                      OBPoint(l.v, w.v),
                      OBPoint(0, w.v),
                      thick_par=t.v,
                      material_obj='steel',
                      surface_name='PlateDef')
# plate_def.sub(PrmElmt('ObjTypeDef', 1))
holes = []

for i in range(col_num.value):
    for j in range(row_num.value):
        hole = OBCircle('hole_{}_{}'.format(i, j),
                        radius=d.value / 2,
                        x=x_clear.value + i * x_sp,
                        y=y_clear.value + j * y_sp)
        hole.sub(OBPrmElmt('IsCutout', 1))
        holes.append(hole)
plate_def.sub(*holes)
plate_def.attach_to(proj)
proj.save_project()
