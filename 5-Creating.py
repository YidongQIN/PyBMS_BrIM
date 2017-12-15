import PyOpenBrIM as ob
import xml.etree.ElementTree as ET


def new_OpenBrIM(name):
    # default new OpenBrIM project with new name
    origin_string = '<O Alignment="None" N="new" T="Project" TransAlignRule="Right">\n    <O N="Units" T="Group">\n        <O Angle="Radian" Force="Kip" Length="Inch" N="Internal" T="Unit" Temperature="Fahrenheit" />\n        <O Angle="Degree" Force="Kip" Length="Feet" N="Geometry" T="Unit" Temperature="Fahrenheit" />\n        <O Angle="Degree" Force="Kip" Length="Inch" N="Property" T="Unit" Temperature="Fahrenheit" />\n    </O>\n    <O N="SW" T="AnalysisCase" WeightFactor="-1" />\n    <O Gravity="386.09" Modes="1" N="Seismic" T="AnalysisCaseEigen" />\n</O>'
    root = ET.fromstring(origin_string)
    root.attrib['N'] = name
    print(root.attrib)
    return root


def save_OpenBrIM(root):
    tree = ET.ElementTree(root)
    out_path = root.attrib['N'] + '.xml'
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


# ----main----


# tree = ob.read_xml('NEW_OpenBrIM.xml')
# root = tree.getroot()
root = new_OpenBrIM('The name of new OpenBrIM Project')

save_OpenBrIM(root)
