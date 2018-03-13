# import PyOpenBrIM as ob
from PyOpenBrIM import *

root = new_OpenBrIM('newTree')  # an Element

# Material as example
materialGroup = new_O('Group', "Parameters of Material")
# <O N="C4000Psi" T="Material" Type="concrete" D="Concrete" >
MAT_C = new_O('Material', 'C4000Psi', Type="concrete", D="Concrete")
MAT_C_P=[]
MAT_C_P.append(new_P("d", "0.0000002248", des="Density"))
MAT_C_P.append(new_P("E", "3604.9965", des="modulus of elasticity"))
MAT_C_P.append(new_P("a", "0.0000055", des="Coefficient of Thermal Expansion"))
MAT_C_P.append(new_P("Fc28", "4" ,des="Concrete Compressive Strength"))
for par in MAT_C_P:
    add_child_node(MAT_C, par)
MAT_S1 = new_O('Material', 'A615Gr60', Type="steel", D="Rebar")
MAT_S1_P=[]
MAT_S1_P.append(new_P('d', '0.0000002248', des="Density"))
MAT_S1_P.append(new_P('E', '3604.9965', des="modulus of elasticity"))
MAT_S1_P.append(new_P('Nu', "0.3", des="Poisson's Ratio"))
MAT_S1_P.append(new_P('a', "0.0000065", des="Coefficient of Thermal Expansion"))
MAT_S1_P.append(new_P('Fy', "60", des=""))
MAT_S1_P.append(new_P('Fu', "90", des=""))
for par in MAT_S1_P:
    add_child_node(MAT_S1, par)
# print("MAT_C is ")
# print(MAT_C)
add_child_node(materialGroup, MAT_C)
add_child_node(materialGroup, MAT_S1)
add_child_node(root, materialGroup)

# ---write to .xml file---
save_OpenBrIM(root)
