# import PyOpenBrIM as ob
from PyOpenBrIM import *

root = new_OpenBrIM('demo_MARC')  # an Element

# Material
materialGroup = new_O('Group', "Parameters of Material")
## concrete
matC = new_O('Material', 'C4000Psi', Type="concrete", D="Concrete")
matC_P = []
matC_P.append(new_P("d", "0.0000002248", des="Density"))
matC_P.append(new_P("E", "3604.9965", des="modulus of elasticity"))
matC_P.append(new_P("a", "0.0000055", des="Coefficient of Thermal Expansion"))
matC_P.append(new_P("Fc28", "4", des="Concrete Compressive Strength"))
add_subNode(matC, matC_P)
## steel rebar
matS1 = new_O('Material', 'A615Gr60', Type="steel", D="Rebar")
matS1_P = []
matS1_P.append(new_P('d', '0.0000002248', des="Density"))
matS1_P.append(new_P('E', '3604.9965', des="modulus of elasticity"))
matS1_P.append(new_P('Nu', "0.3", des="Poisson's Ratio"))
matS1_P.append(new_P('a', "0.0000065", des="Coefficient of Thermal Expansion"))
matS1_P.append(new_P('Fy', "60"))
matS1_P.append(new_P('Fu', "90"))
add_subNode(matS1, matS1_P)
## steel beam
matS2 = new_O('Material', 'A992Fy50', Type="steel", D="steel")
matS2_P = []
matS2_P.append(new_P('d', "0.0000007345", des="Density"))
matS2_P.append(new_P('E', "29000", des="modulus of elasticity"))
matS2_P.append(new_P('Nu', "0.3", des="Poisson's Ratio"))
matS2_P.append(new_P('a', "0.0000065", des="Coefficient of Thermal Expansion"))
matS2_P.append(new_P('Fy', "50"))
matS2_P.append(new_P('Fu', "65"))
add_subNode(matS2, matS2_P)
add_subNode(materialGroup, matC)
add_subNode(materialGroup, matS1)
add_subNode(materialGroup, matS2)
add_subNode(root, materialGroup)
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
add_subNode(PrmtsOfSections, PrmtsOfSections_P)
add_subNode(root, PrmtsOfSections)
# section group
SectionsGroup = new_O('Group', 'Sections')
## section--bottom chord
Section_BottomChord = new_O("Section", "Section_BottomChord")
Section_BottomChord_P = []
Section_BottomChord_P.append(new_P("MaterialS2", "A992Fy50", des="Bottom Chord is steel"))
Section_BottomChord_P.append(new_P("Ax", "7.58"))
Section_BottomChord_P.append(new_P("Iy", "39.5"))
Section_BottomChord_P.append(new_P("Iz", "39.5"))
add_subNode(Section_BottomChord, Section_BottomChord_P)
### outer shape
Section_BottomChord_Out = new_O("Shape", "Shape_BottomChord_Out")
add_subNode(Section_BottomChord_Out, new_O("Point", X="-BottomChord_width/2", Y="-BottomChord_depth/2"))
add_subNode(Section_BottomChord_Out, new_O("Point", X="-BottomChord_width/2", Y="BottomChord_depth/2"))
add_subNode(Section_BottomChord_Out, new_O("Point", X="BottomChord_width/2", Y="BottomChord_depth/2"))
add_subNode(Section_BottomChord_Out, new_O("Point", X="BottomChord_width/2", Y="-BottomChord_depth/2"))
add_subNode(Section_BottomChord, Section_BottomChord_Out)
### inner shape
Section_BottomChord_Int = new_O("Shape", "Shape_BottomChord_Int")
add_subNode(Section_BottomChord_Int, new_P("IsCutout", "1"))
add_subNode(Section_BottomChord_Int, new_O("Point", X="-BottomChord_width/2+BottomChord_thickness",
                                           Y="-BottomChord_depth/2+BottomChord_thickness"))
add_subNode(Section_BottomChord_Int, new_O("Point", X="-BottomChord_width/2+BottomChord_thickness",
                                           Y="BottomChord_depth/2-BottomChord_thickness"))
add_subNode(Section_BottomChord_Int, new_O("Point", X="BottomChord_width/2-BottomChord_thickness",
                                           Y="BottomChord_depth/2-BottomChord_thickness"))
add_subNode(Section_BottomChord_Int, new_O("Point", X="BottomChord_width/2-BottomChord_thickness",
                                           Y="-BottomChord_depth/2+BottomChord_thickness"))
add_subNode(Section_BottomChord, Section_BottomChord_Int)
add_subNode(SectionsGroup, Section_BottomChord)
add_subNode(root, SectionsGroup)
## section--
Section_TopChord = new_O('Section', 'Section_TopChord')
Section_TopChord_P = []
Section_TopChord_P.append(new_P("MaterialSS", "A992Fy50"))
Section_TopChord_P.append(new_P("Ax", "6.43"))
Section_TopChord_P.append(new_P("Iy", "34.3"))
Section_TopChord_P.append(new_P("Iz", "34.3"))
add_subNode(Section_TopChord, Section_TopChord_P)
Shape_TopChord_Out = new_O('Shape', 'Shape_TopChord_Out')
add_subNode(Shape_TopChord_Out, new_O("Point", X="-TopChord_width/2", Y="-TopChord_depth/2"))
add_subNode(Shape_TopChord_Out, new_O("Point", X="-TopChord_width/2", Y="TopChord_depth/2"))
add_subNode(Shape_TopChord_Out, new_O("Point", X="TopChord_width/2", Y="TopChord_depth/2"))
add_subNode(Shape_TopChord_Out, new_O("Point", X="TopChord_width/2", Y="-TopChord_depth/2"))
add_subNode(Section_TopChord, Shape_TopChord_Out)
Shape_TopChord_Int = new_O('Shape', 'Shape_TopChord_Int')
add_subNode(Shape_TopChord_Int, new_P("IsCutout", "1"))
add_subNode(Shape_TopChord_Int,
            new_O("Point", X="-TopChord_width/2+TopChord_thickness", Y="-TopChord_depth/2+TopChord_thickness"))
add_subNode(Shape_TopChord_Int,
            new_O("Point", X="-TopChord_width/2+TopChord_thickness", Y="TopChord_depth/2-TopChord_thickness"))
add_subNode(Shape_TopChord_Int,
            new_O("Point", X="TopChord_width/2-TopChord_thickness", Y="TopChord_depth/2-TopChord_thickness"))
add_subNode(Shape_TopChord_Int,
            new_O("Point", X="TopChord_width/2-TopChord_thickness", Y="-TopChord_depth/2+TopChord_thickness"))
add_subNode(Section_TopChord, Shape_TopChord_Int)
add_subNode(SectionsGroup, Section_TopChord)

Section_Vertical = new_O('Section', 'Section_Vertical')
Section_Vertical_P = []
Section_Vertical_P.append(new_P("MaterialSV", "A992Fy50"))
Section_Vertical_P.append(new_P("Ax", "5.24"))
Section_Vertical_P.append(new_P("Iy", "28.6"))
Section_Vertical_P.append(new_P("Iz", "28.6"))
add_subNode(Section_Vertical, Section_Vertical_P)
Shape_VertiBeam_Out = new_O('Shape', 'Shape_VertiBeam_Out')
add_subNode(Shape_VertiBeam_Out, new_O("Point", X="-VertiBeam_width/2", Y="-VertiBeam_depth/2"))
add_subNode(Shape_VertiBeam_Out, new_O("Point", X="-VertiBeam_width/2", Y="VertiBeam_depth/2"))
add_subNode(Shape_VertiBeam_Out, new_O("Point", X="VertiBeam_width/2", Y="VertiBeam_depth/2"))
add_subNode(Shape_VertiBeam_Out, new_O("Point", X="VertiBeam_width/2", Y="-VertiBeam_depth/2"))
add_subNode(Section_Vertical, Shape_VertiBeam_Out)
Shape_VertiBeam_Int = new_O('Shape', 'Shape_VertiBeam_Int')
add_subNode(Shape_VertiBeam_Int, new_P("IsCutout", "1"))
add_subNode(Shape_VertiBeam_Int,
            new_O("Point", X="-VertiBeam_width/2+VertiBeam_thickness", Y="-VertiBeam_depth/2+VertiBeam_thickness"))
add_subNode(Shape_VertiBeam_Int,
            new_O("Point", X="-VertiBeam_width/2+VertiBeam_thickness", Y="VertiBeam_depth/2-VertiBeam_thickness"))
add_subNode(Shape_VertiBeam_Int,
            new_O("Point", X="VertiBeam_width/2-VertiBeam_thickness", Y="VertiBeam_depth/2-VertiBeam_thickness"))
add_subNode(Shape_VertiBeam_Int,
            new_O("Point", X="VertiBeam_width/2-VertiBeam_thickness", Y="-VertiBeam_depth/2+VertiBeam_thickness"))
add_subNode(Section_Vertical, Shape_VertiBeam_Int)
add_subNode(SectionsGroup, Section_Vertical)

Section_Web = new_O('Section', 'Section_Web')
add_subNode(Section_Web, new_P("MaterialSW", "A992Fy50"))
radius = new_P("Radius", "WebRadius")
circle = new_O('Circle', 'Circle Section')
add_subNode(circle, radius)
add_subNode(Section_Web, circle)
add_subNode(root, Section_Web)

# structural parameters
ParamterOfBridge = new_O('Group', 'Parameters of Marc Bridge')
span_num = 11
x_spacing = 108
y_spacing = 84
z_height = 108
ParamterOfBridge_P = []
ParamterOfBridge_P.append(new_P("span_num", str(span_num), role="Input"))
ParamterOfBridge_P.append(new_P("x_spacing", str(x_spacing), UT="Length", role="Input"))
ParamterOfBridge_P.append(new_P("y_spacing", str(y_spacing), UT="Length", role="Input"))
ParamterOfBridge_P.append(new_P("z_height", str(z_height), UT="Length", role="Input"))
add_subNode(ParamterOfBridge, ParamterOfBridge_P)
add_subNode(root, ParamterOfBridge)
# Points in 4 lists
PointBL = []
PointBR = []
PointTL = []
PointTR = []
for i in range(span_num + 1):
    # Points[y][z][i]=new_O('Point','Points_%d_%d_%d'%(i,y,z),X="%d"%(i*x_spacing),Y="%d"%(y_spacing*y),Z="%d"%(z*z_height))
    PointBL.append(new_O('Point', 'PointBL_%d' % i, X="%d" % (i * x_spacing), Y="%d" % y_spacing, Z="0"))
    PointBR.append(new_O('Point', 'PointBR_%d' % i, X="%d" % (i * x_spacing), Y="0", Z="0"))
    PointTL.append(new_O('Point', 'PointTL_%d' % i, X="%d" % (i * x_spacing), Y="%d" % y_spacing, Z="%d" % z_height))
    PointTR.append(new_O('Point', 'PointTR_%d' % i, X="%d" % (i * x_spacing), Y="0", Z="%d" % z_height))
# Bottom Chord
bottomChordList = []
for i in range(span_num):
    bottomChord = new_O('Line')
    add_subNode(bottomChord, PointBL[i])
    add_subNode(bottomChord, PointBL[i + 1])
    bottomChordList.append(bottomChord)
    bottomChord = new_O('Line')
    add_subNode(bottomChord, PointBR[i])
    add_subNode(bottomChord, PointBR[i + 1])
    bottomChordList.append(bottomChord)
add_subNode(bottomChordList, new_O('Section', 'bottomChordSection', Extends="Section_BottomChord"))
add_subNode(root, bottomChordList)
# Top chord
TopChordList = []
for i in range(1, span_num):
    TopChord = new_O('Line')
    add_subNode(TopChord, PointTL[i])
    add_subNode(TopChord, PointTL[i + 1])
    TopChordList.append(TopChord)
    TopChord = new_O('Line')
    add_subNode(TopChord, PointTR[i])
    add_subNode(TopChord, PointTR[i + 1])
    TopChordList.append(TopChord)
add_subNode(TopChordList, new_O('Section', 'TopChordSection', Extends="Section_TopChord"))
add_subNode(root, TopChordList)
# vertical
for i in range(1, span_num + 1):
    for (a, b) in [(PointBL, PointBR), (PointTR, PointBR), (PointTR, PointTL), (PointBL, PointTL)]:
        chord = new_O('Line')
        add_subNode(chord, a[i])
        add_subNode(chord, b[i])
        add_subNode(chord, new_O('Section', 'Vertical', Extends="Section_Vertical"))
        add_subNode(root, chord)
# oblique
for i in range(1, span_num):
    for (a, b) in [(PointBL, PointTL), (PointBR, PointTR), (PointTL, PointTR)]:
        webbeam = new_O('Line')
        add_subNode(webbeam, a[i])
        add_subNode(webbeam, b[i + 1])
        add_subNode(webbeam, new_O('Section', 'Circle Web', Extends="Section_Web"))
        add_subNode(root, webbeam)
        webbeam = new_O('Line')
        add_subNode(webbeam, a[i + 1])
        add_subNode(webbeam, b[i])
        add_subNode(webbeam, new_O('Section', 'Circle Web', Extends="Section_Web"))
        add_subNode(root, webbeam)
# Z beam
for i in range(span_num):
    if (i % 2) == 0:
        zbeam = new_O('Line')
        add_subNode(zbeam, PointBL[i])
        add_subNode(zbeam, PointBR[i + 1])
        add_subNode(zbeam, new_O('Section', 'Z beam in odd segment', Extends="Section_BottomChord"))
        add_subNode(root, zbeam)
    else:
        zbeam = new_O('Line')
        add_subNode(zbeam, PointBL[i + 1])
        add_subNode(zbeam, PointBR[i])
        add_subNode(zbeam, new_O('Section', 'Z beam in even segment', Extends="Section_BottomChord"))
        add_subNode(root, zbeam)

# 1st segment
firstbottom = new_O('Line')
add_subNode(firstbottom, PointBL[0])
add_subNode(firstbottom, PointBR[0])
add_subNode(firstbottom, new_O('Section', 'first bottom chord', Extends="Section_BottomChord"))
add_subNode(root, firstbottom)
firstBLtoTL = new_O('Line')
add_subNode(firstBLtoTL, PointBL[0])
add_subNode(firstBLtoTL, PointTL[1])
add_subNode(firstBLtoTL, new_O('Section', 'first chord on the left', Extends="Section_BottomChord"))
add_subNode(root, firstBLtoTL)
firstBRtoTR = new_O('Line')
add_subNode(firstBRtoTR, PointBR[0])
add_subNode(firstBRtoTR, PointTR[1])
add_subNode(firstBRtoTR, new_O('Section', 'first chord on the right', Extends="Section_BottomChord"))
add_subNode(root, firstBRtoTR)
# deck
for i in range(span_num):
    deck = new_O('Surface')
    add_subNode(deck, new_P("Opacity", "0.7"))
    add_subNode(deck, new_P("Thickness", "deck_thick"))
    add_subNode(deck, new_P("MaterialC", "C4000Psi", "Material"))
    add_subNode(deck, PointBL[i])
    add_subNode(deck, PointBR[i])
    add_subNode(deck, PointBR[i + 1])
    add_subNode(deck, PointBL[i + 1])
    add_subNode(root, deck)
# ---write to .xml file---
save_OpenBrIM(root)
