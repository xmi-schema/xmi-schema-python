# XmiBeam

## Overview
`XmiBeam` models a physical beam element (horizontal or inclined member). It inherits from `XmiBasePhysicalEntity`, so domain metadata (`type="Physical"`) is populated automatically. Beams typically bridge to analytical `XmiStructuralCurveMember` objects to keep the physical graph synchronized with load-bearing analysis members.

## Class Hierarchy
- Parent: `XmiBasePhysicalEntity`
- Analytical Bridge: `XmiHasStructuralCurveMember` → `XmiStructuralCurveMember`

## Properties

### Required
| Property | Type | Description |
|----------|------|-------------|
| `ID` | `str` | Unique identifier shared across the graph |
| `Name` | `str` | Human-readable label |

### Optional / Domain-Specific
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `SystemLine` | `XmiStructuralCurveMemberSystemLineEnum` | `None` | Alignment line that controls offsets vs. the analytical curve |
| `Length` | `float` | `None` | Member length in model units |
| `LocalAxisX/Y/Z` | `tuple[float, float, float]` | `None` | Direction cosines of the local axes (strings such as `"1,0,0"` are parsed automatically) |
| `BeginNode*Offset` / `EndNode*Offset` | `float` | `0.0` | Translational offsets relative to analytical nodes |

## Relationships
- `XmiHasStructuralCurveMember` (physical → analytical curve)
- `XmiHasMaterial` (indirect via cross-section relationships)
- `XmiHasStructuralNode` / `XmiHasSegment` (through its paired curve member)

## Usage
Use `from_dict()` to parse JSON dictionaries. Validation errors are returned as a list instead of raising.

```python
from xmi.v2.models.entities.physical.xmi_beam import XmiBeam

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

## Bridge Example

```python
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember

curve, _ = XmiStructuralCurveMember.from_dict({
    "ID": "curve-001",
    "Name": "Analytical Beam",
    "EntityType": "XmiStructuralCurveMember",
    "CurveMemberType": "Beam",
    "SystemLine": "TopMiddle",
})
bridge = XmiHasStructuralCurveMember(source=beam, target=curve)
```

## Validation Notes
- Axis vectors accept either comma-delimited strings or numeric tuples.
- `SystemLine` strings are coerced to enums; invalid values surface as validation errors.
- All offsets default to `0.0`, so supplying them is optional unless a physical extent mismatch exists.
- End fixity metadata now resides on the analytical `XmiStructuralCurveMember` rather than the physical beam.
