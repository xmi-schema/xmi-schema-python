# XmiStructuralSurfaceMemberTypeEnum

## Overview

`XmiStructuralSurfaceMemberTypeEnum` is an enumeration that defines the structural function/type of surface members (2D structural elements) in the XMI schema. This classification helps identify the role each surface plays in the structural system.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_structural_surface_member_type_enum.py`

## Enum Values

| Member Name | Value | Description | Typical Orientation |
|-------------|-------|-------------|---------------------|
| `SLAB` | "Slab" | Horizontal floor or roof slab | Horizontal |
| `WALL` | "Wall" | Vertical wall element | Vertical |
| `PAD_FOOTING` | "Pad Footing" | Individual column footing | Horizontal (foundation) |
| `STRIP_FOOTING` | "Strip Footing" | Continuous wall footing | Horizontal (foundation) |
| `PILECAP` | "Pilecap" | Cap connecting pile group | Horizontal (foundation) |
| `ROOF_PANEL` | "Roof Panel" | Architectural roof panel | Sloped/Horizontal |
| `WALL_PANEL` | "Wall Panel" | Architectural wall panel | Vertical |
| `RAFT` | "Raft" | Raft foundation (mat foundation) | Horizontal (foundation) |
| `UNKNOWN` | "Unknown" | Surface type not specified | Any |

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum

# Direct access
surface_type = XmiStructuralSurfaceMemberTypeEnum.SLAB
print(surface_type.value)  # "Slab"

# Case-insensitive lookup
surface_type = XmiStructuralSurfaceMemberTypeEnum("wall")  # Returns WALL
```

### Creating Surface Members

```python
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

# Create slab
slab = XmiStructuralSurfaceMember(
    name="SLAB_L2",
    member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    thickness=200  # mm
)

# Create wall
wall = XmiStructuralSurfaceMember(
    name="WALL_A1",
    member_type=XmiStructuralSurfaceMemberTypeEnum.WALL,
    thickness=300  # mm
)

# Create raft foundation
raft = XmiStructuralSurfaceMember(
    name="RAFT_01",
    member_type=XmiStructuralSurfaceMemberTypeEnum.RAFT,
    thickness=800  # mm
)
```

### Filtering by Surface Type

```python
def get_surfaces_by_type(xmi_model, surface_type):
    """Get all surface members of a specific type."""
    from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

    return [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralSurfaceMember)
        and entity.member_type == surface_type
    ]

# Usage
slabs = get_surfaces_by_type(xmi_model, XmiStructuralSurfaceMemberTypeEnum.SLAB)
walls = get_surfaces_by_type(xmi_model, XmiStructuralSurfaceMemberTypeEnum.WALL)

print(f"Found {len(slabs)} slabs")
print(f"Found {len(walls)} walls")
```

### Categorizing Surface Members

```python
def categorize_surface(surface_type):
    """Categorize surface member into broad groups."""
    floor_types = {
        XmiStructuralSurfaceMemberTypeEnum.SLAB,
    }

    foundation_types = {
        XmiStructuralSurfaceMemberTypeEnum.PAD_FOOTING,
        XmiStructuralSurfaceMemberTypeEnum.STRIP_FOOTING,
        XmiStructuralSurfaceMemberTypeEnum.PILECAP,
        XmiStructuralSurfaceMemberTypeEnum.RAFT,
    }

    wall_types = {
        XmiStructuralSurfaceMemberTypeEnum.WALL,
        XmiStructuralSurfaceMemberTypeEnum.WALL_PANEL,
    }

    if surface_type in floor_types:
        return "Floor/Slab"
    elif surface_type in foundation_types:
        return "Foundation"
    elif surface_type in wall_types:
        return "Wall"
    else:
        return "Other"

# Usage
for surf_type in XmiStructuralSurfaceMemberTypeEnum:
    category = categorize_surface(surf_type)
    print(f"{surf_type.value}: {category}")
```

### Surface Type Statistics

```python
def analyze_surface_types(xmi_model):
    """Analyze distribution of surface member types."""
    from collections import Counter
    from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

    surfaces = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralSurfaceMember)
    ]

    type_counts = Counter(s.member_type for s in surfaces if s.member_type)

    print(f"Total surface members: {len(surfaces)}")
    for surf_type, count in type_counts.most_common():
        percentage = (count / len(surfaces)) * 100
        print(f"{surf_type.value}: {count} ({percentage:.1f}%)")
```

## Integration with XMI Schema

### XMI JSON Format

```json
{
  "StructuralSurfaceMember": [
    {
      "Name": "SLAB_L2",
      "Type": "Slab",
      "Thickness": 200,
      "Nodes": ["N1", "N2", "N3", "N4"]
    },
    {
      "Name": "WALL_A1",
      "Type": "Wall",
      "Thickness": 300,
      "Nodes": ["N5", "N6", "N7", "N8"]
    }
  ]
}
```

### Usage in XmiStructuralSurfaceMember

```python
class XmiStructuralSurfaceMember(XmiBaseEntity):
    member_type: Optional[XmiStructuralSurfaceMemberTypeEnum] = Field(
        None, alias="Type"
    )
```

## Notes

### Future Changes

The code contains comments indicating some types may be deprecated:
- `PILECAP`: "i think this shouldn't be here"
- `ROOF_PANEL`: "this sounds like archi. should not be here"
- `WALL_PANEL`: "this sounds like archi. should not be here"
- `RAFT`: "For future changes to be shifted to foundation type elements"

These architectural elements may be moved to a separate classification system in future versions.

### Common Surface Types

- **SLAB**: Most common horizontal surface (floors, roofs)
- **WALL**: Vertical load-bearing or shear walls
- **Foundation Types**: PAD_FOOTING, STRIP_FOOTING, RAFT for substructure

## Related Classes

### Entity Classes
- [`XmiStructuralSurfaceMember`](../entities/XmiStructuralSurfaceMember.md)

### Other Enums
- [`XmiStructuralSurfaceMemberSystemPlaneEnum`](./XmiStructuralSurfaceMemberSystemPlaneEnum.md)
- [`XmiStructuralSurfaceMemberSpanTypeEnum`](./XmiStructuralSurfaceMemberSpanTypeEnum.md)

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
