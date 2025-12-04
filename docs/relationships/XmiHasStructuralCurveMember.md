# XmiHasStructuralCurveMember

## Overview
`XmiHasStructuralCurveMember` links a physical entity (usually `XmiBeam` or `XmiColumn`) to its analytical `XmiStructuralCurveMember`. The relationship is directional: **physical → analytical**, mirroring how the C# implementation keeps graph references synchronized.

## Class Summary
- **Module**: `src/xmi/v2/models/relationships/xmi_has_structural_curve_member.py`
- **Source**: `XmiBasePhysicalEntity`
- **Target**: `XmiStructuralCurveMember`
- **Purpose**: Maintain feature parity with the C# physical-to-analytical bridge and enable graph queries such as “select the analytical element for this physical beam.”

## Validation Rules
The relationship constructor enforces:
1. `source` must inherit from `XmiBasePhysicalEntity`
2. `target` must be an `XmiStructuralCurveMember`
3. `entity_type` auto-defaults to the class name; `uml_type` remains optional for tooling metadata

Invalid combinations raise `TypeError`, so malformed bridges are caught during parsing.

## Usage Example
```python
beam, _ = XmiBeam.from_dict({...})
curve, _ = XmiStructuralCurveMember.from_dict({
    "ID": "curve-01",
    "CurveMemberType": "Beam",
    "SystemLine": "TopMiddle"
})
bridge = XmiHasStructuralCurveMember(source=beam, target=curve)
```

Once the model loads, traversals are straightforward:
```python
def find_curve_for_physical(model, physical_id):
    physical = next(e for e in model.entities if e.id == physical_id)
    rel = next(
        r for r in model.relationships
        if isinstance(r, XmiHasStructuralCurveMember) and r.source is physical
    )
    return rel.target
```

## Graph Benefits
- Keeps analytical and physical layers synchronized without duplicating data
- Allows downstream graph tooling (e.g., NetworkX, Neo4j) to treat bridges as explicit edges
- Provides a central hook for QA/QC rules: missing bridges, multi-target mappings, or misaligned system lines
