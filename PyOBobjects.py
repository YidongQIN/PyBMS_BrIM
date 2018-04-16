#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM
'''

from PyOpenBrIM import *


class bolted_plate(ObjElmt):

    def __init__(self, plate_name, thick, length, width, diameter, xclearance, yclearance, column, row, material='steel'):
        super(bolted_plate, self).__init__('Surface', plate_name)
        self.thick = thick
        self.length = length
        self.width = width
        self.diameter = diameter
        self.xclearance = xclearance
        self.yclearance = yclearance
        self.column = column
        self.row = row
        self.material = material
        self.x_sp = (length - 2 * xclearance) / (column - 1)
        self.y_sp = (length - 2 * yclearance) / (row - 1)

    def as_elmt(self):
        ''' as a Surface Elmt'''
        self.update(T='Surface')
        plate_def = Surface(Point(0, 0),
                            Point(self.length, 0),
                            Point(self.length, self.width),
                            Point(0, self.width),
                            thick_par=self.thick,
                            material_obj=str(self.material),
                            surface_name=self.name)
        holes = []
        for i in range(self.column):
            for j in range(self.row):
                hole = Circle('hole_{}_{}'.format(i, j), radius=self.diameter / 2,
                              x=self.xclearance + i * self.x_sp,
                              y=self.yclearance + j * self.y_sp)
                hole.sub(PrmElmt('IsCutout', 1))
                holes.append(hole)
        plate_def.sub(*holes)
        return plate_def

    def as_proj(self):
        '''as a template in OpenBrIM Library'''
        plateproj = Project(self.name, 'template')
        t = PrmElmt('t', self.thick, 'Thickness of each plate')
        l = PrmElmt('l', self.length, 'Length of each plate')
        w = PrmElmt('w', self.width, 'Width of each plate')
        d = PrmElmt('d', self.diameter, 'Diameter of each hole')
        x_clear = PrmElmt('x_clear', self.xclearance, 'x clearance from the edge to the hole')
        y_clear = PrmElmt('y_clear', self.yclearance, 'y clearance from the edge to the hole')
        col_num = PrmElmt('ncol', self.column, 'Column Number of holes')
        row_num = PrmElmt('nrow', self.row, 'Row Number of holes')
        plateproj.sub(t, l, w, d, x_clear, y_clear, col_num, row_num)
        plateproj.sub(self.as_elmt())
        return plateproj
