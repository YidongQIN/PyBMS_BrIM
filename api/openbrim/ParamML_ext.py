#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Further development on ParamML to simplify the input of OpenBrIM/ParamML.
Class structure is same as the ParamML.py, the only difference is that 
these classes are not in ParamML, but 
1. Different shapes for section;
2. Basic forms of members, like straight beam.
'''

import math
from api.openbrim.ParamML import *


class RectangleOBShape(OBShape):
    _REQUIRE = ['name', 'length', 'width']

    def __init__(self, length, width, name):
        self.length = length
        self.width = width
        _point_list = [OBPoint(-width / 2, -length / 2),
                       OBPoint(width / 2, -length / 2),
                       OBPoint(width / 2, length / 2),
                       OBPoint(-width / 2, length / 2)]
        super(RectangleOBShape, self).__init__(name, *_point_list)


class PolygonOBShape(OBShape):
    _REQUIRE = ['name', 'points']

    def __init__(self, name, points):
        _point_list = list()
        for _p in points:
            assert isinstance(_p, tuple) and len(_p) == 2
            _point_list.append(OBPoint(_p[0], _p[1]))
        self.points = points
        super(PolygonOBShape, self).__init__(name, *_point_list)


class CubeGeo(OBVolume):
    """plate with rectangle Surfaces, accept 3 dimension parameters instead of 4 points and a thickness """
    _REQUIRE = ['name', 'length', 'width', 'thick']

    def __init__(self, length, width, thick, name=''):
        self.thick = self.prm_to_value(thick)
        self.length = self.prm_to_value(length)
        self.width = self.prm_to_value(width)
        _surface1_ob = OBSurface(OBPoint(-self.width / 2, -self.length / 2, 0),
                                 OBPoint(self.width / 2, -self.length / 2, 0),
                                 OBPoint(self.width / 2, self.length / 2, 0),
                                 OBPoint(-self.width / 2, self.length / 2, 0))

        _surface2_ob = OBSurface(
            OBPoint(-self.width / 2, -self.length / 2, self.thick),
            OBPoint(self.width / 2, -self.length / 2, self.thick),
            OBPoint(self.width / 2, self.length / 2, self.thick),
            OBPoint(-self.width / 2, self.length / 2, self.thick))
        super(CubeGeo, self).__init__(_surface1_ob, _surface2_ob, name)
        # self.elmt = self.geom().elmt

    def set_basepoint(self, x, y, z):
        """the base point is the center of the first Surface."""
        self.move_to(x, y, z)


class BoltedPlateGeo(OBObjElmt):
    _REQUIRE = ['name', 'length', 'width', 'thick',
                'diameter', 'xclearance', 'yclearance',
                'column', 'row', 'material']

    def __init__(self, name,
                 thick, length, width,
                 diameter, xclearance, yclearance,
                 column, row,
                 material='steel'):
        super(BoltedPlateGeo, self).__init__('Surface', name)
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
        self.elmt = self.geom().elmt

    def geom(self):
        """a Surface Elmt, use real number not parameters"""
        plate_def = OBSurface(OBPoint(0, 0),
                              OBPoint(self.length, 0),
                              OBPoint(self.length, self.width),
                              OBPoint(0, self.width),
                              thick_prm_ob=self.thick,
                              material_ob=self.material,
                              name=self.name)
        holes = []
        for i in range(self.column):
            for j in range(self.row):
                hole = OBCircle('hole_{}_{}'.format(i, j),
                                radius=self.diameter / 2,
                                x=self.xclearance + i * self.x_sp,
                                y=self.yclearance + j * self.y_sp)
                hole.sub(OBPrmElmt('IsCutout', 1))
                holes.append(hole)
        plate_def.sub(*holes)
        return plate_def


class PlateFEM(OBObjElmt):
    """FEM model of plate, either normal plate or bolted plate"""
    _REQUIRE = ['name', 'length', 'width', 'thick']

    def __init__(self, length, width, thick, material, name):
        super(PlateFEM, self).__init__('FESurface', name)
        self.thick = self.prm_to_value(thick)
        self.length = self.prm_to_value(length)
        self.width = self.prm_to_value(width)
        self.material = material
        self.elmt = self.fem().elmt

    def fem(self, *nodes):
        """4 FENodes and then the FESurface"""
        if nodes:
            return OBFESurface(*nodes, thick_prm_ob=self.thick, material_ob=self.material, name=self.name)
        else:
            n1 = OBFENode(-self.width / 2, -self.length / 2, 0, 'N1P_{}'.format(self.name))
            n2 = OBFENode(self.width / 2, -self.length / 2, 0, 'N2P_{}'.format(self.name))
            n3 = OBFENode(self.width / 2, self.length / 2, 0, 'N3P_{}'.format(self.name))
            n4 = OBFENode(-self.width / 2, self.length / 2, 0, 'N4P_{}'.format(self.name))
            fes = OBFESurface(n1, n2, n3, n4, self.thick, self.material, self.name)
            return OBGroup(self.name, n1, n2, n3, n4, fes)


class StraightBeamGeo(OBObjElmt):
    """beam with rectangle cross-section, accept length and 3 direction parameters instead of 2 points"""
    _REQUIRE = ['name', 'length', 'section']

    def __init__(self, length, direction_x, direction_y, direction_z, section, beam_name=''):
        super(StraightBeamGeo, self).__init__('Line', beam_name)
        self.length = self.prm_to_value(length)
        self.cos = direction_cos(direction_x, direction_y, direction_z)
        self.section = section
        self.elmt = self.geom().elmt

    def geom(self):
        line = OBLine(OBPoint(0, 0, 0),
                      OBPoint(self.length * self.cos[0],
                              self.length * self.cos[1],
                              self.length * self.cos[2]),
                      self.section)
        return line


class StraightBeamFEM(OBObjElmt):
    """FEM for rectangle section beam"""
    _REQUIRE = ['name', 'length', 'width', 'thick']

    def __init__(self, length, direction_x, direction_y, direction_z, section, beta_angle=0, beam_name=''):
        super(StraightBeamFEM, self).__init__('FELine', beam_name)
        self.length = self.prm_to_value(length)
        self.cos = direction_cos(direction_x, direction_y, direction_z)
        self.section = section
        self.angle = beta_angle
        self.elmt = self.fem().elmt

    def fem(self, *nodes):
        if nodes:
            return OBFELine(*nodes, section_ob=self.section, beta_angle=self.angle, name=self.name)
        else:
            n1 = OBFENode(0, 0, 0)
            n2 = OBFENode(self.length * self.cos[0], self.length * self.cos[1], self.length * self.cos[2])
            fel = OBFELine(n1, n2, self.section, self.angle, self.name)
            return OBGroup(n1, n2, fel)


class LineCubeOB(OBGroup):

    def __init__(self, line_length, line_radius,
                 cube_length, cube_width, cube_thick, name=''):
        _line = OBLine(OBPoint(-line_length, 0, 0), OBPoint(line_length, 0, 0),
                       section_ob=OBSection('Line', '', OBCircle('', line_radius)))
        _box = CubeGeo(cube_length, cube_width, cube_thick)
        _box.move_to(0, 0, -cube_thick / 2)
        super(LineCubeOB, self).__init__(name, _line, _box)


def direction_cos(x, y, z) -> tuple:
    square_root = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    # cos_x = x / square_root
    # cos_y = y / square_root
    # cos_z = z / square_root
    return x / square_root, y / square_root, z / square_root
