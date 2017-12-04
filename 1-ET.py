# import the ET API
import xml.etree.ElementTree as ET
tree = ET.parse('0 MARC.xml')
root = tree.getroot()

# ## ===Basic XML process===
	# print('---find all the OBJECT element in 2nd layer---')
	# marc_object=root.findall('O')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find all the PARAMETER element in 2nd layer---')
	# marc_object=root.findall('P')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

### ===Basic XPath examples===
	# print('---find the OBJECT element in 1st layer/root layer---')
	# marc_object=root.findall(".")
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find the all OBJECT element in 2nd layer---')
	# marc_object=root.findall("*")
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find the all OBJECT or PARAMETER element in any layer---')
	# marc_object=root.findall(".//")
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find OBJECT element in 2nd layer with attrib T="Group"---')
	# marc_object=root.findall('*[@T="Group"]')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find OBJECT element in 2nd layer with attrib T="Group"---')
	# marc_object=root.findall('*[@Unit]')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

### ===Complex XPath examples===
	# print('---find OBJECT element in 2nd layer with attrib T="Group"---')
	# marc_object=root.findall('*[@T="Group"]')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find PARAMETER in any layer with attrib T="Group"---')
	# marc_object=root.findall('.//P[@N="Fy"]')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')

	# print('---find PARAMETER in any layer with attrib T="Group", and then its parent element---')
	# marc_object=root.findall('.//P[@N="Fy"]..')
	# for a in marc_object:
	# 	print(a.tag, a.attrib)
	# print('---E---N---D---')
