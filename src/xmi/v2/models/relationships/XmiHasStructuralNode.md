# XmiHasStructuralPointConnection (XmiHasStructuralNode)

## Overview

`XmiHasStructuralPointConnection` is a relationship class that links structural elements to nodes (point connections). It establishes which nodes are connected to curve members, segments, and other structural entities. This relationship includes special attributes (`is_begin`, `is_end`) to indicate whether a node is at the beginning or end of a member or segment, which is critical for proper structural connectivity and analysis.

## Class Hierarchy

- **Parent**: `XmiBaseRelationship`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/relationships/xmi_has_structural_point_connection.py`

## Properties

### Relationship-Specific Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `source` | `XmiBaseEntity` | Element that connects to the node (member, segment, etc.) | Must be XmiBaseEntity |
| `target` | `XmiStructuralPointConnection` | The node/point connection | Must be XmiStructuralPointConnection |
| `is_begin` | `bool` (optional) | True if this node is at the beginning of the element | Optional flag |
| `is_end` | `bool` (optional) | True if this node is at the end of the element | Optional flag |

### Inherited Properties

Inherits from `XmiBaseRelationship`:
- `id`: Unique identifier (auto-generated UUID)
- `name`: Relationship name (default: "hasStructuralPointConnection")
- `description`: Optional description
- `entity_type`: Type identifier (set to "XmiRelHasStructuralPointConnection")
- `uml_type`: UML relationship type (optional)

## Purpose and Usage

### Node Connectivity

This relationship serves to:

1. **Define Element Endpoints**: Link members/segments to their begin/end nodes
2. **Establish Topology**: Create structural connectivity for analysis
3. **Enable Load Transfer**: Define how forces transfer through connections
4. **Support Visualization**: Provide node positions for rendering elements

### Common Source Entities

Typical source entities:
- **`XmiStructuralCurveMember`**: Beams, columns linking to begin/end nodes
- **`XmiSegment`**: Individual segments linking to consecutive nodes
- **`XmiStructuralSurfaceMember`**: Slabs, walls linking to boundary nodes

### Target Entity

The target is always:
- **`XmiStructuralPointConnection`**: Node/point connection definition

## Relationship Direction

```
[Source Element] --hasStructuralPointConnection--> [XmiStructuralPointConnection]

Examples:
[Beam B01] --hasStructuralPointConnection (is_begin=True)--> [Node N1]
[Beam B01] --hasStructuralPointConnection (is_end=True)-->   [Node N2]

[Segment 0] --hasStructuralPointConnection (is_begin=True)--> [Node N1]
[Segment 0] --hasStructuralPointConnection (is_end=True)-->   [Node N2]
```

## Usage Examples

### Creating Relationships with Begin/End Flags

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.relationships.xmi_has_structural_point_connection import XmiHasStructuralPointConnection

# Create nodes
node1 = XmiStructuralPointConnection(name="N1", coordinate="0,0,0")
node2 = XmiStructuralPointConnection(name="N2", coordinate="6000,0,0")

# Create beam
beam = XmiStructuralCurveMember(
    name="B01",
    curve_member_type="Beam",
    nodes="N1;N2",
    segments="Line"
)

# Create relationships with begin/end flags
node_rel_begin = XmiHasStructuralPointConnection(
    source=beam,
    target=node1,
    is_begin=True,
    is_end=False
)

node_rel_end = XmiHasStructuralPointConnection(
    source=beam,
    target=node2,
    is_begin=False,
    is_end=True
)

print(f"{beam.name} begins at {node1.name} and ends at {node2.name}")
```

### Finding Begin/End Nodes for a Member

```python
from xmi.v2.models.relationships.xmi_has_structural_point_connection import XmiHasStructuralPointConnection

def find_begin_end_nodes(xmi_model, member):
    """Find the begin and end nodes for a curve member."""
    # Find all node relationships for this member
    node_rels = xmi_model.find_relationships_by_source(
        member,
        relationship_type=XmiHasStructuralPointConnection
    )

    begin_node = None
    end_node = None

    for rel in node_rels:
        if rel.is_begin:
            begin_node = rel.target
        elif rel.is_end:
            end_node = rel.target

    return begin_node, end_node

# Usage
beam = find_entity_by_name(xmi_model, "B01")
begin, end = find_begin_end_nodes(xmi_model, beam)

if begin and end:
    print(f"Beam {beam.name}:")
    print(f"  Begin: {begin.name} at {begin.coordinate}")
    print(f"  End: {end.name} at {end.coordinate}")
```

### Finding All Elements Connected to a Node

```python
def find_elements_at_node(xmi_model, node):
    """Find all elements connected to a node."""
    # Find relationships where node is the target
    node_rels = xmi_model.find_relationships_by_target(
        node,
        relationship_type=XmiHasStructuralPointConnection
    )

    elements = [rel.source for rel in node_rels]
    return elements

# Usage
node_n1 = find_entity_by_name(xmi_model, "N1")
elements = find_elements_at_node(xmi_model, node_n1)

print(f"Node {node_n1.name} is connected to {len(elements)} elements:")
for elem in elements:
    print(f"  - {elem.entity_type}: {elem.name}")
```

### Get Ordered Nodes for Segment Chain

```python
def get_segment_nodes_in_order(xmi_model, curve_member):
    """Get nodes in order along a curve member's segments."""
    from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment
    from xmi.v2.models.entities.xmi_segment import XmiSegment

    # Get segments for this member
    segment_rels = xmi_model.find_relationships_by_source(
        curve_member,
        relationship_type=XmiHasSegment
    )

    segments = [rel.target for rel in segment_rels]
    segments.sort(key=lambda s: s.position)

    # Get nodes for each segment
    nodes = []
    for segment in segments:
        begin, end = find_begin_end_nodes(xmi_model, segment)
        if not nodes:  # First segment
            nodes.append(begin)
        nodes.append(end)

    return nodes

# Usage
member = find_entity_by_name(xmi_model, "B01")
nodes = get_segment_nodes_in_order(xmi_model, member)

print(f"Member {member.name} node sequence:")
for i, node in enumerate(nodes):
    print(f"  {i}: {node.name} at {node.coordinate}")
```

## Validation Rules

### Type Validation

- **Source**: Must be any `XmiBaseEntity` subclass
- **Target**: Must be `XmiStructuralPointConnection`
- Attempting to create a relationship with wrong types raises `TypeError`

### Boolean Flags

- `is_begin` and `is_end` are optional
- Typically, one should be `True` and the other `False` (or `None`)
- Both can be `None` for intermediate or unspecified connections

### Required Fields

Both source and target are required:
```python
# Valid
rel = XmiHasStructuralPointConnection(
    source=member,
    target=node,
    is_begin=True
)

# Invalid - will raise validation error
# rel = XmiHasStructuralPointConnection(source=member)  # Missing target
```

### Automatic Defaults

- `name` defaults to "hasStructuralPointConnection"
- `entity_type` automatically set to "XmiRelHasStructuralPointConnection"

## Integration with XMI Schema

### Relationship Creation

Relationships are created during XMI parsing when members specify their nodes:

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B01",
      "Nodes": "N1;N2",
      "BeginNode": "N1",
      "EndNode": "N2",
      ...
    }
  ]
}
```

The `XmiManager`:
1. Parses the `Nodes` string → ["N1", "N2"]
2. Resolves node names to `XmiStructuralPointConnection` objects
3. Creates relationships with `is_begin=True` for N1 and `is_end=True` for N2

## Related Classes

### Source Entity Classes
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Beams, columns
- [`XmiSegment`](../entities/XmiSegment.md) - Individual curve segments
- [`XmiStructuralSurfaceMember`](../entities/XmiStructuralSurfaceMember.md) - Slabs, walls

### Target Entity Class
- [`XmiStructuralPointConnection`](../entities/XmiStructuralPointConnection.md) - Node definition

### Related Relationship Classes
- [`XmiHasStructuralCrossSection`](./XmiHasStructuralCrossSection.md) - Links members to cross-sections
- [`XmiHasSegment`](./XmiHasSegment.md) - Links members to segments
- [`XmiHasGeometry`](./XmiHasGeometry.md) - Links nodes to point geometry

### Base Classes
- `XmiBaseRelationship` - Base class for all relationships
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base class for entities

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates node relationships during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores and queries relationships
