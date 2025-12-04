# XmiStructuralCurveMemberSystemLineEnum

## Overview

`XmiStructuralCurveMemberSystemLineEnum` is an enumeration that defines the reference line (system line) for curve members like beams and columns. The system line determines which point within the cross-section is used as the reference for the member's axis definition.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_structural_curve_member_system_line_enum.py`

## Enum Values

| Member Name | Value | Description |
|-------------|-------|-------------|
| `TOP_LEFT` | "TopLeft" | Top-left corner of cross-section |
| `TOP_MIDDLE` | "TopMiddle" | Top center of cross-section |
| `TOP_RIGHT` | "TopRight" | Top-right corner of cross-section |
| `MIDDLE_LEFT` | "MiddleLeft" | Middle-left edge of cross-section |
| `MIDDLE_MIDDLE` | "MiddleMiddle" | Centroid/center of cross-section |
| `MIDDLE_RIGHT` | "MiddleRight" | Middle-right edge of cross-section |
| `BOTTOM_LEFT` | "BottomLeft" | Bottom-left corner of cross-section |
| `BOTTOM_MIDDLE` | "BottomMiddle" | Bottom center of cross-section |
| `BOTTOM_RIGHT` | "BottomRight" | Bottom-right corner of cross-section |
| `UNKNOWN` | "Unknown" | System line not specified |

## Purpose and Functionality

### System Line Definition

The system line determines:
- **Reference Axis**: Which point in the cross-section the member axis passes through
- **Eccentricity**: Offset between geometric axis and analytical axis
- **Connection Points**: Where members connect to each other
- **Load Application**: Reference for distributed loads

### Visual Representation

```
Cross-Section View (looking along member axis):

TOP_LEFT -------- TOP_MIDDLE -------- TOP_RIGHT
   |                   |                   |
   |                   |                   |
MIDDLE_LEFT --- MIDDLE_MIDDLE --- MIDDLE_RIGHT
   |                   |                   |
   |                   |                   |
BOTTOM_LEFT ---- BOTTOM_MIDDLE ---- BOTTOM_RIGHT
```

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum

# Direct access
system_line = XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
print(system_line.value)  # "MiddleMiddle"

# Case-insensitive lookup
system_line = XmiStructuralCurveMemberSystemLineEnum("top left")  # Returns TOP_LEFT
system_line = XmiStructuralCurveMemberSystemLineEnum("middle middle")  # Returns MIDDLE_MIDDLE
```

### Creating Curve Members

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum

# Beam with centroid reference (typical for analysis)
beam = XmiStructuralCurveMember(
    name="B1",
    member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
    system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
)

# Column with bottom center (typical for construction)
column = XmiStructuralCurveMember(
    name="C1",
    member_type=XmiStructuralCurveMemberTypeEnum.COLUMN,
    system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE
)

# Bracing with top left corner
bracing = XmiStructuralCurveMember(
    name="BR1",
    member_type=XmiStructuralCurveMemberTypeEnum.BRACING,
    system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT
)
```

### Common Practices by Member Type

```python
def get_typical_system_line(member_type):
    """Get typical system line for a member type."""
    from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum

    typical = {
        XmiStructuralCurveMemberTypeEnum.BEAM: XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        XmiStructuralCurveMemberTypeEnum.COLUMN: XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        XmiStructuralCurveMemberTypeEnum.BRACING: XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
    }
    return typical.get(member_type, XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE)

# Usage
from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum

beam_line = get_typical_system_line(XmiStructuralCurveMemberTypeEnum.BEAM)
print(f"Typical beam system line: {beam_line.value}")  # "TopMiddle"
```

### Calculating Eccentricity

```python
def calculate_eccentricity(cross_section, system_line):
    """Calculate eccentricity from centroid based on system line."""
    # Assuming rectangular cross-section for simplicity
    width = cross_section.width
    height = cross_section.height

    # Eccentricity from centroid (y-axis is vertical, z-axis is lateral)
    eccentricities = {
        XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT: (height/2, -width/2),
        XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE: (height/2, 0),
        XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT: (height/2, width/2),
        XmiStructuralCurveMemberSystemLineEnum.MIDDLE_LEFT: (0, -width/2),
        XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE: (0, 0),
        XmiStructuralCurveMemberSystemLineEnum.MIDDLE_RIGHT: (0, width/2),
        XmiStructuralCurveMemberSystemLineEnum.BOTTOM_LEFT: (-height/2, -width/2),
        XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE: (-height/2, 0),
        XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT: (-height/2, width/2),
    }

    return eccentricities.get(system_line, (0, 0))

# Usage
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

section = XmiCrossSection(width=300, height=500)
ecc_y, ecc_z = calculate_eccentricity(section, XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE)
print(f"Eccentricity: y={ecc_y}mm, z={ecc_z}mm")  # y=250mm, z=0mm
```

### System Line Statistics

```python
def analyze_system_lines(xmi_model):
    """Analyze distribution of system lines in model."""
    from collections import Counter
    from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember

    members = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralCurveMember)
    ]

    line_counts = Counter(m.system_line for m in members if m.system_line)

    print(f"Total curve members: {len(members)}")
    for line, count in line_counts.most_common():
        percentage = (count / len(members)) * 100
        print(f"{line.value}: {count} ({percentage:.1f}%)")
```

## Integration with XMI Schema

### XMI JSON Format

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B1",
      "Type": "Beam",
      "SystemLine": "TopMiddle",
      "Nodes": ["N1", "N2"]
    },
    {
      "Name": "C1",
      "Type": "Column",
      "SystemLine": "MiddleMiddle",
      "Nodes": ["N3", "N4"]
    }
  ]
}
```

### Usage in XmiStructuralCurveMember

```python
class XmiStructuralCurveMember(XmiBaseEntity):
    system_line: Optional[XmiStructuralCurveMemberSystemLineEnum] = Field(
        None, alias="SystemLine"
    )
```

## Notes

### Common Conventions

- **Beams**: Often use `TOP_MIDDLE` (top of beam at slab level)
- **Columns**: Typically use `MIDDLE_MIDDLE` (centroid)
- **Analytical Models**: Prefer `MIDDLE_MIDDLE` for simplicity
- **Construction Models**: May use edge references

### Impact on Analysis

System line affects:
- Member connectivity and framing
- Eccentricity in analysis models
- Load distribution
- Deflection calculations

## Related Classes

### Entity Classes
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Uses this enum
- [`XmiCrossSection`](../entities/XmiCrossSection.md) - Defines cross-section geometry

### Other Enums
- [`XmiStructuralCurveMemberTypeEnum`](./XmiStructuralCurveMemberTypeEnum.md) - Curve member types

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md) - Parent enum class

## See Also

- [Curve Member Documentation](../entities/XmiStructuralCurveMember.md)
- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
