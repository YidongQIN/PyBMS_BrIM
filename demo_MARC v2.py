#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
use ClassPyOpenBrIM to generate the xml file of MARC Bridge.
"""

from ClassPyOpenBrIM import *

if __name__ == '__main__':
    marc = PyOpenBrIMElmt('MARC_OOP')
    # Units are in default template of new_project
    marc.new_project()

    # 1. Material
    c4000 = Material('C4000Psi', mat_type="concrete", des="Concrete")
    c4000.mat_property(d="0.0000002248", E="3604.9965", a="0.0000055", Fc28="4")
    rebar = Material('A615Gr60', mat_type="steel", des="Rebar")
    rebar.mat_property(d='0.0000002248', E='3604.9965', Nu="0.3", a="0.0000065", Fy="60", Fu="90")
    girder_steel = Material('A992Fy50', mat_type="steel", des="steel of girder")
    girder_steel.mat_property(d="0.0000007345", E="29000", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
    group_mat = Group('Material Group', c4000, rebar, girder_steel)

    # 2. Sections
    # 2.1 Sections Parameters
    BottomChord_width = PrmElmt("BottomChord_width", "6", ut="Length", role="Input")
    BottomChord_depth = PrmElmt("BottomChord_depth", "6", ut="Length", role="Input")
    BottomChord_thickness = PrmElmt("BottomChord_thickness", "0.375", role="Input")
    TopChord_width = PrmElmt("TopChord_width", "6", ut="Length", role="Input")
    TopChord_depth = PrmElmt("TopChord_depth", "6", ut="Length", role="Input")
    TopChord_thickness = PrmElmt("TopChord_thickness", "0.3125", role="Input")
    deck_thick = PrmElmt("deck_thick", "5", ut="Length", role="Input")
    VertiBeam_width = PrmElmt("VertiBeam_width", "6", ut="Length", role="Input")
    VertiBeam_depth = PrmElmt("VertiBeam_depth", "6", ut="Length", role="Input")
    VertiBeam_thickness = PrmElmt("VertiBeam_thickness", "0.25", ut="Length", role="Input")
    WebRadius = PrmElmt("WebRadius", "1", ut="Length", role="Input")
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
    circle.sub_prm("Radius", "WebRadius")
    sp_cir = Shape('Shape_WebCircle', circle)
    sec_web = Section('Section_Web', girder_steel, sp_cir)
    sec_web.attach_to(group_sections)

    group_sections.attach_to(marc)
    # 3. Structural Parameter

    # 4. Points

    # 5. Lines

    # 6. Surfaces

    # 7. Save and Show
    print('============\nTree of the MARC bridge Elements')
    ShowTree(marc)
    marc.save_project()
