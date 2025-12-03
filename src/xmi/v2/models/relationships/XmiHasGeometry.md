# XmiHasGeometry

## Overview

`XmiHasGeometry` is a relationship class that links structural entities to their geometric representations. It connects entities like nodes, segments, and members to geometric primitives (points, lines, arcs) that define their spatial location and shape. This relationship includes optional `is_begin` and `is_end` flags for multi-point geometries like lines and arcs.

## Class Hierarchy

- **Parent**: `XmiBaseRelationship`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/relationships/xmi_has_geometry.py`

## Properties

### Relationship-Specific Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `source` | `XmiBaseEntity` | Entity that has geometry (node, segment, etc.) | Must be XmiBaseEntity |
| `target` | `XmiBaseGeometry` | The geometric definition | Must be XmiBaseGeometry (Point3D, Line3D, Arc3D) |
| `is_begin` | `bool` (optional) | True if this is the beginning point of line/arc geometry | Optional flag |
| `is_end` | `bool` (optional) | True if this is the end point of line/arc geometry | Optional flag |

### Inherited Properties

Inherits from `XmiBaseRelationship`:
- `id`: Unique identifier (auto-generated UUID)
- `name`: Relationship name (default: "hasGeometry")
- `description`: Optional description
- `entity_type`: Type identifier (set to "XmiRelHasGeometry")
- `uml_type`: UML relationship type (optional)

## Purpose and Usage

### Geometric Definition

This relationship serves to:

1. **Define Spatial Location**: Link entities to their 3D geometric representation
2. **Support Visualization**: Provide coordinates for rendering
3. **Enable Analysis**: Supply geometric properties for calculations
4. **Maintain Topology**: Connect abstract entities to concrete geometry

### Common Source-Target Pairs

Typical relationships:

| Source Entity | Target Geometry | Purpose |
|---------------|-----------------|---------|
| `XmiStructuralPointConnection` | `XmiPoint3D` | Node location |
| `XmiSegment` (LINE type) | `XmiLine3D` | Straight segment geometry |
| `XmiSegment` (CIRCULAR_ARC type) | `XmiArc3D` | Curved segment geometry |

## Relationship Direction

```
[Source Entity] --hasGeometry--> [Geometry]

Examples:
[Node N1] --hasGeometry--> [Point3D at (0,0,0)]
[Segment (LINE)] --hasGeometry--> [Line3D from (0,0,0) to (6000,0,0)]
[Segment (ARC)] --hasGeometry--> [Arc3D with start, end, center points]
```

## Usage Examples

### Creating Point Geometry Relationship

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry

# Create node
node = XmiStructuralPointConnection(
    name="N1",
    coordinate="0,0,0"
)

# Create point geometry
point = XmiPoint3D(
    x=0.0,
    y=0.0,
    z=0.0,
    name="N1_POINT"
)

# Create relationship
geom_rel = XmiHasGeometry(
    source=node,
    target=point
)

print(f"Node {node.name} located at ({point.x}, {point.y}, {point.z})")
```

### Creating Line Geometry Relationship

```python
from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create segment
segment = XmiSegment(
    name="SEG_0",
    position=0,
    segment_type=XmiSegmentTypeEnum.LINE
)

# Create line geometry
line = XmiLine3D(
    start_point=XmiPoint3D(x=0, y=0, z=0),
    end_point=XmiPoint3D(x=6000, y=0, z=0),
    name="SEG_0_LINE"
)

# Create relationship
geom_rel = XmiHasGeometry(
    source=segment,
    target=line
)

print(f"Segment {segment.name} is a line from start to end")
```

### Finding Geometry for an Entity

```python
from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry

def find_geometry_for_entity(xmi_model, entity):
    """Find the geometry for an entity."""
    # Find geometry relationships where entity is the source
    geom_rels = xmi_model.find_relationships_by_source(
        entity,
        relationship_type=XmiHasGeometry
    )

    if geom_rels:
        return geom_rels[0].target

    return None

# Usage
node = find_entity_by_name(xmi_model, "N1")
geometry = find_geometry_for_entity(xmi_model, node)

if geometry:
    print(f"Node {node.name} geometry: {geometry.entity_type}")
    if isinstance(geometry, XmiPoint3D):
        print(f"  Location: ({geometry.x}, {geometry.y}, {geometry.z})")
```

### Finding Entity for Geometry

```python
def find_entity_for_geometry(xmi_model, geometry):
    """Find the entity that owns a geometry."""
    # Find geometry relationships where geometry is the target
    geom_rels = xmi_model.find_relationships_by_target(
        geometry,
        relationship_type=XmiHasGeometry
    )

    if geom_rels:
        return geom_rels[0].source

    return None

# Usage
point = find_entity_by_id(xmi_model, "point-001")
entity = find_entity_for_geometry(xmi_model, point)

if entity:
    print(f"Geometry belongs to {entity.entity_type}: {entity.name}")
```

### Get All Node Locations

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

def get_all_node_locations(xmi_model):
    """Get coordinates of all nodes."""
    nodes = [
        e for e in xmi_model.entities
        if isinstance(e, XmiStructuralPointConnection)
    ]

    locations = {}
    for node in nodes:
        geometry = find_geometry_for_entity(xmi_model, node)
        if geometry and isinstance(geometry, XmiPoint3D):
            locations[node.name] = (geometry.x, geometry.y, geometry.z)

    return locations

# Usage
locations = get_all_node_locations(xmi_model)

print("Node locations:")
for node_name, coords in locations.items():
    print(f"  {node_name}: {coords}")
```

### Get Segment Geometry Details

```python
from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D
import math

def get_segment_geometry_info(xmi_model, segment):
    """Get detailed geometry information for a segment."""
    geometry = find_geometry_for_entity(xmi_model, segment)

    if not geometry:
        return None

    info = {
        "type": geometry.entity_type,
        "segment_name": segment.name
    }

    if isinstance(geometry, XmiLine3D):
        # Calculate line length
        dx = geometry.end_point.x - geometry.start_point.x
        dy = geometry.end_point.y - geometry.start_point.y
        dz = geometry.end_point.z - geometry.start_point.z
        length = math.sqrt(dx**2 + dy**2 + dz**2)

        info["start"] = (geometry.start_point.x, geometry.start_point.y, geometry.start_point.z)
        info["end"] = (geometry.end_point.x, geometry.end_point.y, geometry.end_point.z)
        info["length"] = length

    elif isinstance(geometry, XmiArc3D):
        info["start"] = (geometry.start_point.x, geometry.start_point.y, geometry.start_point.z)
        info["end"] = (geometry.end_point.x, geometry.end_point.y, geometry.end_point.z)
        info["center"] = (geometry.center_point.x, geometry.center_point.y, geometry.center_point.z)
        info["radius"] = geometry.radius

    return info

# Usage
segment = find_entity_by_name(xmi_model, "SEG_0")
geom_info = get_segment_geometry_info(xmi_model, segment)

if geom_info:
    print(f"Segment {segment.name} geometry:")
    for key, value in geom_info.items():
        print(f"  {key}: {value}")
```

### Calculate Model Bounding Box

```python
def calculate_model_bounding_box(xmi_model):
    """Calculate bounding box of all point geometries in the model."""
    from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

    points = [
        e for e in xmi_model.entities
        if isinstance(e, XmiPoint3D)
    ]

    if not points:
        return None

    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    min_z = min(p.z for p in points)
    max_z = max(p.z for p in points)

    return {
        "min": (min_x, min_y, min_z),
        "max": (max_x, max_y, max_z),
        "dimensions": (max_x - min_x, max_y - min_y, max_z - min_z)
    }

# Usage
bbox = calculate_model_bounding_box(xmi_model)

if bbox:
    print("Model bounding box:")
    print(f"  Min: {bbox['min']}")
    print(f"  Max: {bbox['max']}")
    print(f"  Dimensions: {bbox['dimensions']}")
```

## Validation Rules

### Type Validation

- **Source**: Must be any `XmiBaseEntity` subclass
- **Target**: Must be `XmiBaseGeometry` subclass (Point3D, Line3D, Arc3D)
- Attempting to create a relationship with wrong types raises `TypeError`

### Boolean Flags

- `is_begin` and `is_end` are optional
- Primarily used for line and arc geometries to indicate endpoint roles
- Not typically used for point geometries

### Required Fields

Both source and target are required:
```python
# Valid
rel = XmiHasGeometry(
    source=entity,
    target=geometry
)

# Invalid - will raise validation error
# rel = XmiHasGeometry(source=entity)  # Missing target
```

### Automatic Defaults

- `name` defaults to "hasGeometry"
- `entity_type` automatically set to "XmiRelHasGeometry"

## Integration with XMI Schema

### Relationship Creation

Geometry relationships are created during XMI parsing:

1. **Node coordinates** → Create Point3D geometry
2. **Segment types** → Create Line3D or Arc3D geometry based on segment type
3. **Link entities to geometry** → Create XmiHasGeometry relationships

### Typical Parsing Flow

```python
# XmiManager internally:
# 1. Parse node coordinate string "0,0,3000"
coords = node_dict["Coordinate"].split(',')
point_geom = XmiPoint3D(x=float(coords[0]), y=float(coords[1]), z=float(coords[2]))

# 2. Create geometry relationship
geom_rel = XmiHasGeometry(source=node, target=point_geom)

# 3. Add to model
xmi_model.entities.append(point_geom)
xmi_model.relationships.append(geom_rel)
```

## Notes

### One-to-One Relationship

- Typically one entity has one geometry
- One geometry typically belongs to one entity
- Shared geometries (same point used by multiple entities) are possible but rare

### Geometry Types

Three geometry types are supported:
- **Point3D**: Single point in space (x, y, z)
- **Line3D**: Straight line between two points
- **Arc3D**: Circular arc with start, end, and center points

### Performance Considerations

- Geometry relationships are numerous (one per node + one per segment)
- Cache geometry lookups for frequently accessed entities
- Direct geometry access is O(n) without indexing

## Related Classes

### Source Entity Classes
- [`XmiStructuralPointConnection`](../entities/XmiStructuralPointConnection.md) - Nodes with point geometry
- [`XmiSegment`](../entities/XmiSegment.md) - Segments with line or arc geometry

### Target Geometry Classes
- [`XmiPoint3D`](../geometries/XmiPoint3D.md) - 3D point
- [`XmiLine3D`](../geometries/XmiLine3D.md) - Straight line
- [`XmiArc3D`](../geometries/XmiArc3D.md) - Circular arc

### Related Relationship Classes
- [`XmiHasStructuralPointConnection`](./XmiHasStructuralNode.md) - Links members/segments to nodes
- [`XmiHasSegment`](./XmiHasSegment.md) - Links members to segments

### Base Classes
- `XmiBaseRelationship` - Base class for all relationships
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base class for entities
- [`XmiBaseGeometry`](../bases/XmiBaseGeometry.md) - Base class for geometries

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates geometry relationships during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores and queries relationships
