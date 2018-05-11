#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Object-oriented programming for OpenBrIM
'''

import xml.etree.ElementTree as eET

import prettytable as pt


class PyOpenBrIMElmt(object):
    """basic class for ParamML file of OpenBrIM"""

    def __init__(self, name):
        """ name is project name"""
        self.name = name
        self.elmt = eET.Element("", {})
        if name != '':
            self.elmt.attrib['N'] = name

    # read XML from .xml_file or String and get root
    def read_xmlfile(self, in_path):
        tree = eET.parse(in_path)
        self.elmt = tree.getroot()

    def read_xmlstr(self, xmlstr):
        self.elmt = eET.fromstring(xmlstr)

    def new_project(self, template='default'):
        if template == 'default':
            origin_string = '''
<O Alignment="None" N="" T="Project" TransAlignRule="Right">
    <O N="Units" T="Group">
        <O Angle="Radian" Force="Kip" Length="Inch" N="Internal" T="Unit" Temperature="Fahrenheit"/>
        <O Angle="Degree" Force="Kip" Length="Feet" N="Geometry" T="Unit" Temperature="Fahrenheit"/>
        <O Angle="Degree" Force="Kip" Length="Inch" N="Property" T="Unit" Temperature="Fahrenheit"/>
    </O>
    <O N="SW" T="AnalysisCase" WeightFactor="-1"/>
    <O Gravity="386.09" Modes="1" N="Seismic" T="AnalysisCaseEigen"/>
</O>
            '''
        else:
            origin_string = '<O Alignment="None" N="" T="Project" TransAlignRule="Right">\n</O>'
        root = eET.fromstring(origin_string)
        # default new OpenBrIM project named as self.name
        root.attrib['N'] = self.name
        self.elmt = root

    # save the OpenBrIM model with the name in project attribute
    def save_project(self, path=''):
        tree = eET.ElementTree(self.elmt)
        out_path = self.elmt.attrib['N'] + '.xml'
        if path != '':
            out_path = path
        tree.write(out_path, encoding="utf-8", xml_declaration=True)

    def add_sub(self, child):
        for a in to_elmt_list(child):
            self.elmt.append(a)

    # search by path
    def findall_by_xpath(self, xpath):
        tree = eET.ElementTree(self.elmt)
        return tree.findall(xpath)


class ObjElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <O>"""

    def __init__(self, object_type, name='', **obj_attrib):
        super(ObjElmt, self).__init__(name)
        self.elmt.tag = 'O'
        self.elmt.attrib['T'] = object_type
        for k in obj_attrib.keys():
            self.elmt.attrib[k] = obj_attrib[k]


class PrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""

    def __init__(self, name, value, des='', role='Input', par_type='', ut='', uc=''):
        super(PrmElmt, self).__init__(name)
        self.elmt.tag = 'P'
        attrib = dict(V=value, D=des, UT=ut, UC=uc, Role=role, T=par_type)
        assert attrib['T'] != ''
        for k, v in attrib.items():
            if v:
                self.elmt.attrib[k] = v


def add_child_node(parent, child):
    # list(map(lambda p,c:p.append(c),to_elmt_list(parent),to_elmt_list(child)))
    for p in to_elmt_list(parent):
        for c in to_elmt_list(child):
            p.append(c)


# format PyOpenBrIM instance, et.element to [list of et.element]
def to_elmt_list(nodes):
    # change PyOpenBrIM object to et.element
    def to_ob_elmt(node):
        elmt = eET.Element('', {})
        if isinstance(node, eET.Element):
            elmt = node
        elif isinstance(node, PyOpenBrIMElmt):
            elmt = node.elmt
        else:
            print('Unacceptable type of input result.')
        return elmt

    if isinstance(nodes, list):
        node_list = list(map(to_ob_elmt, nodes))
    else:
        node_list = [to_ob_elmt(nodes)]
    return node_list


class ResultsTable(object):
    """this class is used to show search results in format of table"""

    def __init__(self, result):
        self.rowdata = to_elmt_list(result)
        self.result_obj = eET.Element("", {})
        self.result_par = eET.Element("", {})
        self.classify_nodes()
        self.show_table()

    # separate OBJECT and PARAMetER
    def classify_nodes(self):
        for node in self.rowdata:
            if node.tag is 'P':
                self.result_par.append(node)
            if node.tag is 'O':
                self.result_obj.append(node)

    def show_table(self):
        if self.result_obj:
            self.show_objects()
        if self.result_par:
            self.show_parameters()

    # T -- mandatory for OBJECT
    # N, V -- mandatory for PARAMetER
    def show_objects(self):
        tb = pt.PrettyTable(["Name", "OBJECT Type", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in self.result_obj:
            row = []
            if 'N' in anode.attrib:
                row.append(anode.attrib.get("N"))
                anode.attrib.pop('N')
            else:
                row.append('---')
            row.append(anode.attrib.get("T"))
            anode.attrib.pop('T')
            if 'D' in anode.attrib:
                row.append(anode.attrib.get("D"))
                del anode.attrib['D']
            else:
                row.append('---')
            other = ''
            for k, v in anode.attrib.items():
                other = other + k + '=' + v + ', '
            row.append(other[:-2])
            tb.add_row(row)
        print('\n Table of Result OBJECT')
        print(tb)

    def show_parameters(self):
        tb = pt.PrettyTable(["Name", "Value", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for anode in self.result_par:
            row = [anode.attrib.get("N"), anode.attrib.get("V")]
            anode.attrib.pop('N')
            anode.attrib.pop('V')
            if 'D' in anode.attrib:
                row.append(anode.attrib.get("D"))
                del anode.attrib['D']
            else:
                row.append('---')
            other = ''
            for k, v in anode.attrib.items():
                other = other + k + '=' + v + ', '
            row.append(other[:-2])
            tb.add_row(row)
        print('\n Table of Result PARAMetER')
        print(tb)
