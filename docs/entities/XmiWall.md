# XmiWall

## Overview
`XmiWall` captures vertical plate elements such as shear walls, facade panels, or load-bearing walls. It extends `XmiBasePhysicalEntity`, keeping the data structure consistent with other physical types and enabling straightforward linking to analytical shells or curve members.

## Properties
Walls currently only require the base physical metadata. Geometry and analytical data live in separate entities to keep the graph modular. Common relationships include `XmiHasGeometry`, `XmiHasStructuralStorey`, and—when needed—`XmiHasStructuralCurveMember` or other analytical bridges.

## Usage
```python
from xmi.v2.models.entities.xmi_wall import XmiWall

wall, errors = XmiWall.from_dict({
    "ID": "wall-001",
    "Name": "Core Wall",
    "Description": "Lift core wall"
})
```

Walls are frequently grouped by elevation/storey, matched with materials, and associated with analytical shell elements to support design coordination.
