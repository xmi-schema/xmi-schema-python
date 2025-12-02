# XmiStructuralSurfaceMember

## Overview

`XmiStructuralSurfaceMember` represents two-dimensional structural elements in the XMI schema, such as slabs, walls, and foundation elements. These are surface elements defined by boundary nodes forming a closed polygon, with properties including thickness, material, and local coordinate system. Surface members are essential for modeling floor plates, shear walls, and other planar structural components.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/entities/xmi_structural_surface_member.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `surface_member_type` | `XmiStructuralSurfaceMemberTypeEnum` | Type of surface member (Slab, Wall, Pad Footing, etc.) | Must be valid enum value |
| `thickness` | `Union[float, int]` | Thickness of the surface element | Must be numeric, typically > 0 |
| `system_plane` | `XmiStructuralSurfaceMemberSystemPlaneEnum` | Reference plane position (Top, Bottom, Middle, Left, Right) | Must be valid enum value |

### Optional Properties with Defaults

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `area` | `Optional[Union[float, int]]` | `None` | Surface area of the element | Numeric value or None |
| `z_offset` | `Union[float, int]` | `0.0` | Vertical offset from reference plane | Numeric value |
| `local_axis_x` | `Tuple[float, float, float]` | `(1.0, 0.0, 0.0)` | Local X-axis direction vector | Must be 3 floats or comma-separated string |
| `local_axis_y` | `Tuple[float, float, float]` | `(0.0, 1.0, 0.0)` | Local Y-axis direction vector | Must be 3 floats or comma-separated string |
| `local_axis_z` | `Tuple[float, float, float]` | `(0.0, 0.0, 1.0)` | Local Z-axis direction vector (surface normal) | Must be 3 floats or comma-separated string |
| `height` | `Optional[Union[float, int]]` | `None` | Height of the surface element (for walls) | Numeric value or None |

### Inherited Properties

Inherits from `XmiBaseEntity`:
- `name`: Name/identifier of the surface member
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiStructuralSurfaceMember"
- `description`: Optional description

## Enums

### XmiStructuralSurfaceMemberTypeEnum

Defines the structural type of the surface member:

- `SLAB`: Horizontal floor or roof slab
- `WALL`: Vertical wall element
- `PAD_FOOTING`: Isolated pad footing
- `STRIP_FOOTING`: Continuous strip footing
- `PILECAP`: Pile cap foundation element
- `ROOF_PANEL`: Roof panel element
- `WALL_PANEL`: Wall panel element
- `RAFT`: Raft foundation
- `UNKNOWN`: Type is unknown or not specified

### XmiStructuralSurfaceMemberSystemPlaneEnum

Defines the reference plane position of the surface member:

- `BOTTOM`: Bottom face of the element
- `TOP`: Top face of the element
- `MIDDLE`: Mid-plane of the element (neutral axis)
- `LEFT`: Left edge reference (for vertical elements)
- `RIGHT`: Right edge reference (for vertical elements)
- `UNKNOWN`: Reference plane is unknown

## Relationships

`XmiStructuralSurfaceMember` participates in several relationships:

### Source Relationships (this entity is the source):

- **`XmiHasStructuralMaterial`**: Links the surface member to its `XmiStructuralMaterial`
- **`XmiHasStructuralNode`**: Links to multiple `XmiStructuralPointConnection` nodes defining the boundary
- **`XmiHasEdge`**: Links to edge segments defining the perimeter geometry

### Target Relationships (this entity is the target):

- May be referenced by storey or unit relationships for organizational hierarchy
- May be referenced by load or support relationships

## Local Coordinate System

The local coordinate system defines the orientation of the surface member:

- **Local X-axis**: Typically aligned with one edge direction of the surface
- **Local Y-axis**: Perpendicular to X-axis, in the plane of the surface
- **Local Z-axis**: Surface normal (perpendicular to the surface plane)

The axes form a right-handed coordinate system and are essential for:
- Applying loads in local coordinates (e.g., pressure perpendicular to surface)
- Defining material orientation
- Interpreting analysis results (local stresses and moments)

## System Plane and Z-Offset

The system plane and z-offset together define how the surface is positioned relative to its boundary nodes:

### System Plane
- **TOP**: Nodes define the top face; element extends downward
- **BOTTOM**: Nodes define the bottom face; element extends upward
- **MIDDLE**: Nodes define the mid-plane; element extends equally both directions

### Z-Offset
- Additional vertical offset from the system plane reference
- Positive values move the element in the +Z direction
- Useful for modeling offsets from analytical reference planes

Example:
```python
# Slab with top at nodes, 200mm thick
slab = XmiStructuralSurfaceMember(
    system_plane=SystemPlaneEnum.TOP,
    thickness=200.0,
    z_offset=0.0
)
# Physical element extends from Z=0 down to Z=-200

# Wall with middle at nodes, 300mm thick, offset up 50mm
wall = XmiStructuralSurfaceMember(
    system_plane=SystemPlaneEnum.MIDDLE,
    thickness=300.0,
    z_offset=50.0
)
# Physical element extends from Z=-100 to Z=+200 (middle at Z=50)
```

## Usage Examples

### Creating an Instance Directly

```python
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum
from xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum

# Create a floor slab
slab = XmiStructuralSurfaceMember(
    name="S01",
    id="slab-001",
    surface_member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    thickness=200.0,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.TOP,
    area=50.0,  # 50 m²
    local_axis_x=(1.0, 0.0, 0.0),
    local_axis_y=(0.0, 1.0, 0.0),
    local_axis_z=(0.0, 0.0, 1.0),
    description="Level 2 floor slab"
)

# Create a structural wall
wall = XmiStructuralSurfaceMember(
    name="W01",
    id="wall-001",
    surface_member_type=XmiStructuralSurfaceMemberTypeEnum.WALL,
    thickness=300.0,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE,
    height=3000.0,  # 3m high wall
    area=9.0,  # 9 m² (3m x 3m)
    local_axis_x=(0.0, 0.0, 1.0),  # Vertical
    local_axis_y=(1.0, 0.0, 0.0),
    local_axis_z=(0.0, 1.0, 0.0),  # Normal to wall
    description="Shear wall"
)

# Create a foundation element
footing = XmiStructuralSurfaceMember(
    name="F01",
    id="footing-001",
    surface_member_type=XmiStructuralSurfaceMemberTypeEnum.PAD_FOOTING,
    thickness=600.0,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM,
    area=4.0,  # 2m x 2m
    z_offset=-100.0,  # Slight offset below nodes
    description="Column pad footing"
)
```

### Loading from Dictionary

```python
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

# Dictionary from XMI JSON input
surface_member_dict = {
    "Name": "417056",
    "Storey": "417024",
    "Material": "416902",
    "Type": "Slab",
    "SurfaceMemberType": "Slab",
    "Thickness": 600.0,
    "SystemPlane": "Top",
    "Nodes": "420321;420315;420337;420323",
    "Edges": "Line;Line;Line;Line",
    "Area": 30.0,
    "ID": "d2bef6b7-d442-4cc0-9c4a-2da9c02c1921-00065d20",
    "Description": "Level 1 slab",
    "LocalAxisX": "1,0,0",
    "LocalAxisY": "0,1,0",
    "LocalAxisZ": "0,0,1",
    "Height": 0.0,
    "IFCGUID": "3IllQtr49Cm9nABQd0AaG1",
    "ZOffset": 0.0
}

# Parse using from_dict (handles enum conversion and axis parsing)
surface_member, errors = XmiStructuralSurfaceMember.from_dict(surface_member_dict)

if surface_member:
    print(f"Created surface member: {surface_member.name}")
    print(f"Type: {surface_member.surface_member_type}")
    print(f"Thickness: {surface_member.thickness}")
    print(f"Area: {surface_member.area}")
    print(f"System plane: {surface_member.system_plane}")
else:
    print(f"Errors during parsing: {errors}")
```

### Common Patterns

#### Working with Local Axes

```python
# Axes can be specified as strings or tuples
slab1 = XmiStructuralSurfaceMember(
    name="S1",
    id="s1",
    surface_member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    thickness=200.0,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.TOP,
    local_axis_z="0,0,1",  # String format (normal pointing up)
)

slab2 = XmiStructuralSurfaceMember(
    name="S2",
    id="s2",
    surface_member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
    thickness=200.0,
    system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.TOP,
    local_axis_z=(0.0, 0.0, 1.0),  # Tuple format
)

# Both are converted to tuples internally
assert slab1.local_axis_z == slab2.local_axis_z
```

#### Querying Surface Members in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all surface members
surface_members = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiStructuralSurfaceMember)
]

# Filter by type
slabs = [
    sm for sm in surface_members
    if sm.surface_member_type == XmiStructuralSurfaceMemberTypeEnum.SLAB
]

walls = [
    sm for sm in surface_members
    if sm.surface_member_type == XmiStructuralSurfaceMemberTypeEnum.WALL
]

foundations = [
    sm for sm in surface_members
    if sm.surface_member_type in [
        XmiStructuralSurfaceMemberTypeEnum.PAD_FOOTING,
        XmiStructuralSurfaceMemberTypeEnum.STRIP_FOOTING,
        XmiStructuralSurfaceMemberTypeEnum.RAFT
    ]
]

print(f"Total surface members: {len(surface_members)}")
print(f"Slabs: {len(slabs)}")
print(f"Walls: {len(walls)}")
print(f"Foundations: {len(foundations)}")
```

#### Finding Material for a Surface Member

```python
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial

# Find material relationship
material_relationships = xmi_model.find_relationships_by_source(
    surface_member,
    relationship_type=XmiHasStructuralMaterial
)

if material_relationships:
    material = material_relationships[0].target
    print(f"Surface {surface_member.name} uses material: {material.name}")
    print(f"Material type: {material.material_type}")
    print(f"Grade: {material.grade}")
```

#### Finding Boundary Nodes of Surface Member

```python
from xmi.v2.models.relationships.xmi_has_structural_node import XmiHasStructuralNode

# Find node relationships
node_relationships = xmi_model.find_relationships_by_source(
    surface_member,
    relationship_type=XmiHasStructuralNode
)

# Get all boundary nodes
boundary_nodes = [rel.target for rel in node_relationships]

print(f"Surface {surface_member.name} has {len(boundary_nodes)} boundary nodes:")
for i, node in enumerate(boundary_nodes):
    print(f"  Node {i+1}: {node.name} at {node.coordinate}")

# Calculate perimeter (for simple polygons)
if len(boundary_nodes) >= 3:
    perimeter = 0.0
    for i in range(len(boundary_nodes)):
        n1 = boundary_nodes[i]
        n2 = boundary_nodes[(i + 1) % len(boundary_nodes)]
        # Calculate distance between consecutive nodes
        dx = n2.coordinate[0] - n1.coordinate[0]
        dy = n2.coordinate[1] - n1.coordinate[1]
        dz = n2.coordinate[2] - n1.coordinate[2]
        perimeter += (dx**2 + dy**2 + dz**2)**0.5
    print(f"Perimeter: {perimeter:.2f}")
```

#### Calculating Volume and Weight

```python
# Calculate volume from area and thickness
if surface_member.area and surface_member.thickness:
    volume_mm3 = surface_member.area * 1e6 * surface_member.thickness  # Convert m² to mm²
    volume_m3 = volume_mm3 / 1e9  # Convert mm³ to m³
    print(f"Volume: {volume_m3:.3f} m³")

    # Get material to calculate weight
    material_rels = xmi_model.find_relationships_by_source(
        surface_member,
        relationship_type=XmiHasStructuralMaterial
    )

    if material_rels and material_rels[0].target.unit_weight:
        material = material_rels[0].target
        # unit_weight typically in kN/m³
        weight_kn = volume_m3 * material.unit_weight
        print(f"Self-weight: {weight_kn:.2f} kN")
```

## Validation Rules

### Type Validation

- `surface_member_type` must be a valid `XmiStructuralSurfaceMemberTypeEnum` value
- `system_plane` must be a valid `XmiStructuralSurfaceMemberSystemPlaneEnum` value
- `thickness` must be numeric (typically positive)
- All axis vectors must be tuples of exactly 3 floats
- `area`, `height`, and `z_offset` must be numeric or None

### Axis String Parsing

When local axes are provided as strings:
- Must contain exactly 3 comma-separated numeric values
- Whitespace around values is trimmed
- Values are converted to floats

Example valid formats:
- `"1,0,0"`
- `"1.0, 0.0, 0.0"`
- `"0.707, 0.707, 0.0"`

### Coordinate System Rules

- Local axes should form a right-handed coordinate system
- Local Z-axis should represent the surface normal
- Axes should be normalized (unit vectors) for proper interpretation
- The library does not enforce orthogonality, but it's recommended

### Physical Constraints

- Thickness should be positive for physical elements
- Area should be positive if specified
- Height should be positive for vertical elements (walls)

## Integration with XMI Schema

### Typical XMI Dictionary Structure

```json
{
  "StructuralSurfaceMember": [
    {
      "Name": "S01",
      "Material": "MAT-CONCRETE-C40",
      "Type": "Slab",
      "SurfaceMemberType": "Slab",
      "Thickness": 200.0,
      "SystemPlane": "Top",
      "Nodes": "N1;N2;N3;N4",
      "Edges": "Line;Line;Line;Line",
      "Area": 25.0,
      "LocalAxisX": "1,0,0",
      "LocalAxisY": "0,1,0",
      "LocalAxisZ": "0,0,1",
      "Height": 0.0,
      "ZOffset": 0.0,
      "ID": "unique-guid-here",
      "IFCGUID": "ifc-guid-here",
      "Description": "First floor slab"
    }
  ]
}
```

### Dependency Order

`XmiStructuralSurfaceMember` depends on:
1. `XmiStructuralMaterial` (material must exist)
2. `XmiStructuralPointConnection` (boundary nodes must exist)

These dependencies must be loaded before surface members during parsing.

## Notes

### Version Differences (v1 vs v2)

**v2 Advantages:**
- Uses Pydantic for automatic validation
- Field aliases support both PascalCase (JSON) and snake_case (Python)
- `from_dict()` method handles enum conversion automatically
- Type hints provide better IDE support

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation with setters/getters
- Explicit parsing logic in `from_xmi_dict_obj()`

### Boundary Definition

Surface members are defined by:
- **Nodes**: Ordered list of boundary point connections (typically 3-8 nodes)
- **Edges**: Segment types between consecutive nodes (typically "Line", but can include "CircularArc")
- Nodes should be ordered consistently (clockwise or counterclockwise)
- First and last nodes are implicitly connected

### System Plane Usage by Element Type

**Slabs (horizontal)**:
- `TOP`: Top of slab at nodal elevation (most common)
- `BOTTOM`: Bottom of slab at nodal elevation
- `MIDDLE`: Slab centerline at nodal elevation

**Walls (vertical)**:
- `MIDDLE`: Wall centerline at nodal locations (most common)
- `LEFT` / `RIGHT`: Wall face at nodal locations (less common)

**Foundations**:
- `BOTTOM`: Bottom of footing at nodal elevation (most common)
- `TOP`: Top of footing at nodal elevation

### Height vs Thickness

- **Thickness**: Perpendicular to the surface plane (required)
  - For slabs: vertical thickness
  - For walls: horizontal thickness (wall width)
- **Height**: Secondary dimension (optional)
  - For walls: vertical extent (floor to ceiling)
  - Not typically used for horizontal slabs

### Analysis Considerations

- Surface members use shell/plate element formulations in analysis
- Local Z-axis defines the direction of:
  - Applied pressure loads
  - Bending moments (Mx, My)
  - Out-of-plane deformations
- Thickness affects both membrane and bending stiffness
- System plane affects moment distribution

### Performance Considerations

- Local axis tuples are immutable after validation
- Default values avoid unnecessary property storage
- `z_offset` defaults to 0.0 (most common case)
- Use `populate_by_name=True` in model config for flexible field access

## Related Classes

### Entity Classes
- [`XmiStructuralMaterial`](./XmiStructuralMaterial.md) - Material definition
- [`XmiStructuralPointConnection`](./XmiStructuralPointConnection.md) - Boundary node connections
- [`XmiStructuralStorey`](./XmiStructuralStorey.md) - Story organization
- [`XmiStructuralCurveMember`](./XmiStructuralCurveMember.md) - Related linear members (beams, columns)

### Relationship Classes
- `XmiHasStructuralMaterial` - Links to material
- `XmiHasStructuralNode` - Links to boundary nodes
- `XmiHasEdge` - Links to edge segments

### Enum Classes
- `XmiStructuralSurfaceMemberTypeEnum` - Surface member type enumeration
- `XmiStructuralSurfaceMemberSystemPlaneEnum` - System plane position enumeration

### Geometry Classes
- `XmiPoint3D` - Node point geometry
- `XmiLine3D` - Linear edge geometry

### Base Classes
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base entity class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Entry point for parsing XMI data
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for entities and relationships
