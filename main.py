# import PyOpenBrIM as ob
from PyOpenBrIM import *

root=new_OpenBrIM('newTree') # an Element

# Material as example
materialGroup = new_O('Group',"Parameters of Material")
MAT_C = new_O('Material','Concrete')
print("MAT_C is ")
print(MAT_C)
add_child_node(materialGroup, MAT_C)
add_child_node(root,materialGroup)

#---write to .xml file---
save_OpenBrIM(root)
