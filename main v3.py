# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *
import PyOpenBrIM as pob

newOB = PyOpenBrIMElmt('test')
newOB.read_xmlstr('<O> emtpy </O>')
# ResultsTable(newOB)
# marc3 = PyOpenBrIMElmt('Example Marc')
# marc3.read_xmlfile('test.xml')
testobj1=ObjElmt('Group','XXXXXXX',UT='adf',UC='adfad')
newOB.add_sub(testobj1)
ResultsTable(newOB)
# searchpath = newOB.findall_by_path('./O/P')
# ResultsTable(searchpath)