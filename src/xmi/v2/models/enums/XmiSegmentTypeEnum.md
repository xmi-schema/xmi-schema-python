# XmiSegmentTypeEnum

## Overview

`XmiSegmentTypeEnum` is an enumeration that defines the types of geometric segments used in XMI structural members. Segments represent the geometric path between nodes, defining how structural members (beams, columns, etc.) are shaped in 3D space.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_segment_type_enum.py`

## Enum Values

| Member Name | Value | Description | Geometry Class |
|-------------|-------|-------------|----------------|
| `LINE` | "Line" | Straight line segment | `XmiLine3D` |
| `CIRCULAR_ARC` | "Circular Arc" | Circular arc segment | `XmiArc3D` |
| `PARABOLIC_ARC` | "Parabolic Arc" | Parabolic arc segment | Not implemented |
| `BEZIER` | "Bezier" | Bezier curve segment | Not implemented |
| `SPLINE` | "Spline" | Spline curve segment | Not implemented |
| `OTHERS` | "Others" | Other segment types | Not implemented |

## Purpose and Functionality

### Segment Type Definition

Segments are geometric primitives that define the shape of structural members between connection points. The segment type determines:
- How the geometry is represented mathematically
- Which geometry class is used to store the segment data
- How the segment is visualized and analyzed

### Geometry Class Mapping

The enum provides a special method `get_geometry_class()` that maps segment types to their corresponding geometry classes:

```python
def get_geometry_class(self):
    """Get the geometry class associated with this segment type."""
    mapping = {
        XmiSegmentTypeEnum.LINE: XmiLine3D,
        XmiSegmentTypeEnum.CIRCULAR_ARC: XmiArc3D,
    }
    return mapping.get(self)
```

Currently, only LINE and CIRCULAR_ARC have implemented geometry classes.

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum

# Direct access
seg_type = XmiSegmentTypeEnum.LINE
print(seg_type.value)  # "Line"

# Case-insensitive lookup (via XmiBaseEnum)
seg_type = XmiSegmentTypeEnum("line")  # Returns XmiSegmentTypeEnum.LINE
seg_type = XmiSegmentTypeEnum("circular arc")  # Returns XmiSegmentTypeEnum.CIRCULAR_ARC

# From name
seg_type = XmiSegmentTypeEnum.from_name_get_enum("line")  # XmiSegmentTypeEnum.LINE

# From attribute
seg_type = XmiSegmentTypeEnum.from_attribute_get_enum("Line")  # XmiSegmentTypeEnum.LINE
```

### Getting Geometry Class

```python
# Get the geometry class for a segment type
seg_type = XmiSegmentTypeEnum.LINE
geometry_class = seg_type.get_geometry_class()
print(geometry_class)  # <class 'XmiLine3D'>

# Create geometry instance
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

if geometry_class:
    if seg_type == XmiSegmentTypeEnum.LINE:
        # Create line geometry
        line = geometry_class(
            start_point=XmiPoint3D(x=0, y=0, z=0),
            end_point=XmiPoint3D(x=1000, y=0, z=0)
        )
    elif seg_type == XmiSegmentTypeEnum.CIRCULAR_ARC:
        # Create arc geometry
        arc = geometry_class(
            start_point=XmiPoint3D(x=0, y=0, z=0),
            end_point=XmiPoint3D(x=1000, y=0, z=0),
            center_point=XmiPoint3D(x=500, y=500, z=0)
        )
```

### Parsing Segment Type from XMI

```python
from xmi.v2.models.entities.xmi_segment import XmiSegment

def parse_segment(segment_dict):
    """Parse segment from XMI dictionary."""
    # Get segment type string from XMI
    type_str = segment_dict.get("Type", "Line")

    # Convert to enum
    try:
        segment_type = XmiSegmentTypeEnum(type_str.lower())
    except (ValueError, KeyError):
        segment_type = XmiSegmentTypeEnum.LINE  # Default to LINE

    # Get appropriate geometry class
    geometry_class = segment_type.get_geometry_class()

    if not geometry_class:
        raise ValueError(f"Geometry class not implemented for {segment_type}")

    # Create segment with appropriate geometry
    segment = XmiSegment(
        segment_type=segment_type,
        # ... other segment properties
    )

    return segment
```

### Filtering Segments by Type

```python
def get_segments_by_type(xmi_model, segment_type: XmiSegmentTypeEnum):
    """Get all segments of a specific type."""
    from xmi.v2.models.entities.xmi_segment import XmiSegment

    segments = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiSegment) and entity.segment_type == segment_type
    ]
    return segments

# Usage
line_segments = get_segments_by_type(xmi_model, XmiSegmentTypeEnum.LINE)
arc_segments = get_segments_by_type(xmi_model, XmiSegmentTypeEnum.CIRCULAR_ARC)

print(f"Found {len(line_segments)} line segments")
print(f"Found {len(arc_segments)} arc segments")
```

### Checking Implemented Geometry

```python
def is_geometry_implemented(segment_type: XmiSegmentTypeEnum) -> bool:
    """Check if geometry class is implemented for a segment type."""
    return segment_type.get_geometry_class() is not None

# Check all segment types
for seg_type in XmiSegmentTypeEnum:
    implemented = is_geometry_implemented(seg_type)
    status = "✓ Implemented" if implemented else "✗ Not implemented"
    print(f"{seg_type.name}: {status}")

# Output:
# LINE: ✓ Implemented
# CIRCULAR_ARC: ✓ Implemented
# PARABOLIC_ARC: ✗ Not implemented
# BEZIER: ✗ Not implemented
# SPLINE: ✗ Not implemented
# OTHERS: ✗ Not implemented
```

### Segment Type Statistics

```python
def analyze_segment_types(xmi_model):
    """Analyze distribution of segment types in model."""
    from collections import Counter
    from xmi.v2.models.entities.xmi_segment import XmiSegment

    segments = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiSegment)
    ]

    type_counts = Counter(seg.segment_type for seg in segments)

    print(f"Total segments: {len(segments)}")
    for seg_type, count in type_counts.items():
        percentage = (count / len(segments)) * 100
        print(f"{seg_type.value}: {count} ({percentage:.1f}%)")

# Usage
analyze_segment_types(xmi_model)
# Output:
# Total segments: 150
# Line: 120 (80.0%)
# Circular Arc: 30 (20.0%)
```

### Creating Segment with Geometry

```python
def create_segment_with_geometry(start_node, end_node, segment_type_str="Line", center_node=None):
    """Create segment with appropriate geometry based on type."""
    # Parse segment type
    segment_type = XmiSegmentTypeEnum(segment_type_str.lower())

    # Get geometry class
    geometry_class = segment_type.get_geometry_class()

    if not geometry_class:
        raise ValueError(f"Geometry not implemented for {segment_type}")

    # Create geometry based on type
    if segment_type == XmiSegmentTypeEnum.LINE:
        geometry = geometry_class(
            start_point=start_node.geometry,
            end_point=end_node.geometry
        )
    elif segment_type == XmiSegmentTypeEnum.CIRCULAR_ARC:
        if not center_node:
            raise ValueError("Center node required for circular arc")
        geometry = geometry_class(
            start_point=start_node.geometry,
            end_point=end_node.geometry,
            center_point=center_node.geometry
        )

    # Create segment
    segment = XmiSegment(
        segment_type=segment_type,
        geometry=geometry,
        begin_node=start_node,
        end_node=end_node
    )

    return segment

# Usage
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection

node1 = XmiStructuralPointConnection(x=0, y=0, z=0)
node2 = XmiStructuralPointConnection(x=1000, y=0, z=0)

# Create line segment
line_seg = create_segment_with_geometry(node1, node2, "Line")

# Create arc segment
node_center = XmiStructuralPointConnection(x=500, y=500, z=0)
arc_seg = create_segment_with_geometry(node1, node2, "Circular Arc", node_center)
```

## Integration with XMI Schema

### XMI JSON Format

Segment types appear in XMI dictionaries as string values:

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B1",
      "Nodes": ["N1", "N2"],
      "Segments": [
        {
          "Type": "Line"
        }
      ]
    },
    {
      "Name": "B2",
      "Nodes": ["N3", "N4"],
      "Segments": [
        {
          "Type": "Circular Arc"
        }
      ]
    }
  ]
}
```

### Usage in XmiSegment

The `XmiSegment` entity uses this enum to store segment type:

```python
class XmiSegment(XmiBaseEntity):
    segment_type: XmiSegmentTypeEnum = Field(..., alias="SegmentType")
    # ... other fields
```

## Notes

### Implemented vs Not Implemented

Currently, only two segment types have corresponding geometry classes:
- **LINE**: Uses `XmiLine3D` for straight segments
- **CIRCULAR_ARC**: Uses `XmiArc3D` for circular arc segments

Other types (PARABOLIC_ARC, BEZIER, SPLINE, OTHERS) will return `None` from `get_geometry_class()`.

### Future Extensions

To add support for new segment types:
1. Create the geometry class (e.g., `XmiParabolicArc3D`)
2. Update the `get_geometry_class()` mapping
3. Update parsing logic in `XmiManager`

### Common Use Cases

- **LINE**: Most common - straight beams, columns, bracing
- **CIRCULAR_ARC**: Curved members like arches, curved beams
- **PARABOLIC_ARC**: Not commonly used in current implementation
- **BEZIER/SPLINE**: Reserved for future complex curved members
- **OTHERS**: Catch-all for custom segment types

### Performance Considerations

- Enum lookup is O(1) for direct access
- `get_geometry_class()` is a simple dictionary lookup - very fast
- Most structural models are dominated by LINE segments (>90%)

## Related Classes

### Geometry Classes
- [`XmiLine3D`](../geometries/XmiLine3D.md) - Line segment geometry
- [`XmiArc3D`](../geometries/XmiArc3D.md) - Circular arc segment geometry

### Entity Classes
- [`XmiSegment`](../entities/XmiSegment.md) - Uses this enum for segment_type field
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Contains segments

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md) - Parent enum class providing lookup methods

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Uses enum during segment parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores segments with segment types

## See Also

- [XMI Segment Documentation](../entities/XmiSegment.md)
- [Geometry Base Class](../bases/XmiBaseGeometry.md)
- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
