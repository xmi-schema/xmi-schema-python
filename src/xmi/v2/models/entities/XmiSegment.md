# XmiSegment

## Overview

`XmiSegment` represents individual geometric segments that form the path of structural curve members. Segments connect consecutive nodes along a curve member's length and can be straight lines, circular arcs, or other curve types. Segments are typically created during the parsing process rather than being directly specified in the input XMI data.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/entities/xmi_segment.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `position` | `int` | Sequential position of this segment within the parent member | Must be integer ≥ 0 |
| `segment_type` | `XmiSegmentTypeEnum` | Geometric type of the segment (Line, Circular Arc, etc.) | Must be valid enum value |

### Inherited Properties

Inherits from `XmiBaseEntity`:
- `name`: Name/identifier of the segment
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiSegment"
- `description`: Optional description

## Enums

### XmiSegmentTypeEnum

Defines the geometric type of the segment:

- `LINE`: Straight line segment (most common)
- `CIRCULAR_ARC`: Circular arc segment
- `PARABOLIC_ARC`: Parabolic arc segment
- `BEZIER`: Bezier curve segment
- `SPLINE`: Spline curve segment
- `OTHERS`: Other segment types

The enum also provides a `get_geometry_class()` method that returns the appropriate geometry class:
- `LINE` → `XmiLine3D`
- `CIRCULAR_ARC` → `XmiArc3D`
- Others → `None` (not yet implemented)

## Relationships

`XmiSegment` participates in several relationships:

### Source Relationships (this entity is the source):

- **`XmiHasGeometry`**: Links the segment to its geometric definition (`XmiLine3D`, `XmiArc3D`, etc.)
- **`XmiHasStructuralNode`**: Links to begin and end `XmiStructuralPointConnection` nodes (with `is_begin` and `is_end` attributes)

### Target Relationships (this entity is the target):

- **`XmiHasSegment`**: Curve members link to their segments through this relationship (segment is the target)

## Segment Creation

### How Segments are Created

Segments are **not** directly specified in the XMI JSON input. Instead, they are created during the parsing of `StructuralCurveMember` entities:

1. **Input Data**: Curve member includes:
   ```json
   {
     "Nodes": "N1;N2;N3",
     "Segments": "Line;CircularArc"
   }
   ```

2. **Parsing Process**:
   - Parser reads the nodes list (3 nodes)
   - Parser reads the segments list (2 segment types)
   - Parser creates 2 segment entities:
     - Segment 0: Position=0, Type=Line, connecting N1→N2
     - Segment 1: Position=1, Type=CircularArc, connecting N2→N3

3. **Relationships Created**:
   - `XmiHasSegment`: Curve member → Segment
   - `XmiHasStructuralNode`: Segment → Begin/End nodes
   - `XmiHasGeometry`: Segment → Geometry object (Line3D or Arc3D)

### Segment Count vs Node Count

For a curve member with **N nodes**, there are typically **N-1 segments**:
- 2 nodes → 1 segment (simple beam/column)
- 3 nodes → 2 segments (kinked or curved member)
- 4 nodes → 3 segments (multi-segment member)

## Usage Examples

### Creating a Segment Directly

```python
from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum

# Create a line segment
line_segment = XmiSegment(
    name="SEG-001",
    id="segment-001",
    position=0,
    segment_type=XmiSegmentTypeEnum.LINE,
    description="First segment of beam B01"
)

# Create an arc segment
arc_segment = XmiSegment(
    name="SEG-002",
    id="segment-002",
    position=1,
    segment_type=XmiSegmentTypeEnum.CIRCULAR_ARC,
    description="Curved segment"
)
```

### Segments in Context (Typical Parsing Pattern)

```python
# This is how segments are created during XmiManager parsing
# (simplified for illustration)

def parse_curve_member(curve_member_dict):
    nodes_str = curve_member_dict["Nodes"]  # "N1;N2;N3"
    segments_str = curve_member_dict["Segments"]  # "Line;CircularArc"

    node_names = nodes_str.split(";")  # ["N1", "N2", "N3"]
    segment_types = segments_str.split(";")  # ["Line", "CircularArc"]

    segments = []
    for i, seg_type_str in enumerate(segment_types):
        # Create segment entity
        segment = XmiSegment(
            name=f"{curve_member_dict['Name']}_SEG_{i}",
            id=f"{curve_member_dict['ID']}_SEG_{i}",
            position=i,
            segment_type=XmiSegmentTypeEnum.from_attribute_get_enum(seg_type_str)
        )
        segments.append(segment)

        # Create relationships to nodes
        begin_node = find_node(node_names[i])
        end_node = find_node(node_names[i + 1])

        # ... create XmiHasStructuralNode relationships
        # ... create geometry objects based on segment type

    return segments
```

### Querying Segments in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_segment import XmiSegment

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all segments
segments = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiSegment)
]

print(f"Total segments: {len(segments)}")

# Filter by type
line_segments = [
    seg for seg in segments
    if seg.segment_type == XmiSegmentTypeEnum.LINE
]

arc_segments = [
    seg for seg in segments
    if seg.segment_type == XmiSegmentTypeEnum.CIRCULAR_ARC
]

print(f"Line segments: {len(line_segments)}")
print(f"Arc segments: {len(arc_segments)}")
```

### Finding Segments for a Curve Member

```python
from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment

# Find all segments belonging to a curve member
segment_relationships = xmi_model.find_relationships_by_source(
    curve_member,
    relationship_type=XmiHasSegment
)

# Sort segments by position
segments = [rel.target for rel in segment_relationships]
segments.sort(key=lambda seg: seg.position)

print(f"Curve member {curve_member.name} has {len(segments)} segments:")
for seg in segments:
    print(f"  Position {seg.position}: {seg.segment_type.value}")
```

### Finding Nodes for a Segment

```python
from xmi.v2.models.relationships.xmi_has_structural_node import XmiHasStructuralNode

# Find begin and end nodes
node_relationships = xmi_model.find_relationships_by_source(
    segment,
    relationship_type=XmiHasStructuralNode
)

begin_node = None
end_node = None

for rel in node_relationships:
    if rel.is_begin:
        begin_node = rel.target
    elif rel.is_end:
        end_node = rel.target

if begin_node and end_node:
    print(f"Segment {segment.name}:")
    print(f"  Begin: {begin_node.name} at {begin_node.coordinate}")
    print(f"  End: {end_node.name} at {end_node.coordinate}")
```

### Finding Geometry for a Segment

```python
from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D

# Find geometry relationship
geometry_relationships = xmi_model.find_relationships_by_source(
    segment,
    relationship_type=XmiHasGeometry
)

if geometry_relationships:
    geometry = geometry_relationships[0].target

    if isinstance(geometry, XmiLine3D):
        print(f"Line segment from {geometry.begin} to {geometry.end}")
        # Calculate length
        length = ((geometry.end[0] - geometry.begin[0])**2 +
                  (geometry.end[1] - geometry.begin[1])**2 +
                  (geometry.end[2] - geometry.begin[2])**2)**0.5
        print(f"Length: {length:.2f}")

    elif isinstance(geometry, XmiArc3D):
        print(f"Arc segment:")
        print(f"  Begin: {geometry.begin}")
        print(f"  End: {geometry.end}")
        print(f"  Middle: {geometry.middle}")
        # Arc length calculation would require additional geometry
```

### Using Segment Type to Get Geometry Class

```python
# Get the appropriate geometry class for a segment type
segment_type = XmiSegmentTypeEnum.LINE
geometry_class = segment_type.get_geometry_class()

if geometry_class:
    print(f"Segment type {segment_type.value} uses {geometry_class.__name__}")
    # Output: Segment type Line uses XmiLine3D

# Handle unsupported types
segment_type = XmiSegmentTypeEnum.BEZIER
geometry_class = segment_type.get_geometry_class()

if geometry_class is None:
    print(f"Segment type {segment_type.value} is not yet supported")
```

## Validation Rules

### Type Validation

- `position` must be an integer (typically ≥ 0)
- `segment_type` must be a valid `XmiSegmentTypeEnum` value
- Field validators ensure type correctness

### Position Validation

- Position should be sequential (0, 1, 2, ...)
- Position determines the order of segments along the curve member
- Gaps in position numbering may indicate parsing errors

### Consistency Checks

When working with segments, verify:
- Number of segments = number of nodes - 1 (for parent curve member)
- Position values are sequential: 0, 1, 2, ..., N-1
- Each segment has exactly 2 node relationships (begin and end)
- Each segment has exactly 1 geometry relationship

## Integration with XMI Schema

### XMI Input Format

Segments are **not** directly listed in the XMI JSON. Instead, they are encoded within curve members:

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B01",
      "Nodes": "N1;N2;N3",
      "Segments": "Line;Line",
      "BeginNode": "N1",
      "EndNode": "N3",
      ...
    }
  ]
}
```

This will create 2 `XmiSegment` entities during parsing:
- Segment 0: Line from N1 to N2
- Segment 1: Line from N2 to N3

### Dependency Order

`XmiSegment` depends on:
1. `XmiStructuralPointConnection` (begin/end nodes must exist)
2. Parent `XmiStructuralCurveMember` must be parsed first

Segments are created **after** curve members during the parsing process.

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics:**
- Uses Pydantic for automatic validation
- Field aliases support both PascalCase and snake_case
- Type hints improve IDE support
- Cleaner validation with decorators

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation
- Explicit parsing logic

### Segment Geometry Mapping

Currently, only two segment types have geometry implementations:
- `LINE` → `XmiLine3D` (fully supported)
- `CIRCULAR_ARC` → `XmiArc3D` (fully supported)

Other segment types (`PARABOLIC_ARC`, `BEZIER`, `SPLINE`) are defined in the enum but do not have geometry classes yet.

### Segment Ordering

Segments must be ordered by position to reconstruct the curve member's path:
```python
# Correct approach
segments.sort(key=lambda s: s.position)
for seg in segments:
    process_segment(seg)
```

### Performance Considerations

- Segments are numerous in large models (one per curve member span)
- Use relationships efficiently to avoid repeated queries
- Position indexing allows fast segment lookup within a member

### Common Use Cases

1. **Path Reconstruction**: Traverse segments in order to reconstruct member geometry
2. **Segment Analysis**: Analyze individual spans for deflection, stress, etc.
3. **Geometry Queries**: Find actual 3D coordinates along the member path
4. **Visualization**: Render each segment with appropriate geometry (line vs arc)

## Related Classes

### Entity Classes
- [`XmiStructuralCurveMember`](./XmiStructuralCurveMember.md) - Parent curve member containing segments
- [`XmiStructuralPointConnection`](./XmiStructuralPointConnection.md) - Nodes at segment endpoints

### Geometry Classes
- [`XmiLine3D`](../geometries/XmiLine3D.md) - Line segment geometry
- [`XmiArc3D`](../geometries/XmiArc3D.md) - Arc segment geometry
- `XmiPoint3D` - Point coordinates at nodes

### Relationship Classes
- `XmiHasSegment` - Links curve members to their segments
- `XmiHasStructuralNode` - Links segments to begin/end nodes
- `XmiHasGeometry` - Links segments to their geometric representation

### Enum Classes
- `XmiSegmentTypeEnum` - Segment type enumeration with geometry mapping

### Base Classes
- `XmiBaseEntity` - Base entity class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Handles segment creation during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for segments and relationships
