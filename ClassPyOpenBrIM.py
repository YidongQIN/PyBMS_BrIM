#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Object-oriented programming for OpenBrIM
'''

import re
import xml.etree.ElementTree as eET

import prettytable as pt


class PyOpenBrIMElmt(object):
    """basic class for ParamML file of OpenBrIM"""

    def __init__(self, name=''):
        """ name is project name"""
        self.name = name
        self.elmt = eET.Element("", {'N': name})
        self.if_root = False

    # 3 way to create a new project: XML file, XML string or from template
    # read XML from .xml file or String and get root
    def read_xmlfile(self, xml_path):
        """ read in a xml file"""
        if re.match('.*\.xml', xml_path):
            tree = eET.parse(xml_path)
            self.elmt = tree.getroot()
        else:
            print('"{}" is not a .xml file!'.format(xml_path))

    def read_xmlstr(self, xmlstr):
        """read xml string"""
        self.elmt = eET.fromstring(xmlstr)

    def new_project(self, template='default'):
        """create new project with a template"""
        if template == 'default':
            origin_string = """
<O Alignment="None" N="" T="Project" TransAlignRule="Right">
    <O N="Units" T="Group">
        <O Angle="Radian" Force="Kip" Length="Inch" N="Internal" T="Unit" Temperature="Fahrenheit"/>
        <O Angle="Degree" Force="Kip" Length="Feet" N="Geometry" T="Unit" Temperature="Fahrenheit"/>
        <O Angle="Degree" Force="Kip" Length="Inch" N="Property" T="Unit" Temperature="Fahrenheit"/>
    </O>
    <O N="SW" T="AnalysisCase" WeightFactor="-1"/>
    <O Gravity="386.09" Modes="1" N="Seismic" T="AnalysisCaseEigen"/>
</O>
           """
        else:
            origin_string = '<O Alignment="None" N="" T="Project" TransAlignRule="Right">\n</O>'
        root = eET.fromstring(origin_string)
        # default new OpenBrIM project named as self.name
        root.attrib['N'] = self.name
        self.elmt = root
        self.if_root = True

    # save the OpenBrIM model with the name in project attribute
    def save_project(self, path=''):
        """save this element as a Project in a xml file.
        Must have an element name.
        Must be a project object as <O T=Project >.
        default path is the same folder with .py.
        default file name is the element name.
        may input a new file path to """
        if self.elmt.tag != 'O' or self.elmt.attrib['T'] != 'Project':
            print('! WARNING: "{}" is not a Project object as <O T=Project>'.format(self.name))
            return
        if self.elmt.attrib['N'] == '':
            self.name = input('Please name the project:\n')
            self.elmt.attrib['N'] = self.name
        if path == '':
            out_path = self.elmt.attrib['N'] + '.xml'
            print('Project will be save as {}.xml.'.format(self.elmt.attrib['N']))
        elif re.match('.*\.xml', path):
            out_path = path
        else:
            print('Error: should be a xml file')
            return
        tree = eET.ElementTree(self.elmt)
        tree.write(out_path, encoding="utf-8", xml_declaration=True)

    def add_sub(self, child):
        """add one or a list of child elements as sub node"""
        for a in PyOpenBrIMElmt.to_elmt_list(child):
            self.elmt.append(a)

    def attach_to(self, parent):
        """attach this element to a parent element"""
        for p in PyOpenBrIMElmt.to_elmt_list(parent):
            p.append(self.elmt)

    def show_self(self):
        """show element's tag and attributes"""
        print('<{}> {}'.format(self.elmt.tag, self.elmt.attrib))

    def show_sub(self):
        """show all sub elements' tags and attributes"""
        for c in self.elmt:
            print('<{}> {}'.format(c.tag, c.attrib))

    def verify_tag(self, tag):
        """verify the tag (OBJECT or PARAMETER) with the input"""
        if self.elmt.tag != tag:
            return False
        return True

    def verify_attrib(self, **attrib_dict):
        """verify the attributes with the input"""
        for key in attrib_dict:
            if self.elmt.attrib.get(key) != attrib_dict.get(key):
                return False
        return True

    # change node
    def update(self, **kv_map):
        """update the attributes"""
        for key in kv_map:
            if key in self.elmt.attrib:
                self.elmt.set(key, kv_map.get(key))

    def copy_from(self, node, attributes={}):
        """copy all attributes of a node, and then change some attribute if needed"""
        temp = PyOpenBrIMElmt.to_ob_elmt(node)
        for key in temp:
            self.elmt.set(key, temp.attrib[key])
        for key in attributes:
            self.elmt.set(key, attributes[key])

    # search by xpath
    def findall_by_xpath(self, xpath):
        """find all sub node matched the xpath
        (xpath)[https://docs.python.org/3/library/xml.etree.elementtree.html?highlight=xpath#xpath-support]"""
        tree = eET.ElementTree(self.elmt)
        return tree.findall(xpath)

    def find_by_kv(self, **kv_map):
        #@TODO how to find by attributes
        """find all sub nodes by the attributes"""
        pass
        # result_nodes = []
        # for node in self.elmt:
        #     for k,v in kv_map:
        #         map={k:v}
        #         if self.attrib_match(node, map):
        #             result_nodes.append(node)
        # return result_nodes
        # results is a list[] of elements, same as def find_nodes

    # delete a node by attribute
    def del_sub(self, tag, **kv_map):
        #@TODO how to delete
        """remove node with particular tag and attributes"""
        # list all node to be deleted
        # verify if delete or not
        pass

    @staticmethod
    def add_child_node(parent, child):
        """ forget it, use .add_sub() method instead."""
        # list(map(lambda p,c:p.append(c),to_elmt_list(parent),to_elmt_list(child)))
        for p in PyOpenBrIMElmt.to_elmt_list(parent):
            for c in PyOpenBrIMElmt.to_elmt_list(child):
                p.append(c)

    # format PyOpenBrIM instance, et.element to [list of et.element]
    @staticmethod
    def to_elmt_list(nodes):
        """transfer PyOpenBrIM object or element to a list of et.element"""
        if isinstance(nodes, list):
            node_list = list(map(PyOpenBrIMElmt.to_ob_elmt, nodes))
        else:
            node_list = [PyOpenBrIMElmt.to_ob_elmt(nodes)]
        return node_list

    @staticmethod
    def to_ob_elmt(node):
        """make sure PyOpenBrIM instance has been transferred into et.element"""
        if isinstance(node, eET.Element):
            return node
        elif isinstance(node, PyOpenBrIMElmt):
            return node.elmt
        else:
            print('Unacceptable type of input result.')


class ObjElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <O>"""

    def __init__(self, object_type, name='', **obj_attrib):
        """create a new OBJECT in OpenBrIM ParamML
        <O T=? >
        type is mandatory: Point, Line, Group,...
        N=? name is recommended to be provided.
        attributes are required.
        """
        # sub classes,such as clall Point, Line, will override this method
        super(ObjElmt, self).__init__(name)
        self.elmt.tag = 'O'
        self.elmt.attrib['T'] = object_type
        for k in obj_attrib.keys():
            self.elmt.attrib[k] = obj_attrib[k]


class PrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""

    def __init__(self, name, value, des='', role='Input', par_type='', ut='', uc=''):
        """create a new PARAMETER in OpenBrIM ParamML """
        super(PrmElmt, self).__init__(name)
        self.elmt.tag = 'P'
        attrib = dict(V=value, D=des, UT=ut, UC=uc, Role=role, T=par_type)
        for k, v in attrib.items():
            if v:
                self.elmt.attrib[k] = v


class Point(ObjElmt):
    """T=Point
    Mandatory attribute: X, Y, Z"""

    def __init__(self, x, y, z, point_name=''):
        coordinate =dict(X=x,Y=y,Z=z)
        #@TODO Point methods?
        super(Point, self).__init__('Point', name=point_name,**coordinate)
        self.x = x
        self.y = y
        self.z = z


class ResultsTable(object):
    """this class is used to show search results in format of table"""

    def __init__(self, result):
        self.rowdata = PyOpenBrIMElmt.to_elmt_list(result)
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
