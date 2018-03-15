#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'
'''
try to use OOP for OpenBrIM
'''
import xml.etree.ElementTree as ET

import prettytable as pt


class PyOpenBrIMElmt(object):
    """basic class for ParamML file of OpenBrIM"""
    tree = ''

    def __int__(self, name):
        """ name is project name"""
        self.name = name
        # self.tree = tree  # may not use
        # self.root=tree.getroot()

    # read XML from .xml file or String and get root
    def read_xmlfile(self, in_path):
        tree = ET.parse(in_path)
        root = tree.getroot()
        return root

    def read_xmlstr(self, str):
        root = ET.fromstring(str)
        return root

    # write XML
    def write_xml(self, tree, out_path):
        tree.write(out_path, encoding="utf-8", xml_declaration=True)

    def open_project(self, name):
        pass

    # create a new OpenBrIM project and name it
    def new_project(self):
        # default new OpenBrIM project named as self.name
        origin_string = '<O Alignment="None" N="" T="Project" TransAlignRule="Right">\n\t<O N="Units" T="Group">\n\t\t<O Angle="Radian" Force="Kip" Length="Inch" N="Internal" T="Unit" Temperature="Fahrenheit" />\n\t\t<O Angle="Degree" Force="Kip" Length="Feet" N="Geometry" T="Unit" Temperature="Fahrenheit" />\n\t\t<O Angle="Degree" Force="Kip" Length="Inch" N="Property" T="Unit" Temperature="Fahrenheit" />\n\t</O>\n\t<O N="SW" T="AnalysisCase" WeightFactor="-1" />\n\t<O Gravity="386.09" Modes="1" N="Seismic" T="AnalysisCaseEigen" />\n</O>'
        # origin_string='<O Alignment="None" N="" T="Project" TransAlignRule="Right">\n</O>'
        root = ET.fromstring(origin_string)
        root.attrib['N'] = self.name
        # tree = ET.ElementTree(root)
        # root is ET.node = xml.element <></>
        return root

    # save the OpenBrIM model with the name in project attribute
    def save_project(self, root):
        tree = ET.ElementTree(root)
        out_path = root.attrib['N'] + '.xml'
        tree.write(out_path, encoding="utf-8", xml_declaration=True)

    # search by path
    def find_nodes(self, tree, path):
        return tree.findall(path)
        # results is a list[] of elements

    # search by key and value of attributes
    def if_match(self, node, kv_map):
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

    def get_node_by_keyvalue(self, nodelist, kv_map):
        result_nodes = []
        for node in nodelist:
            if if_match(node, kv_map):
                result_nodes.append(node)
        return result_nodes
        # results is a list[] of elements, same as def find_nodes

    # change node
    def change_node_attributes(self, nodelist, kv_map, is_delete=False):
        for node in nodelist:
            for key in kv_map:
                if is_delete:
                    if key in node.attrib:
                        del node.attrib[key]
                else:
                    node.set(key, kv_map.get(key))

    # create and add a new node
    def create_node(self, tag, attribute_new):
        element = ET.Element(tag, attribute_new)
        return element

    # delete a node by attribute
    def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
        for parent_node in nodelist:
            children = parent_node.iter()
            for child in children:
                if child.tag == tag and if_match(child, kv_map):
                    parent_node.remove(child)


class ObjElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <O>"""

    def __init__(self):
        pass

    def new_O(self, type_O, *name, **attributesDict):
        if name == ():
            attribute_O = {'T': type_O}
        else:
            attribute_O = {'T': type_O, 'N': name[0]}
        attribute_O = {**attribute_O, **attributesDict}
        element = ET.Element('O', attribute_O)
        return element

    def add_child_node(self, parentElement, childElement):
        if isinstance(parentElement, ET.Element):
            parentElement.append(childElement)
        elif isinstance(parentElement, list):
            for node in parentElement:
                node.append(childElement)


class PrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""

    def __init__(self):
        pass

    def del_empty_value(self, dict):
        new_dict = {}
        for key in dict:
            if dict[key] != '':
                new_dict[key] = dict[key]
        return new_dict

    # N and V is mandatory for PARAMETER
    def new_P(self, name, value, des='', UT='', UC='', role='Input', type_P=''):
        # def new_P(name, value, des='', UT='', UC='', role='Input', type_P=''):
        attribute_P = {'N': name, 'V': value, 'D': des, 'UT': UT, 'UC': UC, 'Role': role, 'T': type_P}
        attribute_P = self.del_empty_value(attribute_P)
        element = ET.Element('P', attribute_P)
        return element


class ResultsTable(object):
    """# these methods are used for show search results in table format"""

    def __init__(self, results):
        self.results = results
        self.showTable()

    def showTable(self):
        if self.result_obj:
            self.table_OBJECT(self.result_obj)
        if self.result_par:
            self.table_PARAMETER(self.result_par)

    # separate OBJECT and PARAMETER
    def select_OBJECT(self):
        self.result_obj = ET.Element("", {})
        for node in self.results:
            if node.tag is 'O':
                self.result_obj.append(node)
        return self.result_obj

    def select_PARAMETER(self):
        self.result_par = ET.Element("", {})
        for node in self.results:
            if node.tag is 'P':
                self.result_par.append(node)
        return self.result_par

    # T -- main attribute for OBJECT
    # N, V -- main attribute for PARAMETER
    def other_attribute(self, dict):
        if 'T' in dict:
            dict.pop('T')
        if 'N' in dict:
            dict.pop('N')
        if 'V' in dict:
            dict.pop('V')
        if 'D' in dict:
            dict.pop('D')
        atts = ''
        for key, value in dict.items():
            atts = atts + key + '=' + value + ', '
        return atts

    # pretty table
    def table_OBJECT(self, result_Object):
        tb = pt.PrettyTable(["Name", "OBJECT Type", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in result_Object:
            row = [anode.attrib.get("N"), anode.attrib.get("T"), anode.attrib.get("D"),
                   self.other_attribute(anode.attrib)]
            tb.add_row(row)
        print('\n Table of OBJECT found')
        print(tb)

    def table_PARAMETER(self, result_Parameter):
        tb = pt.PrettyTable(["Name", "Value", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in result_Parameter:
            row = [anode.attrib.get("N"), anode.attrib.get("V"), anode.attrib.get("D"),
                   self.other_attribute(anode.attrib)]
            tb.add_row(row)
        print('\n Table of PARAMETER found')
        print(tb)
