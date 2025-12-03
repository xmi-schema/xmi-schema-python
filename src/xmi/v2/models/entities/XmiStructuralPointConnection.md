# XmiStructuralPointConnection

## Overview

`XmiStructuralPointConnection` represents a nodal point in 3D space within a structural model. These are the fundamental connection points where structural members (beams, columns, braces) meet and connect. Each point connection has a specific location in 3D coordinates and can optionally be associated with a structural storey/level.

Point connections serve as:
- **Nodes** for structural analysis (supports, joints, connection points)
- **Endpoints** for structural members (beams, columns)
- **Vertices** for surface members (slabs, walls)
- **Reference points** for loads and boundary conditions

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Module**: `xmi.v2.models.entities.xmi_structural_point_connection`
- **Implementation**: Pydantic model with validation

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `point` | `XmiPoint3D` | 3D coordinates (X, Y, Z) of the point connection | Must be a valid XmiPoint3D instance |

### Optional Properties

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `storey` | `XmiStructuralStorey` | `None` | Associated building storey/level | Must be XmiStructuralStorey instance or None |

### Inherited Properties (from XmiBaseEntity)

| Property | Type | Default | Description | Required |
|----------|------|---------|-------------|----------|
| `id` | `str` | Auto-generated | Unique identifier | Yes (via from_dict) |
| `name` | `str` | `None` | Human-readable name | Yes (via from_dict) |
| `description` | `str` | `None` | Detailed description | No |
| `ifcguid` | `str` | `None` | IFC GUID for interoperability | No |
| `entity_type` | `str` | `"XmiStructuralPointConnection"` | Entity type identifier | No |

## Relationships

`XmiStructuralPointConnection` participates in the following relationships:

- **XmiHasStructuralPointConnection**: Referenced by `XmiStructuralCurveMember` and `XmiStructuralSurfaceMember` to define member endpoints and vertices
- **XmiHasPoint3D**: Owns a `XmiPoint3D` geometry defining its 3D location
- **XmiHasStructuralStorey**: Can be associated with a `XmiStructuralStorey` to indicate floor level

## Usage Examples

### Creating a Point Connection Directly

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create a 3D point geometry
point_geometry = XmiPoint3D(X=0.0, Y=0.0, Z=0.0)

# Create the point connection
node = XmiStructuralPointConnection(
    id="node_001",
    name="Node at Origin",
    point=point_geometry,
    description="Support node at structure origin"
)

print(f"Node: {node.name}")
print(f"Location: X={node.point.X}, Y={node.point.Y}, Z={node.point.Z}")
```

### Loading from Dictionary

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection

# Dictionary from XMI file
node_dict = {
    "id": "97df9034-c7ea-45c0-8bd5-967da4b38874",
    "name": "Point Connection 1",
    "description": "Column base connection",
    "ifcguid": "4ef1f147-45cc-46af-9de7-3dfcfa27c044-000596b6",
    "point": {
        "X": -6067.8,
        "Y": -7812.7,
        "Z": -3667.1
    }
}

# Load and validate
node, errors = XmiStructuralPointConnection.from_dict(node_dict)

if node:
    print(f"Successfully loaded: {node.name}")
    print(f"Coordinates: ({node.point.X}, {node.point.Y}, {node.point.Z})")
else:
    print(f"Errors: {errors}")
```

### Creating Multiple Nodes for a Grid

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create a 3x3 grid of nodes at Z=0
nodes = []
spacing = 5000.0  # 5 meters

for i in range(3):
    for j in range(3):
        point = XmiPoint3D(
            X=i * spacing,
            Y=j * spacing,
            Z=0.0
        )
        node = XmiStructuralPointConnection(
            id=f"node_{i}_{j}",
            name=f"Grid Node ({i},{j})",
            point=point
        )
        nodes.append(node)

print(f"Created {len(nodes)} nodes")
```

### With Storey Association

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create a storey
ground_floor = XmiStructuralStorey(
    id="storey_ground",
    name="Ground Floor",
    elevation=0.0
)

# Create node on that storey
point = XmiPoint3D(X=10000.0, Y=5000.0, Z=0.0)
node = XmiStructuralPointConnection(
    id="node_gf_01",
    name="Ground Floor Column Base",
    point=point,
    storey=ground_floor
)

print(f"Node: {node.name}")
print(f"Storey: {node.storey.name if node.storey else 'None'}")
print(f"Elevation: {node.storey.elevation if node.storey else node.point.Z}")
```

### Handling Validation Errors

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection

# Missing required fields
invalid_dict = {
    "id": "node_invalid",
    "description": "Missing name and point"
}

node, errors = XmiStructuralPointConnection.from_dict(invalid_dict)

if not node:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error}")
    # Output:
    # - Missing attribute: name
    # - Missing attribute: point
```

### Accessing and Modifying Point Coordinates

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create node
point = XmiPoint3D(X=1000.0, Y=2000.0, Z=3000.0)
node = XmiStructuralPointConnection(
    id="node_001",
    name="Column Top",
    point=point
)

# Access coordinates
print(f"Original: ({node.point.X}, {node.point.Y}, {node.point.Z})")

# Modify coordinates (create new point)
new_point = XmiPoint3D(
    X=node.point.X + 500.0,
    Y=node.point.Y,
    Z=node.point.Z
)
node.point = new_point

print(f"Modified: ({node.point.X}, {node.point.Y}, {node.point.Z})")
```

## Validation Rules

### Type Validation
- `point`: Must be an instance of `XmiPoint3D` (not a dictionary or other type)
- `storey`: Must be an instance of `XmiStructuralStorey` or None

### Required Fields (via from_dict)
The `from_dict()` method enforces these requirements:
- `id`: Must be provided
- `name`: Must be provided
- `point`: Must be provided

Note: When creating instances directly via `__init__()`, only `point` is strictly required by Pydantic.

### Field Aliases
The class supports both PascalCase (external/XMI format) and snake_case (internal Python) naming:
- `Point` ↔ `point`
- `Storey` ↔ `storey`

## Coordinate System

### 3D Cartesian Coordinates
Point connections use a 3D Cartesian coordinate system:
- **X-axis**: Typically east-west or along building length
- **Y-axis**: Typically north-south or across building width
- **Z-axis**: Typically vertical (elevation)

### Units
The class does not enforce specific units. Common conventions:
- **Millimeters (mm)**: Common in many structural software packages
- **Meters (m)**: SI standard
- **Feet/Inches**: Imperial units

**Important**: Ensure consistency across your entire model.

### Global vs Local
These coordinates are typically in the **global coordinate system** of the structural model, not local to individual members.

## Common Use Cases

### 1. Creating Support Nodes

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Fixed support at origin
support = XmiStructuralPointConnection(
    id="support_001",
    name="Fixed Support A",
    point=XmiPoint3D(X=0.0, Y=0.0, Z=0.0),
    description="Fixed base support"
)
```

### 2. Loading Nodes from XMI File

```python
import json
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection

with open("nodes.json") as f:
    xmi_data = json.load(f)

nodes = []
errors_log = []

for node_dict in xmi_data.get("StructuralPointConnection", []):
    node, errors = XmiStructuralPointConnection.from_dict(node_dict)
    if node:
        nodes.append(node)
    else:
        errors_log.extend(errors)

print(f"Loaded {len(nodes)} nodes")
if errors_log:
    print(f"Encountered {len(errors_log)} errors")
```

### 3. Finding Nodes by Location

```python
def find_nodes_at_elevation(nodes: list, z: float, tolerance: float = 1.0):
    """Find all nodes at a specific elevation (Z-coordinate)"""
    return [
        node for node in nodes
        if abs(node.point.Z - z) < tolerance
    ]

# Usage
ground_nodes = find_nodes_at_elevation(all_nodes, z=0.0)
print(f"Found {len(ground_nodes)} nodes at ground level")
```

### 4. Calculating Distance Between Nodes

```python
import math

def distance_between_nodes(node1: XmiStructuralPointConnection,
                           node2: XmiStructuralPointConnection) -> float:
    """Calculate 3D distance between two point connections"""
    dx = node2.point.X - node1.point.X
    dy = node2.point.Y - node1.point.Y
    dz = node2.point.Z - node1.point.Z
    return math.sqrt(dx**2 + dy**2 + dz**2)

# Usage
dist = distance_between_nodes(node_a, node_b)
print(f"Distance: {dist:.2f} mm")
```

### 5. Grouping Nodes by Storey

```python
from collections import defaultdict

def group_nodes_by_storey(nodes: list):
    """Group point connections by their associated storey"""
    grouped = defaultdict(list)
    for node in nodes:
        storey_name = node.storey.name if node.storey else "Unassigned"
        grouped[storey_name].append(node)
    return dict(grouped)

# Usage
by_storey = group_nodes_by_storey(all_nodes)
for storey_name, storey_nodes in by_storey.items():
    print(f"{storey_name}: {len(storey_nodes)} nodes")
```

## Notes

### Uniqueness
- Each point connection should have a unique `id`
- Multiple point connections CAN exist at the same 3D location (overlapping nodes)
- However, this is typically avoided in well-formed structural models

### Member Connectivity
Point connections serve as the reference points for:
- **Begin and end nodes** of curve members (beams, columns, braces)
- **Corner vertices** of surface members (slabs, walls)
- These connections are established via relationships, not stored directly in this class

### Storey Assignment
- The `storey` field is optional but helpful for organizing large models
- Not all nodes need a storey assignment (e.g., mid-span nodes)
- Storey elevation and node Z-coordinate don't need to match exactly

### Performance Considerations
- For large models with thousands of nodes, consider:
  - Spatial indexing (e.g., k-d trees, octrees) for fast location queries
  - Caching frequently accessed node sets
  - Avoiding redundant distance calculations

### Version Differences (v1 vs v2)
- **v2** (this version): Uses Pydantic with automatic validation
- **v1**: Uses `__slots__` with manual validation
- v2 provides better type checking and more Pythonic API
- Field aliases in v2 enable seamless XMI file compatibility

## Related Classes

- **`XmiBaseEntity`**: Parent class providing common entity properties
- **`XmiPoint3D`**: Geometry class defining 3D coordinates
- **`XmiStructuralStorey`**: Optional storey/level association
- **`XmiStructuralCurveMember`**: References point connections as begin/end nodes
- **`XmiStructuralSurfaceMember`**: References point connections as vertices
- **`XmiHasStructuralPointConnection`**: Relationship class linking nodes to members
- **`XmiHasPoint3D`**: Relationship linking the connection to its geometry

## See Also

- [XmiPoint3D.md](../geometries/XmiPoint3D.md) - 3D point geometry
- [XmiStructuralStorey.md](XmiStructuralStorey.md) - Building storey/level
- [XmiStructuralCurveMember.md](XmiStructuralCurveMember.md) - Members using point connections
- [XmiBaseEntity.md](../bases/XmiBaseEntity.md) - Base entity documentation
