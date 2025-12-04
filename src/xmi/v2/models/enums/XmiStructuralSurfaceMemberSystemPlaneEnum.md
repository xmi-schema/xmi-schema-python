# XmiStructuralSurfaceMemberSystemPlaneEnum

## Overview

`XmiStructuralSurfaceMemberSystemPlaneEnum` is an enumeration that defines the reference plane (system plane) for surface members like slabs and walls. The system plane determines which horizontal plane or vertical edge of the surface is used as the reference for positioning and thickness measurement.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_structural_surface_member_system_plane_enum.py`

## Enum Values

| Member Name | Value | Description | Typical Use |
|-------------|-------|-------------|-------------|
| `BOTTOM` | "Bottom" | Bottom face of the surface | Slabs (soffit reference) |
| `TOP` | "Top" | Top face of the surface | Slabs (top surface reference) |
| `MIDDLE` | "Middle" | Middle plane of the surface | Analytical modeling |
| `LEFT` | "Left" | Left edge of the surface | Walls (left edge reference) |
| `RIGHT` | "Right" | Right edge of the surface | Walls (right edge reference) |
| `UNKNOWN` | "Unknown" | System plane not specified | Default/fallback |

## Purpose and Functionality

### System Plane Definition

The system plane determines:
- **Reference Location**: Where the surface geometry is defined relative to the physical element
- **Thickness Offset**: How thickness is applied from the reference plane
- **Analytical Model**: Which plane represents the surface in structural analysis

### Horizontal vs Vertical Surfaces

**Horizontal Surfaces (Slabs, Roofs):**
- `BOTTOM`: Reference is the soffit (bottom face)
- `TOP`: Reference is the top surface
- `MIDDLE`: Reference is the mid-plane (analytical model)

**Vertical Surfaces (Walls):**
- `LEFT`: Reference is the left edge
- `RIGHT`: Reference is the right edge
- `MIDDLE`: Reference is the centerline

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum

# Direct access
plane = XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM
print(plane.value)  # "Bottom"

# Case-insensitive lookup
plane = XmiStructuralSurfaceMemberSystemPlaneEnum("bottom")  # Returns BOTTOM
plane = XmiStructuralSurfaceMemberSystemPlaneEnum("TOP")     # Returns TOP

# From name
plane = XmiStructuralSurfaceMemberSystemPlaneEnum.from_name_get_enum("middle")

# From attribute
plane = XmiStructuralSurfaceMemberSystemPlaneEnum.from_attribute_get_enum("Bottom")
```

### Creating Surface Members with System Plane

```python
from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum
from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum

# Slab with bottom reference (typical for construction)
slab_bottom = XmiStructuralSurfaceMember(
    name="SLAB_L1",
    member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM,
    thickness=200  # mm, applied upward from bottom
)

# Slab with middle reference (typical for analysis)
slab_middle = XmiStructuralSurfaceMember(
    name="SLAB_L2",
    member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE,
    thickness=200  # mm, half up, half down from middle
)

# Wall with left reference
wall_left = XmiStructuralSurfaceMember(
    name="WALL_A1",
    member_type=XmiStructuralSurfaceMemberTypeEnum.WALL,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.LEFT,
    thickness=300  # mm, applied to the right from left edge
)
```

### Calculating Actual Z-coordinates

```python
def calculate_actual_elevations(surface_member, reference_z: float):
    """Calculate top and bottom elevations based on system plane."""
    plane = surface_member.system_plane
    thickness = surface_member.thickness

    if plane == XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM:
        # Reference is bottom, thickness goes up
        bottom_z = reference_z
        top_z = reference_z + thickness

    elif plane == XmiStructuralSurfaceMemberSystemPlaneEnum.TOP:
        # Reference is top, thickness goes down
        top_z = reference_z
        bottom_z = reference_z - thickness

    elif plane == XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE:
        # Reference is middle, thickness splits
        bottom_z = reference_z - thickness / 2
        top_z = reference_z + thickness / 2

    else:
        # For walls or unknown, assume middle
        bottom_z = reference_z - thickness / 2
        top_z = reference_z + thickness / 2

    return bottom_z, top_z

# Usage
slab = XmiStructuralSurfaceMember(
    name="SLAB_L2",
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM,
    thickness=200
)

# If nodes are at elevation 3000mm
bottom, top = calculate_actual_elevations(slab, 3000)
print(f"Slab soffit: {bottom} mm")  # 3000 mm
print(f"Slab top: {top} mm")        # 3200 mm
```

### Converting Between Reference Planes

```python
def convert_system_plane(surface_member, from_plane, to_plane, current_z):
    """Convert reference z-coordinate when changing system plane."""
    thickness = surface_member.thickness

    # First, find the middle plane z
    if from_plane == XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM:
        middle_z = current_z + thickness / 2
    elif from_plane == XmiStructuralSurfaceMemberSystemPlaneEnum.TOP:
        middle_z = current_z - thickness / 2
    else:  # MIDDLE
        middle_z = current_z

    # Then convert to target plane
    if to_plane == XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM:
        new_z = middle_z - thickness / 2
    elif to_plane == XmiStructuralSurfaceMemberSystemPlaneEnum.TOP:
        new_z = middle_z + thickness / 2
    else:  # MIDDLE
        new_z = middle_z

    return new_z

# Usage
# Slab at elevation 3000 (bottom reference)
old_z = 3000
new_z = convert_system_plane(
    slab,
    XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM,
    XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE,
    old_z
)
print(f"Middle plane at: {new_z} mm")  # 3100 mm
```

### Filtering by System Plane

```python
def get_surfaces_by_plane(xmi_model, system_plane):
    """Get all surface members with specific system plane."""
    from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember

    surfaces = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralSurfaceMember)
        and entity.system_plane == system_plane
    ]
    return surfaces

# Usage
bottom_ref = get_surfaces_by_plane(
    xmi_model,
    XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM
)
middle_ref = get_surfaces_by_plane(
    xmi_model,
    XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE
)

print(f"Surfaces with BOTTOM reference: {len(bottom_ref)}")
print(f"Surfaces with MIDDLE reference: {len(middle_ref)}")
```

### System Plane Statistics

```python
def analyze_system_planes(xmi_model):
    """Analyze distribution of system planes in model."""
    from collections import Counter
    from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember

    surfaces = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralSurfaceMember)
    ]

    plane_counts = Counter(surf.system_plane for surf in surfaces)

    print(f"Total surface members: {len(surfaces)}")
    for plane, count in plane_counts.items():
        percentage = (count / len(surfaces)) * 100
        print(f"{plane.value}: {count} ({percentage:.1f}%)")

# Usage
analyze_system_planes(xmi_model)
# Output:
# Total surface members: 100
# Bottom: 60 (60.0%)
# Middle: 35 (35.0%)
# Top: 5 (5.0%)
```

### Validation by Member Type

```python
def validate_system_plane(surface_member):
    """Validate system plane is appropriate for member type."""
    from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum

    warnings = []

    # For horizontal members (slabs), LEFT/RIGHT don't make sense
    horizontal_types = {
        XmiStructuralSurfaceMemberTypeEnum.SLAB,
        XmiStructuralSurfaceMemberTypeEnum.PAD_FOOTING,
        XmiStructuralSurfaceMemberTypeEnum.RAFT
    }

    # For vertical members (walls), TOP/BOTTOM might be unusual
    vertical_types = {
        XmiStructuralSurfaceMemberTypeEnum.WALL
    }

    if surface_member.member_type in horizontal_types:
        if surface_member.system_plane in {
            XmiStructuralSurfaceMemberSystemPlaneEnum.LEFT,
            XmiStructuralSurfaceMemberSystemPlaneEnum.RIGHT
        }:
            warnings.append(
                f"Horizontal member {surface_member.name} has "
                f"{surface_member.system_plane.value} reference (unusual)"
            )

    if surface_member.member_type in vertical_types:
        if surface_member.system_plane in {
            XmiStructuralSurfaceMemberSystemPlaneEnum.TOP,
            XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM
        }:
            warnings.append(
                f"Vertical member {surface_member.name} has "
                f"{surface_member.system_plane.value} reference (unusual)"
            )

    return warnings
```

### BIM Interoperability

```python
def get_ifc_reference_plane(system_plane):
    """Map XMI system plane to IFC reference plane."""
    mapping = {
        XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM: "BOTTOM",
        XmiStructuralSurfaceMemberSystemPlaneEnum.TOP: "TOP",
        XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE: "CENTER",
        XmiStructuralSurfaceMemberSystemPlaneEnum.LEFT: "LEFT",
        XmiStructuralSurfaceMemberSystemPlaneEnum.RIGHT: "RIGHT",
        XmiStructuralSurfaceMemberSystemPlaneEnum.UNKNOWN: None
    }
    return mapping.get(system_plane)

# Usage
plane = XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE
ifc_plane = get_ifc_reference_plane(plane)
print(f"IFC reference: {ifc_plane}")  # "CENTER"
```

## Integration with XMI Schema

### XMI JSON Format

System plane appears in surface member definitions:

```json
{
  "StructuralSurfaceMember": [
    {
      "Name": "SLAB_L2",
      "Type": "Slab",
      "SystemPlane": "Bottom",
      "Thickness": 200,
      "Nodes": ["N1", "N2", "N3", "N4"]
    },
    {
      "Name": "WALL_A1",
      "Type": "Wall",
      "SystemPlane": "Left",
      "Thickness": 300,
      "Nodes": ["N5", "N6", "N7", "N8"]
    }
  ]
}
```

### Usage in XmiStructuralSurfaceMember

```python
class XmiStructuralSurfaceMember(XmiBaseEntity):
    system_plane: Optional[XmiStructuralSurfaceMemberSystemPlaneEnum] = Field(
        None, alias="SystemPlane"
    )
    # ... other fields
```

## Notes

### Common Practices

- **Construction Documents**: Typically use BOTTOM for slabs (soffit reference)
- **Analytical Models**: Often use MIDDLE for centerline analysis
- **BIM Models**: May use any reference depending on software

### Coordinate Systems

The system plane interacts with:
- Node coordinates (define reference plane)
- Thickness property (offset from reference)
- Analytical model geometry

### Unknown vs Missing

- Use `UNKNOWN` when system plane is explicitly unknown
- Missing/None when not applicable or using default behavior

### Impact on Analysis

System plane affects:
- Load application points
- Deflection calculation points
- Connection geometry
- Element intersection logic

## Related Classes

### Entity Classes
- [`XmiStructuralSurfaceMember`](../entities/XmiStructuralSurfaceMember.md) - Uses this enum
- [`XmiStructuralPointConnection`](../entities/XmiStructuralPointConnection.md) - Nodes define reference plane

### Other Enums
- [`XmiStructuralSurfaceMemberTypeEnum`](./XmiStructuralSurfaceMemberTypeEnum.md) - Surface member types
- [`XmiStructuralSurfaceMemberSpanTypeEnum`](./XmiStructuralSurfaceMemberSpanTypeEnum.md) - Span behavior

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md) - Parent enum class

## See Also

- [Surface Member Documentation](../entities/XmiStructuralSurfaceMember.md)
- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
