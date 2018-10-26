MD diagram
======

``` sequence
participant Bridge as br
participant Python as py
#participant OpenBrIM as ob
participant Geometry Model as ge
participant Finite Element Model as fe
participant MongoDB as mg

br ->py: new BrIM model
py -> ge: create geometry model
py -> fe: create finite element model
note over ge, fe: OpenBrIM APP view\nand examination
#note over ob: OpenBrIM examination
ge --> py: update attributes
fe --> py: update attributes
#py --> ob: re-create ParamML file
py -> mg: store information
```
```xml
<O D="Concrete" N="C4000Psi" T="Material" Type="concrete">
    <P D="Density" N="d" Role="Input" V="0.0000002248"/>
    <P D="modulus of elasticity" N="E" Role="Input" V="3604.9965"/>
    <P D="Coefficient of Thermal Expansion" N="a" Role="Input" V="0.0000055"/>
    <P D="Concrete Compressive Strength" N="Fc28" Role="Input" V="4"/>
</O>
```

```sequence
participant Geometry Model as ge
participant Python BrIM as py
participant Finite Element Model as fe
#participant OpenBrIM as ob


ge -- py: call get_openbrim_element
py -- fe: 
```

