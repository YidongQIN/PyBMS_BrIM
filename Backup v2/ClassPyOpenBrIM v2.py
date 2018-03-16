#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'
'''
Object-oriented programming for OpenBrIM
'''
import xml.etree.ElementTree as et

import prettytable as pt


class PyOpenBrIMElmt(object):
    """basic class for ParamML file of OpenBrIM"""

    def __init__(self, name):
        """ name is project name"""
        self.name = name
        self.elmt = et.Element("", {})

    # read XML from .xml file or String and get root
    def read_xmlfile(self, in_path):
        # @TODO check path function
        tree = et.parse(in_path)
        self.elmt = tree.getroot()

    def read_xmlstr(self, xmlstr):
        self.elmt = et.fromstring(xmlstr)

    def new_project(self, template='default'):
        # @TODO more template may be added
        if template == 'default':
            origin_string = '''<O Alignment="None" N="" T="Project" 
            TransAlignRule="Right">\n\t<O N="Units" T="Group">
            \n\t\t<O Angle="Radian" Force="Kip" Length="Inch" N="Internal" 
            T="Unit" Temperature="Fahrenheit" />\n\t\t<O Angle="Degree" 
            Force="Kip" Length="Feet" N="Geometry" T="Unit" 
            Temperature="Fahrenheit" />\n\t\t<O Angle="Degree" 
            Force="Kip" Length="Inch" N="Property" T="Unit" 
            Temperature="Fahrenheit" />\n\t</O>\n\t
            <O N="SW" T="AnalysisCase" WeightFactor="-1" />\n\t
            <O Gravity="386.09" Modes="1" N="Seismic" 
            T="AnalysisCaseEigen" />\n</O>'''
        else:
            origin_string = '<O Alignment="None" N="" T="Project" TransAlignRule="Right">\n</O>'
        root = et.fromstring(origin_string)
        # default new OpenBrIM project named as self.name
        root.attrib['N'] = self.name
        # tree = et.ElementTree(root)
        # root is ET.node = xml.element <></>
        # return root
        self.elmt = root

    # save the OpenBrIM model with the name in project attribute
    def save_project(self, path=''):
        tree = et.ElementTree(self.elmt)
        out_path = self.elmt.attrib['N'] + '.xml'
        if path != '':
            out_path = path
        tree.write(out_path, encoding="utf-8", xml_declaration=True)

    def add_sub(self, child):
        for a in to_elmt_list(child):
            self.elmt.append(a)
        # if isinstance(child, list):
        #     for a in child:
        #         self.elmt.append(a)
        # elif isinstance(child, PyOpenBrIMElmt):
        #     self.elmt.append(child.elmt)

    def attach(self, parent):
        pass
        # attach this element/node to a parent

    # search by path
    def findall_by_xpath(self, xpath):
        tree = et.ElementTree(self.elmt)
        return tree.findall(xpath)
        # results is a list[] of elements

    # search by key and value of attributes
    @staticmethod
    def if_match(node, **kv_map):
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

    # @TODO modify, search and delete functions
    def find_by_keyvalue(self, **kv_map):
        pass
        # result_nodes = []
        # for node in self.elmt:
        #     for k,v in kv_map:
        #         map={k:v}
        #         if self.if_match(node, map):
        #             result_nodes.append(node)
        # return result_nodes
        # results is a list[] of elements, same as def find_nodes

    # change node
    def change_node_attributes(self, nodelist, kv_map, is_delete=False):
        pass
        # for node in nodelist:
        #     for key in kv_map:
        #         if is_delete:
        #             if key in node.attrib:
        #                 del node.attrib[key]
        #         else:
        #             node.set(key, kv_map.get(key))

    # delete a node by attribute
    def del_node_by_tagkeyvalue(self, tag, kv_map):
        pass
        # for parent_node in self.elmt:
        #     children = parent_node.iter()
        #     for child in children:
        #         if child.tag == tag and self.if_match(child, kv_map):
        #             parent_node.remove(child)


class ObjElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <O>"""

    def __init__(self, object_type, name='', **obj_attrib):
        super(ObjElmt, self).__init__(name)
        temp_dict = dict(T=object_type)
        if name != '':
            temp_dict['N'] = name
        attributes = {**temp_dict, **obj_attrib}
        self.elmt = et.Element('O', attributes)
        ResultsTable(self.elmt)


class PrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""

    def __init__(self, name):
        self.tag = 'P'
        super(PrmElmt, self).__init__(name)

    @staticmethod
    def del_empty_value(attributes):
        new_attributes = {}
        for key in attributes:
            if attributes[key] != '':
                new_attributes[key] = attributes[key]
        return new_attributes

    # N and V is mandatory for PARAMetER
    def new_par(self, name, value, des='', ut='', uc='', role='Input', type_of_par=''):
        # def new_par(name, value, des='', UT='', UC='', role='Input', type_P=''):
        attributes = dict(N=name, V=value, D=des, UT=ut, UC=uc, Role=role, T=type_of_par)
        attributes = self.del_empty_value(attributes)
        element = et.Element('P', attributes)
        return element


def add_child_node(parent, child):
    # @TODO modify by to_elmt_list
    parent_list = to_elmt_list(parent)
    child_list = to_elmt_list(child)
    for p in parent_list:
        for c in child_list:
            p.append(c)
    # if isinstance(parent, et.Element):
    #     if isinstance(child, et.Element):
    #         parent.append(child)
    #     elif isinstance(child, list):
    #         for child in child:
    #             parent.append(child)
    # elif isinstance(parent, list):
    #     if isinstance(child, et.Element):
    #         for parent in parent:
    #             parent.append(child)
    #     elif isinstance(child, list):
    #         for child in child:
    #             for parent in parent:
    #                 parent.append(child)


def to_elmt_list(nodes):
    node_list = []
    if isinstance(nodes, list):
        for a in nodes:
            node_list.append(to_ob_elmt(a))
    else:
        node_list = [to_ob_elmt(nodes)]
    return node_list


def to_ob_elmt(node):
    elmt = et.Element('', {})
    if isinstance(node, et.Element):
        elmt = node
    elif isinstance(node, PyOpenBrIMElmt):
        elmt = node.elmt
    else:
        print('Unacceptable type of input result.')
    return elmt


class ResultsTable(object):
    """this class is used for show search results in table format"""

    def __init__(self, result):
        self.rowdata = []
        if isinstance(result, PyOpenBrIMElmt):
            self.rowdata = result.elmt
        elif isinstance(result, et.Element) or isinstance(result, list):
            self.rowdata = result
        else:
            print('Unacceptable type of input result.')
        self.result_obj = et.Element("", {})
        self.result_par = et.Element("", {})
        self.classify_nodes()
        self.show_table()

    # separate OBJECT and PARAMetER
    def classify_nodes(self):
        for node in self.rowdata:
            self.obj_or_par(node)
        # if isinstance(self.results, et.Element):
        #     self.obj_or_par(self.results)
        # elif isinstance(self.results, list):
        #     for node in self.results:
        #         self.obj_or_par(node)

    def obj_or_par(self, node):
        if node.tag is 'P':
            self.result_par.append(node)
        if node.tag is 'O':
            self.result_obj.append(node)

    def show_table(self):
        if self.result_obj:
            self.show_objects(self.result_obj)
        if self.result_par:
            self.show_parameters(self.result_par)

    # T -- main attribute for OBJECT
    # N, V -- main attribute for PARAMetER
    @staticmethod
    def other_attribute(attrb_dict):
        # T,N V,D are important attributes for ParamML elements
        # other attributes will be shown in tha last column
        if 'T' in attrb_dict:
            attrb_dict.pop('T')
        if 'N' in attrb_dict:
            attrb_dict.pop('N')
        if 'V' in attrb_dict:
            attrb_dict.pop('V')
        if 'D' in attrb_dict:
            attrb_dict.pop('D')
        atts = ''
        for key, value in attrb_dict.items():
            atts = atts + key + '=' + value + ', '
        atts = atts[0:-2]  # delete the last,
        return atts

    # pretty table
    # @TODO try pandas instead of prettytable?
    def show_objects(self, result_object):
        tb = pt.PrettyTable(["Name", "OBJECT Type", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in result_object:
            row = [anode.attrib.get("N"), anode.attrib.get("T"), anode.attrib.get("D"),
                   self.other_attribute(anode.attrib)]
            tb.add_row(row)
        print('\n Table of Result OBJECT')
        print(tb)

    def show_parameters(self, result_parameter):
        tb = pt.PrettyTable(["Name", "Value", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in result_parameter:
            row = [anode.attrib.get("N"), anode.attrib.get("V"), anode.attrib.get("D"),
                   self.other_attribute(anode.attrib)]
            tb.add_row(row)
        print('\n Table of Result PARAMetER')
        print(tb)
