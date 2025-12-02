# XmiPoint3D

## Overview

`XmiPoint3D` represents a three-dimensional point in Cartesian coordinates. It is the fundamental geometric primitive used throughout the XMI schema to define positions of nodes, endpoints of lines, centers of arcs, and other spatial locations. Points are immutable after creation and serve as building blocks for more complex geometric entities.

## Class Hierarchy

- **Parent**: `XmiBaseGeometry`
- **Grandparent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/geometries/xmi_point_3d.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `x` | `float` | X coordinate in 3D space | Must be numeric (int or float) |
| `y` | `float` | Y coordinate in 3D space | Must be numeric (int or float) |
| `z` | `float` | Z coordinate in 3D space | Must be numeric (int or float) |

### Inherited Properties

Inherits from `XmiBaseGeometry` and `XmiBaseEntity`:
- `name`: Optional name/identifier of the point
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiPoint3D"
- `description`: Optional description

## Relationships

`XmiPoint3D` participates in several relationships:

### Target Relationships (this entity is the target):

- **`XmiHasGeometry`**: Links from `XmiStructuralPointConnection` to define node location
- **Component of other geometries**: Used as `start_point`, `end_point`, `center_point` in `XmiLine3D` and `XmiArc3D`

### Composition

Points are composed into other geometric entities:
- **XmiLine3D**: Uses 2 points (start and end)
- **XmiArc3D**: Uses 3 points (start, end, and center)

## Coordinate System

Points are defined in the global coordinate system of the XMI model:
- **X-axis**: Typically represents East-West direction
- **Y-axis**: Typically represents North-South direction
- **Z-axis**: Typically represents vertical (elevation)

The actual interpretation depends on the `GlobalCoordinateSystem` defined in the `StructuralModel`.

## Usage Examples

### Creating a Point Directly

```python
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create a point at origin
origin = XmiPoint3D(
    x=0.0,
    y=0.0,
    z=0.0,
    name="ORIGIN",
    id="point-origin"
)

# Create a point at specific coordinates
point1 = XmiPoint3D(
    x=1000.0,  # 1000mm in X
    y=2000.0,  # 2000mm in Y
    z=3000.0,  # 3000mm in Z (elevation)
    name="P1",
    id="point-001"
)

# Coordinates can be integers (auto-converted to float)
point2 = XmiPoint3D(
    x=100,
    y=200,
    z=300
)

print(f"Point1: ({point1.x}, {point1.y}, {point1.z})")
# Output: Point1: (1000.0, 2000.0, 3000.0)
```

### Loading from Dictionary

```python
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Dictionary with PascalCase keys (XMI format)
point_dict = {
    "X": 5000.0,
    "Y": 6000.0,
    "Z": 7000.0,
    "Name": "P2",
    "ID": "point-002",
    "Description": "Corner point"
}

# Parse using from_dict
point, errors = XmiPoint3D.from_dict(point_dict)

if point and not errors:
    print(f"Created point {point.name} at ({point.x}, {point.y}, {point.z})")
else:
    print(f"Errors: {errors}")

# Alternative: from_xmi_dict_obj (handles key mapping)
point, errors = XmiPoint3D.from_xmi_dict_obj(point_dict)
```

### Using Pydantic Validation

```python
# Field aliases allow snake_case or PascalCase
point1 = XmiPoint3D(x=1.0, y=2.0, z=3.0)  # snake_case
point2 = XmiPoint3D(X=1.0, Y=2.0, Z=3.0)  # PascalCase (from JSON)

# Both create equivalent points
assert point1.x == point2.x
assert point1.y == point2.y
assert point1.z == point2.z
```

### Common Patterns

#### Distance Between Two Points

```python
import math

def distance_3d(p1: XmiPoint3D, p2: XmiPoint3D) -> float:
    """Calculate Euclidean distance between two 3D points."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dz = p2.z - p1.z
    return math.sqrt(dx**2 + dy**2 + dz**2)

# Example usage
point_a = XmiPoint3D(x=0.0, y=0.0, z=0.0)
point_b = XmiPoint3D(x=3000.0, y=4000.0, z=0.0)

dist = distance_3d(point_a, point_b)
print(f"Distance: {dist:.2f} mm")
# Output: Distance: 5000.00 mm
```

#### Midpoint Calculation

```python
def midpoint(p1: XmiPoint3D, p2: XmiPoint3D) -> XmiPoint3D:
    """Calculate midpoint between two 3D points."""
    return XmiPoint3D(
        x=(p1.x + p2.x) / 2,
        y=(p1.y + p2.y) / 2,
        z=(p1.z + p2.z) / 2,
        name=f"MID_{p1.name}_{p2.name}"
    )

# Example
p1 = XmiPoint3D(x=0.0, y=0.0, z=0.0, name="A")
p2 = XmiPoint3D(x=6000.0, y=8000.0, z=4000.0, name="B")
mid = midpoint(p1, p2)

print(f"Midpoint: ({mid.x}, {mid.y}, {mid.z})")
# Output: Midpoint: (3000.0, 4000.0, 2000.0)
```

#### Point Translation

```python
def translate(point: XmiPoint3D, dx: float, dy: float, dz: float) -> XmiPoint3D:
    """Translate a point by offset values."""
    return XmiPoint3D(
        x=point.x + dx,
        y=point.y + dy,
        z=point.z + dz,
        name=f"{point.name}_TRANSLATED"
    )

# Example
original = XmiPoint3D(x=1000.0, y=2000.0, z=3000.0, name="P1")
translated = translate(original, dx=500.0, dy=-300.0, dz=1000.0)

print(f"Original: ({original.x}, {original.y}, {original.z})")
print(f"Translated: ({translated.x}, {translated.y}, {translated.z})")
# Output: Translated: (1500.0, 1700.0, 4000.0)
```

#### Querying Points in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all Point3D geometry objects
points = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiPoint3D)
]

print(f"Total points: {len(points)}")

# Find points at specific elevation
elevation = 3000.0
points_at_level = [p for p in points if abs(p.z - elevation) < 1.0]
print(f"Points at elevation {elevation}: {len(points_at_level)}")

# Find bounding box
if points:
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    min_z = min(p.z for p in points)
    max_z = max(p.z for p in points)

    print(f"Bounding box:")
    print(f"  X: [{min_x}, {max_x}]")
    print(f"  Y: [{min_y}, {max_y}]")
    print(f"  Z: [{min_z}, {max_z}]")
```

#### Converting to Tuple

```python
def point_to_tuple(point: XmiPoint3D) -> tuple:
    """Convert XmiPoint3D to coordinate tuple."""
    return (point.x, point.y, point.z)

# Example
p = XmiPoint3D(x=100.0, y=200.0, z=300.0)
coords = point_to_tuple(p)
print(coords)
# Output: (100.0, 200.0, 300.0)
```

## Validation Rules

### Type Validation

- All coordinates (`x`, `y`, `z`) must be numeric
- Integer values are automatically converted to float
- Non-numeric values raise `TypeError`

### Required Fields

All three coordinates are required:
```python
# Valid
point = XmiPoint3D(x=0.0, y=0.0, z=0.0)

# Invalid - will raise validation error
# point = XmiPoint3D(x=0.0, y=0.0)  # Missing z
```

### Missing Attributes in from_dict

The `from_dict()` method handles missing coordinates gracefully:
```python
incomplete_dict = {"X": 100.0, "Y": 200.0}  # Missing Z
point, errors = XmiPoint3D.from_dict(incomplete_dict)

# point will be None
# errors will contain: ["Missing attribute: Z"]
```

## Integration with XMI Schema

### Direct XMI Input (Rare)

Points are rarely specified directly in XMI JSON. They are typically embedded within other entities:

```json
{
  "StructuralPointConnection": [
    {
      "Name": "N1",
      "Coordinate": "0,0,0",
      ...
    }
  ]
}
```

The coordinate string is parsed to create an `XmiPoint3D` internally.

### As Components of Other Geometries

Points are typically created as components:

```json
{
  "line": {
    "start_point": {"X": 0.0, "Y": 0.0, "Z": 0.0},
    "end_point": {"X": 1000.0, "Y": 0.0, "Z": 0.0}
  }
}
```

## Notes

### Version Differences (v1 vs v2)

**v2 Advantages:**
- Uses Pydantic for automatic type validation
- Field aliases support both PascalCase (JSON) and snake_case (Python)
- Cleaner validation with decorators
- Better error messages

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation
- Tuple-based coordinate storage internally

### Immutability

While Pydantic models are not strictly immutable by default, it's best practice to treat points as immutable:
```python
# Don't modify existing points
# point.x = 100.0  # Avoid this

# Instead, create new points
new_point = XmiPoint3D(x=100.0, y=point.y, z=point.z)
```

### Coordinate Units

- Coordinates are typically in millimeters (mm) for XMI structural models
- Always verify units in the `StructuralUnit` definitions
- Unit conversions should be handled before creating points

### Floating Point Precision

- Coordinates use Python `float` (double precision)
- Be aware of floating-point precision limits when comparing points
- Use tolerance-based comparisons for equality:

```python
def points_equal(p1: XmiPoint3D, p2: XmiPoint3D, tolerance: float = 1e-6) -> bool:
    """Check if two points are equal within tolerance."""
    return (abs(p1.x - p2.x) < tolerance and
            abs(p1.y - p2.y) < tolerance and
            abs(p1.z - p2.z) < tolerance)
```

### Performance Considerations

- Points are lightweight objects (3 floats + metadata)
- Large models may contain thousands of points
- Use NumPy arrays for bulk geometric operations if performance is critical

## Related Classes

### Geometry Classes
- [`XmiLine3D`](./XmiLine3D.md) - Line defined by two points
- [`XmiArc3D`](./XmiArc3D.md) - Arc defined by three points
- `XmiBaseGeometry` - Base class for all geometry

### Entity Classes
- [`XmiStructuralPointConnection`](../entities/XmiStructuralPointConnection.md) - Node entity that uses Point3D for location
- [`XmiSegment`](../entities/XmiSegment.md) - Segment entity with point-based geometry

### Relationship Classes
- `XmiHasGeometry` - Links entities to their geometric representations
- `XmiHasPoint3D` - Specific relationship for point geometry

### Base Classes
- `XmiBaseGeometry` - Base geometry class
- `XmiBaseEntity` - Ultimate base class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Handles point creation during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for all entities including points
