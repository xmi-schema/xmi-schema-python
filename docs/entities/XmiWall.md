# XmiWall

## Overview
`XmiWall` captures vertical plate elements such as shear walls, cores, facade panels, or precast walls. It extends `XmiBasePhysicalEntity`, aligning with other physical types so downstream graph traversals can pivot between physical metadata and analytical shells.

## Class Hierarchy
- Parent: `XmiBasePhysicalEntity`
- Common Analytical Bridge: `XmiHasStructuralCurveMember` or future shell relationships

## Properties

### Required
| Property | Type | Description |
|----------|------|-------------|
| `ID` | `str` | Graph identifier |
| `Name` | `str` | Display name |

### Optional
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Description` | `str` | `None` | Notes or annotations |
| `IfcGuid` / `NativeID` | `str` | `None` | Source system identifiers |
| `Type` | `Literal["Physical"]` | `Physical` | Domain classification |

## Relationships
- `XmiHasGeometry` → outlines or extrusions
- `XmiHasStructuralStorey` → building level grouping
- `XmiHasStructuralCurveMember` / shell bridge → analytical representation
- `XmiHasStructuralMaterial` (indirect via linked analytical entities)

## Usage

```python
from xmi.v2.models.entities.physical.xmi_wall import XmiWall

wall, errors = XmiWall.from_dict({
    "ID": "wall-001",
    "Name": "Core Wall",
    "Description": "Lift core wall",
})
assert not errors
```

## Validation Notes
- No additional validation beyond the base class; walls serve as metadata nodes.
- Analytical or geometric details should be linked through relationships to maintain a modular graph.
