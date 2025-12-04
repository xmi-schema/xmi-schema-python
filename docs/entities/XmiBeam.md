# XmiBeam

## Overview
`XmiBeam` models a physical beam element (horizontal or inclined member) within the XMI schema. It inherits from `XmiBasePhysicalEntity`, so its domain classification is automatically set to `Physical`. Each beam typically maps to an analytical `XmiStructuralCurveMember` through the `XmiHasStructuralCurveMember` relationship.

## Key Properties
| Field | Type | Description |
|-------|------|-------------|
| `SystemLine` | `XmiStructuralCurveMemberSystemLineEnum` | Reference line (e.g., `TopMiddle`, `MiddleMiddle`) used for alignment with analytical geometry |
| `Length` | `float` | Member length in model units |
| `LocalAxisX/Y/Z` | `Tuple[float, float, float]` | Direction cosines of the local axes (string input such as `"1,0,0"` is parsed automatically) |
| `BeginNode*Offset` / `EndNode*Offset` | `float` | Translational offsets between the analytical curve and physical extents |
| `EndFixityStart/EndFixityEnd` | `Optional[str]` | Fixity string (e.g., `FFFFFF`) describing boundary conditions |

## Construction
Use `XmiBeam.from_dict()` when parsing raw dictionaries. Axis strings and enums are normalized during parsing, and validation errors are returned in a list instead of raising immediately.

```python
from xmi.v2.models.entities.xmi_beam import XmiBeam

beam_dict = {
    "ID": "beam-001",
    "Name": "L1 Beam",
    "EntityType": "XmiBeam",
    "SystemLine": "TopMiddle",
    "Length": 6000.0,
    "LocalAxisX": "1,0,0",
    "LocalAxisY": "0,1,0",
    "LocalAxisZ": "0,0,1",
}

beam, errors = XmiBeam.from_dict(beam_dict)
assert not errors
```

## Bridge Pattern
Pair a beam with an analytical curve member:

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember

curve, _ = XmiStructuralCurveMember.from_dict({
    "ID": "curve-001",
    "Name": "Analytical Beam",
    "EntityType": "XmiStructuralCurveMember",
    "CurveMemberType": "Beam",
    "SystemLine": "TopMiddle"
})
bridge = XmiHasStructuralCurveMember(source=beam, target=curve)
```

The bridge relationship keeps physical geometry aligned with analytical members when building graph traversals.
