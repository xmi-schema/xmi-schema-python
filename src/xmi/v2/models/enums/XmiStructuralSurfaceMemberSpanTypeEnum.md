# XmiStructuralSurfaceMemberSpanTypeEnum

## Overview

`XmiStructuralSurfaceMemberSpanTypeEnum` is an enumeration that defines the spanning behavior of surface members (slabs, walls) in the XMI schema. This classification indicates how load is distributed and carried by the surface element.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_structural_surface_member_span_type_enum.py`

## Enum Values

| Member Name | Value | Description |
|-------------|-------|-------------|
| `ONE_WAY` | "One Way" | Surface spans primarily in one direction |
| `TWO_WAY` | "Two Way" | Surface spans in two orthogonal directions |
| `UNKNOWN` | "Unknown" | Span type not specified |

## Purpose and Functionality

### Span Type Definition

The span type determines:
- **Load Distribution**: How loads are carried to supports
- **Structural Behavior**: Bending and deflection patterns
- **Reinforcement Design**: Direction and amount of reinforcement
- **Analysis Method**: Appropriate analysis and design approach

### One-Way vs Two-Way Behavior

**One-Way Spanning:**
- Load carried primarily in one direction
- Typical for slabs with length/width ratio > 2
- Simpler analysis (beam theory)
- Reinforcement primarily in one direction

**Two-Way Spanning:**
- Load carried in both directions
- Typical for square or nearly square slabs
- More complex analysis (plate theory)
- Reinforcement required in both directions

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_structural_surface_member_span_type_enum import XmiStructuralSurfaceMemberSpanTypeEnum

# Direct access
span_type = XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY
print(span_type.value)  # "Two Way"

# Case-insensitive lookup
span_type = XmiStructuralSurfaceMemberSpanTypeEnum("one way")  # Returns ONE_WAY
```

### Creating Surface Members with Span Type

```python
from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum

# One-way slab (long rectangular slab)
one_way_slab = XmiStructuralSurfaceMember(
    name="SLAB_1W",
    member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    span_type=XmiStructuralSurfaceMemberSpanTypeEnum.ONE_WAY,
    thickness=150  # mm
)

# Two-way slab (square or nearly square)
two_way_slab = XmiStructuralSurfaceMember(
    name="SLAB_2W",
    member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    span_type=XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY,
    thickness=200  # mm
)
```

### Determining Span Type from Geometry

```python
def determine_span_type(surface_member, aspect_ratio_threshold=2.0):
    """Determine span type based on slab geometry."""
    # Get slab dimensions from nodes (simplified)
    # In practice, would analyze actual node coordinates

    # Assuming we have length and width
    length = surface_member.length  # hypothetical property
    width = surface_member.width    # hypothetical property

    aspect_ratio = max(length, width) / min(length, width)

    if aspect_ratio > aspect_ratio_threshold:
        return XmiStructuralSurfaceMemberSpanTypeEnum.ONE_WAY
    else:
        return XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY

# Usage (conceptual)
# span_type = determine_span_type(slab)
```

### Filtering by Span Type

```python
def get_surfaces_by_span(xmi_model, span_type):
    """Get all surface members with specific span type."""
    from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember

    return [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralSurfaceMember)
        and entity.span_type == span_type
    ]

# Usage
one_way = get_surfaces_by_span(xmi_model, XmiStructuralSurfaceMemberSpanTypeEnum.ONE_WAY)
two_way = get_surfaces_by_span(xmi_model, XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY)

print(f"One-way slabs: {len(one_way)}")
print(f"Two-way slabs: {len(two_way)}")
```

### Span Type Statistics

```python
def analyze_span_types(xmi_model):
    """Analyze distribution of span types in model."""
    from collections import Counter
    from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember

    surfaces = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralSurfaceMember)
    ]

    span_counts = Counter(s.span_type for s in surfaces if s.span_type)

    print(f"Total surface members: {len(surfaces)}")
    for span_type, count in span_counts.items():
        percentage = (count / len(surfaces)) * 100
        print(f"{span_type.value}: {count} ({percentage:.1f}%)")

# Usage
analyze_span_types(xmi_model)
# Output:
# Total surface members: 50
# Two Way: 30 (60.0%)
# One Way: 15 (30.0%)
# Unknown: 5 (10.0%)
```

### Design Implications

```python
def get_design_method(span_type):
    """Get appropriate design method for span type."""
    methods = {
        XmiStructuralSurfaceMemberSpanTypeEnum.ONE_WAY: "Beam strip method / One-way slab theory",
        XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY: "Plate theory / Yield line analysis",
        XmiStructuralSurfaceMemberSpanTypeEnum.UNKNOWN: "Determine from geometry"
    }
    return methods.get(span_type, "Unknown")

# Usage
for span_type in XmiStructuralSurfaceMemberSpanTypeEnum:
    method = get_design_method(span_type)
    print(f"{span_type.value}: {method}")
```

## Integration with XMI Schema

### XMI JSON Format

```json
{
  "StructuralSurfaceMember": [
    {
      "Name": "SLAB_1W",
      "Type": "Slab",
      "SpanType": "One Way",
      "Thickness": 150
    },
    {
      "Name": "SLAB_2W",
      "Type": "Slab",
      "SpanType": "Two Way",
      "Thickness": 200
    }
  ]
}
```

### Usage in XmiStructuralSurfaceMember

```python
class XmiStructuralSurfaceMember(XmiBaseEntity):
    span_type: Optional[XmiStructuralSurfaceMemberSpanTypeEnum] = Field(
        None, alias="SpanType"
    )
```

## Notes

### Design Considerations

**One-Way Slabs:**
- Main reinforcement in short direction
- Distribution steel in long direction
- Simpler detailing and construction

**Two-Way Slabs:**
- Reinforcement in both directions
- More efficient for square geometries
- May require drop panels or column capitals

### Applicability

- Primarily relevant for slabs and horizontal surfaces
- Less applicable to walls (typically span vertically)
- Not typically used for foundations

### Common Thresholds

Industry guidelines for determining span type:
- Length/Width < 2.0: Generally two-way
- Length/Width ≥ 2.0: Generally one-way
- Edge support conditions also affect behavior

## Related Classes

### Entity Classes
- [`XmiStructuralSurfaceMember`](../entities/XmiStructuralSurfaceMember.md)

### Other Enums
- [`XmiStructuralSurfaceMemberTypeEnum`](./XmiStructuralSurfaceMemberTypeEnum.md)
- [`XmiStructuralSurfaceMemberSystemPlaneEnum`](./XmiStructuralSurfaceMemberSystemPlaneEnum.md)

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md)

## See Also

- [Surface Member Documentation](../entities/XmiStructuralSurfaceMember.md)
- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
