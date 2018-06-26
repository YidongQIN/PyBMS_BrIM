#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
PyELMT gets all interfaces' methods

"""
from Interfaces import *


# from Interfaces.BrDatabase import *
# from Interfaces.BrOpenBrIM import *


class PyElmt(object):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """Basic attributes for a PyELMT is type, id.
        name is optional, as well as description.
        Each interface has a corresponding attribute"""
        self.id = elmt_id
        self.type = elmt_type
        if elmt_name:
            self.name = elmt_name
        else:
            self.name = elmt_type + '_' + str(elmt_id)
        # two interfaces: Database and OpenBrIM
        self.db_config: dict = dict()  # dict(database=, table=, user=,...)
        self.openBrIM: dict = dict()  # dict of eET.elements
        self.des: str = None

    def set_mongo_doc(self):
        """write info into the mongo.collection.document"""
        with ConnMongoDB(**self.db_config) as _db:
            _db.update_data(self.db_config['table'], self.id,
                            **self._attr_to_mongo_dict(self))

    def get_mongo_doc(self):
        with ConnMongoDB(**self.db_config) as _db:
            _result = _db.find_by_kv(self.db_config['table'], '_id', self.id)
            _newattr = self._mongo_id_to_self_id(_result)
            self.check_update_attr(**_newattr)
            return _newattr

    def set_openbrim(self, model_class, ob_class, **attrib_dict):
        """create a OpenBrim object, in fact an eET.element"""
        _model: PyOpenBrIMElmt = ob_class(**attrib_dict)
        assert model_class in ['fem', 'geo', 'abst']
        self.openBrIM[model_class] = _model
        return _model

    def get_openbrim(self, model_class):
        if not model_class:
            return self.openBrIM
        else:
            try:
                return self.openBrIM[model_class]
            except KeyError:
                print("{} has no OpenBrIM model of {}".format(self.name, model_class))
                return

    def set_sap2k(self):
        pass

    def get_sap2k(self):
        pass

    #
    def check_update_attr(self, **attributes_dict):
        for _k, _v in attributes_dict.items():
            try:
                if not _v == self.__dict__[_k]:
                    print('!Attribute changed! {}.{}->{}'.format(self.name, _k, _v))
            except KeyError:
                pass
            self.__dict__[_k] = _v

    def set_dbconfig(self, database, table, **db_config):
        db_config['database'] = database
        db_config['table'] = table
        if self.type == 'Sensor':  # for now, only Sensor use MySQL
            self._set_mysql_config(**db_config)
        else:
            self._set_mongo_config(**db_config)

    def _set_mongo_config(self, database, table, host='localhost', port=27017):
        """get db config and connect to MongoDB"""
        self.db_config = {'host': host, 'port': port, 'database': database, 'table': table}

    def _set_mysql_config(self, database, user, password, host='localhost', port=3306, **kwargs):
        """get db config and connect to MySQL"""
        self.db_config = {'user': user, 'password': password, 'database': database,
                          'host': host, 'port': port}
        if 'table' not in kwargs.keys():
            print('The table/collection name is needed')
        self.db_config['table'] = kwargs['table']

    def describe(self, des):
        """describe, attached documents, etc"""
        assert isinstance(des, str)
        self.des = des

    @staticmethod
    def _attr_pop(elmt, *pop_list):
        _d = dict(elmt.__dict__.items())
        for _pop in pop_list:
            try:
                _d.pop(_pop)
            except KeyError:
                print("No {} in the attributes of {}".format(_pop, elmt.name))
        return _d

    @staticmethod
    def _attr_pick(elmt, *pick_list):
        """keys are from the pick_list, and find corresponding attributes from the element__dict__.
        return a dict"""
        _d = dict()
        for _pick in pick_list:
            try:
                _d[_pick] = elmt.__dict__[_pick]
            except KeyError:
                pass
        return _d

    @staticmethod
    def _attr_to_mongo_dict(elmt):
        """dump some of the attributes to dict.
        the default pop out list is: 'openbrim','db_config'. """
        return AbstractELMT._attr_pop(elmt, 'id', 'openbrim', 'db_config')

    @staticmethod
    def _mongo_id_to_self_id(doc: dict):
        """change the field(key) '_id' to 'id'. """
        _d = {**doc}
        _d['id'] = _d['_id']
        _d.pop('_id')
        return _d


class AbstractELMT(PyElmt):
    _DICT_OPENBRIM_CLASS = dict(Project=OBProject,
                                Parameter=OBPrmElmt,
                                Shape=OBShape,
                                Section=OBSection,
                                Group=OBGroup,
                                Unit=OBUnit,
                                Text=OBText3D)

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """abstract elements, such as material, section, load case"""
        super(AbstractELMT, self).__init__(elmt_type, elmt_id, elmt_name)

    def set_openbrim(self, model_class='abst', ob_class=None, **attrib_dict):
        if not ob_class:
            ob_class = AbstractELMT._DICT_OPENBRIM_CLASS[self.type]
        return super(AbstractELMT, self).set_openbrim(model_class, ob_class, **attrib_dict)


class PhysicalELMT(PyElmt):
    """PhysicalELMT is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""
    _DICT_FEM_CLASS = dict(Node=OBFENode,
                           Line=OBFELine,
                           Beam=StraightBeamFEM,
                           Truss=StraightBeamFEM,
                           Surface=OBFESurface,
                           BoltedPlate=OBFESurface,
                           Volume=OBVolume)
    _DICT_GEO_CLASS = dict(Node=OBPoint,
                           Line=OBLine,
                           Beam=OBLine,
                           Truss=OBLine,
                           Surface=OBSurface,
                           BoltedPlate=BoltedPlateGeo,
                           Volume=OBVolume)

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """real members of structure"""
        super(PhysicalELMT, self).__init__(elmt_type, elmt_id, elmt_name)
        # geometry info:
        self.position = XYZ()
        self.direction = RXYZ()  # local coordinate system
        self.dimension = dict()
        self.section = None
        # physical info: material
        self.material = None

    # may not use the below

    def set_position(self, x=0, y=0, z=0):
        self.position.x = x
        self.position.y = y
        self.position.z = z

    def set_direction(self, **drc):
        for k in drc:
            if k not in ['dx', 'dy', 'dz']:
                print('= = Direction of {} is recommended to be dx,dy,dz'.format(self.name))
        self.direction = drc

    def set_dimension(self, **dims):
        for k in dims:
            if k not in ['length', 'width', 'thick']:
                print('= = Dimension of {} is recommended to be length, width, thick, etc'.format(self.name))
        self.dimension = dims


def parameter_format(k):
    if isinstance(k, int):
        return k
    elif isinstance(k, float):
        try:
            return int(k)
        except ValueError:
            return k
    elif isinstance(k, str):
        try:
            return float(k)
        except ValueError:
            return k
    else:
        from BMS_BrIM.Py_Design import Parameter
        if isinstance(k, Parameter):
            return k.value
        else:
            print("Error formatting parameter")
            print(type(k))
            return


class XY(object):
    def __init__(self, x=0, y=0):
        if x is not None:
            self.x = parameter_format(x)
        if y is not None:
            self.y = parameter_format(y)


class XYZ(object):

    def __init__(self, x=0, y=0, z=0):
        if x is not None:
            self.x = parameter_format(x)
        if y is not None:
            self.y = parameter_format(y)
        if z is not None:
            self.z = parameter_format(z)


class RXYZ(object):

    def __init__(self, rx=0, ry=0, rz=0):
        self.rx = rx
        self.ry = ry
        self.rz = rz
