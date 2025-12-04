# XmiColumn

## Overview
`XmiColumn` represents a physical vertical (or near-vertical) structural member. The class inherits from `XmiBasePhysicalEntity`, ensuring the physical domain metadata is always set. Columns almost always bridge to analytical `XmiStructuralCurveMember` instances of type `Column`.

## Class Hierarchy
- Parent: `XmiBasePhysicalEntity`
- Analytical Bridge: `XmiHasStructuralCurveMember` → `XmiStructuralCurveMember`

## Properties

### Required
| Property | Type | Description |
|----------|------|-------------|
| `ID` | `str` | Graph identifier reused by relationships |
| `Name` | `str` | Friendly label |

### Optional / Domain-Specific
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `SystemLine` | `XmiStructuralCurveMemberSystemLineEnum` | `None` | Cross-section reference line used to align to the analytical axis |
| `Length` | `float` | `None` | Column height |
| `LocalAxisX/Y/Z` | `tuple[float, float, float]` | `None` | Local axis orientation; accepts comma-separated strings |
| `BeginNode*Offset`, `EndNode*Offset` | `float` | `0.0` | Translational offsets from the native authoring click location to the analytical node after the software applies its placement adjustments |

## Relationships
- `XmiHasStructuralCurveMember` (column → analytical curve)
- `XmiHasStructuralStorey` (group by building levels)
- `XmiHasStructuralMaterial` (indirect through cross-section links)

## Usage

```python
from xmi.v2.models.entities.physical.xmi_column import XmiColumn

column_dict = {
    "ID": "column-001",
    "Name": "Story 1 Column",
    "EntityType": "XmiColumn",
    "SystemLine": "MiddleMiddle",
    "Length": 3600.0,
    "LocalAxisX": "0,0,1",
    "LocalAxisY": "1,0,0",
    "LocalAxisZ": "0,1,0",
}
column, errors = XmiColumn.from_dict(column_dict)
assert not errors
```

## Bridge Example

```python
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember

curve, _ = XmiStructuralCurveMember.from_dict({
    "ID": "curve-column-01",
    "CurveMemberType": "Column",
    "SystemLine": "MiddleMiddle",
})
bridge = XmiHasStructuralCurveMember(source=column, target=curve)
```

## Validation Notes
- Axis vectors are normalized when supplied in string form.
- Missing bridge relationships surface as `XmiHasStructuralCurveMember` errors during model loading.
- Optional offsets mirror whatever the native tool applied after the user clicked to place the element—keep them when the physical pick location differs from the analytical nodes, omit them for a direct alignment.
- Physical columns no longer accept `EndFixity*` fields; supply those on the analytical member if the exporter captures them.
