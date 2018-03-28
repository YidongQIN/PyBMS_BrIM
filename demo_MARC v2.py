#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
use ClassPyOpenBrIM to generate the xml file of MARC Bridge.
modified Mar26, 2018
"""

__author__ = 'Yidong QIN'

from ClassPyOpenBrIM import *

if __name__ == '__main__':

    marc = Project('MARC_OOP')
    # 1. Material
    c4000 = Material('C4000Psi', mat_type="concrete", des="Concrete")
    c4000.mat_property(d='0.0000002248', E="3604.9965", a="0.0000055", Fc28="4")
    rebar = Material('A615Gr60', mat_type="steel", des="Rebar")
    rebar.mat_property(d='0.0000002248', E='3604.9965', Nu="0.3", a="0.0000065", Fy="60", Fu="90")
    girder_steel = Material('A992Fy50', mat_type="steel", des="steel of girder")
    girder_steel.mat_property(d="0.0000007345", E="29000", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
    group_mat = Group('Material Group', c4000, rebar, girder_steel)
    group_mat.attach_to(marc)
    # 2. Sections
    # 2.1 Sections Parameters
    BottomChord_width = PrmElmt('BottomChord_width', 0, ut="Length", role="Input")
    BottomChord_depth = PrmElmt("BottomChord_depth", 6, ut="Length", role="Input")
    BottomChord_thickness = PrmElmt("BottomChord_thickness", 0.375, role="Input")
    TopChord_width = PrmElmt("TopChord_width", 6, ut="Length", role="Input")
    TopChord_depth = PrmElmt("TopChord_depth", 6, ut="Length", role="Input")
    TopChord_thickness = PrmElmt("TopChord_thickness", 0.3125, role="Input")
    deck_thick = PrmElmt("deck_thick", "5", ut="Length", role="Input")
    VertiBeam_width = PrmElmt("VertiBeam_width", 6, ut="Length", role="Input")
    VertiBeam_depth = PrmElmt("VertiBeam_depth", 6, ut="Length", role="Input")
    VertiBeam_thickness = PrmElmt("VertiBeam_thickness", 0.25, ut="Length", role="Input")
    WebRadius = PrmElmt("WebRadius", 1, ut="Length", role="Input")
    group_sec_par = Group('Parameters Group of Sections', BottomChord_width, BottomChord_depth, BottomChord_thickness,
                          TopChord_width, TopChord_depth, TopChord_thickness, deck_thick, VertiBeam_width,
                          VertiBeam_depth,
                          VertiBeam_thickness, WebRadius)
    group_sec_par.attach_to(marc)
    # 2.2 Sections
    group_sections = Group('Sections Group')
    # 2.2.1 bottom chord
    sp_bc_out = Shape('Shape_BottomChord_Out',
                      Point("-BottomChord_width/2", "-BottomChord_depth/2"),
                      Point("-BottomChord_width/2", "BottomChord_depth/2"),
                      Point("BottomChord_width/2", "BottomChord_depth/2"),
                      Point("BottomChord_width/2", "-BottomChord_depth/2"))
    sp_bc_int = Shape('Shape_BottomChord_Int',
                      Point("-BottomChord_width/2+BottomChord_thickness", "-BottomChord_depth/2+BottomChord_thickness"),
                      Point("-BottomChord_width/2+BottomChord_thickness", "BottomChord_depth/2-BottomChord_thickness"),
                      Point("BottomChord_width/2-BottomChord_thickness", "BottomChord_depth/2-BottomChord_thickness"),
                      Point("BottomChord_width/2-BottomChord_thickness", "-BottomChord_depth/2+BottomChord_thickness"))
    sp_bc_int.is_cutout()
    sec_bc = Section('Section_BottomChord', girder_steel, sp_bc_out, sp_bc_int, Ax="7.58", Iy="39.5", Iz="39.5")
    sec_bc.attach_to(group_sections)
    # 2.2.2 top chord
    sp_top_out = Shape('Shape_TopChord_Out',
                       Point("-TopChord_width/2", "-TopChord_depth/2"),
                       Point("-TopChord_width/2", "TopChord_depth/2"),
                       Point("TopChord_width/2", "TopChord_depth/2"),
                       Point("TopChord_width/2", "-TopChord_depth/2"))
    sp_top_int = Shape('Shape_TopChord_Int',
                       Point("-TopChord_width/2+TopChord_thickness", "-TopChord_depth/2+TopChord_thickness"),
                       Point("-TopChord_width/2+TopChord_thickness", "TopChord_depth/2-TopChord_thickness"),
                       Point("TopChord_width/2-TopChord_thickness", "TopChord_depth/2-TopChord_thickness"),
                       Point("TopChord_width/2-TopChord_thickness", "-TopChord_depth/2+TopChord_thickness"))
    sp_top_int.is_cutout()
    sec_top = Section('Section_TopChord', girder_steel, sp_top_out, sp_top_int, Ax="6.43", Iy="34.3", Iz="34.3")
    sec_top.attach_to(group_sections)
    # 2.2.3 vertical chord
    sp_ver_out = Shape('Shape_VertiBeam_Out',
                       Point("-VertiBeam_width/2", "-VertiBeam_depth/2"),
                       Point("-VertiBeam_width/2", "VertiBeam_depth/2"),
                       Point("VertiBeam_width/2", "VertiBeam_depth/2"),
                       Point("VertiBeam_width/2", "-VertiBeam_depth/2"))
    sp_ver_int = Shape('Shape_VertiBeam_Int',
                       Point("-VertiBeam_width/2+VertiBeam_thickness", "-VertiBeam_depth/2+VertiBeam_thickness"),
                       Point("-VertiBeam_width/2+VertiBeam_thickness", "VertiBeam_depth/2-VertiBeam_thickness"),
                       Point("VertiBeam_width/2-VertiBeam_thickness", "VertiBeam_depth/2-VertiBeam_thickness"),
                       Point("VertiBeam_width/2-VertiBeam_thickness", "-VertiBeam_depth/2+VertiBeam_thickness"))
    sp_ver_int.is_cutout()
    sec_ver = Section('Section_VertiBeam', girder_steel, sp_ver_out, sp_ver_int, Ax="5.24", Iy="28.6", Iz="28.6")
    sec_ver.attach_to(group_sections)
    # 2.2.4 web
    circle = ObjElmt('Circle')
    circle.param("Radius", "WebRadius")
    sp_cir = Shape('Shape_WebCircle', circle)
    sec_web = Section('Section_Web', girder_steel, sp_cir)
    sec_web.attach_to(group_sections)
    group_sections.attach_to(marc)
    # 3. Structural Parameter
    span_num = PrmElmt("span_num", 11, role="Input")
    x_spacing = PrmElmt("x_spacing", 108.0, ut="Length", role="Input")
    y_spacing = PrmElmt("y_spacing", 84, ut="Length", role="Input")
    z_height = PrmElmt("z_height", 108, ut="Length", role="Input")
    group_strct = Group('Structural Parameters Group', span_num, x_spacing, y_spacing, z_height)
    group_strct.attach_to(marc)
    # 4. Points
    pointBL = []
    pointBR = []
    pointTL = []
    pointTR = []
    for i in range(span_num.value + 1):
        pointBL.append(Point(i * x_spacing.value, y_spacing.value, 0, point_name='PointBL_%d' % i))
        pointBR.append(Point(i * x_spacing.value, 0, 0, point_name='PointBR_%d' % i))
        pointTL.append(Point(i * x_spacing.value, y_spacing.value, z_height.value, point_name='PointTL_%d' % i))
        pointTR.append(Point(i * x_spacing.value, 0, z_height.value, point_name='PointTR_%d' % i))
    # 5. Lines
    # 5.1 bottom BR BL
    bottomChordList = []
    for i in range(span_num.value):
        bottomChordList.append(Line(pointBL[i], pointBL[i + 1], Extends(sec_bc)))
        bottomChordList.append(Line(pointBR[i], pointBR[i + 1], Extends(sec_bc)))
    bottomChords = Group('Bottom Chords', *bottomChordList)
    # 5.2 top chords, TR,TL
    topChordList = []
    for i in range(1, span_num.value):
        topChordList.append(Line(pointTL[i], pointTL[i + 1], Extends(sec_top)))
        topChordList.append(Line(pointTR[i], pointTR[i + 1], Extends(sec_top)))
    topChords = Group('Top Chords', *topChordList)
    marc.add_sub(bottomChords, topChords)
    # 5.3 vertical
    verChords = []
    for i in range(1, span_num.value + 1):
        for (a, b) in [(pointBL, pointBR), (pointTR, pointBR), (pointTR, pointTL), (pointBL, pointTL)]:
            verChords.append(Line(a[i], b[i], Extends(sec_ver)))
    group_vertical = Group('Vertical Chords', *verChords)
    group_vertical.attach_to(marc)
    # 5.4 oblique
    obliqChords = []
    for i in range(1, span_num.value):
        for (a, b) in [(pointBL, pointTL), (pointBR, pointTR), (pointTL, pointTR)]:
            obliqChords.append(Line(a[i], b[i + 1], Extends(sec_web)))
            obliqChords.append(Line(a[i + 1], b[i], Extends(sec_web)))
    Group('Oblique Chords', *obliqChords).attach_to(marc)
    # 5.5 Z beam in deck
    z_beams = []
    for i in range(span_num.value):
        if (i % 2) == 0:
            z_beams.append(Line(pointBL[i], pointBR[i + 1], Extends(sec_bc)))
        else:
            z_beams.append(Line(pointBL[i + 1], pointBR[i], Extends(sec_bc)))
    group_zbeam = Group('Z beams', *z_beams)
    group_zbeam.attach_to(marc)
    # 5.6 the 1st segment
    first_seg = [Line(pointBL[0], pointBR[0], Extends(sec_bc)),
                 Line(pointBL[0], pointTL[1], Extends(sec_bc)),
                 Line(pointBR[0], pointTR[1], Extends(sec_bc))]
    Group('First Segment', *first_seg).attach_to(marc)
    # 6. Surfaces
    decks = []
    for i in range(span_num.value):
        decks.append(
            Surface(pointBL[i], pointBR[i], pointBR[i + 1], pointBL[i + 1],
                    deck_thick, c4000, 'concrete deck'))
    Group('Decks', *decks).attach_to(marc)
    # 7. FEM
    # 7.1 Node
    nodeBL = []
    nodeBR = []
    nodeTL = []
    nodeTR = []
    for i in range(span_num.value + 1):
        nodeBL.append(FENode(0, 0, 0, 'NodeBL_{}'.format(i)).as_point(pointBL[i]))
        nodeBR.append(FENode(0, 0, 0, 'NodeBR_{}'.format(i)).as_point(pointBR[i]))
        nodeTL.append(FENode(0, 0, 0, 'NodeTL_{}'.format(i)).as_point(pointTL[i]))
        nodeTR.append(FENode(0, 0, 0, 'NodeTR_{}'.format(i)).as_point(pointTR[i]))

    # 7.2 FELine
    bottomFELineList = []
    for i in range(span_num.value):
        bottomFELineList.append(FELine(nodeBL[i], nodeBL[i + 1], sec_bc))
        bottomFELineList.append(FELine(nodeBR[i], nodeBR[i + 1], sec_bc))
    Group('Bottom FELines', *bottomFELineList).attach_to(marc)
    # 7.2.2 top FELines, TR,TL
    topFELineList = []
    for i in range(1, span_num.value):
        topFELineList.append(FELine(nodeTL[i], nodeTL[i + 1], sec_top))
        topFELineList.append(FELine(nodeTR[i], nodeTR[i + 1], sec_top))
    Group('Top FELines', *topFELineList).attach_to(marc)
    # 7.2.3 vertical
    verFELines = []
    for i in range(1, span_num.value + 1):
        for (a, b) in [(nodeBL, nodeBR), (nodeTR, nodeBR), (nodeTR, nodeTL), (nodeBL, nodeTL)]:
            verFELines.append(FELine(a[i], b[i], sec_ver))
    Group('Vertical FELines', *verFELines).attach_to(marc)
    # 7.2.4 oblique
    obliqFELines = []
    for i in range(1, span_num.value):
        for (a, b) in [(nodeBL, nodeTL), (nodeBR, nodeTR), (nodeTL, nodeTR)]:
            obliqFELines.append(FELine(a[i], b[i + 1], sec_web))
            obliqFELines.append(FELine(a[i + 1], b[i], sec_web))
    Group('Oblique FELines', *obliqFELines).attach_to(marc)
    # 7.2.5 Z beam in deck
    z_FEbeams = []
    for i in range(span_num.value):
        if (i % 2) == 0:
            z_beams.append(FELine(nodeBL[i], nodeBR[i + 1], sec_bc))
        else:
            z_beams.append(FELine(nodeBL[i + 1], nodeBR[i], sec_bc))
    group_zbeam = Group('Z FEbeams', *z_FEbeams)
    group_zbeam.attach_to(marc)
    # 7.2.6 the 1st segment
    first_FEseg = [FELine(nodeBL[0], nodeBR[0], sec_bc),
                   FELine(nodeBL[0], nodeTL[1], sec_bc),
                   FELine(nodeBR[0], nodeTR[1], sec_bc)]
    Group('First Segment', *first_FEseg).attach_to(marc)
    # 7.3 FESurface
    FEdecks = []
    for i in range(span_num.value):
        FEdecks.append(
            FESurface(nodeBL[i], nodeBR[i], nodeBR[i + 1], nodeBL[i + 1],
                    deck_thick, c4000, 'concrete deck'))
    Group('FEDecks', *FEdecks).attach_to(marc)
    # 8. Save and Show
    ShowTree(marc)
    marc.save_project()
