# 1-PyMARC
---
Practise how to use Python XML.etree.ElementTree API  to process ParamML of OpenBrIM projects.
The example here is the MARC Bridge in GT campus.

## Goals
Aiming at realizing three functions:

1. Creating models
2. Mapping ParamML models to other format
3. Querying project information

## Ideas
Func.1 can wait.
Func.2 and 3 is similar, its core is locating elements and then querying the attributes.
In OpenBrIM, the tag is either 'O' or 'P'.
The XPath can be useful when locating elements.

## Documetation

* About OpenBrIM
[ParamML](https://sites.google.com/a/redeqn.com/paramml-author-s-guide/) is specially designed XML language for [OpenBrIM](https://openbrim.appspot.com/www/brim/) project.

* About xml.etree.ElementTree
The documetation of *ET* (short of ElementTree) is [here](https://docs.python.org/3/library/xml.etree.elementtree.html#).

* About XPath
The ET module provides limited support for XPath expressions for locating elements in a tree.
