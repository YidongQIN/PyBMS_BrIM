# import PyOpenBrIM as ob
from PyOpenBrIM import *

root = new_OpenBrIM('newTree')  # an Element

# Material
materialGroup = new_O('Group', "Parameters of Material")
## concrete
MAT_C = new_O('Material', 'C4000Psi', Type="concrete", D="Concrete")
MAT_C_P = []
MAT_C_P.append(new_P("d", "0.0000002248", des="Density"))
MAT_C_P.append(new_P("E", "3604.9965", des="modulus of elasticity"))
MAT_C_P.append(new_P("a", "0.0000055", des="Coefficient of Thermal Expansion"))
MAT_C_P.append(new_P("Fc28", "4", des="Concrete Compressive Strength"))
for par in MAT_C_P:
    add_child_node(MAT_C, par)
## steel rebar
MAT_S1 = new_O('Material', 'A615Gr60', Type="steel", D="Rebar")
MAT_S1_P = []
MAT_S1_P.append(new_P('d', '0.0000002248', des="Density"))
MAT_S1_P.append(new_P('E', '3604.9965', des="modulus of elasticity"))
MAT_S1_P.append(new_P('Nu', "0.3", des="Poisson's Ratio"))
MAT_S1_P.append(new_P('a', "0.0000065", des="Coefficient of Thermal Expansion"))
MAT_S1_P.append(new_P('Fy', "60"))
MAT_S1_P.append(new_P('Fu', "90"))
for par in MAT_S1_P:
    add_child_node(MAT_S1, par)
## steel beam
MAT_S2 = new_O('Material', 'A992Fy50', Type="steel", D="steel")
MAT_S2_P = []
MAT_S2_P.append(new_P('d', "0.0000007345", des="Density"))
MAT_S2_P.append(new_P('E', "29000", des="modulus of elasticity"))
MAT_S2_P.append(new_P('Nu', "0.3", des="Poisson's Ratio"))
MAT_S2_P.append(new_P('a', "0.0000065", des="Coefficient of Thermal Expansion"))
MAT_S2_P.append(new_P('Fy', "50"))
MAT_S2_P.append(new_P('Fu', "65"))
for par in MAT_S2_P:
    add_child_node(MAT_S2, par)
add_child_node(materialGroup, MAT_C)
add_child_node(materialGroup, MAT_S1)
add_child_node(materialGroup, MAT_S2)
# Section
## section parameter group
PrmtsOfSections = new_O('Group', 'Parameters of Sections')
PrmtsOfSections_P = []
PrmtsOfSections_P.append(new_P("BottomChord_width", "6", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("BottomChord_depth", "6", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("BottomChord_thickness", "0.375", role="Input"))
PrmtsOfSections_P.append(new_P("TopChord_width", "6", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("TopChord_depth", "6", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("TopChord_thickness", "0.3125", role="Input"))
PrmtsOfSections_P.append(new_P("deck_thick", "5", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("VertiBeam_width", "6", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("VertiBeam_depth", "6", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("VertiBeam_thickness", "0.25", UT="Length", role="Input"))
PrmtsOfSections_P.append(new_P("WebRadius", "1", UT="Length", role="Input"))
for par in PrmtsOfSections_P:
    add_child_node(PrmtsOfSections, par)
# section group
SectionsGroup = new_O('Group', 'Sections')
## section--bottom chord
Section_BottomChord = new_O("Section", "Section_BottomChord")
Section_BottomChord_P = []
Section_BottomChord_P.append(new_P("MaterialS2", "A992Fy50", des="Bottom Chord is steel"))
Section_BottomChord_P.append(new_P("Ax", "7.58"))
Section_BottomChord_P.append(new_P("Iy", "39.5"))
Section_BottomChord_P.append(new_P("Iz", "39.5"))
for par in Section_BottomChord_P:
    add_child_node(Section_BottomChord, par)
### outer shape
Section_BottomChord_Out = new_O("Shape", "Shape_BottomChord_Out")
add_child_node(Section_BottomChord_Out, new_O("Point", X="-BottomChord_width/2", Y="-BottomChord_depth/2"))
add_child_node(Section_BottomChord_Out, new_O("Point", X="-BottomChord_width/2", Y="BottomChord_depth/2"))
add_child_node(Section_BottomChord_Out, new_O("Point", X="BottomChord_width/2", Y="BottomChord_depth/2"))
add_child_node(Section_BottomChord_Out, new_O("Point", X="BottomChord_width/2", Y="-BottomChord_depth/2"))
add_child_node(Section_BottomChord, Section_BottomChord_Out)
### inner shape
Section_BottomChord_Int = new_O("Shape", "Shape_BottomChord_Int")
add_child_node(Section_BottomChord_Int, new_O("Point", X="-BottomChord_width/2+BottomChord_thickness",
                                              Y="-BottomChord_depth/2+BottomChord_thickness"))
add_child_node(Section_BottomChord_Int, new_O("Point", X="-BottomChord_width/2+BottomChord_thickness",
                                              Y="BottomChord_depth/2-BottomChord_thickness"))
add_child_node(Section_BottomChord_Int, new_O("Point", X="BottomChord_width/2-BottomChord_thickness",
                                              Y="BottomChord_depth/2-BottomChord_thickness"))
add_child_node(Section_BottomChord_Int, new_O("Point", X="BottomChord_width/2-BottomChord_thickness",
                                              Y="-BottomChord_depth/2+BottomChord_thickness"))
add_child_node(Section_BottomChord, Section_BottomChord_Int)
add_child_node(SectionsGroup, Section_BottomChord)
## section--
Section_TopChord= new_O('Section','Section_TopChord')
Section_TopChord_P=[]
Section_TopChord_P.append(new_P("MaterialSS", "A992Fy50"))
Section_TopChord_P.append(new_P("Ax", "6.43"))
Section_TopChord_P.append(new_P("Iy", "34.3"))
Section_TopChord_P.append(new_P("Iz", "34.3"))
for par in Section_TopChord_P:
    add_child_node(Section_TopChord,par)
Shape_TopChord_Out= new_O('Shape','Shape_TopChord_Out')
add_child_node(Shape_TopChord_Out, new_O("Point",X="-TopChord_width/2", Y="-TopChord_depth/2"))
add_child_node(Shape_TopChord_Out, new_O("Point",X="-TopChord_width/2", Y="TopChord_depth/2"))
add_child_node(Shape_TopChord_Out, new_O("Point",X="TopChord_width/2", Y="TopChord_depth/2"))
add_child_node(Shape_TopChord_Out, new_O("Point",X="TopChord_width/2", Y="-TopChord_depth/2"))
add_child_node(Section_TopChord, Shape_TopChord_Out)
Shape_TopChord_Int= new_O('Shape','Shape_TopChord_Int')
add_child_node(Shape_TopChord_Int, new_P("IsCutout", "1"))
add_child_node(Shape_TopChord_Int, new_O("Point",X="-TopChord_width/2+TopChord_thickness", Y="-TopChord_depth/2+TopChord_thickness"))
add_child_node(Shape_TopChord_Int, new_O("Point",X="-TopChord_width/2+TopChord_thickness", Y="TopChord_depth/2-TopChord_thickness"))
add_child_node(Shape_TopChord_Int, new_O("Point",X="TopChord_width/2-TopChord_thickness", Y="TopChord_depth/2-TopChord_thickness"))
add_child_node(Shape_TopChord_Int, new_O("Point",X="TopChord_width/2-TopChord_thickness", Y="-TopChord_depth/2+TopChord_thickness"))
add_child_node(Section_TopChord, Shape_TopChord_Int)
add_child_node(SectionsGroup, Section_TopChord)


Section_Vertical= new_O('Section','Section_Vertical')
Section_Vertical_P=[]
Section_Vertical_P.append(new_P("MaterialSV", "A992Fy50"))
Section_Vertical_P.append(new_P("Ax", "5.24"))
Section_Vertical_P.append(new_P("Iy", "28.6"))
Section_Vertical_P.append(new_P("Iz", "28.6"))
for par in Section_Vertical_P:
    add_child_node(Section_Vertical,par)
Shape_VertiBeam_Out= new_O('Shape','Shape_VertiBeam_Out')
add_child_node(Shape_VertiBeam_Out, new_O("Point",X="-VertiBeam_width/2", Y="-VertiBeam_depth/2"))
add_child_node(Shape_VertiBeam_Out, new_O("Point",X="-VertiBeam_width/2", Y="VertiBeam_depth/2"))
add_child_node(Shape_VertiBeam_Out, new_O("Point",X="VertiBeam_width/2", Y="VertiBeam_depth/2"))
add_child_node(Shape_VertiBeam_Out, new_O("Point",X="VertiBeam_width/2", Y="-VertiBeam_depth/2"))
add_child_node(Section_Vertical,Shape_VertiBeam_Out)
Shape_VertiBeam_Int= new_O('Shape','Shape_VertiBeam_Int')
add_child_node(Shape_VertiBeam_Int, new_P("IsCutout", "1"))
add_child_node(Shape_VertiBeam_Int, new_O("Point",X="-VertiBeam_width/2+VertiBeam_thickness", Y="-VertiBeam_depth/2+VertiBeam_thickness"))
add_child_node(Shape_VertiBeam_Int, new_O("Point",X="-VertiBeam_width/2+VertiBeam_thickness", Y="VertiBeam_depth/2-VertiBeam_thickness"))
add_child_node(Shape_VertiBeam_Int, new_O("Point",X="VertiBeam_width/2-VertiBeam_thickness", Y="VertiBeam_depth/2-VertiBeam_thickness"))
add_child_node(Shape_VertiBeam_Int, new_O("Point",X="VertiBeam_width/2-VertiBeam_thickness", Y="-VertiBeam_depth/2+VertiBeam_thickness"))
add_child_node(Section_Vertical,Shape_VertiBeam_Int)
add_child_node(SectionsGroup, Section_Vertical)

Section_Web= new_O('Section','Section_Web')
add_child_node(Section_Web, new_P("MaterialSW", "A992Fy50"))
radius = new_P("Radius", "WebRadius")
circle = new_O('Circle','Circle Section')
add_child_node(circle,radius)
add_child_node(Section_Web,circle)


# ---add all level 1 elements
add_child_node(root, materialGroup)
add_child_node(root, PrmtsOfSections)
add_child_node(root, SectionsGroup)

# ---write to .xml file---
save_OpenBrIM(root)
