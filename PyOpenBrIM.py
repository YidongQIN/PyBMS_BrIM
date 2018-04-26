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

    def __init__(self, tag_o_p, name, **attrib_dict):
        if name:
            attributes = dict(N=name)
        else:
            attributes = {}
        for k, v in attrib_dict.items():
            if v != '':
                attributes[k] = v
        self.elmt = eET.Element(tag_o_p, **attributes)
        self.name = name

    def parse_xmlfile(self, xml_path):
        """ read a xml file"""
        if re.match('.*\.xml', xml_path):
            tree = eET.parse(xml_path)
            self.elmt = tree.getroot()
        else:
            print('"{}" is not a .xml file!'.format(xml_path))

    def read_xmlstr(self, xmlstr):
        """read xml string"""
        self.elmt = eET.fromstring(xmlstr)

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
        print('- Sub elements of "{}":'.format(self.name))
        for c in self.elmt:
            count = count + 1
            print('  <{}> {}'.format(c.tag, c.attrib))
        print('- Totally {} sub elements.\n'.format(count))

    def get_attrib(self, key):
        a = self.elmt.attrib.get(key)
        if a:
            try:
                print('{} is a number'.format(self.name))
                return float(a)
            except (ValueError, TypeError):
                print('{} is not a number'.format(self.name))
                return a
        else:
            print('{} has no attribute {}'.format(self, key))
            return ''

    def add_attr(self, **attrib_dict):
        for key in attrib_dict:
            value = attrib_dict.get(key)
            if isinstance(value, (int, float)):
                value = str(value)
            self.elmt.set(key, value)

    def update(self, **attrib_dict):
        """update the attributes"""
        for key in attrib_dict:
            if key in self.elmt.attrib:
                self.elmt.set(key, attrib_dict.get(key))

    def copy_attrib_from(self, elmt, *attrib_key):
        """copy from an element the attributes in the dict"""
        temp = PyOpenBrIMElmt.to_ob_elmt(elmt)
        for key in attrib_key:
            if temp.attrib[key]:
                self.elmt.set(key, temp.attrib[key])

    def findall_by_xpath(self, xpath, if_print='N'):
        """return a list of all sub elmt that matched the
        (xpath)[https://docs.python.org/3/library/xml.etree.elementtree.
        html?highlight=xpath#xpath-support]"""
        tree = eET.ElementTree(self.elmt)
        results = tree.findall(xpath)
        if if_print.upper() == 'Y':
            for a in results:
                print('<{}> {}'.format(a.tag, a.attrib))
        return results

    def find_by_xpath(self, xpath, if_print='N'):
        # tree = eET.ElementTree(self.elmt)
        results = self.elmt.findall(xpath)
        if if_print.upper() == 'Y':
            for a in results:
                print('<{}> {}'.format(a.tag, a.attrib))
        return results

    def findsub_by_attributes(self, **attributes):
        results = []
        for any_elmt in self.elmt:
            if PyOpenBrIMElmt.match_attribute(any_elmt, **attributes):
                results.append(any_elmt)
        return results

    def findall_by_attribute(self, **attributes):
        """find in elmt.iter() by the attributes"""
        # results is a list[] of elements
        results = []
        for any_elmt in self.elmt.iter():
            if PyOpenBrIMElmt.match_attribute(any_elmt, **attributes):
                results.append(any_elmt)
        return results

    def del_all_sub(self):
        """remove all sub elements from this elmt"""
        to_del = self.elmt.findall('./')
        print('These elements will be deleted')
        for c in to_del:
            print('<{}> {}'.format(c.tag, c.attrib))
            self.elmt.remove(c)
        # self.elmt.clear() remove subs, but also all attributes of itself

    def del_sub(self, tag='O or P', **attrib_dict):
        elmt_to_del = []
        for child in self.elmt:
            if PyOpenBrIMElmt.match_tag(child, tag) and PyOpenBrIMElmt.match_attribute(child, **attrib_dict):
                elmt_to_del.append(child)
        for one in elmt_to_del:
            self.elmt.remove(one)

    def check_del_sub(self, tag='O or P', **attrib_dict):
        """remove elmt with particular tag and attributes"""
        elmt_to_del = []
        confirm = ''
        for child in self.elmt:
            if PyOpenBrIMElmt.match_tag(child, tag) and PyOpenBrIMElmt.match_attribute(child, **attrib_dict):
                elmt_to_del.append(child)
        # list all elmt to be deleted
        if elmt_to_del:
            print('Confirm the Elements to be deleted')
            for one in elmt_to_del:
                print('<{}> {}'.format(one.tag, one.attrib))
            confirm = input('Sure to delete? Y/N:\n')
        else:
            print('Find NO element to delete')
        # verify if delete or not
        if confirm.upper() == 'Y':
            for one in elmt_to_del:
                self.elmt.remove(one)
            print('Totally {} elements deleted'.format(len(elmt_to_del)))

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
    def match_attribute(elmt, **attrib_dict):
        """if the elmt.attribute match every item in the inputted attributes dict"""
        if isinstance(elmt, eET.Element):
            for key in attrib_dict.keys():
                if elmt.attrib.get(key) != attrib_dict[key]:
                    return False
            return True
        else:
            print('!Type Error: Not an element to match attribute')

    @staticmethod
    def match_tag(elmt, tag):
        """tag = 'O', 'P' or 'OP'"""
        if isinstance(elmt, eET.Element):
            if tag == 'OP':
                if elmt.tag in ['O', 'P']:
                    return True
            elif tag == 'O' or tag == 'P':
                if elmt.tag == tag:
                    return True
            else:
                print('tag should be "O", "P" or "OP".')
            return False
        else:
            print('!Type Error: Not an element to match tag')

    @staticmethod
    def to_elmt_list(*elmts):
        """format PyOpenBrIM object or element to a [list of et.element]"""
        if isinstance(elmts, list):
            elmt_list = list(map(PyOpenBrIMElmt.to_ob_elmt, elmts))
        elif isinstance(elmts, tuple):
            elmt_list = list(map(PyOpenBrIMElmt.to_ob_elmt, list(elmts)))
        else:
            elmt_list = [PyOpenBrIMElmt.to_ob_elmt(elmts)]
        return elmt_list

    @staticmethod
    def to_ob_elmt(elmt):
        """make sure PyOpenBrIM instance has been transferred into et.element"""
        if isinstance(elmt, eET.Element):
            return elmt
        elif isinstance(elmt, PyOpenBrIMElmt):
            return elmt.elmt
        else:
            print('{} Unacceptable type of input to be converted to OpenBrIM elements.'.format(elmt))

    @staticmethod
    def prm_to_value(elmt):
        """PARAMETER to its value"""
        if isinstance(elmt, PrmElmt):
            return elmt.value
        elif isinstance(elmt, (int, float)):
            return elmt
        else:
            print('{} is not a <P>')

    @staticmethod
    def prm_to_name(elmt):
        """PARAMETER to its name, maybe used when refer?"""
        if isinstance(elmt, PrmElmt):
            return elmt.get_attrib('N')
        elif isinstance(elmt, str):
            return elmt
        else:
            print('{} is not a <P>')


class ObjElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <O>"""

    def __init__(self, object_type, obj_name='', **obj_attrib):
        """create a new OBJECT in OpenBrIM ParamML.\n
        Mandatory is Type <O T= ? > such as Point, Line, Group, ...\n
        N = ? as name is recommended to be provided.\n
        attributes are in format of dict.
        """
        # sub classes will override this method by object_type = 'Point"...
        super(ObjElmt, self).__init__('O', obj_name, T=object_type, **obj_attrib)
        self.type = object_type

    def sub(self, *child):
        """add one or a list of child elements as sub elmt"""
        # children=list(child)
        for a in PyOpenBrIMElmt.to_elmt_list(*child):
            self.elmt.append(a)

    def sub_par(self, par_name, par_value):
        self.sub(PrmElmt(par_name, par_value))

    def param(self, par_name, par_value, des='', role='', par_type=''):
        """sometimes, a just one OBJECT need the PARAMETER \n
        its better to define it when the OBJECT created.\n
        Example: <O> Circle need a <P> N="Radius" V="WebRadius". """
        self.sub(PrmElmt(par_name, par_value, des, role, par_type))

    def extend(self, extend_from):
        if isinstance(extend_from, ObjElmt):
            self.elmt.attrib['T'] = extend_from.elmt.attrib['T']
            self.elmt.attrib['Extends'] = extend_from.elmt.attrib['N']

    def prm_refer(self, elmt, refer_name):
        if isinstance(elmt, PyOpenBrIMElmt):
            self.sub(PrmElmt(refer_name, elmt.name,
                             par_type=elmt.get_attrib('T'), role=''))

    def move(self, dx, dy, dz):
        # @TODO
        pass

    def rotate(self, rx, ry, rz):
        pass


class PrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""

    def __init__(self, par_name, value, des='', role='', par_type='', ut='', uc=''):
        """create a new PARAMETER in OpenBrIM ParamML. \n
        Mandatory: name, value.\n
        D-> des is description of the parameter.\n
        par_type is the Type of parameter, such as Material. """
        if par_name:
            super(PrmElmt, self).__init__('P', par_name, V=str(value), D=des, UT=ut, UC=uc, Role=role, T=par_type)
            try:
                self.value = float(value)
                if self.value == int(self.value):
                    self.value = int(self.value)
            except (ValueError, TypeError):
                self.value = str(value)
            self.v = self.value  # just for short
        else:
            print('Parameter must have name and value')


class Project(ObjElmt):
    def __init__(self, proj_name, template='empty'):
        """create new project with a template"""
        super(Project, self).__init__('Project', proj_name)
        if template == 'template':
            origin_string = '<O N="" T="Project" D="A template in OpenBrIM Library">\n</O>'
        elif template == 'SI':
            origin_string = """
<O N="" T="Project" Alignment="None" TransAlignRule="Right">
    <O N="Units" T="Group">
        <O N="Internal" T="Unit" Length="Millimeter" Force="Newton" Angle="Radian" Temperature="Celsius" />
        <O N="Geometry" T="Unit" Length="Meter" Force="KiloNewton" Angle="Radian" Temperature="Celsius" />
        <O N="Property" T="Unit" Length="Millimeter" Force="Newton" Angle="Radian" Temperature="Celsius" />
    </O>
    <O N="SW" T="AnalysisCase" WeightFactor="-1" />
    <O N="Seismic" T="AnalysisCaseEigen" Modes="1" Gravity="9806.65" />
</O>
            """
        elif template == 'US':
            origin_string = """
<O N="" T="Project" Alignment="None" TransAlignRule="Right">
    <O N="Units" T="Group">
        <O N="Internal" T="Unit" Length="Inch" Force="Kip" Angle="Radian" Temperature="Fahrenheit" />
        <O N="Geometry" T="Unit" Length="Feet" Force="Kip" Angle="Degree" Temperature="Fahrenheit" />
        <O N="Property" T="Unit" Length="Inch" Force="Kip" Angle="Degree" Temperature="Fahrenheit" />
    </O>
    <O N="SW" T="AnalysisCase" WeightFactor="-1"/>
    <O Gravity="386.09" Modes="1" N="Seismic" T="AnalysisCaseEigen"/>
</O>
           """
        else:
            origin_string = '<O N="" T="Project">\n</O>'
        self.read_xmlstr(origin_string)
        self.elmt.attrib['N'] = proj_name

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


class Material(ObjElmt):
    def __init__(self, mat_name, des='', mat_type='', **attrib_dict):
        """Material name is mandatory.\n
        Material Type is Steel, Concrete, etc. Type is not T as T='Material'.\n
        there may be no other attributes.
        """
        super(Material, self).__init__('Material', mat_name, D=des, Type=mat_type, **attrib_dict)

    def mat_property(self, **name_value):
        """parameters generally defined of the material, \n
        such as d->Density, E-> modulus of elasticity, \n
        Nu->Poisson's Ratio, a->Coefficient of Thermal Expansion, \n
        Fc28/Fy/Fu -> Strength.
        """
        for key, value in name_value.items():
            self.add_mat_par(key, value)

    def add_mat_par(self, n, v, des=''):
        d = dict(d="Density",
                 E="modulus of Elasticity",
                 a="Coefficient of Thermal Expansion",
                 Nu="Poisson's Ratio",
                 Fc28="Concrete Compressive Strength",
                 Fy="Steel Yield Strength",
                 Fu="Steel Ultimate Strength").get(n)
        if des != '':
            d = des
        self.elmt.append(eET.Element('P', N=n, V=str(v), D=d))

    def show_mat(self):
        print('{} is {} ({}):'.format(self.name, self.elmt.attrib['Type'], self.elmt.attrib['D']))
        for each_par in self.elmt:
            print('\t<{0}>{3}: {1}={2} '.format(each_par.tag,
                                                each_par.attrib['N'],
                                                each_par.attrib['V'],
                                                each_par.attrib['D']))


class Section(ObjElmt):
    """section mandatory attribute is name.\n
    use a parameter to refer to a Material element."""

    def __init__(self, sect_name, material, *shape_list, **property_dict):
        super(Section, self).__init__('Section', sect_name)
        if isinstance(material, Material):
            self.sub(PrmElmt('Material', material.name, par_type='Material', des='Material_{}'.format(self.name)))
        self.sub(*shape_list)
        self.sect_property(**property_dict)

    def sect_property(self, **properties):
        """parameters generally mechanical characters, \n
        such as Ax, Iy, Iz, \n """
        for ch, value in properties.items():
            self.elmt.append(eET.Element('P', N=ch, V=str(value)))


class Shape(ObjElmt):

    def __init__(self, shape_name, *obj_list):
        super(Shape, self).__init__('Shape', shape_name)
        self.sub(*obj_list)
        # for point in point_list:
        #     self.sub(point)

    def is_cutout(self, y_n='Y'):
        if y_n.upper() == 'Y':
            self.sub(PrmElmt("IsCutout", "1", role="Input"))


class Circle(ObjElmt):

    def __init__(self, cir_name, radius, x=0, y=0, ):
        super(Circle, self).__init__('Circle', cir_name, X=str(x), Y=str(y))
        self.radius = radius
        self.sub(PrmElmt('Radius', radius))


class Unit(ObjElmt):

    def __init__(self, unit_name, angle_unit="Degree", force_unit="Newton", length_unit="Meter",
                 temperature_unit="Fahrenheit"):
        """units system of the project.\n
        name=Internal, Geometry, Property.\n
        angle_unit=Radian, Degree.\n
        force_unit=Kip\n
        length_unit=Inch, Meter\n
        temperature_unit=Fahrenheit\n
        """
        super(Unit, self).__init__('Unit', unit_name,
                                   angle=angle_unit,
                                   force=force_unit,
                                   length=length_unit,
                                   temperature=temperature_unit)


class Extends(ObjElmt):

    def __init__(self, extends_from):
        if isinstance(extends_from, ObjElmt):
            super(Extends, self).__init__(extends_from.elmt.attrib['T'], Extends=extends_from.elmt.attrib['N'])
        else:
            print('Should be extended from a OBJECT')


class Group(ObjElmt):

    def __init__(self, group_name, *elmts_list):
        super(Group, self).__init__('Group', obj_name=group_name)
        self.sub(*elmts_list)

    def regroup(self, *elmts):
        self.del_all_sub()
        self.sub(elmts)


class Point(ObjElmt):
    """T=Point
    Mandatory attribute: X, Y, Z"""

    def __init__(self, x, y, z=0, point_name=''):
        """coordinates x,y,z, may be parameters or real numbers."""
        super(Point, self).__init__('Point', obj_name=point_name,
                                    X=str(x), Y=str(y), Z=str(z))
        self.x = x
        self.y = y
        self.z = z
        # self.check_num()

    def check_num(self):
        """typically the coordinates should be numbers.
        But parameters are allowed, and in that case the values are strings"""
        if not isinstance(self.x, (int, float)):
            print('WARNING: X Coordinate is NOT a number.')
        if not isinstance(self.y, (int, float)):
            print('WARNING: Y Coordinate is NOT a number.')
        if self.z:
            if not isinstance(self.z, (int, float)):
                print('WARNING: Z Coordinate is NOT a number.')


class Line(ObjElmt):
    """T=Line, Two points and one section needed"""

    def __init__(self, point1, point2, section=None, line_name=''):
        super(Line, self).__init__('Line', line_name)
        self.add_point(point1)
        self.p1 = (point1.x, point1.y)
        self.add_point(point2)
        self.p2 = (point2.x, point2.y)
        self.set_section(section)

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
        if isinstance(point_obj, Point):
            self.elmt.append(point_obj.elmt)
        else:
            print('Type Error: Point Object is required.')

    def set_section(self, section_obj):
        """section has attribute of material. default is <O Extends=>"""
        if isinstance(section_obj, (Section, Extends)):
            self.sub(Extends(section_obj))
        elif isinstance(section_obj, str):
            print('{} section is not a SECTION object'.format(self.name))
            self.sub(PrmElmt('', section_obj))
        else:
            print('No Section.')


class Surface(ObjElmt):
    def __init__(self, point1, point2, point3, point4, thick_par=None, material_obj=None, surface_name=''):
        super(Surface, self).__init__('Surface', surface_name)
        self.add_point(point1)
        self.p1 = (point1.x, point1.y, point1.z)
        self.add_point(point2)
        self.p2 = (point2.x, point2.y, point2.z)
        self.add_point(point3)
        self.p3 = (point3.x, point3.y, point3.z)
        self.add_point(point4)
        self.p4 = (point4.x, point4.y, point4.z)
        if material_obj:
            self.refer_mat_obj(material_obj)
        if thick_par:
            self.thick_par(thick_par)
        self.check_surface()

    def check_surface(self):
        """should have >= 3 Points, 1 Thickness and 1 Material"""
        if len(self.elmt.findall("./O[@T='Point']")) < 3:
            print('> Warning: Not 4 Points in the Surface OBJECT: {}'.format(self.name))
            return False
        if len(self.elmt.findall("./P[@N='Thickness']")) != 1:
            print('> Warning: Not a thick parameter in the Surface object {}'.format(self.name))
            return False
        if len(self.elmt.findall("./P[@T='Material']")) != 1:
            print('> Warning: Not a material parameter in the Surface object {}'.format(self.name))
            return False
        return True

    def add_point(self, point_obj):
        if isinstance(point_obj, Point):
            self.elmt.append(point_obj.elmt)
        else:
            print('An object of Point is needed')

    def thick_par(self, thick_par):
        # if isinstance(thick_par, PrmElmt) and PyOpenBrIMElmt.match_attribute(thick_par.elmt, N='Thickness'):
        if isinstance(thick_par, PrmElmt):
            self.sub(PrmElmt('Thickness', thick_par.elmt.attrib['N'], role=''))
        elif isinstance(thick_par, (float, int)):
            self.sub(PrmElmt("Thickness", str(thick_par)))
        elif isinstance(thick_par, str):
            self.sub(PrmElmt("Thickness", thick_par))
        else:
            print("{} requires a PARAMETER @N=Thickness.".format(self.name))

    def refer_mat_obj(self, mat_obj):
        """material is an OBJECT.\n
        But in Surface it should be a parameter that refer to the Material Object\n
        not mandatory"""
        if isinstance(mat_obj, Material):
            self.sub(PrmElmt('Material', mat_obj.elmt.attrib['N'],
                             par_type='Material',
                             role='',
                             des='Material_Surface_{}'.format(self.name)))
        elif isinstance(mat_obj, str):
            print('Material of Surface {} is a string, please make sure'.format(self.name))
            self.sub(PrmElmt('Material', mat_obj,
                             par_type='Material',
                             role='',
                             des='Material_Surface_{}'.format(self.name)))
        else:
            print("{} requires an OBJECT of Material.".format(self.name))

    def change_thick(self, thickness, des='', role='', par_type='Surface_Thickness', ut='', uc=''):
        """thickness parameter of Surface.\n Only thickness is mandatory"""
        self.check_del_sub('P', N="Thickness")
        self.sub(PrmElmt("Thickness", str(thickness), des, role, par_type, ut, uc))
        # self.elmt.append(eET.Element
        # ('P', dict(N="Thickness", V=str(thickness), D=des, Role=role, T=par_type, UT=ut, UC=uc)))

    def change_material(self, material, des='', role='', name='SurfaceMaterial', ut='', uc=''):
        """material parameter of Surface.\n Only material is mandatory"""
        self.check_del_sub('P', T="Material")
        self.sub(PrmElmt(name, material, des, role, 'Material', ut, uc))
        # self.elmt.append(eET.Element('P', dict(T='Material', V=material, D=des, N=name, Role=role, UT=ut, UC=uc)))

    def calc_area(self):
        pass


class Volume(ObjElmt):

    def __init__(self, volume_name, x, y, z):
        super(Volume, self).__init__('Volume', volume_name)
        self.x = x
        self.y = y
        self.z = z
        self.add_attr(X=self.x,Y=self.y,Z=self.z)

    def set_surface(self,point1, point2, point3, point4):
        self.sub(Surface(point1, point2, point3, point4))

class FENode(ObjElmt):

    def __init__(self, x, y, z, node_name=''):
        super(FENode, self).__init__('Node', node_name, X=x, Y=y, Z=z)
        self.x = x
        self.y = y
        self.z = z
        self.tx = 0
        self.ty = 0
        self.tz = 0
        self.rx = 0
        self.ry = 0
        self.rz = 0

    def coordinate(self, x, y, z):
        self.x = x
        self.elmt.attrib['X'] = str(x)
        self.y = y
        self.elmt.attrib['Y'] = str(y)
        self.z = z
        self.elmt.attrib['Z'] = str(z)

    def fixity(self, tx=0, ty=0, tz=0, rx=0, ry=0, rz=0):
        self.tx = tx
        self.elmt.attrib['Tx'] = str(tx)
        self.ty = ty
        self.elmt.attrib['Ty'] = str(ty)
        self.tz = tz
        self.elmt.attrib['Tz'] = str(tz)
        self.rx = rx
        self.elmt.attrib['Rx'] = str(rx)
        self.ry = ry
        self.elmt.attrib['Ry'] = str(ry)
        self.rz = rz
        self.elmt.attrib['Rz'] = str(rz)

    def as_point(self, point_obj):
        if isinstance(point_obj, Point):
            self.copy_attrib_from(point_obj, 'X', 'Y', 'Z')
            self.x = point_obj.x
            self.y = point_obj.y
            self.z = point_obj.z
            # self.name=point_obj.name
            return self
        else:
            print('{} is not a Point Object'.format(point_obj))


class FELine(ObjElmt):

    def __init__(self, node1, node2, section, beta_angle=0, feline_name=''):
        super(FELine, self).__init__('FELine', feline_name)
        if isinstance(node1, FENode) and isinstance(node2, FENode) and isinstance(section, Section):
            self.prm_refer(node1, 'Node1')
            self.n1 = node1
            self.prm_refer(node2, 'Node2')
            self.n2 = node2
            self.prm_refer(section, 'Section')
        if beta_angle:
            self.param_simple('BetaAngle', beta_angle, '')

    def as_line(self, line_obj: Line):
        pass

    def set_node_start(self, node):
        self.del_sub('P', N='Node1')
        self.prm_refer(node, 'Node1')
        self.n1 = node

    def set_node_end(self, node):
        self.del_sub('P', N='Node2')
        self.prm_refer(node, 'Node2')
        self.n2 = node


class FESurface(ObjElmt):

    def __init__(self, node1, node2, node3, node4, thick_par, material_obj, fes_name=''):
        super(FESurface, self).__init__('FESurface', fes_name)
        self.prm_refer(node1, 'Node1')
        self.n1 = (node1.x, node1.y, node1.z)
        self.prm_refer(node2, 'Node2')
        self.n2 = (node2.x, node2.y, node2.z)
        self.prm_refer(node3, 'Node3')
        self.n3 = (node3.x, node3.y, node3.z)
        self.prm_refer(node4, 'Node4')
        self.n4 = (node4.x, node4.y, node4.z)
        self.prm_refer(thick_par, 'Thickness')
        self.prm_refer(material_obj, 'Material')

    def as_surface(self, surface_obj):
        pass


class ShowTree(object):
    """show results in tree-like format"""

    def __init__(self, result):
        self.elmts = PyOpenBrIMElmt.to_elmt_list(result)
        for one_branch in self.elmts:
            ShowTree.branch(one_branch, 0)

    @staticmethod
    def branch(elmt, level):
        for tab in range(level):
            print('.   ', end='')
        other_info = ''
        for key in elmt.attrib:
            other_info = other_info + '{}={}\t'.format(key, elmt.attrib[key])
        # for key in ['T', 'N', 'V', 'Extends']:
        #     if elmt.attrib.get(key):
        #         other_info = other_info + '{}={}\t'.format(key, elmt.attrib[key])
        print('|--<{}> {}'.format(elmt.tag, other_info))
        for sub in elmt:
            ShowTree.branch(sub, level + 1)


class ShowTable(object):
    """this class is used to show search results in format of table"""

    def __init__(self, result):
        self.elmts = PyOpenBrIMElmt.to_elmt_list(result)
        self.result_obj = eET.Element("", {})
        self.result_par = eET.Element("", {})
        self.classify_elmts()
        self.show_table()

    # separate OBJECT and PARAMetER
    def classify_elmts(self):
        for elmt in self.elmts:
            if elmt.tag is 'P':
                self.result_par.append(elmt)
            if elmt.tag is 'O':
                self.result_obj.append(elmt)

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
        for elmt in self.result_obj:
            row = []
            if 'N' in elmt.attrib:
                row.append(elmt.attrib.get("N"))
                elmt.attrib.pop('N')
            else:
                row.append('---')
            row.append(elmt.attrib.get("T"))
            elmt.attrib.pop('T')
            if 'D' in elmt.attrib:
                row.append(elmt.attrib.get("D"))
                del elmt.attrib['D']
            else:
                row.append('---')
            other = ''
            for k, v in elmt.attrib.items():
                other = other + k + '=' + v + ', '
            row.append(other[:-2])
            tb.add_row(row)
        print('\n Table of Result OBJECT')
        print(tb)

    def show_parameters(self):
        tb = pt.PrettyTable(["Name", "Value", "Description", "Other Attributes"])
        tb.align["Other Attributes"] = "l"
        for elmt in self.result_par:
            row = [elmt.attrib.get("N"), elmt.attrib.get("V")]
            elmt.attrib.pop('N')
            elmt.attrib.pop('V')
            if 'D' in elmt.attrib:
                row.append(elmt.attrib.get("D"))
                del elmt.attrib['D']
            else:
                row.append('---')
            other = ''
            for k, v in elmt.attrib.items():
                other = other + k + '=' + v + ', '
            row.append(other[:-2])
            tb.add_row(row)
        print('\n Table of Result PARAMetER')
        print(tb)
