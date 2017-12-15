#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

import xml.etree.ElementTree as ET
import prettytable as pt


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


def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)


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
        row = [anode.attrib.get("N"), anode.attrib.get("V"), anode.attrib.get("D"), other_attribute(anode.attrib)]
        tb.add_row(row)
    print('\n Table of PARAMETER found')
    print(tb)
    # return tb


# ----main----
if __name__ == '__main__':

    tree = read_xml('0 MARC.xml')
    root = tree.getroot()

    # find the node
    search_method = input('Search by 1.Path or 2.Attributes?\n')
    if search_method is '1':
        path = './O/P'
        # path = input('input the path in Xpath format\n')
        results = find_nodes(root, path)
    else:
        # op = input('Object or Parameter? Type "O" or "P"\n')
        # kv = input('Input attributes in format of dict {"key":"value",}')
        op = "*"
        kv = {"T": "Material"}
        # kv = {"D": "modulus of elasticity"}
        results = get_node_by_keyvalue(root.iter(op), kv)

    if select_OBJECT(results):
        table_OBJECT(select_OBJECT(results))
    if select_PARAMETER(results):
        table_PARAMETER(select_PARAMETER(results))

    # modify the XML file
    # modify_kv=input('Input new attribute')
    modify_kv = {"D": "This is concrete"}
    change_node_attributes(results, modify_kv)

    # creat new node
    # new_node_tag = input('Input the tag of new node')
    # new_node_kv = input('Input the attributes of new node')
    new_node_tag = 'P'
    new_node_kv = {"N": "Nu", "V": "0.2", "D": "Poisson's Ratio"}
    a = create_node(new_node_tag, new_node_kv)
    add_child_node(results, a)

    # delete node
    # del_tag=input('Input the tag of the node to delete')
    # del_attribute=input('Input the attributes of the node to delete')
    del_tag = "P"
    del_attribute = {"N": "Fy"}
    del_node_by_tagkeyvalue(results, del_tag, del_attribute)

    # output results in new XML
    write_xml(tree, "xx.xml")
