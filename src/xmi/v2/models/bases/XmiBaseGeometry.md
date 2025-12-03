# XmiBaseGeometry

## Overview

`XmiBaseGeometry` is the abstract base class for all geometric primitives in the XMI schema. It inherits from `XmiBaseEntity` and serves as the parent for point, line, and arc geometry classes. This base class ensures that all geometric objects have consistent identification and metadata while providing specialized validation for geometric types.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Grandparent**: `BaseModel` (Pydantic), `ABC`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/bases/xmi_base_geometry.py`
- **Children**: `XmiPoint3D`, `XmiLine3D`, `XmiArc3D`

## Properties

### Inherited Properties

Inherits all properties from `XmiBaseEntity`:
- `id`: Unique identifier (GUID)
- `name`: Human-readable name/identifier
- `ifcguid`: IFC Global Unique Identifier
- `native_id`: Original identifier from source application
- `description`: Optional description or notes
- `entity_type`: Type name of the geometry (auto-set to class name)

### Overridden Properties

| Property | Type | Description | Default | Alias |
|----------|------|-------------|---------|-------|
| `entity_type` | `str` | Type name of the geometry class | Class name (e.g., "XmiPoint3D") | "EntityType" |

## Purpose and Functionality

### Geometry Type Management

`XmiBaseGeometry` provides:

1. **Type Identification**: Ensures `entity_type` is set to the specific geometry class name
2. **Consistent Interface**: All geometric primitives share common base properties
3. **Validation Hook**: Provides extension point for geometry-specific validation

### Type Setting

The `set_entity_type` validator ensures the `entity_type` field is properly set:
```python
@model_validator(mode="before")
@classmethod
def set_entity_type(cls, values):
    values["EntityType"] = values.get("EntityType") or values.get("entity_type") or cls.__name__
    return values
```

This guarantees:
- If `EntityType` not provided → use class name
- Works with both PascalCase and snake_case inputs
- Each geometry instance knows its type (Point3D, Line3D, Arc3D)

## Usage Examples

### Direct Instantiation (Subclasses)

```python
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D

# Create point - entity_type automatically set to "XmiPoint3D"
point = XmiPoint3D(
    x=1000.0,
    y=2000.0,
    z=3000.0,
    name="P1"
)
print(f"Type: {point.entity_type}")  # "XmiPoint3D"
print(f"ID: {point.id}")  # Auto-generated UUID

# Create line - entity_type automatically set to "XmiLine3D"
line = XmiLine3D(
    start_point=XmiPoint3D(x=0, y=0, z=0),
    end_point=XmiPoint3D(x=1000, y=0, z=0),
    name="LINE-001"
)
print(f"Type: {line.entity_type}")  # "XmiLine3D"

# Create arc - entity_type automatically set to "XmiArc3D"
arc = XmiArc3D(
    start_point=XmiPoint3D(x=0, y=0, z=0),
    end_point=XmiPoint3D(x=1000, y=0, z=0),
    center_point=XmiPoint3D(x=500, y=500, z=0),
    name="ARC-001"
)
print(f"Type: {arc.entity_type}")  # "XmiArc3D"
```

### Working with Geometry Base Properties

```python
# All geometries have base entity properties
geometries = [point, line, arc]

for geom in geometries:
    print(f"Geometry: {geom.entity_type}")
    print(f"  ID: {geom.id}")
    print(f"  Name: {geom.name}")
    print(f"  Description: {geom.description or 'N/A'}")
```

### Common Patterns

#### Type Checking Geometry Objects

```python
from xmi.v2.models.bases.xmi_base_geometry import XmiBaseGeometry
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D

def is_geometry(obj) -> bool:
    """Check if an object is a geometry."""
    return isinstance(obj, XmiBaseGeometry)

def get_geometry_type(obj) -> str:
    """Get the type of a geometry object."""
    if isinstance(obj, XmiBaseGeometry):
        return obj.entity_type
    return "Not a geometry"

# Usage
point = XmiPoint3D(x=0, y=0, z=0)
print(is_geometry(point))  # True
print(get_geometry_type(point))  # "XmiPoint3D"

material = XmiStructuralMaterial(material_type="Concrete", grade="C30")
print(is_geometry(material))  # False
```

#### Filtering Geometries from Model

```python
def get_all_geometries(xmi_model):
    """Extract all geometric objects from the model."""
    return [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiBaseGeometry)
    ]

def group_geometries_by_type(xmi_model):
    """Group geometries by their type."""
    from collections import defaultdict
    grouped = defaultdict(list)

    for entity in xmi_model.entities:
        if isinstance(entity, XmiBaseGeometry):
            grouped[entity.entity_type].append(entity)

    return dict(grouped)

# Usage
all_geometries = get_all_geometries(xmi_model)
print(f"Total geometries: {len(all_geometries)}")

grouped = group_geometries_by_type(xmi_model)
for geom_type, geoms in grouped.items():
    print(f"{geom_type}: {len(geoms)}")
# Output:
# XmiPoint3D: 150
# XmiLine3D: 200
# XmiArc3D: 25
```

#### Find Geometry by ID

```python
def find_geometry_by_id(xmi_model, geometry_id: str):
    """Find a geometry object by its ID."""
    for entity in xmi_model.entities:
        if isinstance(entity, XmiBaseGeometry) and entity.id == geometry_id:
            return entity
    return None

# Usage
geometry = find_geometry_by_id(xmi_model, "point-001")
if geometry:
    print(f"Found {geometry.entity_type}: {geometry.name}")
```

#### Geometry Factory Pattern

```python
class GeometryFactory:
    """Factory for creating geometry objects with consistent naming."""

    def __init__(self, prefix: str = "GEOM"):
        self.prefix = prefix
        self.counters = {"point": 0, "line": 0, "arc": 0}

    def create_point(self, x: float, y: float, z: float) -> XmiPoint3D:
        """Create a point with auto-generated ID and name."""
        self.counters["point"] += 1
        return XmiPoint3D(
            x=x, y=y, z=z,
            id=f"{self.prefix}-POINT-{self.counters['point']:04d}",
            name=f"P{self.counters['point']}"
        )

    def create_line(self, start: XmiPoint3D, end: XmiPoint3D) -> XmiLine3D:
        """Create a line with auto-generated ID and name."""
        self.counters["line"] += 1
        return XmiLine3D(
            start_point=start,
            end_point=end,
            id=f"{self.prefix}-LINE-{self.counters['line']:04d}",
            name=f"L{self.counters['line']}"
        )

# Usage
factory = GeometryFactory()
p1 = factory.create_point(0, 0, 0)
p2 = factory.create_point(1000, 0, 0)
line = factory.create_line(p1, p2)

print(f"Created: {p1.name}, {p2.name}, {line.name}")
# Output: Created: P1, P2, L1
```

#### Export Geometry Metadata

```python
def export_geometry_info(geometry: XmiBaseGeometry) -> dict:
    """Export common geometry metadata."""
    info = {
        "type": geometry.entity_type,
        "id": geometry.id,
        "name": geometry.name
    }

    # Add type-specific information
    if isinstance(geometry, XmiPoint3D):
        info["coordinates"] = (geometry.x, geometry.y, geometry.z)
    elif isinstance(geometry, XmiLine3D):
        info["start"] = (geometry.start_point.x, geometry.start_point.y, geometry.start_point.z)
        info["end"] = (geometry.end_point.x, geometry.end_point.y, geometry.end_point.z)
    elif isinstance(geometry, XmiArc3D):
        info["start"] = (geometry.start_point.x, geometry.start_point.y, geometry.start_point.z)
        info["end"] = (geometry.end_point.x, geometry.end_point.y, geometry.end_point.z)
        info["center"] = (geometry.center_point.x, geometry.center_point.y, geometry.center_point.z)

    return info

# Usage
point = XmiPoint3D(x=100, y=200, z=300, name="P1")
info = export_geometry_info(point)
print(info)
# {'type': 'XmiPoint3D', 'id': '...', 'name': 'P1', 'coordinates': (100, 200, 300)}
```

#### Validating Geometry Collections

```python
def validate_geometry_collection(geometries: list) -> dict:
    """Validate a collection of geometries."""
    results = {
        "total": len(geometries),
        "by_type": {},
        "missing_names": [],
        "duplicate_ids": []
    }

    # Count by type
    from collections import Counter
    type_counts = Counter(g.entity_type for g in geometries)
    results["by_type"] = dict(type_counts)

    # Find geometries without names
    results["missing_names"] = [
        g.id for g in geometries
        if not g.name or g.name == g.id
    ]

    # Find duplicate IDs
    id_counts = Counter(g.id for g in geometries)
    results["duplicate_ids"] = [
        id_ for id_, count in id_counts.items()
        if count > 1
    ]

    return results

# Usage
validation = validate_geometry_collection(all_geometries)
print(f"Total: {validation['total']}")
print(f"Points: {validation['by_type'].get('XmiPoint3D', 0)}")
print(f"Missing names: {len(validation['missing_names'])}")
```

## Validation Rules

### Automatic Type Setting

The `set_entity_type` validator ensures:
- `entity_type` is always set (never None or empty)
- Uses class name if not explicitly provided
- Works with both PascalCase ("EntityType") and snake_case ("entity_type")

### Inheritance from XmiBaseEntity

All validation from `XmiBaseEntity` applies:
- Auto-generate `id` if not provided
- Set `name` to `id` if not provided
- All fields support PascalCase/snake_case aliases

## Integration with XMI Schema

### Geometry in XMI JSON

Geometry objects are typically embedded within other entities or created during parsing:

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

During parsing, `XmiManager` creates a `XmiPoint3D` geometry from the coordinate string:
```python
# Internally, XmiManager does something like:
coords = node_dict["Coordinate"].split(',')
point_geometry = XmiPoint3D(
    x=float(coords[0]),
    y=float(coords[1]),
    z=float(coords[2]),
    name=f"{node_dict['Name']}_POINT"
)
# entity_type is automatically set to "XmiPoint3D"
```

### Relationship to Entities

Geometries are linked to entities via `XmiHasGeometry` relationships:
- `XmiStructuralPointConnection` → `XmiPoint3D` (node location)
- `XmiSegment` → `XmiLine3D` or `XmiArc3D` (segment geometry)

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics (XmiBaseGeometry):**
- Inherits from Pydantic `XmiBaseEntity`
- Automatic `entity_type` setting via validator
- Clean inheritance hierarchy
- Type hints for better IDE support

**v1 Characteristics:**
- Separate base class with manual validation
- `__slots__` for memory efficiency
- Explicit property getters/setters

### Abstract Base Class

`XmiBaseGeometry` is not directly instantiable. Use concrete subclasses:
```python
# This will work:
point = XmiPoint3D(x=0, y=0, z=0)
line = XmiLine3D(start_point=p1, end_point=p2)
arc = XmiArc3D(start_point=p1, end_point=p2, center_point=p3)

# This conceptually should not be done (though Python allows it):
# geometry = XmiBaseGeometry()  # Don't do this
```

### Geometry Subclasses

Three concrete geometry classes inherit from `XmiBaseGeometry`:

1. **XmiPoint3D**: Single point in 3D space
   - Properties: `x`, `y`, `z`
   - Most fundamental geometric primitive

2. **XmiLine3D**: Straight line segment
   - Properties: `start_point`, `end_point`
   - Represents straight structural members

3. **XmiArc3D**: Circular arc segment
   - Properties: `start_point`, `end_point`, `center_point`, `radius`
   - Represents curved structural members

### Pydantic Configuration

```python
model_config = ConfigDict(populate_by_name=True)
```

Allows both field names and aliases:
```python
# Both work:
point1 = XmiPoint3D(x=0, y=0, z=0)
point2 = XmiPoint3D(X=0, Y=0, Z=0)  # PascalCase from JSON
```

### entity_type Usage

The `entity_type` field is useful for:
- Runtime type identification without `isinstance()` checks
- Serialization and deserialization
- Logging and debugging
- Filtering and grouping

### Performance Considerations

- `XmiBaseGeometry` adds minimal overhead (one string field)
- Geometry objects are lightweight
- Validation happens once at creation time
- Large models may have thousands of geometries (especially points)

### Common Pitfalls

1. **Type Confusion**: Remember geometry objects are distinct from entity objects
2. **Direct Instantiation**: Don't try to create `XmiBaseGeometry` directly, use subclasses
3. **Missing Type Checks**: When working with mixed entity/geometry collections, check types properly
4. **Geometry Relationships**: Geometries are targets of `XmiHasGeometry`, not standalone top-level entities

## Related Classes

### Direct Subclasses (Geometries)
- [`XmiPoint3D`](../geometries/XmiPoint3D.md) - 3D point geometry
- [`XmiLine3D`](../geometries/XmiLine3D.md) - Straight line geometry
- [`XmiArc3D`](../geometries/XmiArc3D.md) - Circular arc geometry

### Parent Classes
- [`XmiBaseEntity`](./XmiBaseEntity.md) - Base class for all entities

### Entity Classes That Use Geometries
- [`XmiStructuralPointConnection`](../entities/XmiStructuralPointConnection.md) - Uses XmiPoint3D
- [`XmiSegment`](../entities/XmiSegment.md) - Uses XmiLine3D or XmiArc3D

### Relationship Classes
- `XmiHasGeometry` - Links entities to their geometric representations
- `XmiHasPoint3D` - Specific relationship for point geometry
- `XmiHasLine3D` - Specific relationship for line geometry
- `XmiHasArc3D` - Specific relationship for arc geometry

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates geometry objects during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores geometry entities
