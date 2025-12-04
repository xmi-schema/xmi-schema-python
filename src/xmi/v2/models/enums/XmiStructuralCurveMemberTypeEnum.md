# XmiStructuralCurveMemberTypeEnum

## Overview

`XmiStructuralCurveMemberTypeEnum` is an enumeration that defines the structural function/type of curve members (linear structural elements) in the XMI schema. This classification helps identify the role each member plays in the structural system.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_structural_curve_member_type_enum.py`

## Enum Values

| Member Name | Value | Description | Typical Orientation |
|-------------|-------|-------------|---------------------|
| `BEAM` | "Beam" | Horizontal load-bearing member | Horizontal |
| `COLUMN` | "Column" | Vertical load-bearing member | Vertical |
| `BRACING` | "Bracing" | Lateral stability member | Diagonal |
| `OTHER` | "Other" | Other member types | Any |
| `UNKNOWN` | "Unknown" | Member type not specified | Any |

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum

# Direct access
member_type = XmiStructuralCurveMemberTypeEnum.BEAM
print(member_type.value)  # "Beam"

# Case-insensitive lookup
member_type = XmiStructuralCurveMemberTypeEnum("column")  # Returns COLUMN
```

### Creating Curve Members

```python
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember

# Create beam
beam = XmiStructuralCurveMember(
    name="B1",
    member_type=XmiStructuralCurveMemberTypeEnum.BEAM
)

# Create column
column = XmiStructuralCurveMember(
    name="C1",
    member_type=XmiStructuralCurveMemberTypeEnum.COLUMN
)

# Create bracing
bracing = XmiStructuralCurveMember(
    name="BR1",
    member_type=XmiStructuralCurveMemberTypeEnum.BRACING
)
```

### Filtering by Member Type

```python
def get_members_by_type(xmi_model, member_type):
    """Get all curve members of a specific type."""
    from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember

    return [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralCurveMember)
        and entity.member_type == member_type
    ]

# Usage
beams = get_members_by_type(xmi_model, XmiStructuralCurveMemberTypeEnum.BEAM)
columns = get_members_by_type(xmi_model, XmiStructuralCurveMemberTypeEnum.COLUMN)

print(f"Found {len(beams)} beams")
print(f"Found {len(columns)} columns")
```

### Member Type Statistics

```python
def analyze_member_types(xmi_model):
    """Analyze distribution of curve member types."""
    from collections import Counter
    from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember

    members = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralCurveMember)
    ]

    type_counts = Counter(m.member_type for m in members if m.member_type)

    print(f"Total curve members: {len(members)}")
    for mem_type, count in type_counts.most_common():
        percentage = (count / len(members)) * 100
        print(f"{mem_type.value}: {count} ({percentage:.1f}%)")
```

## Integration with XMI Schema

### XMI JSON Format

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B1",
      "Type": "Beam",
      "Nodes": ["N1", "N2"]
    },
    {
      "Name": "C1",
      "Type": "Column",
      "Nodes": ["N3", "N4"]
    }
  ]
}
```

### Usage in XmiStructuralCurveMember

```python
class XmiStructuralCurveMember(XmiBaseEntity):
    member_type: Optional[XmiStructuralCurveMemberTypeEnum] = Field(
        None, alias="Type"
    )
```

## Notes

### Common Member Types

- **BEAM**: Most common horizontal framing members
- **COLUMN**: Vertical load-bearing members
- **BRACING**: Diagonal members for lateral stability
- **OTHER**: Struts, ties, or specialty members

## Related Classes

### Entity Classes
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md)

### Other Enums
- [`XmiStructuralCurveMemberSystemLineEnum`](./XmiStructuralCurveMemberSystemLineEnum.md)

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
