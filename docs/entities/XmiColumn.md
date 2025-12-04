# XmiColumn

## Overview
`XmiColumn` represents a physical vertical (or near-vertical) structural member. Like other physical classes, it inherits from `XmiBasePhysicalEntity` so the domain classification is `Physical` automatically. Columns often pair with analytical `XmiStructuralCurveMember` instances of type `Column` to capture structural behavior.

## Key Properties
| Field | Type | Description |
|-------|------|-------------|
| `SystemLine` | `XmiStructuralCurveMemberSystemLineEnum` | Alignment line within the cross-section |
| `Length` | `float` | Column height/length |
| `LocalAxisX/Y/Z` | `Tuple[float, float, float]` | Direction cosines of local axes |
| `BeginNode*Offset` / `EndNode*Offset` | `float` | Translational offsets relative to analytical nodes |
| `EndFixityStart/EndFixityEnd` | `Optional[str]` | Fixity code (e.g., `FFFFFF`) describing releases |

## Construction
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
```

## Bridge Pattern
Columns are linked to analytical curve members (type `Column`) using `XmiHasStructuralCurveMember`:

```python
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember

curve, _ = XmiStructuralCurveMember.from_dict({
    "ID": "curve-column-01",
    "CurveMemberType": "Column",
    "SystemLine": "MiddleMiddle"
})
bridge = XmiHasStructuralCurveMember(source=column, target=curve)
```

This mapping keeps analytical models synchronized with the physical asset graph, enabling downstream queries such as “find the analytical element for this physical column.”
