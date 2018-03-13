# import PyOpenBrIM as ob
from PyOpenBrIM import *

root = new_OpenBrIM('newTree')  # an Element

# Material as example
materialGroup = new_O('Group', "Parameters of Material")
# <O N="C4000Psi" T="Material" Type="concrete" D="Concrete" >
MAT_C = new_O('Material', 'Concrete', Type="concrete", D="Concrete")
MAT_C_P1 = new_P('d', '0.0000002248', des="Density")
MAT_C_P2 = new_P('E', '3604.9965', des="modulus of elasticity")
# print("MAT_C is ")
# print(MAT_C)
add_child_node(materialGroup, MAT_C)
add_child_node(root, materialGroup)

# ---write to .xml file---
save_OpenBrIM(root)
