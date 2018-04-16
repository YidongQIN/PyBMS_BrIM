#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM
'''

from PyOpenBrIM import *


class BoltedPlate(ObjElmt):

    def __init__(self, plate_name,
                 thick, length, width,
                 diameter, xclearance, yclearance,
                 column, row,
                 material='steel'):
        super(BoltedPlate, self).__init__('Surface', plate_name)
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
        self.as_prmodel()

    def as_elmt(self):
        """a Surface Elmt, use real number not parameters"""
        plate_def = Surface(Point(0, 0),
                            Point(self.length, 0),
                            Point(self.length, self.width),
                            Point(0, self.width),
                            thick_par=self.thick,
                            material_obj=self.material,
                            surface_name=self.name)
        holes = []
        for i in range(self.column):
            for j in range(self.row):
                hole = Circle('hole_{}_{}'.format(i, j),
                              radius=self.diameter / 2,
                              x=self.xclearance + i * self.x_sp,
                              y=self.yclearance + j * self.y_sp)
                hole.sub(PrmElmt('IsCutout', 1))
                holes.append(hole)
        plate_def.sub(*holes)
        return plate_def

    def as_prmodel(self):
        """to generate a ParamML model that can be modified in the APP.
        the REPEAT in ParamML is complex, so that the row number and the column number is nut parameterized"""
        paramodel = Surface(Point(0, 0),
                            Point('l', 0),
                            Point('l', 'w'),
                            Point(0, 'w'),
                            thick_par='t',
                            material_obj=self.material,
                            surface_name=self.name)
        holes = []
        for i in range(self.column):
            for j in range(self.row):
                hole = Circle('hole_{}_{}'.format(i, j),
                              radius='d/2',
                              x='x_clear + ' + str(i * self.x_sp),
                              y='y_clear + ' + str(j * self.y_sp))
                hole.sub(PrmElmt('IsCutout', 1))
                holes.append(hole)
        paramodel.sub(*holes)
        t = PrmElmt('t', self.thick, 'Thickness of each plate', role='Input')
        l_p = PrmElmt('l', self.length, 'Length of each plate', role='Input')
        w = PrmElmt('w', self.width, 'Width of each plate', role='Input')
        d = PrmElmt('d', self.diameter, 'Diameter of each hole', role='Input')
        x_clear = PrmElmt('x_clear', self.xclearance, 'x clearance from the edge to the hole', role='Input')
        y_clear = PrmElmt('y_clear', self.yclearance, 'y clearance from the edge to the hole', role='Input')
        # col_num = PrmElmt('ncol', self.column, 'Column Number of holes')
        # row_num = PrmElmt('nrow', self.row, 'Row Number of holes')
        paramodel.sub(t, l_p, w, d, x_clear, y_clear)  # , col_num, row_num)
        return paramodel

    def as_proj(self):
        """as a template in OpenBrIM Library"""
        plateproj = Project(self.name, 'template')
        plateproj.sub(self.as_elmt())
        self.elmt = plateproj
