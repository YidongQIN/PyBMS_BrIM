#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

import xml.etree.ElementTree as ET

import prettytable as pt


class PyOpenBrIMElmt(object):




    # read XML
    def read_xml(in_path):
        tree = ET.parse(in_path)
        return tree


    # write XML
    def write_xml(tree, out_path):
        tree.write(out_path, encoding="utf-8", xml_declaration=True)


    # create a new OpenBrIM project and name it
    def new_OpenBrIM(name):
        # default new OpenBrIM project with new name
        origin_string = '<O Alignment="None" N="new" T="Project" TransAlignRule="Right">\n    <O N="Units" T="Group">\n        <O Angle="Radian" Force="Kip" Length="Inch" N="Internal" T="Unit" Temperature="Fahrenheit" />\n        <O Angle="Degree" Force="Kip" Length="Feet" N="Geometry" T="Unit" Temperature="Fahrenheit" />\n        <O Angle="Degree" Force="Kip" Length="Inch" N="Property" T="Unit" Temperature="Fahrenheit" />\n    </O>\n    <O N="SW" T="AnalysisCase" WeightFactor="-1" />\n    <O Gravity="386.09" Modes="1" N="Seismic" T="AnalysisCaseEigen" />\n</O>'
        root = ET.fromstring(origin_string)
        root.attrib['N'] = name
        # tree = ET.ElementTree(root)
        return root


    # save the OpenBrIM model with the name in project attribute
    def save_OpenBrIM(root):
        tree = ET.ElementTree(root)
        out_path = root.attrib['N'] + '.xml'
        tree.write(out_path, encoding="utf-8", xml_declaration=True)


    # search by path
    def find_nodes(tree, path):
        return tree.findall(path)
        # results is a list[] of elements


    # search by key and value of attributes
    def if_match(node, kv_map):
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True


    def get_node_by_keyvalue(nodelist, kv_map):
        result_nodes = []
        for node in nodelist:
            if if_match(node, kv_map):
                result_nodes.append(node)
        return result_nodes
        # results is a list[] of elements, same as def find_nodes


    # change node
    def change_node_attributes(nodelist, kv_map, is_delete=False):
        for node in nodelist:
            for key in kv_map:
                if is_delete:
                    if key in node.attrib:
                        del node.attrib[key]
                else:
                    node.set(key, kv_map.get(key))


    # create and add a new node
    def create_node(tag, attribute_new):
        element = ET.Element(tag, attribute_new)
        return element


    # N and V is mandatory for PARAMETER
    def del_empty_value(dict):
        new_dict = {}
        for key in dict:
            if dict[key] != '':
                new_dict[key] = dict[key]
        return new_dict


    def new_P(name, value, des='', UT='', UC='', role='Input', type_P=''):
    # def new_P(name, value, des='', UT='', UC='', role='Input', type_P=''):
        attribute_P = {'N': name, 'V': value, 'D': des, 'UT': UT, 'UC': UC, 'Role': role, 'T': type_P}
        attribute_P = del_empty_value(attribute_P)
        element = ET.Element('P', attribute_P)
        return element


    def new_O(type_O, *name, **attributesDict):
        if name == ():
            attribute_O = {'T': type_O}
        else:
            attribute_O = {'T': type_O, 'N': name[0]}
        attribute_O = {**attribute_O, **attributesDict}
        element = ET.Element('O', attribute_O)
        return element


    def add_child_node(parentElement, childElement):
        # for node in nodelist: # this is wrong because node is child element of nodelist
        #     node.append(element) #the element will be the child of child elements of nodelist

        # if parement is a node list, append childElement to each of them
        # if not, parement is only ONE node, append
        if isinstance(parentElement, ET.Element):
            parentElement.append(childElement)
        elif isinstance(parentElement, list):
            for node in parentElement:
                node.append(childElement)


    # print(len(parentElement))


    # delete a node by attribute
    def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
        for parent_node in nodelist:
            children = parent_node.iter()
            for child in children:
                if child.tag == tag and if_match(child, kv_map):
                    parent_node.remove(child)


    # separate OBJECT and PARAMETER
    def select_OBJECT(nodelist):
        node_O = ET.Element("", {})
        for node in nodelist:
            if node.tag is 'O':
                node_O.append(node)
        return node_O


    def select_PARAMETER(nodelist):
        node_P = ET.Element("", {})
        for node in nodelist:
            if node.tag is 'P':
                node_P.append(node)
        return node_P


    # T -- main attribute for OBJECT
    # N, V -- main attribute for PARAMETER
    def other_attribute(dict):
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
    def table_OBJECT(result_Object):
        tb = pt.PrettyTable(["Name", "OBJECT Type", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in result_Object:
            row = [anode.attrib.get("N"), anode.attrib.get("T"), anode.attrib.get("D"), other_attribute(anode.attrib)]
            tb.add_row(row)
        print('\n Table of OBJECT found')
        print(tb)


    def table_PARAMETER(result_Parameter):
        tb = pt.PrettyTable(["Name", "Value", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in result_Parameter:
            row = [anode.attrib.get("N"), anode.attrib.get("V"), anode.attrib.get("D"),
                   other_attribute(anode.attrib)]
            tb.add_row(row)
        print('\n Table of PARAMETER found')
        print(tb)
        # return tb
