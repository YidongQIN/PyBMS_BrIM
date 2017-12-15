import xml.etree.ElementTree as ET
import PyOpenBrIM as ob

# create OBJECT or PARAMETER automatically
# 之前的create node等可以作为参考。此处的newOP也是要作为ob程序包的一部分

def str_to_dict(str):
    pass
# emp: <P N="z_height" V="108" UT="Length" Role="Input"/>
# N and V is mandatory
def new_P(N,V,Role,UT,UC,D,T=default):
    pass

'''emp of Object
    <O N="Sections" T="Group">
        <O N="Section_BottomChord" T="Section">
'''
# 参考xml的自动补齐？ O[N='a']>

def new_O(T):
    pass

# object 需要创建模板，即上面是一个总体的，下面根据每种type编写模板化的
# ----main----

root = ob.new_OpenBrIM('New_OpenBrIM_project')

results = ob.find_nodes(root, './O')
ob.table_OBJECT(ob.select_OBJECT(results))

ob.save_OpenBrIM(root)
