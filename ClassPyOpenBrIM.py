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
    def parse_xmlfile(self, xml_path):
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
        """save this element as a Project in a xml file. \n
        Must be a project object as <O T=Project >. \n
        Must have an Project name as the file name. \n
        default path is the same folder with .py. \n
        default file name is the element name. \n
        may input a new file path to """
        if self.elmt.tag != 'O' or self.elmt.attrib.get('T') != 'Project':
            print('! WARNING: "{}" is not a Project object as <O T=Project>'.format(self.name))
            return
        if self.elmt.attrib['N'] == '':
            self.name = input('Please name the project:\n')
        self.elmt.attrib['N'] = self.name
        if path == '':
            out_path = self.elmt.attrib['N'] + '.xml'
        elif re.match('.*\.xml', path):
            out_path = path
        else:
            print('Error: should be a xml file')
            return
        tree = eET.ElementTree(self.elmt)
        tree.write(out_path, encoding="utf-8", xml_declaration=True)
        print('Project is saved @ "{}".'.format(out_path))

    def add_sub(self, *child):
        """add one or a list of child elements as sub node"""
        # children=list(child)
        for a in PyOpenBrIMElmt.to_elmt_list(child):
            self.elmt.append(a)

    def attach_to(self, parent):
        """attach this element to parent element(s)"""
        for p in PyOpenBrIMElmt.to_elmt_list(parent):
            p.append(self.elmt)

    def show_info(self, if_self='Y', if_sub='N'):
        """show tags and attributes of itself or sub elements"""
        if if_self.upper() == 'Y':
            print('<{}> {}'.format(self.elmt.tag, self.elmt.attrib))
            if if_sub.upper() == 'Y':
                pass
        if if_sub.upper() == 'Y':
            self.show_sub()

    def show_sub(self):
        """show all sub elements' tags and attributes"""
        count = 0
        print('- - Sub elements of "{}" list below:'.format(self.name))
        for c in self.elmt:
            count = count + 1
            print('\t<{}> {}'.format(c.tag, c.attrib))
        print('- - totally {} sub elements---'.format(count))

    def get_attrib(self, key):
        return self.elmt.attrib[key]

    def update(self, **attrib_dict):
        """update the attributes"""
        for key in attrib_dict:
            if key in self.elmt.attrib:
                self.elmt.set(key, attrib_dict.get(key))

    def copy_from(self, node, **attrib_dict):
        """copy all attributes of a node, and then change some attribute if needed"""
        temp = PyOpenBrIMElmt.to_ob_elmt(node)
        for key in temp:
            self.elmt.set(key, temp.attrib[key])
        for key in attrib_dict:
            self.elmt.set(key, attrib_dict[key])

    def findall_by_xpath(self, xpath, if_print='N'):
        """find all sub node matched the xpath
        (xpath)[https://docs.python.org/3/library/xml.etree.elementtree.html?highlight=xpath#xpath-support]"""
        tree = eET.ElementTree(self.elmt)
        results = tree.findall(xpath)
        if if_print.upper() == 'Y':
            for a in results:
                print('<{}> {}'.format(a.tag, a.attrib))
        return results

    def findall_by_attribute(self, **attributes):
        """find all sub nodes by the attributes"""
        # results is a list[] of elements
        results = []
        for any_node in self.elmt.iter():
            if PyOpenBrIMElmt.match_attribute(any_node, **attributes):
                results.append(any_node)
        return results

    def del_all_sub(self):
        """remove all sub elements from this node"""
        # do not use self.elmt.clear() because it remove all sub and attributes
        to_del = self.elmt.findall('./')
        print('These elements will be deleted')
        for c in to_del:
            print('<{}> {}'.format(c.tag, c.attrib))
            self.elmt.remove(c)

    def del_sub(self, tag='OP', **attrib_dict):
        """remove node with particular tag and attributes"""
        node_to_del = []
        confirm = ''
        for child in self.elmt:
            if PyOpenBrIMElmt.match_tag(child, tag) and PyOpenBrIMElmt.match_attribute(child, **attrib_dict):
                node_to_del.append(child)
        # list all node to be deleted
        if node_to_del:
            print('Confirm the Elements to be deleted')
            for one in node_to_del:
                print('<{}> {}'.format(one.tag, one.attrib))
            confirm = input('Sure to delete? Y/N:\n')
        else:
            print('Find NO element to delete')
        # verify if delete or not
        if confirm.upper() == 'Y':
            for one in node_to_del:
                self.elmt.remove(one)
            print('Totally {} elements deleted'.format(len(node_to_del)))

    def verify_tag(self, tag):
        """verify the tag (OBJECT or PARAMETER) with the input"""
        verified = PyOpenBrIMElmt.match_tag(self.elmt, tag)
        if verified:
            print('"{}".tag is {}'.format(self.name, tag))
        else:
            print('"{}".tag is NOT {}'.format(self.name, tag))
        return verified

    def verify_attributes(self, **attrib_dict):
        """verify the attributes with the inputted attributes dict"""
        verified = PyOpenBrIMElmt.match_attribute(self.elmt, **attrib_dict)
        if verified:
            print('"{}" attributes match'.format(self.name))
        else:
            print('"{}" attributes NOT match'.format(self.name))
        return verified

    @staticmethod
    def match_attribute(node, **attrib_dict):
        assert isinstance(node, eET.Element)
        """if the node.attribute match every item in the inputted attributes dict"""
        for key in attrib_dict.keys():
            if node.attrib.get(key) != attrib_dict[key]:
                return False
        return True

    @staticmethod
    def match_tag(node, tag):
        """tag = 'O', 'P' or 'OP'"""
        assert isinstance(node, eET.Element)
        if tag == 'OP':
            if node.tag in ['O', 'P']:
                return True
        elif tag == 'O' or tag == 'P':
            if node.tag == tag:
                return True
        else:
            print('tag should be "O", "P" or "OP".')
        return False

    @staticmethod
    def to_elmt_list(nodes):
        """format PyOpenBrIM object or element to a [list of et.element]"""
        if isinstance(nodes, list):
            node_list = list(map(PyOpenBrIMElmt.to_ob_elmt, nodes))
        elif isinstance(nodes, tuple):
            node_list = list(map(PyOpenBrIMElmt.to_ob_elmt, list(nodes)))
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
        """create a new OBJECT in OpenBrIM ParamML.\n
        Mandatory is Type <O T= ? > such as Point, Line, Group, ...\n
        N = ? as name is recommended to be provided.\n
        attributes are in format of dict.
        """
        # sub classes will override this method by object_type = 'Point"...
        super(ObjElmt, self).__init__(name)
        self.elmt.tag = 'O'
        self.elmt.attrib['T'] = object_type
        for k in obj_attrib.keys():
            self.elmt.attrib[k] = obj_attrib[k]


class PrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""

    def __init__(self, name, value, des='', role='Input', par_type='', ut='', uc=''):
        """create a new PARAMETER in OpenBrIM ParamML. \n
        Mandatory: name, value.\n
        D-> des is description of the parameter.\n
        par_type is the Type of parameter, such as Material. """
        super(PrmElmt, self).__init__(name)
        self.elmt.tag = 'P'
        attrib = dict(V=value, D=des, UT=ut, UC=uc, Role=role, T=par_type)
        for k, v in attrib.items():
            if v:
                self.elmt.attrib[k] = v


class Material(ObjElmt):
    pass


class Section(ObjElmt):
    pass


class Shape(ObjElmt):
    pass


class Unit(ObjElmt):
    pass


class Group(ObjElmt):

    def __init__(self, group_name, *elmts_list):
        super(Group, self).__init__('Group', name=group_name)
        self.add_sub(elmts_list)


class Point(ObjElmt):
    """T=Point
    Mandatory attribute: X, Y, Z"""

    def __init__(self, x, y, z, point_name=''):
        # coordinates may be parameters not numbers!
        super(Point, self).__init__('Point', name=point_name)
        self.elmt.attrib['X'] = str(x)
        self.elmt.attrib['Y'] = str(y)
        self.elmt.attrib['Z'] = str(z)
        self.x = x
        self.y = y
        self.z = z
        self.check_num()

    def check_num(self):
        """typically the coordinates should be numbers.
        But parameters are allowed, and in that case the values are strings"""
        if not isinstance(self.x, (int, float)):
            print('WARNING: X Coordinate is NOT a number.')
        if not isinstance(self.y, (int, float)):
            print('WARNING: Y Coordinate is NOT a number.')
        if not isinstance(self.z, (int, float)):
            print('WARNING: Z Coordinate is NOT a number.')


class Line(ObjElmt):
    """T=Line, Two points and one section needed"""

    def __init__(self, point1=None, point2=None, section=None, line_name=''):
        super(Line, self).__init__('Line', name=line_name)
        # start=time.clock()
        if point1:
            self.add_point(point1)
        if point2:
            self.add_point(point2)
        if section:
            self.set_section(section)
        # print(time.clock()-start)

    def check_line(self):
        """should have Two Points and One Section"""
        points = self.elmt.findall("./O[@T='Point']")
        sects = self.elmt.findall("./O[@T='Section']")
        if len(points) != 2:
            return False
        if len(sects) != 1:
            return False
        return True

    def line_update(self, point1, point2, section):
        self.add_point(point1)
        self.add_point(point2)
        self.set_section(section)

    def add_point(self, point_obj):
        assert isinstance(point_obj, Point), print('An object of class Point is needed')
        self.elmt.append(point_obj.elmt)

    def set_section(self, section_obj):
        """section has attribute of material"""
        assert isinstance(section_obj, Section), print('An object of class Section is needed')
        self.elmt.append(section_obj.elmt)


class Surface(ObjElmt):
    def __init__(self, point1=None, point2=None, point3=None, point4=None, thick_par=None, material_obj=None,
                 surface_name=''):
        super(Surface, self).__init__('Surface', name=surface_name)
        self.name = surface_name
        if point1:
            self.add_point(point1)
        if point2:
            self.add_point(point2)
        if point3:
            self.add_point(point3)
        if point4:
            self.add_point(point4)
        if material_obj:
            self.add_mat_par(material_obj)
        if thick_par:
            self.add_thick_par(thick_par)
        self.check_surface()

    def check_surface(self):
        """should have 4 Points, 1 Thickness and 1 Material"""
        if len(self.elmt.findall("./O[@T='Point']")) != 4:
            print('!ERROR: Not 4 Points in the Surface OBJECT: {}'.format(self.name))
            return False
        if len(self.elmt.findall("./P[@N='Thickness']")) != 1:
            print('!ERROR: Not 1 thick parameter in the Surface object {}'.format(self.name))
            return False
        if len(self.elmt.findall("./P[@T='Material']")) != 1:
            print('!ERROR: Not 1 material parameter in the Surface object {}'.format(self.name))
            return False
        return True

    def add_point(self, point_obj):
        if isinstance(point_obj, Point):
            self.elmt.append(point_obj.elmt)
        else:
            print('An object of class Point is needed')

    def add_thick_par(self, thick_par):
        if isinstance(thick_par, PrmElmt) and PyOpenBrIMElmt.match_attribute(thick_par.elmt, N='Thickness'):
            self.add_sub(thick_par)
        elif str(thick_par).isdigit():
            self.add_sub(PrmElmt("Thickness", str(thick_par)))
        else:
            print("a PARAMETER @N=Thickness is required.")

    def add_mat_par(self, mat_obj):
        """material is an OBJECT.\n
        But in Surface it should be a parameter that refer to the Material Object"""
        if isinstance(mat_obj, ObjElmt) and PyOpenBrIMElmt.match_attribute(mat_obj.elmt, T='Material'):
            self.add_sub(PrmElmt('SurfaceMaterial_{}'.format(self.name), mat_obj.elmt.attrib['N'], par_type='Material'))
        else:
            print("a OBJECT @T=Material is required.")

    def change_thick(self, thickness, des='', role='Input', par_type='Surface_Thickness', ut='', uc=''):
        """thickness parameter of Surface.\n Only thickness is mandatory"""
        self.del_sub('P', N="Thickness")
        self.add_sub(PrmElmt("Thickness", str(thickness), des, role, par_type, ut, uc))
        # self.elmt.append(eET.Element('P', dict(N="Thickness", V=str(thickness), D=des, Role=role, T=par_type, UT=ut, UC=uc)))

    def change_material(self, material, des='', role='Input', name='SurfaceMaterial', ut='', uc=''):
        """material parameter of Surface.\n Only material is mandatory"""
        self.del_sub('P', T="Material")
        self.add_sub(PrmElmt(name, material, des, role, 'Material', ut, uc))
        # self.elmt.append(eET.Element('P', dict(T='Material', V=material, D=des, N=name, Role=role, UT=ut, UC=uc)))

    def set_parameter(self, name, value, des=''):
        self.add_sub(PrmElmt(name, value, des))


class FELine(ObjElmt):
    pass


class FESurface(ObjElmt):
    pass


class ShowTree(object):
    """show results in tree-like format"""

    def __init__(self, result):
        self.elmts = PyOpenBrIMElmt.to_elmt_list(result)
        for one_branch in self.elmts:
            ShowTree.branch(one_branch, 0)

    @staticmethod
    def branch(node, level):
        for tab in range(level):
            print('\t', end='')
        other_info = ''
        #@TODO O P different attrib to show
        for key in ['T', 'N']:
            if node.attrib.get(key):
                other_info = other_info + '{}={}\t'.format(key, node.attrib[key])
        print('|--<{}> {}'.format(node.tag, other_info))
        for sub in node:
            ShowTree.branch(sub, level + 1)


class ShowTable(object):
    """this class is used to show search results in format of table"""

    def __init__(self, result):
        self.elmts = PyOpenBrIMElmt.to_elmt_list(result)
        self.result_obj = eET.Element("", {})
        self.result_par = eET.Element("", {})
        self.classify_nodes()
        self.show_table()

    # separate OBJECT and PARAMetER
    def classify_nodes(self):
        for node in self.elmts:
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
