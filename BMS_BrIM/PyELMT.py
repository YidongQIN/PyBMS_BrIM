#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
PyELMT gets all interfaces' methods.
Each PyELMT has 3 kinds of attributes:
1. distinguished naming: type and _id.
2. characteristic attr: depends on element typy.
    For example, Material will have E=elastic modulel, d=density, etc.
    Whie Parameter will only have a value.
3. Interfaces, including a OpenBrIM interface, a MongoDB interface so far.
    Each Interface will be a combination of setter() and getter().
"""

from Interfaces import *


class PyELMT(object):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """Basic mandatory attributes of PyELMT are type, id;
        the optional attribute is name."""
        self._id = elmt_id
        self.type = elmt_type
        if elmt_name:
            self.name = elmt_name
        else:
            self.name = elmt_type + '_' + str(elmt_id)
        # two interfaces: Database and OpenBrIM
        self.db_config = dict()  # dict(database=, table=, user=,...)
        self.openBrIM: dict or PyOpenBrIMElmt  # dict of eET.elements

    def set_openbrim(self, ob_class: (OBPrmElmt, OBObjElmt), **attrib_dict: dict):
        """attrib_dict is used to add other redundancy info,
        so don't update the element.__dict__ with it."""
        # get attributes required by the OpenBrIM type
        _required_attr: dict = _attr_pick(self, *ob_class._REQUIRE)
        # _openbrim_attrib = {**_required_attr, **attrib_dict}
        try:
            _ob_model: PyOpenBrIMElmt = ob_class(**_required_attr, **attrib_dict)
            return _ob_model
        except TypeError as e:
            print("TypeError: <{}>.set_openbrim()".format(self.name), e)
            return

    def get_openbrim(self, model_class: str = None):
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

    def update_attr(self, **attributes_dict: dict):
        for _k, _v in attributes_dict.items():
            try:
                if not _v == self.__dict__[_k]:
                    print('<{}> changed by update()'.format(self.name))
                    print('* {} -> {}'.format(_k, _v))
            except KeyError:
                print("<{}> new attribute by update()".format(self.name))
                print('* {} -> {}'.format(_k, _v))
            self.__dict__[_k] = _v

    def _set_mysql_config(self, database, user, password, host='localhost', port=3306, **kwargs):
        """get db config and connect to MySQL"""
        self.db_config = {'user': user, 'password': password, 'database': database,
                          'host': host, 'port': port}
        if 'table' not in kwargs.keys():
            print('The table/collection name is needed')
        self.db_config['table'] = kwargs['table']

    def link_elmt(self, attrib, elmt):
        """link the PyELMT to another PyELMT."""
        self.__dict__[attrib] = elmt
        self.__dict__["{}_ob".format(attrib)] = elmt.openBrIM
        self.__dict__["{}_id".format(attrib)] = elmt._id
        """
        option #1, only one attribute is linked, the PyELMT. Then in the set_openbrim() method, use a try...block to find corresponding ob node.
        #2, in the interfaces.__init__, create a new class, much like the PyOpenBrIM, to accept the OB type and variables together.
        """


class Document(object):
    """Document only store in MongoDB or file, no OpenBrIm eET.
    The class name is not sure yet."""

    def __init__(self, name: str, id: int = None, des: str = None):
        self.name = name
        self._id = id
        if des:
            self.des = des

    # def update_attr(self, **attributes_dict):
    #     for _k, _v in attributes_dict.items():
    #         try:
    #             if not _v == self.__dict__[_k]:
    #                 print('<{}> changed by update()'.format(self.name))
    #                 print(' .{} -> {}'.format(_k, _v))
    #         except KeyError:
    #             print("<{}> new attribute by update()".format(self.name))
    #             print(' .{} -> {}'.format(_k, _v))
    #         self.__dict__[_k] = _v


def _attr_pick(elmt, *pick_list):
    """keys are from the pick_list, and find corresponding attributes from the element.__dict__."""
    _d = dict()
    for _pick in pick_list:
        try:
            _d[_pick] = elmt.__dict__[_pick]
        except KeyError:
            # print("PyELMT._attr_pick(): No '{}' in {}".format(_pick, elmt.name))
            pass
    return _d


def _attr_pop(elmt, *pop_list):
    """pop attributes whose key is in the list, return the rest ones."""
    _d = dict()
    for _k, _v in elmt.__dict__.items():
        if (_k not in pop_list) and _v:
            _d[_k] = _v
    return _d


def _attr_to_mongo_dict(elmt: PyELMT):
    """dump some of the attributes to dict."""

    def is_unacceptable(one_item):
        """object whose type is unaccecptable, like PyELMT or PyOpenBrIMElmt,
        cannot be encoded into mongoDB."""
        _unaccept_type = (PyELMT, PyOpenBrIMElmt)
        if isinstance(one_item, _unaccept_type):
            return True
        return False

    def should_pop(attribute_value):
        """attributes of PyELMT is complex.
        If the elmt.attribute is only one object, judge it by is_unacceptable();
        If the elmt.attribute is a collection (tuple or list, like shapes in Section), judge by its element(s)."""
        if isinstance(attribute_value, (tuple, list)):
            _to_list = list(attribute_value)
            return is_unacceptable(_to_list[0])
        return is_unacceptable(attribute_value)

    def _pop_list(elmt):
        """typically, the _pop_list =['openBrIM', 'db_config',
        'section_ob', 'section','material_ob', 'material',
        'thick_prm_ob', 'thick_prm','shape', 'shape_ob',
        'node1', 'node1_ob','node2', 'node2_ob']"""
        _pop_key = ['db_config', 'openBrIM']
        for _k, _v in elmt.__dict__.items():
            if should_pop(_v):
                _pop_key.append(_k)
        _pop_key = list(set(_pop_key))
        return _pop_key

    _after_pop = _attr_pop(elmt, *_pop_list(elmt))
    return _after_pop

# def parameter_format(k):
#     if isinstance(k, int):
#         return k
#     elif isinstance(k, float):
#         try:
#             return int(k)
#         except ValueError:
#             return k
#     elif isinstance(k, str):
#         try:
#             return float(k)
#         except ValueError:
#             return k
#     else:
#         from BMS_BrIM.Py_Abstract import Parameter
#         if isinstance(k, Parameter):
#             return k.value
#         else:
#             print("Error formatting parameter")
#             print(type(k))
#             return

# class XY(object):
#     def __init__(self, x=0, y=0):
#         if x is not None:
#             self.x = parameter_format(x)
#         if y is not None:
#             self.y = parameter_format(y)
#
#
# class XYZ(object):
#
#     def __init__(self, x=0, y=0, z=0):
#         if x is not None:
#             self.x = parameter_format(x)
#         if y is not None:
#             self.y = parameter_format(y)
#         if z is not None:
#             self.z = parameter_format(z)
#
#
# class RXYZ(object):
#
#     def __init__(self, rx=0, ry=0, rz=0):
#         self.rx = rx
#         self.ry = ry
#         self.rz = rz
