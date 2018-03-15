# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *
import PyOpenBrIM as pob

newOB = PyOpenBrIMElmt('test')
newOB.read_xmlfile('newTree.xml')
ResultsTable(newOB)
searchpath = newOB.findall_by_path('./O/P')
ResultsTable(searchpath)