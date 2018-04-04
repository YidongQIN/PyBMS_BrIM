# 1-PyMARC
---
Practise how to use Python XML.etree.ElementTree API  to process ParamML of OpenBrIM projects.
The example here is the MARC Bridge in GT campus.

## GOALS

### version 1

Aiming at realizing three functions:

1. Creating models
2. Mapping ParamML models to other format
3. Querying project information

basically, all these works have been done in PyOpenBrIM.py.


### version 2

Aiming at apply object-oriented programming in ClassPyOpenBrIM.py.

Basic class: PyOpenBrIMElmt.
Sub class: ObjElmt & PrmElmt.
Sub-Sub class: Point, Line, Surface,..., inherited from ObjElmt.

### version 3

aiming at model transfer function between 3D model and FEM model.


## PROGRESS HISTORY

### Dec.12, 2017

Querying function is realized:
- by path, based on Xpath.
- by attributes, which is formatted as dictionary in Python.

Output format is based on
- [PrettyTable](https://pypi.python.org/pypi/PrettyTable)

### Mar.13, 2018

Use OpenBrIM Module to create the xml file in ParamML for MARC bridge.

### Mar.21,2018

the preliminary ClassPyOpenBrIM is done.
In the next, apply it to re-create the xml for MARC bridge in order to test and modify it.

### Arp 4, 2018

establish the FEM model, and then export SAP2000 file and excel file of it.

in the next, try to transfer the 3D model to FEM model.

## IDEAS FOR NEXT

use PyOpenBrIM v2 (that is ClassPyOpenBrIM) to generate the xml file for MARC bridge and see what can be further developed.

New class are required.

* class Damage(ObjElmt)

    use a element to represent the damage in bridge.

    But how many kinds of damage?

    How can the damage be considered in the structure evaluation?

* class Monitor(ObjElmt)

* class Repair(ObjElmt)


## UN-DONE

1. more templates, for project, units, sections, materials.
2. uniform the variable name of different classes and methods.
    For example, 'attributes', 'attribute_dict' and 'attrib_dict'.
3. Method to draw the section.

## TIPS

sometimes, parameters are used to refer to another object.
the best example is the material of section. <O T='Section'> has a sub element <P T='Material' V='Material Name'>

In OpenBrIM, the tag is either 'O' or 'P', so the element.tag is not very useful.

The XPath can be useful when locating elements.

## DOCUMENTS

* About OpenBrIM
[ParamML](https://sites.google.com/a/redeqn.com/paramml-author-s-guide/) is specially designed XML language for [OpenBrIM](https://openbrim.appspot.com/www/brim/) project.

* About xml.etree.ElementTree
The documetation of *ET* (short of ElementTree) is [here](https://docs.python.org/3/library/xml.etree.elementtree.html#).

* About XPath
The ET module provides limited support for (XPath)[https://docs.python.org/3/library/xml.etree.elementtree.html?highlight=xpath#xpath-support] to locate elements in a tree.
