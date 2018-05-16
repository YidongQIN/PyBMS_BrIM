#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM, including geometry models and FEM models, 
Basic flow: PyOpenBrIM ->PyObjects -> PyElmt
as OpenBrIM is still complex for directly used
of course, PyElmt can use PyOB, PyObj just pack some of the classes.

'''

import math

from PyOpenBrIM import *


class CubeGeo(ObjElmt):
    """plate with rectangle Surfaces, accept 3 dimension parameters instead of 4 points and a thickness """

    def __init__(self, length, width, thick, cube_name=''):
        super(CubeGeo, self).__init__('Volume', cube_name)
        self.thick = self.prm_to_value(thick)
        self.length = self.prm_to_value(length)
        self.width = self.prm_to_value(width)
        self.model = self.geom()

    def set_basepoint(self, x, y, z):
        """the base point is the center of the first Surface."""
        self.model.move_to(x, y, z)

    def geom(self):
        plate_geomodel = Volume(
            Surface(Point(-self.width / 2, -self.length / 2, 0),
                    Point(self.width / 2, -self.length / 2, 0),
                    Point(self.width / 2, self.length / 2, 0),
                    Point(-self.width / 2, self.length / 2, 0)),
            Surface(Point(-self.width / 2, -self.length / 2, self.thick),
                    Point(self.width / 2, -self.length / 2, self.thick),
                    Point(self.width / 2, self.length / 2, self.thick),
                    Point(-self.width / 2, self.length / 2, self.thick)))
        return plate_geomodel


class BoltedPlateGeo(ObjElmt):

    def __init__(self, plate_name,
                 thick, length, width,
                 diameter, xclearance, yclearance,
                 column, row,
                 material='steel'):
        super(BoltedPlateGeo, self).__init__('Surface', plate_name)
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
        self.model = self.geom()

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


class PlateFEM(ObjElmt):
    """FEM model of plate, either normal plate or bolted plate"""

    def __init__(self, length, width, thick, material):
        """parameters should be nodes or? if nodes, what is the difference with FESurface?"""
        # @TODO FEM model needs nodes, not parameters
        super(PlateFEM, self).__init__('FESurface')
        self.thick = self.prm_to_value(thick)
        self.length = self.prm_to_value(length)
        self.width = self.prm_to_value(width)
        self.material = material

    def set_node(self, x, y, z):
        self.sub(FENode(x, y, z))

    def link_node(self, node: FENode):
        self.sub(node)


class StraightBeamGeo(ObjElmt):
    """beam with rectangle Surfaces, accept length and 3 direction parameters instead of 2 points"""

    def __init__(self, length, direction_x, direction_y, direction_z, section, beam_name=''):
        super(StraightBeamGeo, self).__init__('Line', beam_name)
        self.length = self.prm_to_value(length)
        self.cos = direction_cos(direction_x, direction_y, direction_z)
        self.section = section
        self.model = self.geom()

    def geom(self):
        line = Line(Point(0, 0, 0), Point(self.length*self.cos[0],
                                          self.length*self.cos[1],
                                          self.length*self.cos[2]),
                    self.section)
        return line


def direction_cos(x, y, z)->tuple:
    square_root = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
    cos_x = x / square_root
    cos_y = y / square_root
    cos_z = z / square_root
    return cos_x, cos_y, cos_z
