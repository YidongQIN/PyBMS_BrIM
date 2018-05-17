#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python Elements for BrIM. 
"""

from PyDatabase import *
from PyPackObj import *


class PyElmt(object):
    """PyElmt is used to represent real members of bridges
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, obj_type, obj_id):
        self.id = obj_id
        self.type = obj_type
        self.name = '{}_{}'.format(self.type, self.id)
        # may the 2 parameter be enough to define the element?
        self.geo_class: ObjElmt
        self.fem_class: ObjElmt
        self.section: str
        # self.material: str
        self.dbconfig = None
        # self.description: str

    def init_by_db(self):
        pass

    def init_by_io(self):
        pass

    def read_db(self):
        pass

    # def conn_db(self, db_config):
    #     """user, passwd, host, database, port"""
    #     self.dbconfig = dict(db_config)  # copy a dict
    #     db = ConnMySQL(**self.dbconfig)
    #     sql = 'select {} from bridge_test.{} where sensorID ={}'.format(", ".join(col_names), tbname, self.id)
    #     db.query(sql)
    #     info = db.fetch_row()
    #     db.close()
    #     return info

    def set_attr_value(self):
        pass

    @property
    def material(self):
        return self.material

    @material.setter
    def material(self, mat: (Material, Extends, str)):
        self.material = mat

    def set_section(self, section: (Section, str)):
        self.section = section

    # def geo_xml(self, *define, **dicts):
    #     self.geomodel = self.geo_class(*define, **dicts)
    #
    # def fem_xml(self, *define, **dicts):
    #     self.femodel = self.fem_class(*define, **dicts)
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, des):
        self._description = des


class Beam(PyElmt):

    def __init__(self, beam_id):
        # init no so many parameters, put the points and nodes to set_model() methods
        super(Beam, self).__init__('BEAM', beam_id, Line, FELine)

    def set_points(self, *points, section):
        if len(points) == 2:
            if isinstance(points[0], Point) and isinstance(points[1], Point):
                self.two_point(*points)
            elif isinstance(points[0], FENode) and isinstance(points[1], FENode):
                self.two_node(*points)
        elif len(points) == 6:
            for a in points:
                if not isinstance(a, (float, int)):
                    print("Beam {}'s Coordinates must be numbers".format(self.id))
            self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = points
        self.section = section
        self.geo_xml(Point(self.x1, self.y1, self.z1), Point(self.x2, self.y2, self.z2), section=self.section)
        self.fem_xml(FENode(self.x1, self.y1, self.z1), FENode(self.x2, self.y2, self.z2), section=self.section)
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


class Plate(PyElmt):

    def __init__(self, plate_id):
        super(PyElmt, self).__init__('Plate', plate_id, Surface, FESurface)
        pass