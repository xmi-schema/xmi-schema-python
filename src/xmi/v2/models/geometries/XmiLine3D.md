# XmiLine3D

## Overview

`XmiLine3D` represents a straight line segment in three-dimensional space, defined by two endpoints. It is the most common geometric primitive for segments in structural curve members, representing straight beams, columns, and bracing elements. Lines are immutable after creation and provide the foundation for linear structural analysis.

## Class Hierarchy

- **Parent**: `XmiBaseGeometry`
- **Grandparent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/geometries/xmi_line_3d.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `start_point` | `XmiPoint3D` | Starting point of the line segment | Must be XmiPoint3D instance |
| `end_point` | `XmiPoint3D` | Ending point of the line segment | Must be XmiPoint3D instance |

### Inherited Properties

Inherits from `XmiBaseGeometry` and `XmiBaseEntity`:
- `name`: Optional name/identifier of the line
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiLine3D"
- `description`: Optional description

## Relationships

`XmiLine3D` participates in the following relationships:

### Target Relationships (this entity is the target):

- **`XmiHasGeometry`**: Links from `XmiSegment` to define segment geometry
- **`XmiHasLine3D`**: Specific relationship type for line geometry

### Composition

Lines are composed of:
- **start_point**: `XmiPoint3D` defining the beginning of the line
- **end_point**: `XmiPoint3D` defining the end of the line

## Geometric Properties

### Length Calculation

The length of a line segment can be calculated using the Euclidean distance formula:

```
length = √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]
```

### Direction Vector

The direction from start to end:

```
direction = (x₂-x₁, y₂-y₁, z₂-z₁)
```

### Unit Vector

Normalized direction:

```
unit_vector = direction / length
```

## Usage Examples

### Creating a Line Directly

```python
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create two points
start = XmiPoint3D(x=0.0, y=0.0, z=0.0, name="START")
end = XmiPoint3D(x=6000.0, y=0.0, z=0.0, name="END")

# Create a horizontal line (6m beam)
line = XmiLine3D(
    start_point=start,
    end_point=end,
    name="LINE-001",
    id="line-001"
)

print(f"Line from {line.start_point.name} to {line.end_point.name}")
```

### Creating Different Line Orientations

```python
# Horizontal line (beam along X-axis)
horizontal = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=3000.0),
    end_point=XmiPoint3D(x=6000.0, y=0.0, z=3000.0),
    name="BEAM-H"
)

# Vertical line (column along Z-axis)
vertical = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=0.0, z=3000.0),
    name="COLUMN-V"
)

# Diagonal line (bracing)
diagonal = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=3000.0, y=4000.0, z=0.0),
    name="BRACE-D"
)
```

### Loading from Dictionary

```python
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Dictionary format
line_dict = {
    "start_point": {
        "X": 0.0,
        "Y": 0.0,
        "Z": 0.0
    },
    "end_point": {
        "X": 5000.0,
        "Y": 0.0,
        "Z": 0.0
    },
    "name": "LINE-B01"
}

# Parse using from_dict
line, errors = XmiLine3D.from_dict(line_dict)

if line and not errors:
    print(f"Created line: {line.name}")
    print(f"Start: ({line.start_point.x}, {line.start_point.y}, {line.start_point.z})")
    print(f"End: ({line.end_point.x}, {line.end_point.y}, {line.end_point.z})")
else:
    print(f"Errors: {errors}")
```

### Common Patterns

#### Calculate Line Length

```python
import math

def line_length(line: XmiLine3D) -> float:
    """Calculate the length of a line segment."""
    dx = line.end_point.x - line.start_point.x
    dy = line.end_point.y - line.start_point.y
    dz = line.end_point.z - line.start_point.z
    return math.sqrt(dx**2 + dy**2 + dz**2)

# Example
line = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=3000.0, y=4000.0, z=0.0)
)

length = line_length(line)
print(f"Line length: {length:.2f} mm")
# Output: Line length: 5000.00 mm
```

#### Get Direction Vector

```python
def direction_vector(line: XmiLine3D) -> tuple:
    """Get the direction vector from start to end."""
    dx = line.end_point.x - line.start_point.x
    dy = line.end_point.y - line.start_point.y
    dz = line.end_point.z - line.start_point.z
    return (dx, dy, dz)

def unit_vector(line: XmiLine3D) -> tuple:
    """Get the normalized direction vector."""
    direction = direction_vector(line)
    length = math.sqrt(sum(d**2 for d in direction))
    if length == 0:
        return (0, 0, 0)
    return tuple(d / length for d in direction)

# Example
line = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=6000.0, y=0.0, z=0.0)
)

direction = direction_vector(line)
unit = unit_vector(line)

print(f"Direction: {direction}")
# Output: Direction: (6000.0, 0.0, 0.0)

print(f"Unit vector: {unit}")
# Output: Unit vector: (1.0, 0.0, 0.0)
```

#### Point Along Line (Interpolation)

```python
def point_at_parameter(line: XmiLine3D, t: float) -> XmiPoint3D:
    """
    Get a point along the line at parameter t.

    Args:
        line: The line segment
        t: Parameter from 0 (start) to 1 (end)

    Returns:
        Point at position t along the line
    """
    x = line.start_point.x + t * (line.end_point.x - line.start_point.x)
    y = line.start_point.y + t * (line.end_point.y - line.start_point.y)
    z = line.start_point.z + t * (line.end_point.z - line.start_point.z)

    return XmiPoint3D(x=x, y=y, z=z)

# Example: Get midpoint
line = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=6000.0, y=0.0, z=3000.0)
)

midpoint = point_at_parameter(line, 0.5)
quarter_point = point_at_parameter(line, 0.25)

print(f"Midpoint: ({midpoint.x}, {midpoint.y}, {midpoint.z})")
# Output: Midpoint: (3000.0, 0.0, 1500.0)
```

#### Check if Point is on Line

```python
def is_point_on_line(line: XmiLine3D, point: XmiPoint3D, tolerance: float = 1e-6) -> bool:
    """
    Check if a point lies on the line segment within tolerance.

    Args:
        line: The line segment
        point: Point to check
        tolerance: Distance tolerance

    Returns:
        True if point is on the line
    """
    # Vector from start to point
    dx1 = point.x - line.start_point.x
    dy1 = point.y - line.start_point.y
    dz1 = point.z - line.start_point.z

    # Vector from start to end
    dx2 = line.end_point.x - line.start_point.x
    dy2 = line.end_point.y - line.start_point.y
    dz2 = line.end_point.z - line.start_point.z

    # Cross product magnitude (perpendicular distance)
    cross = math.sqrt(
        (dy1 * dz2 - dz1 * dy2)**2 +
        (dz1 * dx2 - dx1 * dz2)**2 +
        (dx1 * dy2 - dy1 * dx2)**2
    )

    line_length = math.sqrt(dx2**2 + dy2**2 + dz2**2)

    if line_length == 0:
        return False

    perpendicular_distance = cross / line_length

    return perpendicular_distance < tolerance

# Example
line = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=10.0, y=0.0, z=0.0)
)

point_on = XmiPoint3D(x=5.0, y=0.0, z=0.0)
point_off = XmiPoint3D(x=5.0, y=1.0, z=0.0)

print(is_point_on_line(line, point_on))   # True
print(is_point_on_line(line, point_off))  # False
```

#### Querying Lines in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all Line3D geometry objects
lines = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiLine3D)
]

print(f"Total lines: {len(lines)}")

# Find all horizontal lines (constant Z)
horizontal_lines = [
    line for line in lines
    if abs(line.start_point.z - line.end_point.z) < 1.0
]

# Find all vertical lines (constant X and Y)
vertical_lines = [
    line for line in lines
    if abs(line.start_point.x - line.end_point.x) < 1.0 and
       abs(line.start_point.y - line.end_point.y) < 1.0
]

print(f"Horizontal lines: {len(horizontal_lines)}")
print(f"Vertical lines: {len(vertical_lines)}")

# Calculate total length
total_length = sum(line_length(line) for line in lines)
print(f"Total line length: {total_length:.2f} mm")
```

#### Reverse Line Direction

```python
def reverse_line(line: XmiLine3D) -> XmiLine3D:
    """Create a new line with reversed direction."""
    return XmiLine3D(
        start_point=line.end_point,
        end_point=line.start_point,
        name=f"{line.name}_REVERSED"
    )

# Example
original = XmiLine3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0, name="A"),
    end_point=XmiPoint3D(x=6000.0, y=0.0, z=0.0, name="B"),
    name="LINE-AB"
)

reversed_line = reverse_line(original)
print(f"Original: {original.start_point.name} → {original.end_point.name}")
print(f"Reversed: {reversed_line.start_point.name} → {reversed_line.end_point.name}")
# Output: Reversed: B → A
```

## Validation Rules

### Type Validation

- `start_point` must be an `XmiPoint3D` instance
- `end_point` must be an `XmiPoint3D` instance
- Both fields are required (cannot be None)

### Required Fields

Both points are mandatory:
```python
# Valid
line = XmiLine3D(
    start_point=XmiPoint3D(x=0, y=0, z=0),
    end_point=XmiPoint3D(x=1, y=0, z=0)
)

# Invalid - will raise validation error
# line = XmiLine3D(start_point=point1)  # Missing end_point
```

### Degenerate Lines

Lines where start and end points are identical (zero length) are technically valid but may cause issues in analysis:

```python
# Valid but degenerate
degenerate = XmiLine3D(
    start_point=XmiPoint3D(x=0, y=0, z=0),
    end_point=XmiPoint3D(x=0, y=0, z=0)
)

# Check for degenerate lines
if line_length(degenerate) < 1e-6:
    print("Warning: Degenerate line detected")
```

### Missing Attributes in from_dict

The `from_dict()` method handles validation:

```python
incomplete_dict = {
    "start_point": {"X": 0, "Y": 0, "Z": 0}
    # Missing end_point
}

line, errors = XmiLine3D.from_dict(incomplete_dict)
# line will be None
# errors will contain: ["Missing attribute: end_point"]
```

## Integration with XMI Schema

### As Segment Geometry

Lines are typically created as geometry for segments:

```python
# During parsing of StructuralCurveMember with "Segments": "Line"
segment = XmiSegment(position=0, segment_type=XmiSegmentTypeEnum.LINE)

# Create line geometry from segment nodes
line = XmiLine3D(
    start_point=begin_node_point,
    end_point=end_node_point
)

# Create relationship
geometry_rel = XmiHasGeometry(source=segment, target=line)
```

### Typical Creation Context

```python
# This happens internally during XmiManager parsing
# 1. Parse curve member with nodes: "N1;N2"
# 2. Parse segment types: "Line"
# 3. Create segment entity
# 4. Get point geometries from N1 and N2
# 5. Create Line3D from those points
# 6. Link segment to Line3D via XmiHasGeometry
```

## Notes

### Version Differences (v1 vs v2)

**v2 Advantages:**
- Uses Pydantic for automatic validation
- Cleaner validation with decorators
- Better error messages
- Type hints improve IDE support

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation
- Tuple-based storage for points

### Immutability

Treat lines as immutable after creation:
```python
# Don't modify existing lines
# line.start_point = new_point  # Avoid this

# Instead, create new lines
new_line = XmiLine3D(start_point=new_point, end_point=line.end_point)
```

### Coordinate Units

- Line coordinates inherit units from their points (typically millimeters)
- Lengths calculated from coordinates will be in the same units

### Floating Point Precision

When comparing lines or checking collinearity, use tolerance-based comparisons due to floating-point precision limits.

### Performance Considerations

- Lines are lightweight objects (2 point references + metadata)
- Large models may contain thousands of lines
- Geometric calculations (length, direction) are computed on-demand

### Common Applications

- **Straight beams**: Horizontal lines connecting column nodes
- **Columns**: Vertical lines between floor levels
- **Bracing**: Diagonal lines in lateral load resisting systems
- **Foundation beams**: Horizontal lines at foundation level

## Related Classes

### Geometry Classes
- [`XmiPoint3D`](./XmiPoint3D.md) - Points defining line endpoints
- [`XmiArc3D`](./XmiArc3D.md) - Curved alternative to straight lines
- `XmiBaseGeometry` - Base class for all geometry

### Entity Classes
- [`XmiSegment`](../entities/XmiSegment.md) - Segment entity that uses Line3D
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Curve members containing line segments

### Relationship Classes
- `XmiHasGeometry` - Links segments to line geometry
- `XmiHasLine3D` - Specific relationship for line geometry

### Enum Classes
- `XmiSegmentTypeEnum` - Defines LINE segment type

### Base Classes
- `XmiBaseGeometry` - Base geometry class
- `XmiBaseEntity` - Ultimate base class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Handles line creation during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for all entities including lines
