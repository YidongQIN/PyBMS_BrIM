#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
This is the toolbox for Interfaces classes.
"""
import json


# 1. I/O function
def input(elmt, source, data_format):
    """read a file or a string"""

    def input_file(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    def input_json(json_str):
        _d = json.loads(json_str)
        return _d

    def input_xml(xmi_str):
        return xmi_str

    if data_format == "file":
        elmt.loads(input_file(source))
    elif data_format == "json":
        elmt.loads(input_json(source))
    elif data_format == "xml":
        elmt.loads(input_xml(source))
    else:
        print("Unknown Data format")


def output(elmt, file_path):
    """write the attributes into JSON"""
    _j = json.dumps(elmt.__dict__, indent=2)
    with open(file_path, 'w') as _f:
        _f.write(_j)


def dumps(self):
    """dump self.__dict__ to str"""
    pass


def loads(self, data):
    """load other data format to dict"""
    pass


def update(elmt, **attributes_dict):
    """update self.__dict__ with new attributes"""
    print('<{}> updated'.format(elmt))
    for _k, _v in attributes_dict.items():
        try:
            if not _v == elmt.__dict__[_k]:
                print('{} changed'.format(_k))
        except KeyError:
            print("new attribute")
            print(' .{} -> {}'.format(_k, _v))
        elmt.__dict__[_k] = _v


def attr_pick(self, *pick_list):
    """pick up some of the attributes"""
    _d = dict()
    for _pick in pick_list:
        try:
            _d[_pick] = self.__dict__[_pick]
        except KeyError:
            print("attr_pick(): No '{}'".format(_pick))
    return _d


def attr_pop(self, *pop_list):
    """pop attributes out and return the rest."""
    _d = dict()
    for _k, _v in self.__dict__.items():
        if (_k not in pop_list) and _v:
            _d[_k] = _v
    return _d


def check_class(obj, type):
    if isinstance(obj, type):
        return True
    print("# interface.check_class()", obj, "not type of", type)
    return False


def check_attrib(self, type):
    _pick = list()
    for _k, _v in self.__dict__.items():
        if self.check_class(_v, type):
            _pick.append(_k)
    return _pick


if __name__ == '__main__':
    print("This is {}, which has ".format(__file__))
    print(dir())
