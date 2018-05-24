#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python Elements for BrIM. 
"""

from PyOBJ import *


class ProjGroups(OBProject, PyAbst):

    def __init__(self, proj_name, template = 'empty'):
        super(ProjGroups, self).__init__(proj_name, template)
        self.prm_group = OBGroup('Parameter Group')
        self.mat_group = OBGroup('Material Group')
        self.sec_group = OBGroup('Section Group')
        self.geo_group = OBGroup('Geometry Model')
        self.fem_group = OBGroup('FEM Model')
        self.sub(self.prm_group, self.mat_group, self.sec_group, self.geo_group, self.fem_group)

    def include(self, *members:PyElmt):
        """ add one member to the project"""
        #@TODO PyAbst and PyReal are different
        for member in members:
            try:
                self.fem_group.sub(member.model_fem)
                self.geo_group.sub(member.model_geo)
                # self.
            except BaseException as e:
                print('= = Some error about {} has been ignored'.format(member.name))
                print(e)


class Material(PyAbst):

    def __init__(self, mat_id, mat_name):
        super(Material, self).__init__('Material',mat_id, mat_name)
        print(self.name)

    # @property
    # def name(self):
    #     # super(Material, self).name(self.mat_name)
    #     return self.mat_name


'''
        class OBMaterial(OBObjElmt):
    def __init__(self, mat_name, des='', mat_type='', **attrib_dict):
        """Material name is mandatory.\n
        Material Type is Steel, Concrete, etc. Type is not T as T='Material'.\n
        there may be no other attributes.
        """
        super(OBMaterial, self).__init__('Material', mat_name, D=des, Type=mat_type, **attrib_dict)
'''

class Beam(PyReal):

    def __init__(self, beam_id):
        # init no so many parameters, put the points and nodes to set_model() methods
        super(Beam, self).__init__('BEAM', beam_id)
        self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = [None] * 6

    def set_points(self, *points):
        if len(points) == 2:
            if isinstance(points[0], OBPoint) and isinstance(points[1], OBPoint):
                self.two_point(*points)
            elif isinstance(points[0], OBFENode) and isinstance(points[1], OBFENode):
                self.two_node(*points)
        elif len(points) == 6:
            for a in points:
                if not isinstance(a, (float, int)):
                    print("Beam {}'s Coordinates must be numbers".format(self.id))
            self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = points
        # self.geo_xml(Point(self.x1, self.y1, self.z1), Point(self.x2, self.y2, self.z2), section=self.section)
        # self.fem_xml(FENode(self.x1, self.y1, self.z1), FENode(self.x2, self.y2, self.z2), section=self.section)
        # Line() material is included in section definition

    def two_point(self, point1, point2):
        self.x1 = point1.x
        self.y1 = point1.x
        self.z1 = point1.x
        self.x2 = point2.x
        self.y2 = point2.x
        self.z2 = point2.x

    def two_node(self, node1, node2):
        self.x1 = node1.x
        self.y1 = node1.x
        self.z1 = node1.x
        self.x2 = node2.x
        self.y2 = node2.x
        self.z2 = node2.x

    def coordinates(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2


class Plate(PyReal):

    def __init__(self, plate_id):
        super(PyReal, self).__init__('Plate', plate_id)