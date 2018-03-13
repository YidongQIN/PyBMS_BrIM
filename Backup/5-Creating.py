import xml.etree.ElementTree as ET
import PyOpenBrIM as ob

# N and V is mandatory
def del_empty_value(dict):
    new_dict = {}
    for key in dict:
        if dict[key] != '':
            new_dict[key] = dict[key]
    return new_dict


def new_P(name, value, des='', UT='', UC='', role='', type_P=''):
    attribute_P = {'N': name, 'V': value, 'D': des, 'UT': UT, 'UC': UC, 'Role': role, 'T': type_P}
    attribute_P = del_empty_value(attribute_P)
    element = ET.Element('P', attribute_P)
    return element


'''emp of Object
    <O N="Sections" T="Group">
        <O N="Section_BottomChord" T="Section">
'''


def new_O(type_O, *name):
    if name == ():
        attribute_O={'T': type_O}
    else:
        attribute_O = {'T': type_O, 'N': name[0]}
    element = ET.Element('O', attribute_O)
    return element

# object 需要创建模板，即上面是一个总体的，下面根据每种type编写模板化的
# ----main----

# root = ob.new_OpenBrIM('New_OpenBrIM_project')
#
# results = ob.find_nodes(root, './O')
# ob.table_OBJECT(ob.select_OBJECT(results))

a = new_O("z_height", "108")
print(a.attrib)
# ob.save_OpenBrIM(root)
