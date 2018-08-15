#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Object-oriented programming for OpenBrIM.
Directly to ParamML transfer.
'''

import re
import xml.etree.ElementTree as eET

import prettytable as pt


class PyOpenBrIMElmt(object):
    """basic class for ParamML file of OpenBrIM"""

    def __init__(self, tag_o_p, name, **attrib_dict):
        if name:
            _attributes = dict(N=name)
        else:
            _attributes = {}
        for _k, _v in attrib_dict.items():
            # if _v:
            _attributes[_k] = str(_v)
        self.elmt = eET.Element(tag_o_p, **_attributes)
        self.name = name

    def parse_xmlfile(self, xml_path):
        """ read a xml_file"""
        if re.match(".*\.xml", xml_path):
            tree = eET.parse(xml_path)
            self.elmt = tree.getroot()
        else:
            print('"{}" is not a .xml_file!'.format(xml_path))

    def read_xmlstr(self, xmlstr):
        """read xml string"""
        self.elmt = eET.fromstring(xmlstr)

    def attach_to(self, parent):
        """attach this element to parent element(s)"""
        for _parent in PyOpenBrIMElmt.to_elmt_list(parent):
            _parent.append(self.elmt)

    def show_info(self, if_sub=False):
        """show tags and attributes of itself or sub elements"""
        print('<{}> {}'.format(self.elmt.tag, self.elmt.attrib))
        if if_sub:
            self.show_sub()

    def sub(self, *child):
        """add one or a list of child elements as sub elmt"""
        # children=list(child)
        for a in PyOpenBrIMElmt.to_elmt_list(*child):
            self.elmt.append(a)

    def show_sub(self):
        """show all sub elements' tags and attributes"""
        _count = 0
        print('- Sub elements of "{}":'.format(self.name))
        for _child in self.elmt:
            _count = _count + 1
            print('  - <{}> {}'.format(_child.tag, _child.attrib))
        print('- Totally {} sub elements.\n'.format(_count))

    def get_attrib(self, key):
        _value = self.elmt.attrib.get(key)
        if _value:
            try:
                _fv = float(_value)
                # print('# {}.{} is a float of {}'.format(self.name, key, _fv))
                return _fv
            except ValueError:
                # print('# {}.{} is not a float'.format(self.name, key))
                return _value
        else:
            print('!BrParamML.get_attrib: {} does not have the attribute of {}'.format(self.name, key))
            return

    def set_attrib(self, **attrib_dict):
        for _key, _value in attrib_dict.items():
            if self.elmt.attrib.get(_key):
                print('Update {}.{} with new value <{}>'.format(self.name, _key, _value))
            else:
                print('Add {} new attribute <{}> = <{}>'.format(self.name, _key, _value))
            self.elmt.set(_key, str(_value))

    def copy_attrib_from(self, elmt, *attrib_key_list):
        """copy from an element the attributes in the dict"""
        _temp = PyOpenBrIMElmt.to_ob_elmt(elmt)
        if not attrib_key_list:
            self.set_attrib(**_temp.attrib)
        else:
            for _key in attrib_key_list:
                try:
                    self.elmt.set(_key, _temp.attrib[_key])
                except KeyError:
                    print('Element {} has no attribute {}, so set to 0'.format(elmt.name, _key))
                    self.elmt.set(_key, '0')

    def findall_by_xpath(self, xpath):
        """return a list of all sub elmt that matched the
        (xpath)[https://docs.python.org/3/library/xml.etree.elementtree.
        html?highlight=xpath#xpath-support]"""
        # tree = eET.ElementTree(self.elmt)
        # results = tree.findall(xpath)
        _results = self.elmt.findall(xpath)
        print("ALL Results of '{}' in {} are:".format(xpath, self.name))
        for _one in _results:
            print('  - <{}> {}'.format(_one.tag, _one.attrib))
        return _results

    def find_by_xpath(self, xpath):
        _result = self.elmt.find(xpath)
        print("One Result of '{}' in {} are:".format(xpath, self.name))
        print('  - <{}> {}'.format(_result.tag, _result.attrib))
        return _result

    def find_sub_by_attributes(self, **attributes):
        """only the sub nodes, no sub-sub nodes"""
        _results = []
        for _one_elmt in self.elmt:
            if PyOpenBrIMElmt.match_attribute(_one_elmt, **attributes):
                _results.append(_one_elmt)
        return _results

    def findall_by_attribute(self, **attributes):
        """find in elmt.iter() by the attributes"""
        # results is a list[] of elements
        _results = []
        for any_elmt in self.elmt.iter():
            if PyOpenBrIMElmt.match_attribute(any_elmt, **attributes):
                _results.append(any_elmt)
        return _results

    def del_all_sub(self):
        """remove all sub elements from this elmt"""
        _del = self.elmt.findall('./')
        print('These elements will be deleted')
        for _d in _del:
            print('<{}> {}'.format(_d.tag, _d.attrib))
            self.elmt.remove(_d)
        # self.elmt.clear() remove subs, but also all attributes of itself

    def del_sub(self, tag='O or P', **attrib_dict):
        _elmt_to_del = []
        for _child in self.elmt:
            if PyOpenBrIMElmt.match_tag(_child, tag) and PyOpenBrIMElmt.match_attribute(_child, **attrib_dict):
                _elmt_to_del.append(_child)
        for _d in _elmt_to_del:
            self.elmt.remove(_d)

    def check_del_sub(self, tag='O or P', **attrib_dict):
        """remove elmt with particular tag and attributes"""
        elmt_to_del = []
        confirm = False
        for _child in self.elmt:
            if PyOpenBrIMElmt.match_tag(_child, tag) and PyOpenBrIMElmt.match_attribute(_child, **attrib_dict):
                elmt_to_del.append(_child)
        # list all elmt to be deleted
        if elmt_to_del:
            print('Confirm the Elements to be deleted')
            for one in elmt_to_del:
                print('<{}> {}'.format(one.tag, one.attrib))
            confirm = input('Sure to delete? True/False:\n')
        else:
            print('Find NO element to delete')
        # verify if delete or not
        if confirm:
            for one in elmt_to_del:
                self.elmt.remove(one)
            print('Totally {} elements deleted'.format(len(elmt_to_del)))

    def __len__(self):
        return len(self.elmt)

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
            print(
                'Type of <{}> is {}.\nUnacceptable type to be converted to OpenBrIM elements.'.format(elmt, type(elmt)))

    @staticmethod
    def prm_to_value(elmt):
        """PARAMETER to its value"""
        if isinstance(elmt, OBPrmElmt):
            return elmt.value
        elif isinstance(elmt, (int, float)):
            return elmt
        else:
            print('{} is not a <P>')

    @staticmethod
    def prm_to_name(elmt):
        """PARAMETER to its name, maybe used when refer?"""
        if isinstance(elmt, OBPrmElmt):
            return elmt.get_attrib('N')
        elif isinstance(elmt, str):
            return elmt
        else:
            print('{} is not a <P>')


class OBObjElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <O>"""
    _REQUIRE=['name']

    def __init__(self, ob_type, name='', **obj_attrib):
        """create a new OBJECT in OpenBrIM ParamML.\n
        Mandatory is Type <O T= ? > such as Point, Line, Group, ...\n
        N = ? as name is recommended to be provided.\n
        attributes are in format of dict.
        """
        self.type = ob_type
        super(OBObjElmt, self).__init__('O', name, T=ob_type, **obj_attrib)

    # def sub(self, *child):
    #     """add one or a list of child elements as sub elmt"""
    #     # children=list(child)
    #     for a in PyOpenBrIMElmt.to_elmt_list(*child):
    #         self.elmt.append(a)

    def sub_new_par(self, par_name, par_value):
        self.sub(OBPrmElmt(par_name, par_value))

    def new_parameter(self, par_name, par_value, des='', role='', par_type=''):
        """sometimes, a just one OBJECT need the PARAMETER \n
        its better to define it when the OBJECT created.\n
        Example: <O> Circle need a <P> N="Radius" V="WebRadius". """
        self.sub(OBPrmElmt(par_name, par_value, des, role, par_type))

    def extend(self, extend_from):
        if isinstance(extend_from, OBObjElmt):
            self.elmt.attrib['T'] = extend_from.elmt.attrib['T']
            self.elmt.attrib['Extends'] = extend_from.elmt.attrib['N']

    def refer_elmt(self, elmt, refer_name):
        if isinstance(elmt, PyOpenBrIMElmt):
            self.sub(OBPrmElmt(refer_name, elmt.name,
                               ob_type=elmt.get_attrib('T'), role=''))

    def move_to(self, new_x, new_y, new_z):
        self.set_attrib(X=new_x, Y=new_y, Z=new_z)

    def rotate_angle(self, angle_x=0, angle_y=0, angle_z=0):
        self.set_attrib(RX=angle_x, RY=angle_y, RZ=angle_z)

    #
    # def rotate_one(self, r_axis, cosine):
    #     """ undecided how"""
    #     if -1 <= cosine <= 1:
    #         if cosine == 0:
    #             return
    #         elif cosine == 1:
    #             self.set_attrib(**{r_axis: 'PI/2'})
    #     else:
    #         print('Value Error for cosine of {}'.format(self.name))


class OBPrmElmt(PyOpenBrIMElmt):
    """Sub-class of PyOpenBrIMElmt for tag <P>"""
    _REQUIRE = ['name', 'value', 'ob_type']

    def __init__(self, name, value, des='', role='', ob_type='', ut='', uc=''):
        """create a new PARAMETER in OpenBrIM ParamML. \n
        Mandatory: name, value.\n
        D-> des is describe of the parameter.\n
        par_type is the Type of parameter, such as Material. """
        _name = name.strip()
        if not _name:
            print('The name of Parameter cannot be EMPTY')
            raise ValueError
        try:
            self.value = float(value)
            if self.value == int(self.value):
                self.value = int(self.value)
        except ValueError:
            self.value = str(value)
        super(OBPrmElmt, self).__init__('P', _name, V=self.value, D=des, UT=ut, UC=uc, Role=role, T=ob_type)

    def sub(self, *child):
        super(OBPrmElmt, self).sub()
        print("BrParamML.OBPrmELMT cannot sub child elements.s")
        raise TypeError


class OBProject(OBObjElmt):
    _REQUIRE = ['name', ]

    def __init__(self, name, template='SI'):
        """create new project with a template"""
        super(OBProject, self).__init__('Project', name)
        if template == 'template':
            origin_string = '<O T="Project" D="A template in OpenBrIM Library">\n</O>'
        elif template == 'SI':
            origin_string = """
<O T="Project" Alignment="None" TransAlignRule="Right">
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
<O T="Project" Alignment="None" TransAlignRule="Right">
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
            origin_string = '<O T="Project">\n</O>'
        self.read_xmlstr(origin_string)
        self.elmt.attrib['N'] = name

    def save_project(self, path=''):
        """save this element as a Project in a xml_file. \n
        Must have an Project name as the file name. \n
        default path is the same folder with .py. \n
        default file name is the element name. \n
        may input a new file path."""
        if self.elmt.attrib['N'] == '':
            self.name = input('Please name the project:\n')
        self.elmt.attrib['N'] = self.name
        if path == '':
            out_path = self.name + '.xml'
        elif re.match('.*\.xml', path):
            out_path = path
        else:
            print('Error: should be a xml_file')
            raise ValueError
        tree = eET.ElementTree(self.elmt)
        tree.write(out_path, encoding="utf-8", xml_declaration=True)
        print('Project is saved @ "{}".'.format(out_path))


class OBMaterial(OBObjElmt):
    _DESDICT = dict(d="Density",
                    E="modulus of Elasticity",
                    a="Coefficient of Thermal Expansion",
                    Nu="Poisson's Ratio",
                    Fc28="Concrete Compressive Strength",
                    Fy="Steel Yield Strength",
                    Fu="Steel Ultimate Strength")
    _REQUIRE = ['name', *_DESDICT.keys()]

    def __init__(self, name, des='', ob_type='', **attrib_dict):
        """Material name is mandatory.\n
        Material Type is Steel, Concrete, etc. Type is not T as T='Material'.\n
        there may be no other attributes.
        """
        super(OBMaterial, self).__init__('Material', name, D=des, Type=ob_type)
        self.mat_property(**attrib_dict)

    def mat_property(self, **key_value):
        """parameters generally defined of the material, \n
        such as d->Density, E-> modulus of elasticity, \n
        Nu->Poisson's Ratio, a->Coefficient of Thermal Expansion, \n
        Fc28/Fy/Fu -> Strength.
        """
        for _key, _value in key_value.items():
            self.add_mat_par(_key, _value)

    def add_mat_par(self, n, v, _des=''):
        if not _des:
            _des = OBMaterial._DESDICT.get(n)
        self.new_parameter(n, str(v), des=_des)
        # self.elmt.append(eET.Element('P', N=n, V=str(v), D=_des))

    def show_mat_table(self):
        print('{} is {} ({}):'.format(self.name, self.elmt.attrib['Type'], self.elmt.attrib['D']))
        tb = pt.PrettyTable(["Tag", "Name", "Value", "Description"])
        tb.align = 'l'
        for each_par in self.elmt:
            row = [each_par.tag, each_par.attrib['N'], each_par.attrib['V'], each_par.attrib['D']]
            tb.add_row(row)
        print('Table of Material parameters:')
        print(tb)


class OBSection(OBObjElmt):
    """section mandatory attribute is name.\n
    use a parameter to refer to a Material element."""
    _REQUIRE = ['name', 'material_ob']

    def __init__(self, name, material_ob=None, *shape_ob):
        super(OBSection, self).__init__('Section', name)
        if isinstance(material_ob, OBMaterial):
            self.sub(OBPrmElmt('Material', material_ob.name, ob_type='Material', des='Material_{}'.format(self.name)))
        self.sub(*shape_ob)

    def sect_property(self, **properties):
        """parameters generally mechanical characters, \n
        such as Ax, Iy, Iz, \n """
        for _property_name, _property_value in properties.items():
            self.elmt.append(OBPrmElmt(_property_name, str(_property_value)))


class OBShape(OBObjElmt):
    _REQUIRE = ['name', 'points']

    def __init__(self, name, *point_ob):
        super(OBShape, self).__init__('Shape', name)
        self.sub(*point_ob)

    def is_cutout(self, y_n=True):
        if y_n:
            self.sub(OBPrmElmt("IsCutout", "1", role="Input"))


class OBCircle(OBObjElmt):
    _REQUIRE = ['name', 'radius']

    def __init__(self, name, radius, x=0, y=0, ):
        super(OBCircle, self).__init__('Circle', name, X=str(x), Y=str(y))
        self.radius = radius
        self.sub(OBPrmElmt('Radius', radius))


class OBUnit(OBObjElmt):
    _REQUIRE = ['name']

    def __init__(self, name,
                 angle_unit="Degree",
                 force_unit="Newton",
                 length_unit="Meter",
                 temperature_unit="Fahrenheit"):
        """units system of the project.\n
        name=Internal, Geometry, Property.\n
        angle_unit=Radian, Degree.\n
        force_unit=Kip\n
        length_unit=Inch, Meter\n
        temperature_unit=Fahrenheit\n
        """
        super(OBUnit, self).__init__('Unit', name,
                                     angle=angle_unit,
                                     force=force_unit,
                                     length=length_unit,
                                     temperature=temperature_unit)


class OBExtends(OBObjElmt):

    def __init__(self, extends_from_ob):
        if isinstance(extends_from_ob, OBObjElmt):
            super(OBExtends, self).__init__(extends_from_ob.elmt.attrib['T'], Extends=extends_from_ob.elmt.attrib['N'])
        else:
            print('Should be extended from a OBJECT')


class OBGroup(OBObjElmt):
    _REQUIRE = ['name', 'id']

    def __init__(self, name, *elmt_ob_list):
        super(OBGroup, self).__init__('Group', name=name)
        self.sub(*elmt_ob_list)

    def regroup(self, *elmts):
        self.del_all_sub()
        self.sub(elmts)

    def __len__(self):
        return len(self.elmt)


class OBFENode(OBObjElmt):
    _REQUIRE = ['name', 'x', 'y', 'z', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'Tx', 'Ty', 'Tz', 'Rx', 'Ry', 'Rz']

    def __init__(self, x, y, z, tx=0, ty=0, tz=0, rx=0, ry=0, rz=0, name=''):
        super(OBFENode, self).__init__('Node', name,
                                       X=x, Y=y, Z=z,
                                       Tx=tx, Ty=ty, Tz=tz,
                                       Rx=rx, Ry=ry, Rz=rz)
        self.x = x
        self.y = y
        self.z = z
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def set_coordinate(self, x, y, z):
        self.x = x
        self.elmt.attrib['X'] = str(x)
        self.y = y
        self.elmt.attrib['Y'] = str(y)
        self.z = z
        self.elmt.attrib['Z'] = str(z)

    def set_fixity(self, tx=0, ty=0, tz=0, rx=0, ry=0, rz=0):
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

    def same_as_point(self, point_ob):
        if isinstance(point_ob, OBPoint):
            self.copy_attrib_from(point_ob, 'X', 'Y', 'Z')
            self.x = point_ob.x
            self.y = point_ob.y
            self.z = point_ob.z
            return self
        else:
            print('{} is not a Point OBObject'.format(point_ob))


class OBFELine(OBObjElmt):
    _REQUIRE = ['name', 'node1_ob', 'node2_ob', 'section_ob']

    def __init__(self, node1_ob, node2_ob, section_ob, beta_angle=0, name=''):
        super(OBFELine, self).__init__('FELine', name)
        if isinstance(node1_ob, OBFENode) and isinstance(node2_ob, OBFENode) and isinstance(section_ob, OBSection):
            self.refer_elmt(node1_ob, 'Node1')
            # self.n1 = node1_ob
            self.refer_elmt(node2_ob, 'Node2')
            # self.n2 = node2_ob
            self.refer_elmt(section_ob, 'Section')
        if beta_angle:
            self.new_parameter('BetaAngle', beta_angle)

    def set_node_start(self, node):
        self.del_sub('P', N='Node1')
        self.refer_elmt(node, 'Node1')
        self.n1 = node

    def set_node_end(self, node):
        self.del_sub('P', N='Node2')
        self.refer_elmt(node, 'Node2')
        self.n2 = node


class OBFESurface(OBObjElmt):
    _REQUIRE = ['name', 'node1_ob', 'node2_ob', 'node3_ob', 'node4_ob', 'thick_prm_ob', 'material_ob']

    def __init__(self, node1_ob, node2_ob, node3_ob, node4_ob, thick_prm_ob, material_ob, name=''):
        super(OBFESurface, self).__init__('FESurface', name)
        self.refer_elmt(node1_ob, 'Node1')
        # self.n1 = (node1_ob.x, node1_ob.y, node1_ob.z)
        self.refer_elmt(node2_ob, 'Node2')
        # self.n2 = (node2_ob.x, node2_ob.y, node2_ob.z)
        self.refer_elmt(node3_ob, 'Node3')
        # self.n3 = (node3_ob.x, node3_ob.y, node3_ob.z)
        self.refer_elmt(node4_ob, 'Node4')
        # self.n4 = (node4_ob.x, node4_ob.y, node4_ob.z)
        self.refer_elmt(thick_prm_ob, 'Thickness')
        self.refer_elmt(material_ob, 'Material')


class OBPoint(OBObjElmt):
    """T=Point
    Mandatory attribute: X, Y, Z"""
    _REQUIRE = ['name', 'x', 'y', 'z']

    def __init__(self, x, y, z=0, name=''):
        """coordinates x,y,z, may be parameters or real numbers."""
        super(OBPoint, self).__init__('Point', name=name, X=x, Y=y, Z=z)
        self.x = x
        self.y = y
        self.z = z
        # self.check_num()

    def same_as_node(self, node_ob):
        assert isinstance(node_ob, OBFENode), TypeError
        self.copy_attrib_from(node_ob, 'X', 'Y', 'Z')
        self.x = node_ob.x
        self.y = node_ob.y
        self.z = node_ob.z
        return self

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


class OBLine(OBObjElmt):
    """T=Line, Two points and one section needed."""
    _REQUIRE = ['name', 'node1_ob', 'node2_ob', 'section_ob']

    def __init__(self, node1_ob, node2_ob, section_ob=None, name=''):
        super(OBLine, self).__init__('Line', name)
        self.add_point(node1_ob)
        # self.p1 = (node1OB.x, node1OB.y)
        self.add_point(node2_ob)
        # self.p2 = (node2OB.x, node2OB.y)
        self.set_section(section_ob)

    def check_line(self):
        """should have Two Points and One Section"""
        points = self.elmt.findall("./O[@T='Point']")
        sects = self.elmt.findall("./O[@T='Section']")
        if len(points) != 2:
            return False
        if len(sects) != 1:
            return False
        return True

    def line_update(self, point1_ob, point2_ob, section_ob):
        self.add_point(point1_ob)
        self.add_point(point2_ob)
        self.set_section(section_ob)

    def add_point(self, point_ob):
        if isinstance(point_ob, OBPoint):
            self.elmt.append(point_ob.elmt)
        elif isinstance(point_ob, OBFENode):
            self.elmt.append(OBPoint(0, 0).same_as_node(point_ob).elmt)
        else:
            print('Type Error: Point Object is required.')

    def set_section(self, section_ob):
        """section has attribute of material. default is <O Extends=>"""
        if isinstance(section_ob, OBSection):
            self.sub(OBExtends(section_ob))
            # self.sub(section_obj)
        elif isinstance(section_ob, str):
            print('{} section is not a SECTION object'.format(self.name))
            self.sub(OBPrmElmt('Section', section_ob))
        else:
            print('No Section.')


class OBSurface(OBObjElmt):
    _REQUIRE = ['name', 'node1_ob', 'node2_ob', 'node3_ob', 'node4_ob', 'thick_prm_ob', 'material_ob']

    def __init__(self, node1_ob, node2_ob, node3_ob, node4_ob, thick_prm_ob=None, material_ob=None, name=''):
        super(OBSurface, self).__init__('Surface', name)
        self.add_point(node1_ob)
        # self.p1 = (point1OB.x, point1OB.y, point1OB.z)
        self.add_point(node2_ob)
        # self.p2 = (point2OB.x, point2OB.y, point2OB.z)
        self.add_point(node3_ob)
        # self.p3 = (point3OB.x, point3OB.y, point3OB.z)
        self.add_point(node4_ob)
        # self.p4 = (point4OB.x, point4OB.y, point4OB.z)
        if material_ob:
            self.refer_mat_obj(material_ob)
        if thick_prm_ob:
            self.thick_par(thick_prm_ob)
        # self.check_surface()

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

    def add_point(self, point_ob):
        if isinstance(point_ob, OBPoint):
            self.elmt.append(point_ob.elmt)
        elif isinstance(point_ob, OBFENode):
            self.elmt.append(OBPoint(0, 0).same_as_node(point_ob).elmt)
        else:
            print('Type Error: Point Object is required.')

    def thick_par(self, thick_par):
        # if isinstance(thick_par, PrmElmt) and PyOpenBrIMElmt.match_attribute(thick_par.elmt, N='Thickness'):
        if isinstance(thick_par, OBPrmElmt):
            self.sub(OBPrmElmt('Thickness', thick_par.elmt.attrib['N'], role=''))
        elif isinstance(thick_par, (float, int)):
            self.sub(OBPrmElmt("Thickness", str(thick_par)))
        elif isinstance(thick_par, str):
            self.sub(OBPrmElmt("Thickness", thick_par))
        else:
            print("{} requires a PARAMETER @N=Thickness.".format(self.name))

    def refer_mat_obj(self, mat_ob):
        """material is an OBJECT.\n
        But in Surface it should be a parameter that refer to the Material Object\n
        not mandatory"""
        if isinstance(mat_ob, OBMaterial):
            self.sub(OBPrmElmt('Material', mat_ob.elmt.attrib['N'],
                               ob_type='Material',
                               role='',
                               des='Material_Surface_{}'.format(self.name)))
        elif isinstance(mat_ob, str):
            # print('Material of Surface <{}> is a string, please make sure'.format(self.name))
            self.sub(OBPrmElmt('Material', mat_ob,
                               ob_type='Material',
                               role='',
                               des='Material_Surface_{}'.format(self.name)))
        else:
            print("{} requires an OBJECT of Material.".format(self.name))

    def change_thick(self, thickness, des='', role='', par_type='Surface_Thickness', ut='', uc=''):
        """thickness parameter of Surface.\n Only thickness is mandatory"""
        self.check_del_sub('P', N="Thickness")
        self.sub(OBPrmElmt("Thickness", str(thickness), des, role, par_type, ut, uc))

    def change_material(self, material, des='', role='', name='SurfaceMaterial', ut='', uc=''):
        """material parameter of Surface.\n Only material is mandatory"""
        self.check_del_sub('P', T="Material")
        self.sub(OBPrmElmt(name, material, des, role, 'Material', ut, uc))


class OBVolume(OBObjElmt):
    _REQUIRE = ['name', 'surface1_ob', 'surface2_ob']

    def __init__(self, surface1_ob, surface2_ob, name=''):
        super(OBVolume, self).__init__('Volume', name)
        self.sub(surface1_ob, surface2_ob)

    def set_surface(self, point1, point2, point3, point4):
        self.sub(OBSurface(point1, point2, point3, point4))


class OBText3D(OBObjElmt):
    def __init__(self, text, x, y, z, size=5):
        super(OBText3D, self).__init__('Text3D', '', Label=text, FontSize=str(size))
        self.sub(OBPoint(x, y, z))
        self.sub(OBPoint(x + 5, y, z))
        self.sub(OBPoint(x, y, z + 5))


class ShowTree(object):
    """show results in tree-like format"""

    def __init__(self, result):
        print("\n|.... ElementTree Start")
        self.elmts = PyOpenBrIMElmt.to_elmt_list(result)
        for one_branch in self.elmts:
            ShowTree.branch(one_branch, 0)
        print("|.... ElementTree End\n")

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
            if 'D ' in elmt.attrib:
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
