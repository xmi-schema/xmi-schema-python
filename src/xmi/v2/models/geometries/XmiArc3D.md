# XmiArc3D

## Overview

`XmiArc3D` represents a circular arc segment in three-dimensional space, defined by three points: start, end, and center. Arcs are used for curved structural members such as curved beams, circular ramps, or any structural element following a circular path. The arc is defined in 3D space and can be planar or non-planar depending on the three defining points.

## Class Hierarchy

- **Parent**: `XmiBaseGeometry`
- **Grandparent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/geometries/xmi_arc_3d.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `start_point` | `XmiPoint3D` | Starting point of the arc | Must be XmiPoint3D instance |
| `end_point` | `XmiPoint3D` | Ending point of the arc | Must be XmiPoint3D instance |
| `center_point` | `XmiPoint3D` | Center point of the circular arc | Must be XmiPoint3D instance |

### Optional Properties

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `radius` | `Optional[float]` | `None` | Radius of the arc | Numeric value or None |

### Inherited Properties

Inherits from `XmiBaseGeometry` and `XmiBaseEntity`:
- `name`: Optional name/identifier of the arc
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiArc3D"
- `description`: Optional description

## Relationships

`XmiArc3D` participates in the following relationships:

### Target Relationships (this entity is the target):

- **`XmiHasGeometry`**: Links from `XmiSegment` to define curved segment geometry
- **`XmiHasArc3D`**: Specific relationship type for arc geometry

### Composition

Arcs are composed of:
- **start_point**: `XmiPoint3D` defining the beginning of the arc
- **end_point**: `XmiPoint3D` defining the end of the arc
- **center_point**: `XmiPoint3D` defining the center of the circular arc
- **radius**: Optional explicit radius (can be calculated from points)

## Geometric Properties

### Arc Characteristics

An arc is defined by three points that must satisfy these geometric constraints:
- Start and end points must be equidistant from the center point
- The three points define a unique circular arc
- The arc follows the shorter path from start to end around the circle (< 180°)

### Radius Calculation

If not explicitly provided, the radius can be calculated as the distance from the center to either endpoint:

```
radius = √[(x_start - x_center)² + (y_start - y_center)² + (z_start - z_center)²]
```

### Arc Length Calculation

The arc length depends on the central angle θ:

```
arc_length = radius × θ

where θ = 2 × arcsin(chord_length / (2 × radius))
```

### Arc Direction

The arc direction (clockwise or counterclockwise) depends on the order of the three points and the viewing perspective.

## Usage Examples

### Creating an Arc Directly

```python
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

# Create a horizontal circular arc (90-degree arc)
start = XmiPoint3D(x=5000.0, y=0.0, z=0.0, name="ARC_START")
end = XmiPoint3D(x=0.0, y=5000.0, z=0.0, name="ARC_END")
center = XmiPoint3D(x=0.0, y=0.0, z=0.0, name="ARC_CENTER")

arc = XmiArc3D(
    start_point=start,
    end_point=end,
    center_point=center,
    radius=5000.0,
    name="ARC-001",
    id="arc-001"
)

print(f"Arc from {arc.start_point.name} to {arc.end_point.name}")
print(f"Center: {arc.center_point.name}, Radius: {arc.radius}")
```

### Creating Different Arc Configurations

```python
# Quarter circle in XY plane
quarter_circle = XmiArc3D(
    start_point=XmiPoint3D(x=10000.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=10000.0, z=0.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    radius=10000.0,
    name="QUARTER_CIRCLE"
)

# Vertical arc (curved column)
vertical_arc = XmiArc3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=1000.0, y=0.0, z=3000.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=1500.0),
    name="CURVED_COLUMN"
)

# Small arc segment (curved beam)
curved_beam = XmiArc3D(
    start_point=XmiPoint3D(x=0.0, y=0.0, z=3000.0),
    end_point=XmiPoint3D(x=6000.0, y=0.0, z=3500.0),
    center_point=XmiPoint3D(x=3000.0, y=0.0, z=8000.0),
    name="CURVED_BEAM"
)
```

### Loading from Dictionary

```python
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D

# Dictionary format
arc_dict = {
    "start_point": {
        "X": 5000.0,
        "Y": 0.0,
        "Z": 0.0
    },
    "end_point": {
        "X": 0.0,
        "Y": 5000.0,
        "Z": 0.0
    },
    "center_point": {
        "X": 0.0,
        "Y": 0.0,
        "Z": 0.0
    },
    "radius": 5000.0,
    "name": "ARC-B01"
}

# Parse using from_dict
arc, errors = XmiArc3D.from_dict(arc_dict)

if arc and not errors:
    print(f"Created arc: {arc.name}")
    print(f"Start: ({arc.start_point.x}, {arc.start_point.y}, {arc.start_point.z})")
    print(f"End: ({arc.end_point.x}, {arc.end_point.y}, {arc.end_point.z})")
    print(f"Center: ({arc.center_point.x}, {arc.center_point.y}, {arc.center_point.z})")
    print(f"Radius: {arc.radius}")
else:
    print(f"Errors: {errors}")
```

### Common Patterns

#### Calculate Arc Radius from Points

```python
import math

def calculate_radius(arc: XmiArc3D) -> float:
    """Calculate the radius from center to start point."""
    dx = arc.start_point.x - arc.center_point.x
    dy = arc.start_point.y - arc.center_point.y
    dz = arc.start_point.z - arc.center_point.z
    return math.sqrt(dx**2 + dy**2 + dz**2)

# Example
arc = XmiArc3D(
    start_point=XmiPoint3D(x=5000.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=5000.0, z=0.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=0.0)
)

radius = calculate_radius(arc)
print(f"Calculated radius: {radius:.2f} mm")
# Output: Calculated radius: 5000.00 mm
```

#### Verify Arc Consistency

```python
def verify_arc_consistency(arc: XmiArc3D, tolerance: float = 1.0) -> bool:
    """
    Verify that start and end points are equidistant from center.

    Args:
        arc: The arc to verify
        tolerance: Acceptable difference in distances (mm)

    Returns:
        True if arc is geometrically consistent
    """
    # Calculate distance from center to start
    dx1 = arc.start_point.x - arc.center_point.x
    dy1 = arc.start_point.y - arc.center_point.y
    dz1 = arc.start_point.z - arc.center_point.z
    r1 = math.sqrt(dx1**2 + dy1**2 + dz1**2)

    # Calculate distance from center to end
    dx2 = arc.end_point.x - arc.center_point.x
    dy2 = arc.end_point.y - arc.center_point.y
    dz2 = arc.end_point.z - arc.center_point.z
    r2 = math.sqrt(dx2**2 + dy2**2 + dz2**2)

    # Check if radii are equal within tolerance
    return abs(r1 - r2) < tolerance

# Example
arc = XmiArc3D(
    start_point=XmiPoint3D(x=5000.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=5000.0, z=0.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=0.0)
)

is_valid = verify_arc_consistency(arc)
print(f"Arc is {'valid' if is_valid else 'invalid'}")
```

#### Calculate Arc Length

```python
def arc_length(arc: XmiArc3D) -> float:
    """
    Calculate the arc length.

    Returns:
        Arc length in same units as coordinates
    """
    # Calculate radius
    radius = calculate_radius(arc)

    # Calculate chord length (straight line distance from start to end)
    dx = arc.end_point.x - arc.start_point.x
    dy = arc.end_point.y - arc.start_point.y
    dz = arc.end_point.z - arc.start_point.z
    chord_length = math.sqrt(dx**2 + dy**2 + dz**2)

    # Calculate central angle using chord length
    # θ = 2 × arcsin(chord / (2 × radius))
    if radius == 0:
        return 0.0

    sin_half_angle = chord_length / (2 * radius)
    # Clamp to valid range for arcsin due to floating point errors
    sin_half_angle = max(-1.0, min(1.0, sin_half_angle))

    central_angle = 2 * math.asin(sin_half_angle)

    # Arc length = radius × angle
    return radius * central_angle

# Example
arc = XmiArc3D(
    start_point=XmiPoint3D(x=5000.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=5000.0, z=0.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=0.0)
)

length = arc_length(arc)
print(f"Arc length: {length:.2f} mm")
# Output: Arc length: 7853.98 mm (≈ π/2 × 5000)
```

#### Calculate Central Angle

```python
def central_angle(arc: XmiArc3D) -> float:
    """
    Calculate the central angle of the arc in radians.

    Returns:
        Central angle in radians
    """
    radius = calculate_radius(arc)

    # Vectors from center to start and end
    v1x = arc.start_point.x - arc.center_point.x
    v1y = arc.start_point.y - arc.center_point.y
    v1z = arc.start_point.z - arc.center_point.z

    v2x = arc.end_point.x - arc.center_point.x
    v2y = arc.end_point.y - arc.center_point.y
    v2z = arc.end_point.z - arc.center_point.z

    # Dot product
    dot = v1x * v2x + v1y * v2y + v1z * v2z

    # Angle = arccos(dot / (r1 × r2))
    if radius == 0:
        return 0.0

    cos_angle = dot / (radius * radius)
    # Clamp to valid range for arccos
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.acos(cos_angle)

# Example
arc = XmiArc3D(
    start_point=XmiPoint3D(x=5000.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=5000.0, z=0.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=0.0)
)

angle_rad = central_angle(arc)
angle_deg = math.degrees(angle_rad)

print(f"Central angle: {angle_deg:.2f}°")
# Output: Central angle: 90.00°
```

#### Point at Arc Parameter

```python
def point_at_parameter(arc: XmiArc3D, t: float) -> XmiPoint3D:
    """
    Get a point along the arc at parameter t.

    Args:
        arc: The arc
        t: Parameter from 0 (start) to 1 (end)

    Returns:
        Point at position t along the arc
    """
    # Calculate the angle at parameter t
    total_angle = central_angle(arc)
    current_angle = t * total_angle

    # Get initial angle (angle from center to start point)
    # We need to rotate around the arc's normal
    # For simplicity, this example assumes a 2D arc in XY plane
    # Full 3D implementation would require proper rotation matrices

    # Vector from center to start
    v_start_x = arc.start_point.x - arc.center_point.x
    v_start_y = arc.start_point.y - arc.center_point.y

    # Initial angle
    initial_angle = math.atan2(v_start_y, v_start_x)

    # New angle
    new_angle = initial_angle + current_angle

    # Calculate radius
    radius = calculate_radius(arc)

    # New point (assuming XY plane arc)
    x = arc.center_point.x + radius * math.cos(new_angle)
    y = arc.center_point.y + radius * math.sin(new_angle)
    z = arc.start_point.z + t * (arc.end_point.z - arc.start_point.z)

    return XmiPoint3D(x=x, y=y, z=z)

# Example: Get midpoint of arc
arc = XmiArc3D(
    start_point=XmiPoint3D(x=5000.0, y=0.0, z=0.0),
    end_point=XmiPoint3D(x=0.0, y=5000.0, z=0.0),
    center_point=XmiPoint3D(x=0.0, y=0.0, z=0.0)
)

midpoint = point_at_parameter(arc, 0.5)
print(f"Arc midpoint: ({midpoint.x:.2f}, {midpoint.y:.2f}, {midpoint.z:.2f})")
# Output: Arc midpoint: (3535.53, 3535.53, 0.00)
```

#### Querying Arcs in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all Arc3D geometry objects
arcs = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiArc3D)
]

print(f"Total arcs: {len(arcs)}")

# Find arcs by radius range
large_arcs = [arc for arc in arcs if arc.radius and arc.radius > 10000.0]
small_arcs = [arc for arc in arcs if arc.radius and arc.radius <= 5000.0]

print(f"Large radius arcs (>10m): {len(large_arcs)}")
print(f"Small radius arcs (≤5m): {len(small_arcs)}")

# Calculate total arc length
total_length = sum(arc_length(arc) for arc in arcs)
print(f"Total arc length: {total_length:.2f} mm")

# Find arcs in horizontal plane (constant Z)
horizontal_arcs = [
    arc for arc in arcs
    if abs(arc.start_point.z - arc.center_point.z) < 1.0 and
       abs(arc.end_point.z - arc.center_point.z) < 1.0
]

print(f"Horizontal arcs: {len(horizontal_arcs)}")
```

## Validation Rules

### Type Validation

- `start_point`, `end_point`, and `center_point` must be `XmiPoint3D` instances
- `radius` must be numeric or None
- All three points are required (cannot be None)

### Required Fields

All three points are mandatory:
```python
# Valid
arc = XmiArc3D(
    start_point=XmiPoint3D(x=1, y=0, z=0),
    end_point=XmiPoint3D(x=0, y=1, z=0),
    center_point=XmiPoint3D(x=0, y=0, z=0)
)

# Invalid - will raise validation error
# arc = XmiArc3D(start_point=p1, end_point=p2)  # Missing center_point
```

### Geometric Consistency

For a valid arc:
- Start and end points must be equidistant from the center (same radius)
- The three points should not be collinear
- Radius (if provided) should match the calculated radius

```python
# Validate geometric consistency
if not verify_arc_consistency(arc, tolerance=1.0):
    print("Warning: Arc geometry is inconsistent")
```

### Degenerate Arcs

Arcs with zero radius or where all three points are coincident are technically valid but may cause issues:

```python
# Degenerate arc (all points the same)
degenerate = XmiArc3D(
    start_point=XmiPoint3D(x=0, y=0, z=0),
    end_point=XmiPoint3D(x=0, y=0, z=0),
    center_point=XmiPoint3D(x=0, y=0, z=0)
)

# Check for degenerate arcs
if calculate_radius(arc) < 1e-6:
    print("Warning: Degenerate arc detected")
```

### Missing Attributes in from_dict

The `from_dict()` method handles validation:

```python
incomplete_dict = {
    "start_point": {"X": 0, "Y": 0, "Z": 0},
    "end_point": {"X": 1, "Y": 0, "Z": 0}
    # Missing center_point
}

arc, errors = XmiArc3D.from_dict(incomplete_dict)
# arc will be None
# errors will contain: ["Missing attribute: center_point"]
```

## Integration with XMI Schema

### As Segment Geometry

Arcs are created as geometry for circular arc segments:

```python
# During parsing of StructuralCurveMember with "Segments": "CircularArc"
segment = XmiSegment(position=0, segment_type=XmiSegmentTypeEnum.CIRCULAR_ARC)

# Create arc geometry from segment nodes and middle point
arc = XmiArc3D(
    start_point=begin_node_point,
    end_point=end_node_point,
    center_point=calculated_center_point
)

# Create relationship
geometry_rel = XmiHasGeometry(source=segment, target=arc)
```

### Typical Creation Context

Arcs typically require additional information beyond just the "Nodes" list:
- A third point defining the arc (middle point or center)
- Or curvature information to calculate the center

This information may come from:
- Additional node in the nodes list
- Bulge factor or arc height
- Explicit center point coordinates

## Notes

### Version Differences (v1 vs v2)

**v2 Advantages:**
- Uses Pydantic for automatic validation
- Cleaner validation with decorators
- Better error messages
- Optional radius field

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation
- May have different field names

### Immutability

Treat arcs as immutable after creation:
```python
# Don't modify existing arcs
# arc.start_point = new_point  # Avoid this

# Instead, create new arcs
new_arc = XmiArc3D(
    start_point=new_point,
    end_point=arc.end_point,
    center_point=arc.center_point
)
```

### 3D vs 2D Arcs

- Arcs can be fully 3D (all three points at different elevations)
- Most structural arcs are planar (all three points in the same plane)
- The arc plane is defined by the three points
- Out-of-plane arcs may require special handling in analysis

### Arc Direction and Handedness

- The arc follows the shorter path from start to end (<180°)
- For arcs >180°, split into multiple segments
- Arc direction matters for load application and analysis

### Coordinate Units

- Arc coordinates and radius inherit units from points (typically millimeters)
- Calculated lengths will be in the same units

### Performance Considerations

- Arcs are slightly more complex than lines (3 points vs 2)
- Geometric calculations (length, angle) involve transcendental functions
- Cache calculated values if used repeatedly

### Common Applications

- **Curved beams**: Arches, curved roof structures
- **Circular ramps**: Parking garages, helical stairs
- **Curved columns**: Decorative or functional curved supports
- **Circular foundations**: Ring foundations, circular walls

## Related Classes

### Geometry Classes
- [`XmiPoint3D`](./XmiPoint3D.md) - Points defining arc (start, end, center)
- [`XmiLine3D`](./XmiLine3D.md) - Straight alternative to curved arcs
- `XmiBaseGeometry` - Base class for all geometry

### Entity Classes
- [`XmiSegment`](../entities/XmiSegment.md) - Segment entity that uses Arc3D
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Curve members containing arc segments

### Relationship Classes
- `XmiHasGeometry` - Links segments to arc geometry
- `XmiHasArc3D` - Specific relationship for arc geometry

### Enum Classes
- `XmiSegmentTypeEnum` - Defines CIRCULAR_ARC segment type

### Base Classes
- `XmiBaseGeometry` - Base geometry class
- `XmiBaseEntity` - Ultimate base class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Handles arc creation during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for all entities including arcs
