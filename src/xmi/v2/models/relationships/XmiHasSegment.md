# XmiHasSegment

## Overview

`XmiHasSegment` is a relationship class that links structural curve members to their individual segments. It establishes the decomposition of a curve member's path into geometric segments (lines, arcs) that connect consecutive nodes. This relationship is fundamental for representing multi-span members, curved elements, and members with intermediate nodes.

## Class Hierarchy

- **Parent**: `XmiBaseRelationship`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/relationships/xmi_has_segment.py`

## Properties

### Relationship-Specific Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `source` | `XmiBaseEntity` | Curve member that contains the segment | Must be XmiBaseEntity (typically XmiStructuralCurveMember) |
| `target` | `XmiSegment` | The segment definition | Must be XmiSegment |

### Inherited Properties

Inherits from `XmiBaseRelationship`:
- `id`: Unique identifier (auto-generated UUID)
- `name`: Relationship name (default: "hasSegment")
- `description`: Optional description
- `entity_type`: Type identifier (set to "XmiRelHasSegment")
- `uml_type`: UML relationship type (optional)

## Purpose and Usage

### Segment Organization

This relationship serves to:

1. **Decompose Member Path**: Break curve members into individual geometric segments
2. **Support Complex Geometry**: Enable curved, kinked, or multi-span members
3. **Define Segment Order**: Sequence segments along member length (via segment `position`)
4. **Enable Analysis**: Provide geometric primitives for structural calculations

### Common Source Entities

Typical source entities:
- **`XmiStructuralCurveMember`**: Beams, columns, braces that may have multiple segments

### Target Entity

The target is always:
- **`XmiSegment`**: Segment definition with type (LINE, CIRCULAR_ARC) and position

## Relationship Direction

```
[XmiStructuralCurveMember] --hasSegment--> [XmiSegment]

Example:
[Beam B01 (N1;N2;N3)] --hasSegment--> [Segment 0: Line N1→N2]
[Beam B01 (N1;N2;N3)] --hasSegment--> [Segment 1: Line N2→N3]
```

## Usage Examples

### Creating Relationships

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum
from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment

# Create curve member
beam = XmiStructuralCurveMember(
    name="B01",
    curve_member_type="Beam",
    nodes="N1;N2;N3",
    segments="Line;Line"
)

# Create segments
segment_0 = XmiSegment(
    name="B01_SEG_0",
    position=0,
    segment_type=XmiSegmentTypeEnum.LINE
)

segment_1 = XmiSegment(
    name="B01_SEG_1",
    position=1,
    segment_type=XmiSegmentTypeEnum.LINE
)

# Create relationships
seg_rel_0 = XmiHasSegment(source=beam, target=segment_0)
seg_rel_1 = XmiHasSegment(source=beam, target=segment_1)

print(f"{beam.name} has {2} segments")
```

### Finding Segments for a Member

```python
from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment

def find_segments_for_member(xmi_model, member):
    """Find all segments for a curve member, ordered by position."""
    # Find segment relationships where member is the source
    segment_rels = xmi_model.find_relationships_by_source(
        member,
        relationship_type=XmiHasSegment
    )

    # Extract segments and sort by position
    segments = [rel.target for rel in segment_rels]
    segments.sort(key=lambda s: s.position)

    return segments

# Usage
beam = find_entity_by_name(xmi_model, "B01")
segments = find_segments_for_member(xmi_model, beam)

print(f"Beam {beam.name} has {len(segments)} segments:")
for seg in segments:
    print(f"  Position {seg.position}: {seg.segment_type.value}")
```

### Finding Member for a Segment

```python
def find_member_for_segment(xmi_model, segment):
    """Find the curve member that contains a segment."""
    # Find segment relationships where segment is the target
    segment_rels = xmi_model.find_relationships_by_target(
        segment,
        relationship_type=XmiHasSegment
    )

    if segment_rels:
        return segment_rels[0].source

    return None

# Usage
segment = find_entity_by_name(xmi_model, "B01_SEG_0")
member = find_member_for_segment(xmi_model, segment)

if member:
    print(f"Segment {segment.name} belongs to member {member.name}")
```

### Analyzing Segment Types per Member

```python
from collections import Counter

def analyze_member_segments(xmi_model, member):
    """Analyze segment composition of a member."""
    segments = find_segments_for_member(xmi_model, member)

    analysis = {
        "total_segments": len(segments),
        "segment_types": Counter(s.segment_type.value for s in segments),
        "positions": [s.position for s in segments]
    }

    return analysis

# Usage
beam = find_entity_by_name(xmi_model, "B01")
analysis = analyze_member_segments(xmi_model, beam)

print(f"Member {beam.name} segment analysis:")
print(f"  Total segments: {analysis['total_segments']}")
print(f"  Segment types: {dict(analysis['segment_types'])}")
print(f"  Positions: {analysis['positions']}")
```

### Get Complete Member Path

```python
def get_member_path(xmi_model, member):
    """Get complete geometric path of a member through its segments."""
    from xmi.v2.models.relationships.xmi_has_structural_point_connection import XmiHasStructuralPointConnection
    from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry

    segments = find_segments_for_member(xmi_model, member)

    path = []
    for segment in segments:
        # Get segment geometry
        geom_rels = xmi_model.find_relationships_by_source(
            segment,
            relationship_type=XmiHasGeometry
        )

        if geom_rels:
            geometry = geom_rels[0].target
            path.append({
                "position": segment.position,
                "type": segment.segment_type.value,
                "geometry": geometry
            })

    return path

# Usage
member = find_entity_by_name(xmi_model, "B01")
path = get_member_path(xmi_model, member)

print(f"Member {member.name} path:")
for seg in path:
    print(f"  Segment {seg['position']}: {seg['type']}")
```

### Count Members by Segment Count

```python
def count_members_by_segment_count(xmi_model):
    """Count how many members have 1, 2, 3... segments."""
    from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
    from collections import Counter

    members = [
        e for e in xmi_model.entities
        if isinstance(e, XmiStructuralCurveMember)
    ]

    segment_counts = []
    for member in members:
        segments = find_segments_for_member(xmi_model, member)
        segment_counts.append(len(segments))

    return Counter(segment_counts)

# Usage
counts = count_members_by_segment_count(xmi_model)

print("Members by segment count:")
for seg_count, member_count in sorted(counts.items()):
    print(f"  {seg_count} segment(s): {member_count} members")
```

## Validation Rules

### Type Validation

- **Source**: Must be any `XmiBaseEntity` subclass (typically `XmiStructuralCurveMember`)
- **Target**: Must be `XmiSegment`
- Attempting to create a relationship with wrong types raises `TypeError`

### Required Fields

Both source and target are required:
```python
# Valid
rel = XmiHasSegment(
    source=curve_member,
    target=segment
)

# Invalid - will raise validation error
# rel = XmiHasSegment(source=curve_member)  # Missing target
```

### Automatic Defaults

- `name` defaults to "hasSegment"
- `entity_type` automatically set to "XmiRelHasSegment"

## Integration with XMI Schema

### Relationship Creation

Relationships are created during XMI parsing based on the `Segments` attribute:

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B01",
      "Nodes": "N1;N2;N3",
      "Segments": "Line;Line",
      ...
    }
  ]
}
```

The `XmiManager`:
1. Parses `Nodes` → ["N1", "N2", "N3"] (3 nodes)
2. Parses `Segments` → ["Line", "Line"] (2 segment types)
3. Creates 2 `XmiSegment` entities (positions 0 and 1)
4. Creates 2 `XmiHasSegment` relationships linking member to segments

### Segment Count Rule

For N nodes, there are typically N-1 segments:
- 2 nodes → 1 segment (simple beam)
- 3 nodes → 2 segments (kinked beam)
- 4 nodes → 3 segments (multi-span beam)

## Notes

### Segment Ordering

Segments must be ordered by `position` to properly represent the member path:
- Position 0: First segment (from node 0 to node 1)
- Position 1: Second segment (from node 1 to node 2)
- And so on...

### One-to-Many Relationship

- One member can have many segments (common for multi-span or curved members)
- One segment belongs to exactly one member

### Performance Considerations

- For large models, cache segment lookups per member
- Segment relationships are numerous (one per span)
- Sorting by position is O(n log n) but typically n is small (1-10 segments per member)

## Related Classes

### Source Entity Class
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Curve member containing segments

### Target Entity Class
- [`XmiSegment`](../entities/XmiSegment.md) - Individual segment definition

### Related Relationship Classes
- [`XmiHasStructuralPointConnection`](./XmiHasStructuralNode.md) - Links segments to nodes
- [`XmiHasGeometry`](./XmiHasGeometry.md) - Links segments to geometric definitions (Line3D, Arc3D)
- [`XmiHasCrossSection`](./XmiHasCrossSection.md) - Links members to cross-sections

### Geometry Classes
- [`XmiLine3D`](../geometries/XmiLine3D.md) - Line segment geometry
- [`XmiArc3D`](../geometries/XmiArc3D.md) - Arc segment geometry

### Enum Classes
- `XmiSegmentTypeEnum` - Defines segment types (LINE, CIRCULAR_ARC, etc.)

### Base Classes
- `XmiBaseRelationship` - Base class for all relationships
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base class for entities

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates segment relationships during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores and queries relationships
