#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python Elements for BrIM. 
"""

from BMS_BrIM.PyELMT import *


class Parameter(AbstractELMT):

    def __init__(self, prm_id, prm_name, prm_value):
        super(Parameter, self).__init__('Parameter', prm_id, prm_name)
        self.value = prm_value
        self.openBrIM = self.set_openbrim()


class Material(AbstractELMT):
    _DESCRIBE_DICT = dict(d="Density",
                          E="Modulus of Elasticity",
                          a="Coefficient of Thermal Expansion",
                          Nu="Poisson's Ratio",
                          Fc28="Concrete Compressive Strength",
                          Fy="Steel Yield Strength",
                          Fu="Steel Ultimate Strength")

    def __init__(self, mat_id, mat_name, **mat_property):
        """Material name is mandatory. Material Type is Steel, Concrete, etc."""
        super(Material, self).__init__('Material', mat_id, mat_name)
        # self.stage = 'Design'
        # if mat_property:
        self.set_property(**mat_property)
        self.set_openbrim()

    def set_property(self, **mat_property):
        """set the property of material. should use key in:
        [d, E, a, Nu, Fc28, Fy, Fu]"""
        print("Material <{}> property setting:".format(self.name))
        for _k, _v in mat_property.items():
            self.__dict__[_k] = _v
            print("  - {}={}\t".format(_k, _v), end='')
            try:
                print('#', Material._DESCRIBE_DICT[_k])
            except KeyError:
                print("! UnKnown property")

    def get_property(self, property_key):
        try:
            return float(self.__dict__[property_key])
        except KeyError:
            print("{} does not have {}".format(self.name, property_key))
            return

    def show_material_property(self):
        print('# Material Property <{}>'.format(self.name))
        for _k, _v in self.__dict__.items():
            if _v:
                print(' - ', _k, '=', _v)


class Shape(AbstractELMT):
    """Shape is drawn by points. The basic forms are rectangle and circle.
    Shape is stored in the Section doc in MongoDB, not independent."""

    def __init__(self, shape_id, name, shape_form, *args, is_cut=False):
        super(Shape, self).__init__('Shape', shape_id, name)
        # choose a shape form from Rectangle, Circle. Else?
        if shape_form == RectangleOBShape:
            _l = args[0]
            _w = args[1]
            self.set_openbrim(RectangleOBShape, length=_l, width=_w)
        elif shape_form == OBCircle:
            _r = args[0]
            self.set_openbrim(OBCircle, radius=_r)
        else:
            # default shape is polygon, so the parameters are points coordinates.
            self.set_openbrim(PolygonOBShape, points=args)
        if is_cut:
            self.openBrIM.sub(OBPrmElmt("IsCutout", "1"))
        self.is_cutout = is_cut
        # self.set_mongo_doc()


class Section(AbstractELMT):

    def __init__(self, section_id, name, *shapes: Shape):
        super(Section, self).__init__('Section', section_id, name)
        self.sub = shapes
        self.shapesOB = [_.openBrIM for _ in shapes]
        self.shapesID = [_._id for _ in shapes]
        self.set_openbrim(OBSection)
        self.openBrIM.sub(*self.shapesOB)


class Group(AbstractELMT):
    """Container of PyELMT = a OBGroup"""

    def __init__(self, name, *child):
        super(Group, self).__init__('Group', None, name)
        self.openBrIM = OBGroup(name)
        self._sub = list()
        self.append(*child)

    def append(self, *child):
        """get sub nodes, both the PyELMT and the OpenBrIM in self._sub. """
        for _c in child:
            # 1. self._sub.append;
            self._sub.append(_c)
            # 2. self.openBrIM sub();
            if isinstance(_c, AbstractELMT):
                self.openBrIM.sub(_c.openBrIM)
            elif isinstance(_c, PhysicalELMT):
                self.openBrIM.sub(_c.openBrIM['fem'])
                self.openBrIM.sub(_c.openBrIM['geo'])
            else:
                print("Un-acceptable class of ", _c)
                raise TypeError
            # 3. self.mongoDB update it.
            _c.set_dbconfig(self.db_config['database'], self.db_config['table'])
            _c.set_mongo_doc()

    def delete(self, *child):
        for _c in child:
            try:
                self._sub.pop(_c)
                self.openBrIM.del_sub(_c.openBrIM.elmt.tag, **_c.openBrIM.elmt.attrib)
            except TypeError:
                print("! {} cannot delete {}".format(self.name, _c.name))

    def __len__(self):
        return len(self._sub)

    def __iter__(self):
        return iter(self._sub)

    def show_structure(self):
        def tree(elmt, level):
            for _l in range(level):
                print("*    ", end='')
            print("*<{}>, _id={}".format(elmt.name, elmt._id))
            try:
                for _c in elmt:
                    tree(_c, level + 1)
            except AttributeError:
                pass

        tree(self, 0)


class GroupCollection(Group):
    """A project has 6 groups, and these 6 groups are collections(tables) in MongoDB.
    PS: not all groups will be seen in MongoDB."""
    _DESCRIBE_DICT = {
        'basic_info': 'Basic Information about the project',
        'parameter': 'parameters of the model',
        'material': 'all materials',
        'section': 'all sections and shapes',
        'model_fem': 'FEM model, including FENodes, FELines, FESurfaces, etc',
        'model_geometry': 'Geometry Model',
    }

    def __init__(self, name, des=None):
        super(GroupCollection, self).__init__(name)
        self.mongoCollectionName = self.name
        if not des:
            try:
                des = GroupCollection._DESCRIBE_DICT[name]
            except KeyError:
                des = "Unknown Group. A NEW table/Collection in MongoDB."
        self.des = des  # description of the collection as _id=0
        self.db_config['table'] = self.name


class ProjGroups(AbstractELMT):
    """a BrIM Project = Mongo Database = OpenBrIM_Project.
    There should be 6 groups( = collections = tables) where all info is stored.
    """

    def __init__(self, name, template='empty', **db_config):
        """project is a new MongoDB, so no id"""
        super(ProjGroups, self).__init__('Project', elmt_id=0, elmt_name=name)
        # self.template = template
        self.openBrIM = self.set_openbrim(OBProject, **{'template': template})
        # Project cannot append sub, only its groups can
        self._proj_sub_groups()
        # automatically set up the MongoDB config
        self.set_dbconfig(**db_config)
        self._init_mongo_doc()

    def _proj_sub_groups(self):
        self.proj_info = GroupCollection('basic_info')
        self.prm_group = GroupCollection('parameter')
        self.mat_group = GroupCollection('material')
        self.sec_group = GroupCollection('section')
        self.fem_group = GroupCollection('model_fem')
        self.geo_group = GroupCollection('model_geometry')
        self._sub = [self.proj_info, self.prm_group,
                     self.mat_group, self.sec_group,
                     self.fem_group, self.geo_group]
        for _s in self._sub:
            self.openBrIM.sub(_s.openBrIM)
            _s.set_dbconfig(self.name, _s.name)
        return self._sub

    def set_dbconfig(self, database=None, table=None, **db_config):
        """One project = One Mongo Database"""
        super(ProjGroups, self).set_dbconfig(self.name, table=None, **db_config)

    def _init_mongo_doc(self):
        with ConnMongoDB(**self.db_config) as _db:
            for _col in self._sub:
                _db.insert_data(_col.name, _id='InitialCollection', des=_col.des)

    def sub(self, sub_group, *child):
        """Project cannot have sub elements.
        Project only have some tables/collections/GroupCollections.
        Theses GroupCollections will accept docs."""
        try:
            _n = self._sub.index(sub_group)
            self._sub[_n].append(*child)
        except KeyError:
            print("Cannot find this GroupCollection.")
            raise

    def update_mongo(self):
        pass

    def __iter__(self):
        return iter(self._sub)


if __name__ == "__main__":
    print("Test of Py_Abstract")
    print('=====')
