#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM, including geometry models and FEM models, 
as well as class database. 
Basic flow: PyOpenBrIM ->PyObjects -> PyElmt
as OpenBrIM is still complex for directly used
of course, PyElmt can use PyOB, PyObj just pack some of the classes
'''



from PyOpenBrIM import *


class Plate(Volume):

    def __init__(self, length, width, thick, plate_name=''):
        super(Plate, self).__init__(
            Surface(Point(-width / 2, -length / 2, 0),
                    Point(width / 2, -length / 2, 0),
                    Point(width / 2, length / 2, 0),
                    Point(-width / 2, length / 2, 0)),
            Surface(Point(-width / 2, -length / 2, thick),
                    Point(width / 2, -length / 2, thick),
                    Point(width / 2, length / 2, thick),
                    Point(-width / 2, length / 2, thick)),
            plate_name)


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
        pass

    def as_proj(self):
        """as a template in OpenBrIM Library"""
        plateproj = Project(self.name, 'template')
        plateproj.sub(self.geom())
        self.elmt = plateproj
        return plateproj

