# XmiSlab

## Overview
`XmiSlab` models horizontal plate-like physical elements such as floors, podium slabs, or roof decks. The class extends `XmiBasePhysicalEntity`, so the shared metadata (ID, name, IFC GUID, physical domain) is standardized. Analytical geometry is captured on related shell entities rather than on the slab object itself.

## Class Hierarchy
- Parent: `XmiBasePhysicalEntity`
- Common Bridge: `XmiHasStructuralCurveMember` → `XmiStructuralSurfaceMember`

## Properties

### Required
| Property | Type | Description |
|----------|------|-------------|
| `ID` | `str` | Unique identifier for the slab |
| `Name` | `str` | Human-readable name |

### Optional
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Description` | `str` | `None` | Additional metadata |
| `IfcGuid` / `NativeID` | `str` | `None` | Source application identifiers |
| `Type` | `Literal["Physical"]` | `Physical` | Domain classification inherited from the base class |

## Relationships
- `XmiHasGeometry` → polygon perimeter or solid representation
- `XmiHasStructuralSurfaceMember` (or future shell bridge) → analytical mesh
- `XmiHasStructuralStorey` → elevation grouping
- `XmiHasStructuralMaterial` (indirect through analytical shells)

## Usage

```python
from xmi.v2.models.entities.physical.xmi_slab import XmiSlab

slab, errors = XmiSlab.from_dict({
    "ID": "slab-001",
    "Name": "Level 2 Slab",
    "Description": "Post-tensioned floor",
})
assert not errors
```

## Validation Notes
- No extra validation beyond the base class is required; the object is intentionally lightweight.
- All geometry or material references should be modeled via relationships so slab metadata stays decoupled from analytical surfaces.
