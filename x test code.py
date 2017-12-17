import xml.etree.ElementTree as ET


def str_to_dict(str):
    # 参考xml的自动补齐？ O[N='a']>
    pass


def del_empty_value(dict):
    new_dict = {}
    for key in dict:
        if dict[key] != None :
            new_dict[key] = dict[key]
    return new_dict

def new_O(type_O, *name):
    if name == ():
        attribute_O={'T': type_O}
    else:
        attribute_O = {'T': type_O, 'N': name[0]}
    element = ET.Element('O', attribute_O)
    return element


def add_attrib(element,dict):
    # 因为Object的属性比较复杂，所以单独一个函数？是否把object抽象成属性和层次关系两个函数？
    pass

a = new_O('mater','SB object','another name')
print(a.attrib)
