md diagram

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

