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
        self.thick = self.prm_to_value(thick)
        self.length = self.prm_to_value(length)
        self.width = self.prm_to_value(width)
        self.diameter = self.prm_to_value(diameter)
        self.xclearance = self.prm_to_value(xclearance)
        self.yclearance = self.prm_to_value(yclearance)
        self.column = self.prm_to_value(column)
        self.row = self.prm_to_value(row)
        self.material = material
        self.x_sp = (self.length - 2 * self.xclearance) / (self.column - 1)
        self.y_sp = (self.width - 2 * self.yclearance) / (self.row - 1)
        # self.Pthick = self.prm_to_name(thick)
        # self.Plength = self.prm_to_name(length)
        # self.Pwidth = self.prm_to_name(width)
        # self.Pdiameter = self.prm_to_name(diameter)
        # self.Pxclearance = self.prm_to_name(xclearance)
        # self.Pyclearance = self.prm_to_name(yclearance)
        # self.Pcolumn = self.prm_to_name(column)
        # self.Prow = self.prm_to_name(row)

    def geom(self):
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

    def fem(self):
        """FEM is totally different from geometry model.
        it needs Nodes, not only Points: both coordinates(x,y,z)and fixity,
        and connection with other elements. """
        pass

    def as_proj(self):
        """as a template in OpenBrIM Library"""
        plateproj = Project(self.name, 'template')
        plateproj.sub(self.geom())
        self.elmt = plateproj
        return plateproj

    # def as_prmodel(self):
    #     """to generate a ParamML model that can be modified in the APP.
    #     *** GIVEN UP
    #     the REPEAT in ParamML is complex, so that the row number and the column number is nut parameterized"""
    #     paramodel = Surface(Point(0, 0),
    #                         Point('lengthOfPlate', 0),
    #                         Point('lengthOfPlate', 'widthOfPlate'),
    #                         Point(0, 'widthOfPlate'),
    #                         thick_par='thickOfPlate',
    #                         material_obj=self.material,
    #                         surface_name=self.name)
    #     holes = []
    #     for i in range(self.column):
    #         for j in range(self.row):
    #             hole = Circle('hole_{}_{}'.format(i, j),
    #                           radius='diaOfHole/2',
    #                           x='x_clearOfHole + ' + str(i * self.x_sp),
    #                           y='y_clearOfHole + ' + str(j * self.y_sp))
    #             hole.sub(PrmElmt('IsCutout', 1))
    #             holes.append(hole)
    #     paramodel.sub(*holes)
    #     t = PrmElmt('thickOfPlate', self.Pthick, 'Thickness of each plate')
    #     l_p = PrmElmt('lengthOfPlate', self.Plength, 'Length of each plate')
    #     w = PrmElmt('widthOfPlate', self.Pwidth, 'Width of each plate')
    #     d = PrmElmt('diaOfHole', self.Pdiameter, 'Diameter of each hole')
    #     x_clear = PrmElmt('x_clearOfHole', self.Pxclearance, 'x clearance from the edge to the hole')
    #     y_clear = PrmElmt('y_clearOfHole', self.Pyclearance, 'y clearance from the edge to the hole')
    #     paramodel.sub(t, l_p, w, d, x_clear, y_clear)  # , col_num, row_num)
    #     return paramodel


